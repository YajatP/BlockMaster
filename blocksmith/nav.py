from __future__ import annotations
from typing import Tuple, List, Dict, Optional
import heapq

Vec3 = Tuple[int,int,int]

def astar_2d(world, start: Vec3, goal: Vec3) -> Optional[List[Vec3]]:
    sx, sy, sz = start
    gx, gy, gz = goal
    assert sy == gy, "A* only supports same Y plane"
    y = sy

    def neighbors(x: int, z: int):
        for dx, dz in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, nz = x+dx, z+dz
            if world.is_walkable(nx, y, nz):
                yield (nx, y, nz)

    def h(x: int, z: int) -> int:
        return abs(x-gx) + abs(z-gz)

    open_set = [(0, (sx,y,sz))]
    came: Dict[Vec3, Optional[Vec3]] = {(sx,y,sz): None}
    g: Dict[Vec3, int] = {(sx,y,sz): 0}

    while open_set:
        _, curr = heapq.heappop(open_set)
        if curr == (gx,y,gz):
            path = [curr]
            while came[curr] is not None:
                curr = came[curr]  # type: ignore
                path.append(curr)
            return list(reversed(path))
        cx, _, cz = curr
        for n in neighbors(cx, cz):
            nd = g[curr] + 1
            if n not in g or nd < g[n]:
                g[n] = nd
                came[n] = curr
                heapq.heappush(open_set, (nd + h(n[0], n[2]), n))
    return None
