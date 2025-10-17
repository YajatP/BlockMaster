from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, List, Iterable
from .nav import astar_2d

Vec3 = Tuple[int,int,int]

@dataclass
class MoveTo:
    target: Vec3

@dataclass
class PlaceBlock:
    pos: Vec3
    block_id: int

@dataclass
class FillLine:
    start: Vec3
    end: Vec3
    block_id: int

@dataclass
class HollowBox:
    origin: Vec3
    size: Tuple[int,int,int]
    block_id: int

Action = MoveTo | PlaceBlock | FillLine | HollowBox

def plan_line(start: Vec3, end: Vec3, block_id: int) -> List[Action]:
    (x1,y1,z1), (x2,y2,z2) = start, end
    assert (x1==x2) + (y1==y2) + (z1==z2) >= 2, "FillLine must be axis-aligned"
    acts: List[Action] = []
    if x1 != x2:
        step = 1 if x2>x1 else -1
        for x in range(x1, x2+step, step):
            acts.append(PlaceBlock((x,y1,z1), block_id))
    elif z1 != z2:
        step = 1 if z2>z1 else -1
        for z in range(z1, z2+step, step):
            acts.append(PlaceBlock((x1,y1,z), block_id))
    else:
        step = 1 if y2>y1 else -1
        for y in range(y1, y2+step, step):
            acts.append(PlaceBlock((x1,y,z1), block_id))
    return acts

def macro_hollow_box(origin: Vec3, size: Tuple[int,int,int], block_id: int) -> List[Action]:
    x0,y0,z0 = origin
    w,h,d = size
    x1, y1, z1 = x0+w-1, y0+h-1, z0+d-1
    edges: List[Action] = []
    edges += plan_line((x0,y0,z0),(x1,y0,z0), block_id)
    edges += plan_line((x1,y0,z0),(x1,y0,z1), block_id)
    edges += plan_line((x1,y0,z1),(x0,y0,z1), block_id)
    edges += plan_line((x0,y0,z1),(x0,y0,z0), block_id)
    edges += plan_line((x0,y1,z0),(x1,y1,z0), block_id)
    edges += plan_line((x1,y1,z0),(x1,y1,z1), block_id)
    edges += plan_line((x1,y1,z1),(x0,y1,z1), block_id)
    edges += plan_line((x0,y1,z1),(x0,y1,z0), block_id)
    for (x,z) in [(x0,z0),(x0,z1),(x1,z0),(x1,z1)]:
        edges += plan_line((x,y0,z),(x,y1,z), block_id)
    return edges

def execute(world, agent_y: int, actions: Iterable[Action], reach: int = 4) -> None:
    for act in actions:
        if isinstance(act, MoveTo):
            path = astar_2d(world, world.get_agent().pos, act.target)
            if path is None:
                raise RuntimeError(f"Path not found to {act.target}")
            for p in path[1:]:
                world.move_agent_to(*p)
        elif isinstance(act, PlaceBlock):
            tx, ty, tz = act.pos
            ax, ay, az = world.get_agent().pos
            candidate = None
            for dx, dz in [(1,0),(-1,0),(0,1),(0,-1),(2,0),(-2,0),(0,2),(0,-2)]:
                px, py, pz = tx+dx, ay, tz+dz
                if abs(px-tx)+abs(pz-tz) <= reach and world.is_walkable(px, py, pz):
                    candidate = (px, py, pz); break
            if candidate is None and abs(ax-tx)+abs(az-tz) <= reach:
                candidate = (ax, ay, az)
            if candidate is None:
                raise RuntimeError(f"No reachable placement tile near {act.pos}")
            path = astar_2d(world, world.get_agent().pos, candidate)
            if path is None:
                raise RuntimeError(f"Path not found to placement tile {candidate}")
            for p in path[1:]:
                world.move_agent_to(*p)
            world.set_block(tx, ty, tz, act.block_id)
        elif isinstance(act, FillLine):
            for sub in plan_line(act.start, act.end, act.block_id):
                execute(world, agent_y, [sub], reach)
        elif isinstance(act, HollowBox):
            for sub in macro_hollow_box(act.origin, act.size, act.block_id):
                execute(world, agent_y, [sub], reach)
        else:
            raise ValueError(f"Unknown action {act}")
