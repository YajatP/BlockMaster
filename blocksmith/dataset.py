from __future__ import annotations
import numpy as np

GRID_N = 16

def grid2d_perimeter(n: int) -> np.ndarray:
    g = np.zeros((n,n), dtype=np.uint8)
    g[0,:]=1; g[-1,:]=1; g[:,0]=1; g[:,-1]=1
    G = np.zeros((GRID_N, GRID_N), dtype=np.uint8)
    G[:n,:n] = g
    return G

def make_episode(n: int) -> list[tuple[np.ndarray, int]]:
    target = grid2d_perimeter(n)
    current = np.zeros_like(target)
    steps = []
    coords = [(r,c) for r in range(n) for c in range(n) if r in (0,n-1) or c in (0,n-1)]
    for (r,c) in coords:
        x = np.concatenate([current.flatten(), target.flatten()])
        y = r*GRID_N + c
        steps.append((x,y))
        current[r,c] = 1
    return steps

def build_dataset(episodes: int = 400, seed: int | None = 42):
    if seed is not None:
        np.random.seed(seed)
    X, y = [], []
    for _ in range(episodes):
        n = np.random.randint(6, GRID_N+1)
        for x_i, y_i in make_episode(n):
            X.append(x_i); y.append(y_i)
    return np.asarray(X, dtype=np.float32), np.asarray(y, dtype=np.int32)
