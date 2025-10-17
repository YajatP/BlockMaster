from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

try:
    from .io_minecraft import MCClient
except Exception:  # pragma: no cover
    MCClient = None  # type: ignore

Vec3 = Tuple[int,int,int]

@dataclass
class AgentState:
    pos: Vec3

class WorldBase:
    def get_agent(self) -> AgentState: ...
    def move_agent_to(self, x: int, y: int, z: int) -> None: ...
    def is_walkable(self, x: int, y: int, z: int) -> bool: ...
    def is_occupied(self, x: int, y: int, z: int) -> bool: ...
    def set_block(self, x: int, y: int, z: int, block_id: int) -> None: ...
    def get_block(self, x: int, y: int, z: int) -> int: ...

class GridWorld(WorldBase):
    """In-memory voxel world for tests/CI."""
    def __init__(self, w: int, d: int, h: int, start: Vec3 = (1,1,1), floor_y: int = 0):
        import numpy as np
        self.w, self.d, self.h = w, d, h
        self.grid = np.zeros((w,d,h), dtype=int)  # [x,z,y]
        self.floor_y = floor_y
        self.agent = AgentState(pos=start)

    def in_bounds(self, x: int, y: int, z: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h and 0 <= z < self.d

    def get_agent(self) -> AgentState:
        return self.agent

    def move_agent_to(self, x: int, y: int, z: int) -> None:
        assert self.in_bounds(x,y,z), "Move out of bounds"
        assert self.is_walkable(x,y,z), "Move to non-walkable"
        self.agent = AgentState((x,y,z))

    def is_occupied(self, x: int, y: int, z: int) -> bool:
        if not self.in_bounds(x,y,z): return True
        return bool(self.grid[x,z,y] == 1)

    def is_walkable(self, x: int, y: int, z: int) -> bool:
        if not self.in_bounds(x,y,z): return False
        if self.grid[x,z,y] != 0: return False
        if y == self.floor_y: return True
        return self.grid[x,z,y-1] == 1

    def set_block(self, x: int, y: int, z: int, block_id: int) -> None:
        assert self.in_bounds(x,y,z), "Placement out of bounds"
        self.grid[x,z,y] = 1 if block_id != 0 else 0

    def get_block(self, x: int, y: int, z: int) -> int:
        if not self.in_bounds(x,y,z): return 1
        return int(self.grid[x,z,y])

class MCWorld(WorldBase):  # pragma: no cover
    def __init__(self, client: MCClient):
        self.client = client

    def get_agent(self) -> AgentState:
        return AgentState(self.client.player_pos())

    def move_agent_to(self, x: int, y: int, z: int) -> None:
        self.client.mc.player.setTilePos(x,y,z)  # teleport for simplicity

    def is_walkable(self, x: int, y: int, z: int) -> bool:
        if self.client.get_block(x,y,z) != 0: return False
        if y == 0: return True
        return self.client.get_block(x,y-1,z) != 0

    def is_occupied(self, x: int, y: int, z: int) -> bool:
        return self.client.get_block(x,y,z) != 0

    def set_block(self, x: int, y: int, z: int, block_id: int) -> None:
        self.client.set_block(x,y,z,block_id)

    def get_block(self, x: int, y: int, z: int) -> int:
        return self.client.get_block(x,y,z)
