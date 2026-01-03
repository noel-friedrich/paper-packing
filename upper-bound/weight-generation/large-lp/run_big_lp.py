"""
Prefix-sum LP for rectangle packing dual weights.

Instance: big rectangle L x W, small rectangles a x b and b x a.
We minimize total weight with constraints that every allowed small
rectangle has sum >= 1, using the 2D prefix-sum variables F.

Configured to run with Gurobi via gurobipy on a cluster (e.g. Euler).

SOLVE_METHOD can be:
  - "simplex" : primal simplex with checkpoints
  - "barrier" : barrier method (no checkpoints)
  - "pdhg"    : PDHG (first-order) method (no checkpoints here)
"""

import gurobipy as gp
from gurobipy import GRB
import time
import os
import numpy as np

# ============================================================
# GLOBAL CONFIGURATION
# ============================================================

# Instance: big grid size and small rectangle sizes
L = 1189   # width  (x dimension: x = 0..L-1)
W = 841    # height (y dimension: y = 0..W-1)
A = 37     # small rect width
B = 26     # small rect height

# Solver method:
#   "simplex" -> primal simplex with checkpoints
#   "barrier" -> barrier method (no checkpoint resume)
#   "pdhg"    -> PDHG first-order method (no checkpoint resume)
SOLVE_METHOD = "pdhg"               # "simplex", "barrier", or "pdhg"

# Solver parameters
THREADS = int(os.getenv("SLURM_CPUS_PER_TASK", "8"))
PRESOLVE = 2                        # 0=off, 1=conservative, 2=aggressive
print(f"running with THREADS={THREADS}")

# Simplex checkpointing
TIME_SLICE_SECONDS = 3600           # per-slice TimeLimit, in seconds
MAX_SLICES = None                   # None = unlimited; or an int to cap slices
CHECKPOINT_PREFIX = "checkpoint"    # files: checkpoint_*.bas / checkpoint_*.sol

# Logging / model output
LOGFILE = "gurobi_run.log"
WRITE_MPS = False                   # will output the initial LP as a .mps file

# run crossover
RUN_CROSSOVER = False
BARRIER_PDHG_MAXTIME = 60 * 60 * 47 # in seconds, only applies to PDHG

# ============================================================
# MODEL BUILDING: PREFIX-SUM LP
# ============================================================

