import numpy as np

weights = np.load("Am_in_An/A10_in_A0/rounded_1189_841_37_26_weights.npy")

assert weights.shape == (1189, 841) and weights.dtype == np.int64
assert weights.min() >= 0
assert weights.sum() < 1039_000_000

# prefix-sum matrix over large rectangle
S = np.zeros((weights.shape[0] + 1, weights.shape[1] + 1), dtype=np.int64)
S[1:, 1:] = weights.cumsum(axis=0).cumsum(axis=1)

def all_rect_sums_at_least(w, h, threshold):
    # returns all sums for (w, h) windows as a 2d array
    sums = S[w:, h:] - S[:-w, h:] - S[w:, :-h] + S[:-w, :-h]
    return sums.min() >= threshold

assert all_rect_sums_at_least(26, 37, 1_000_000)  # horizontal
assert all_rect_sums_at_least(37, 26, 1_000_000)  # vertical