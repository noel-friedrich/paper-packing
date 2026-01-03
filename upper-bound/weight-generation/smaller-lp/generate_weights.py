import argparse
from pathlib import Path
import numpy as np

def solve_weight_lp(
    L,
    W,
    a,
    b,
    allow_rotation=True,
    img_path=None,
    gurobi_msg=False,
    solver_id=0,
    numeric_focus=True,
):
    from PIL import Image
    from matplotlib import pyplot as plt
    import gurobipy as gp
    from gurobipy import GRB

    """
    Gurobi (gurobipy) version of the optimal weight LP.

    variables: w[y,x] in [0,1] for x=0..L-1, y=0..W-1
    minimize sum_{x,y} w[y,x]
    subject to: for every placement of an a x b (and optionally b x a) rectangle,
        sum of w over that rectangle >= 1
    """

    gp.setParam("OutputFlag", int(gurobi_msg))

    # Build model
    m = gp.Model("OptimalWeightLayout")

    if numeric_focus:
        m.Params.FeasibilityTol = 1e-9
        m.Params.OptimalityTol  = 1e-9
        m.Params.NumericFocus = 3

    m.Params.OutputFlag = 1 if gurobi_msg else 0

    m.Params.Method = solver_id # PDHG: 6 , Simplex Primal: 0, Barrier: 2

    # Variables: w[y,x] in [0,1]
    w = m.addVars(W, L, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="w")

    # Objective: minimize sum of all weights
    m.setObjective(gp.quicksum(w[y, x] for y in range(W) for x in range(L)), GRB.MINIMIZE)

    # Small rectangle orientations
    rect_dims = [(a, b)]
    if allow_rotation and (a, b) != (b, a):
        rect_dims.append((b, a))

    # Constraints
    for (rect_w, rect_h) in rect_dims:
        if rect_w > L or rect_h > W:
            continue

        max_x = L - rect_w + 1
        max_y = W - rect_h + 1

        for y0 in range(max_y):
            for x0 in range(max_x):
                m.addConstr(
                    gp.quicksum(
                        w[y, x]
                        for y in range(y0, y0 + rect_h)
                        for x in range(x0, x0 + rect_w)
                    ) >= 1.0,
                    name=f"cover_{rect_w}x{rect_h}_{x0}_{y0}",
                )

    # Solve
    m.optimize()
    if m.Status != GRB.OPTIMAL:
        raise RuntimeError(f"Gurobi ended with status {m.Status} (not optimal).")
    
    print("\nLP Finished.")

    obj_value = float(m.ObjVal)

    # Extract solution
    weight_grid = np.zeros((W, L), dtype=np.float64)
    for y in range(W):
        for x in range(L):
            weight_grid[y, x] = w[y, x].X

    # Save image if requested
    if img_path is not None:
        w_min = float(weight_grid.min())
        w_max = float(weight_grid.max())

        if abs(w_max - w_min) < 1e-12:
            norm = np.zeros_like(weight_grid, dtype=np.float64)
        else:
            norm = (weight_grid - w_min) / (w_max - w_min)

        cmap = plt.get_cmap("viridis")
        rgba = cmap(norm)
        rgb = (rgba[..., :3] * 255).astype(np.uint8)

        img_path = Path(img_path)
        if img_path.suffix != "png":
            img_path = img_path.parent / f"{img_path.name}.png"

        img = Image.fromarray(rgb, mode="RGB")
        img.save(img_path)

        print(f"Saved weight image at {img_path}")

    return m, weight_grid, obj_value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="generate_weights.py",
        description="Generate an optimal weighing pattern by solving an LP using Gurobi",
    )

    parser.add_argument("L", type=int, help="Height of larger rectangle")
    parser.add_argument("W", type=int, help="Width of larger rectangle")
    parser.add_argument("a", type=int, help="Height of smaller rectangle")
    parser.add_argument("b", type=int, help="Width of smaller rectangle")

    parser.add_argument("-o", "--out-img", type=Path, help="Path of the weightmap image (.png) to be outputted")
    parser.add_argument("-w", "--out-weights", type=Path, help="Path of the weightmap weights (.npy) to be outputted")
    parser.add_argument("-r", "--disable-rotation", action="store_true", help="If set, rotated smaller rectangles (90°) won't be considered")
    parser.add_argument("-v", "--verbose", action="store_true", help="If set, Gurobi's log will be outputted to stdout")
    parser.add_argument("-s", "--solver", choices=["simplex", "barrier", "pdhg"], default="simplex", help="Solver that Gurobi uses to solve the LP")

    args = parser.parse_args()
    L, W, a, b = args.L, args.W, args.a, args.b
    solver_id = {"simplex": 0, "barrier": 2, "pdhg": 6}[args.solver]

    assert L > 0, f"L must be strictly positive ({L=})"
    assert W > 0, f"W must be strictly positive ({W=})"
    assert a > 0, f"a must be strictly positive ({a=})"
    assert b > 0, f"b must be strictly positive ({b=})"

    assert L >= a and W >= b, f"smaller rectangle must be at least as large as larger rectangle"

    if args.disable_rotation:
        print(f"Solving non-rotated ({L}, {W}, {a}, {b}) LP with {args.solver}...\n")
    else:
        print(f"Solving ({L}, {W}, {a}, {b}) LP with {args.solver}...\n")
        
    if L * W > 100 * 100:
        print(f"Warning: This LP has a lot of weights ({L * W}) and might take a while to solve.")

    model, weights, obj_value = solve_weight_lp(
        L, W, a, b,
        allow_rotation=(not args.disable_rotation),
        gurobi_msg=args.verbose,
        img_path=args.out_img,
        solver_id=solver_id,
        numeric_focus=True
    )
    
    if args.out_weights:
        weights_path: Path = args.out_weights
        if weights_path.suffix != "npy":
            weights_path = weights_path.parent / f"{weights_path.name}.npy"

        np.save(weights_path, weights)
        print(f"Saved weights at {weights_path}")

    print("\nWeight Generation finished.")
    print(f"  - Optimal Value reached: {obj_value}")

    min_weight, max_weight = weights.min(), weights.max()
    print(f"  - Minimum Weight: {min_weight}")
    print(f"  - Maximal Weight: {max_weight}")