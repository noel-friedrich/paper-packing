The area bound of (841, 594, 37, 26) is 519.2869022869023, giving an upper bound of 519.  
We provide a proof that 518 is also an upper bound:

Using an argument as presented in the paper, we provide a rounded weightmap
available at [/Am_in_An/A10_in_A1/rounded_841_594_37_26_weights.npy](/Am_in_An/A10_in_A1/rounded_841_594_37_26_weights.npy).

This weightmap can be machine-verified like the proof presented in the paper
using the python script at [/Am_in_An/A10_in_A1/verify_A10_A1_weights.py](/Am_in_An/A10_in_A1/verify_A10_A1_weights.py).

The weights are also available in unrounded form available at
[/Am_in_An/A10_in_A1/optimal_841_594_37_26_weights.npy](/Am_in_An/A10_in_A1/optimal_841_594_37_26_weights.npy). The weight sum is `518.8261021485345`.

The weights were found using a similar method to the one presented in the paper,
i.e., by solving the large linear program using Gurobi and the PDHG method.

![/Am_in_An/A10_in_A1/optimal_841_594_37_26_weights.png](/Am_in_An/A10_in_A1/optimal_841_594_37_26_weights.png)