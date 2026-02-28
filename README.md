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

To compute the optimal weights for smaller instances locally, there also exists a smaller command line utility available at  [upper-bound/weight-generation/smaller-lp/generate_weights.py](/upper-bound/weight-generation/smaller-lp/generate_weights.py). Note that the utility requires the python packages Pillow, numpy, matplotlib and gurobipy to be installed. Additionally, [Gurobi](https://www.gurobi.com/downloads/) must be installed on the machine.  Here is the help output for the utility program used to create smaller weightmaps:

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

## A(m) in A(n)

Upper and lower bound proofs for A(m) in A(n) can be found [here](/Am_in_An/). Here is a table of all relevant directories:

|  | A0 | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | A10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **A0**  | [A0 in A0](/Am_in_An/A0_in_A0/) | [A1 in A0](/Am_in_An/A1_in_A0/) | [A2 in A0](/Am_in_An/A2_in_A0/) | [A3 in A0](/Am_in_An/A3_in_A0/) | [A4 in A0](/Am_in_An/A4_in_A0/) | [A5 in A0](/Am_in_An/A5_in_A0/) | [A6 in A0](/Am_in_An/A6_in_A0/) | [A7 in A0](/Am_in_An/A7_in_A0/) | [A8 in A0](/Am_in_An/A8_in_A0/) | [A9 in A0](/Am_in_An/A9_in_A0/) | [A10 in A0](/Am_in_An/A10_in_A0/) |
| **A1**  |  | [A1 in A1](/Am_in_An/A1_in_A1/) | [A2 in A1](/Am_in_An/A2_in_A1/) | [A3 in A1](/Am_in_An/A3_in_A1/) | [A4 in A1](/Am_in_An/A4_in_A1/) | [A5 in A1](/Am_in_An/A5_in_A1/) | [A6 in A1](/Am_in_An/A6_in_A1/) | [A7 in A1](/Am_in_An/A7_in_A1/) | [A8 in A1](/Am_in_An/A8_in_A1/) | [A9 in A1](/Am_in_An/A9_in_A1/) | [A10 in A1](/Am_in_An/A10_in_A1/) |
| **A2**  |  |  | [A2 in A2](/Am_in_An/A2_in_A2/) | [A3 in A2](/Am_in_An/A3_in_A2/) | [A4 in A2](/Am_in_An/A4_in_A2/) | [A5 in A2](/Am_in_An/A5_in_A2/) | [A6 in A2](/Am_in_An/A6_in_A2/) | [A7 in A2](/Am_in_An/A7_in_A2/) | [A8 in A2](/Am_in_An/A8_in_A2/) | [A9 in A2](/Am_in_An/A9_in_A2/) | [A10 in A2](/Am_in_An/A10_in_A2/) |
| **A3**  |  |  |  | [A3 in A3](/Am_in_An/A3_in_A3/) | [A4 in A3](/Am_in_An/A4_in_A3/) | [A5 in A3](/Am_in_An/A5_in_A3/) | [A6 in A3](/Am_in_An/A6_in_A3/) | [A7 in A3](/Am_in_An/A7_in_A3/) | [A8 in A3](/Am_in_An/A8_in_A3/) | [A9 in A3](/Am_in_An/A9_in_A3/) | [A10 in A3](/Am_in_An/A10_in_A3/) |
| **A4**  |  |  |  |  | [A4 in A4](/Am_in_An/A4_in_A4/) | [A5 in A4](/Am_in_An/A5_in_A4/) | [A6 in A4](/Am_in_An/A6_in_A4/) | [A7 in A4](/Am_in_An/A7_in_A4/) | [A8 in A4](/Am_in_An/A8_in_A4/) | [A9 in A4](/Am_in_An/A9_in_A4/) | [A10 in A4](/Am_in_An/A10_in_A4/) |
| **A5**  |  |  |  |  |  | [A5 in A5](/Am_in_An/A5_in_A5/) | [A6 in A5](/Am_in_An/A6_in_A5/) | [A7 in A5](/Am_in_An/A7_in_A5/) | [A8 in A5](/Am_in_An/A8_in_A5/) | [A9 in A5](/Am_in_An/A9_in_A5/) | [A10 in A5](/Am_in_An/A10_in_A5/) |
| **A6**  |  |  |  |  |  |  | [A6 in A6](/Am_in_An/A6_in_A6/) | [A7 in A6](/Am_in_An/A7_in_A6/) | [A8 in A6](/Am_in_An/A8_in_A6/) | [A9 in A6](/Am_in_An/A9_in_A6/) | [A10 in A6](/Am_in_An/A10_in_A6/) |
| **A7**  |  |  |  |  |  |  |  | [A7 in A7](/Am_in_An/A7_in_A7/) | [A8 in A7](/Am_in_An/A8_in_A7/) | [A9 in A7](/Am_in_An/A9_in_A7/) | [A10 in A7](/Am_in_An/A10_in_A7/) |
| **A8**  |  |  |  |  |  |  |  |  | [A8 in A8](/Am_in_An/A8_in_A8/) | [A9 in A8](/Am_in_An/A9_in_A8/) | [A10 in A8](/Am_in_An/A10_in_A8/) |
| **A9**  |  |  |  |  |  |  |  |  |  | [A9 in A9](/Am_in_An/A9_in_A9/) | [A10 in A9](/Am_in_An/A10_in_A9/) |
| **A10** |  |  |  |  |  |  |  |  |  |  | [A10 in A10](/Am_in_An/A10_in_A10/) |


Lower bounds are given as arrangement files that can be loaded into [noel-friedrich.de/forp](https://noel-friedrich.de/forp/) as `.txt` files. Upper bounds are given as short descriptions contained in appropriate `.txt` files.