def build_weight_lp(L, W, a, b, name="weight_lp", include_both_orientations=True):
    """
    Build the prefix-sum LP for an L x W grid with rectangles of size (a,b) and (b,a).

    L : int  -- width  (x dimension, columns, x = 0..L-1)
    W : int  -- height (y dimension, rows,    y = 0..W-1)
    a, b : int -- small rectangle dimensions

    Returns
    -------
    model : gurobipy.Model
    F     : dict[(x,y)] -> GRBVar for x=1..L, y=1..W
            (prefix-sum variables; F(0,*) and F(*,0) are implicitly 0)
    """
    print(f"Building model for L={L}, W={W}, a={a}, b={b} ...")
    model = gp.Model(name)

    # Redirect solver log to file (also appears on stdout)
    model.Params.LogFile = LOGFILE

    # Apply general solver parameters
    model.Params.Presolve = PRESOLVE
    model.Params.Threads = THREADS

    # --------------------------------------------------------
    # 1. Create F[x,y] variables for x=1..L, y=1..W
    #    F(0,y) and F(x,0) are treated as constant 0 and are not created
    # --------------------------------------------------------
    F = model.addVars(
        range(1, L + 1),
        range(1, W + 1),
        lb=0.0,            # prefix sums are nonnegative
        name="F"
    )

    # Helper: return F(x,y) if x,y>0, else constant 0.0
    def Fvar(x, y):
        if x <= 0 or y <= 0:
            return 0.0  # boundary of prefix-sum is 0 by definition
        else:
            return F[x, y]

    # --------------------------------------------------------
    # 2. Nonnegativity constraints for w(x,y) >= 0.
    #
    #    w(x-1,y-1) = F[x,y] - F[x-1,y] - F[x,y-1] + F[x-1,y-1] >= 0
    #    for x=1..L, y=1..W.
    # --------------------------------------------------------
    print("Adding nonnegativity constraints (w >= 0)...")
    start = time.time()
    for x in range(1, L + 1):
        for y in range(1, W + 1):
            expr = (
                Fvar(x, y)
                - Fvar(x - 1, y)
                - Fvar(x, y - 1)
                + Fvar(x - 1, y - 1)
            )
            # No need to name constraints for performance
            model.addConstr(expr >= 0.0)
    print(f"  Done nonnegativity in {time.time() - start:.1f} seconds.")

    # --------------------------------------------------------
    # 3. Rectangle constraints for orientation (a,b)
    #
    #    Top-left pixel (i,j) in original grid: 0 <= i <= L-a, 0 <= j <= W-b.
    #    Sum over that rectangle:
    #        F[i+a, j+b] - F[i, j+b] - F[i+a, j] + F[i, j]  >= 1
    # --------------------------------------------------------
    print("Adding rectangle constraints for orientation (a,b)...")
    start = time.time()
    for i in range(0, L - a + 1):
        for j in range(0, W - b + 1):
            expr = (
                Fvar(i + a, j + b)
                - Fvar(i,     j + b)
                - Fvar(i + a, j)
                + Fvar(i,     j)
            )
            model.addConstr(expr >= 1.0)
    print(f"  Done (a,b) rectangles in {time.time() - start:.1f} seconds.")

    # --------------------------------------------------------
    # 4. Rectangle constraints for orientation (b,a), if desired
    # --------------------------------------------------------
    if include_both_orientations and (a != b):
        print("Adding rectangle constraints for orientation (b,a)...")
        start = time.time()
        for i in range(0, L - b + 1):
            for j in range(0, W - a + 1):
                expr = (
                    Fvar(i + b, j + a)
                    - Fvar(i,     j + a)
                    - Fvar(i + b, j)
                    + Fvar(i,     j)
                )
                model.addConstr(expr >= 1.0)
        print(f"  Done (b,a) rectangles in {time.time() - start:.1f} seconds.")

    # --------------------------------------------------------
    # 5. Objective: minimize total weight = F[L, W]
    # --------------------------------------------------------
    model.setObjective(F[L, W], GRB.MINIMIZE)

    print("Model build complete.")
    print(f"  Variables:   {model.NumVars}")
    print(f"  Constraints: {model.NumConstrs}")

    return model, F


# ============================================================
# SIMPLEX WITH CHECKPOINTS
# ============================================================

def run_simplex_with_checkpoints(model, checkpoint_prefix, time_slice_seconds, max_slices=None):
    """
    Run primal simplex in time slices, writing a .bas and .sol checkpoint
    after each slice if a solution exists.
    """
    print("Running simplex with checkpoints...")
    model.Params.Method = 1    # 1 = primal simplex

    slice_idx = 0
    while True:
        if (max_slices is not None) and (slice_idx >= max_slices):
            print("Reached MAX_SLICES limit, stopping.")
            break

        model.Params.TimeLimit = time_slice_seconds
        print(f"=== Starting simplex slice {slice_idx}, TimeLimit = {time_slice_seconds} seconds ===")
        model.optimize()

        status = model.Status
        print(f"Slice {slice_idx} ended with status {status}.")

        if model.SolCount > 0:
            sol_file = f"{checkpoint_prefix}_{slice_idx}.sol"
            bas_file = f"{checkpoint_prefix}_{slice_idx}.bas"
            print(f"  Writing checkpoint solution to {sol_file}")
            model.write(sol_file)
            print(f"  Writing checkpoint basis to {bas_file}")
            model.write(bas_file)

        if status == GRB.OPTIMAL:
            print("Optimal solution found.")
            break

        if status == GRB.TIME_LIMIT:
            print("Time slice reached TimeLimit, continuing with next slice...")
            slice_idx += 1
            continue

        print(f"Stopping due to solver status {status}.")
        break


# ============================================================
# BARRIER SOLVE (ONE SHOT)
# ============================================================

