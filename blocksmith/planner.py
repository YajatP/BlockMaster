from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, List, Optional
import numpy as np
from .actions import Action, PlaceBlock, HollowBox

Vec3 = Tuple[int,int,int]

@dataclass
class Plan:
    actions: List[Action]

def detect_hollow_box(target: np.ndarray) -> Optional[Tuple[Vec3, Tuple[int,int,int]]]:
    w,d,h = target.shape
    coords = np.argwhere(target==1)
    if coords.size == 0:
        return None
    xmin, ymin, zmin = coords.min(axis=0)
    xmax, ymax, zmax = coords.max(axis=0)
    W,D,H = (xmax-xmin+1, ymax-ymin+1, zmax-zmin+1)
    ideal = np.zeros_like(target, dtype=np.uint8)
    xs, ys, zs = xmin, ymin, zmin
    xe, ye, ze = xmax, ymax, zmax
    ideal[xs:xe+1, zs, ys] = 1; ideal[xs:xe+1, ze, ys] = 1
    ideal[xs, zs:ze+1, ys] = 1; ideal[xe, zs:ze+1, ys] = 1
    ideal[xs:xe+1, zs, ye] = 1; ideal[xs:xe+1, ze, ye] = 1
    ideal[xs, zs:ze+1, ye] = 1; ideal[xe, zs:ze+1, ye] = 1
    for (x,z) in [(xs,zs),(xs,ze),(xe,zs),(xe,ze)]:
        ideal[x, z, ys:ye+1] = 1
    if np.array_equal(ideal, target):
        return (int(xs), int(ys), int(zs)), (int(W), int(H), int(D))
    return None

def plan_build(origin: Vec3, target: np.ndarray, block_id: int = 1) -> Plan:
    w,d,h = target.shape
    hb = detect_hollow_box(target)
    if hb is not None:
        o, size = hb
        ox, oy, oz = origin
        hx, hy, hz = o
        return Plan([HollowBox((ox+hx, oy+hy, oz+hz), size, block_id)])
    acts: List[Action] = []
    for y in range(h):
        for z in range(d):
            for x in range(w):
                if target[x,z,y] == 1:
                    acts.append(PlaceBlock((origin[0]+x, origin[1]+y, origin[2]+z), block_id))
    return Plan(acts)
