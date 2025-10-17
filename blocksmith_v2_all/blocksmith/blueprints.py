from __future__ import annotations
import numpy as np

def hollow_box_3d(w: int, d: int, h: int) -> np.ndarray:
    assert w>=2 and d>=2 and h>=2
    arr = np.zeros((w,d,h), dtype=np.uint8)
    arr[:,0,0]=1; arr[:,d-1,0]=1; arr[0,:,0]=1; arr[w-1,:,0]=1
    arr[:,0,h-1]=1; arr[:,d-1,h-1]=1; arr[0,:,h-1]=1; arr[w-1,:,h-1]=1
    for (x,z) in [(0,0),(0,d-1),(w-1,0),(w-1,d-1)]:
        arr[x,z,:]=1
    return arr

def pillar_3d(h: int) -> np.ndarray:
    arr = np.zeros((1,1,h), dtype=np.uint8)
    arr[0,0,:]=1
    return arr

def grid2d_perimeter(n: int) -> np.ndarray:
    g = np.zeros((n,n), dtype=np.uint8)
    g[0,:]=1; g[-1,:]=1; g[:,0]=1; g[:,-1]=1
    return g

def to_3d_from_2d(g2: np.ndarray, height: int = 1) -> np.ndarray:
    w,d = g2.shape
    g3 = np.zeros((w,d,height), dtype=np.uint8)
    g3[:,:,0] = g2
    return g3