def run_barrier(model):
    """
    Solve the LP once using barrier method (no checkpointing).
    """
    print("Running barrier method (no checkpoints)...")
    model.Params.Method = 2    # 2 = barrier

    if not RUN_CROSSOVER:
        model.Params.Crossover = 0

    if BARRIER_PDHG_MAXTIME:
        model.Params.TimeLimit = BARRIER_PDHG_MAXTIME

    model.optimize()


# ============================================================
# PDHG SOLVE (ONE SHOT)
# ============================================================

def run_pdhg(model):
    """
    Solve the LP once using PDHG (first-order) method.

    This uses Method=6. By default Gurobi will run PDHG to its
    tolerances and then perform crossover to get a basic solution.
    You can tune PDHGAbsTol, PDHGRelTol, PDHGConvTol, PDHGIterLimit,
    PDHGGPU, etc., here if desired.
    """
    print("Running PDHG method (no checkpoints)...")
    model.Params.Method = 6    # 6 = PDHG

    if not RUN_CROSSOVER:
        model.Params.Crossover = 0
    
    if BARRIER_PDHG_MAXTIME:
        model.Params.TimeLimit = BARRIER_PDHG_MAXTIME

    model.optimize()


# ============================================================
# Weights saving using numpy
# ============================================================

def extract_and_save_weights(model, F, L, W, out_prefix="weights"):
    """
    Given an optimal model and F-variables from the prefix-sum LP, reconstruct
    the per-pixel weights w[x,y] and save them to a .npz file.

    w(x,y) = F(x+1,y+1) - F(x,y+1) - F(x+1,y) + F(x,y),
    where F(0,*) and F(*,0) are treated as 0.
    """

    if model.Status != GRB.OPTIMAL and model.SolCount == 0:
        print("No solution available; skipping weight extraction.")
        return

    print("Extracting weights w(x,y) from F solution...")

    # Build a 2D array of F values including the 0 border: shape (L+1, W+1)
    Fval = np.zeros((L + 1, W + 1), dtype=float)

    # F is defined on x=1..L, y=1..W; row/col 0 stay at 0
    for x in range(1, L + 1):
        for y in range(1, W + 1):
            Fval[x, y] = F[x, y].X

    # Now reconstruct w[x,y] for x=0..L-1, y=0..W-1
    w = np.zeros((L, W), dtype=float)
    for x in range(L):
        for y in range(W):
            w[x, y] = (
                Fval[x + 1, y + 1]
                - Fval[x,     y + 1]
                - Fval[x + 1, y    ]
                + Fval[x,     y    ]
            )

    total_weight = w.sum()
    print(f"  Total weight from reconstructed w = {total_weight:.10f}")

    # Save to a compressed NumPy file
    out_file = f"{out_prefix}_L{L}_W{W}.npz"
    print(f"  Saving w[x,y] to {out_file}")
    np.savez_compressed(out_file, w=w)


# ============================================================
# MAIN
# ============================================================

def main():
    # Build model
    model, F = build_weight_lp(L, W, A, B, name="weight_lp")

    # Optionally write the model (can be large!)
    if WRITE_MPS:
        print("Writing model to prefix_lp.mps ...")
        model.write("prefix_lp.mps")

    # Run the chosen method
    method = SOLVE_METHOD.lower()
    if method == "simplex":
        run_simplex_with_checkpoints(
            model,
            checkpoint_prefix=CHECKPOINT_PREFIX,
            time_slice_seconds=TIME_SLICE_SECONDS,
            max_slices=MAX_SLICES
        )
    elif method == "barrier":
        run_barrier(model)
    elif method == "pdhg":
        run_pdhg(model)
    else:
        raise ValueError(f"Unknown SOLVE_METHOD: {SOLVE_METHOD}")

    # Report final status and objective if available
    status = model.Status
    print(f"Final solver status: {status}")
    if status == GRB.OPTIMAL:
        print(f"Optimal objective (total weight) = {model.ObjVal}")
    elif model.SolCount > 0:
        print(f"Best available objective (not proven optimal) = {model.ObjVal}")
    else:
        print("No solution found.")

    # Try to extract and save weights if we have a solution
    extract_and_save_weights(model, F, L, W, out_prefix="weights")


if __name__ == "__main__":
    main()
