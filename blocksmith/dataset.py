import numpy as np
from .blueprints import GRID_N, random_target

def make_episode():
    target, n, name = random_target()
    current = np.zeros_like(target)
    steps = []
    # Expert policy: scanline perimeter fill order
    coords = [(r, c) for r in range(n) for c in range(n)
              if r in (0, n - 1) or c in (0, n - 1)]
    for (r, c) in coords:
        x = np.concatenate([current.flatten(), target.flatten()])
        y = r * GRID_N + c  # 0..255
        steps.append((x, y))
        current[r, c] = 1
    return steps

def build_dataset(episodes: int = 400, seed: int | None = 42):
    if seed is not None:
        rng = np.random.default_rng(seed)
        np.random.seed(seed)
    X, y = [], []
    for _ in range(episodes):
        for x_i, y_i in make_episode():
            X.append(x_i); y.append(y_i)
    X = np.asarray(X, dtype=np.float32)
    y = np.asarray(y, dtype=np.int32)
    return X, y
