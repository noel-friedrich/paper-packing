import numpy as np

# import and verify weights from disk
weights = np.load("upper-bound/weights/rounded-weights.npy")
assert weights.shape == (1189, 841) and weights.dtype == np.int64

# assert that all valid rectangle placements (horizontal) have weight >= 1e6
assert all(
    weights[i:i+26, j:j+37].sum() >= 1e6
    for i in range(1189-26+1)
    for j in range(841-37+1))

# assert that all valid rectangle placements (vertical) have weight >= 1e6
assert all(
    weights[i:i+37, j:j+26].sum() >= 1e6
    for i in range(1189-37+1)
    for j in range(841-26+1))

# assert the total weight sum is correct and nonnegative weights
assert weights.min() >= 0 and weights.sum() < 1039e6