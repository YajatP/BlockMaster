import numpy as np

GRID_N = 16  # fixed input size for simple examples

def _pad_to_grid(mat: np.ndarray, n: int = GRID_N) -> np.ndarray:
    M = np.zeros((n, n), dtype=np.uint8)
    h, w = mat.shape
    M[:h, :w] = mat
    return M

def perimeter_mask(n: int) -> np.ndarray:
    m = np.zeros((n, n), dtype=np.uint8)
    m[0, :] = 1; m[-1, :] = 1; m[:, 0] = 1; m[:, -1] = 1
    return m

def hollow_square(n: int) -> np.ndarray:
    return perimeter_mask(n)

def pillar(h: int, n: int = 1) -> np.ndarray:
    # single block footprint; height handled at deploy-time (y-axis)
    m = np.zeros((n, n), dtype=np.uint8)
    m[0, 0] = 1
    return m

def random_target(max_n: int = 16, min_n: int = 6) -> tuple[np.ndarray, int, str]:
    """Return (target_grid16, logical_n, name) for a random simple blueprint."""
    n = int(np.random.randint(min_n, max_n + 1))
    choice = np.random.choice(["perimeter", "hollow_square"])  # extend as needed
    if choice in ("perimeter", "hollow_square"):
        tgt = hollow_square(n)
    else:
        tgt = hollow_square(n)
    return _pad_to_grid(tgt), n, choice
