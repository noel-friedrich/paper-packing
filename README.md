# paper-packing
Materials regarding the paper packing project, proving that exactly 1038 sheets of A10 fit into one A0 orthogonally.

## Links

- YouTube video about this project: [youtu.be/zDKBCIMkDbw](https://youtu.be/zDKBCIMkDbw?si=bkWE1IyyBZIP6sHm)
- Library of Papel: [noel-friedrich.de/papel/](https://noel-friedrich.de/papel/)
- **F**un **O**rthogonal **R**ectangle **P**acking Website: [noel-friedrich.de/forp/](https://noel-friedrich.de/forp/)

## Lower Bound

The lower bound is proven by giving an arrangement of 1038 sheets of A10 in a single A0. The packing is avaiable as a .txt file [here](/lower-bound/forp_1038s-1189x841-37x26.txt) and as an image (vector graphic [here](/lower-bound/forp_1038s-1189x841-37x26.svg)).

## Upper Bound

The optimal weights for the (1189, 841, 37, 26) instance can be found at [upper-bound/weights](/upper-bound/weights/).

The code used for generating this large weightmap can be found at [upper-bound/weight-generation/large-lp](/upper-bound/weight-generation/large-lp/).

### Smaller Weight Generation

To compute the optimal weights for smaller instances locally, there also exists a smaller command line utility available at  [upper-bound/weight-generation/smaller-lp/generate_weights.py](/upper-bound/weight-generation/smaller-lp/generate_weights.py). Note that the utility requires the python packages Pillow, numpy, matplotlib and gurobipy to be installed. Additionally, [Gurobi](https://www.gurobi.com/downloads/) must be installed on the machine.  Here is the help output for the utility:

```
usage: generate_weights.py [-h] [-o OUT_IMG] [-w OUT_WEIGHTS] [-r] [-v] [-s {simplex,barrier,pdhg}] L W a b

Generate an optimal weighing pattern by solving an LP using Gurobi

positional arguments:
  L                     Height of larger rectangle
  W                     Width of larger rectangle
  a                     Height of smaller rectangle
  b                     Width of smaller rectangle

options:
  -h, --help            show this help message and exit
  -o OUT_IMG, --out-img OUT_IMG
                        Path of the weightmap image (.png) to be outputted
  -w OUT_WEIGHTS, --out-weights OUT_WEIGHTS
                        Path of the weightmap weights (.npy) to be outputted
  -r, --disable-rotation
                        If set, rotated smaller rectangles (90°) won't be considered
  -v, --verbose         If set, Gurobi's log will be outputted to stdout
  -s {simplex,barrier,pdhg}, --solver {simplex,barrier,pdhg}
                        Solver that Gurobi uses to solve the LP
```