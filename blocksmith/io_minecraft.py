from __future__ import annotations
from typing import Tuple

try:
    from mcpi.minecraft import Minecraft
    from mcpi import block as _block
except Exception:  # pragma: no cover - optional dependency
    Minecraft = None  # type: ignore
    _block = None  # type: ignore

class MCClient:
    """Real Minecraft client via mcpi (RaspberryJuice)."""
    def __init__(self, host: str = "127.0.0.1", port: int = 4711):
        if Minecraft is None:
            raise RuntimeError("mcpi not available. Install mcpi and ensure RaspberryJuice is running.")
        self.mc = Minecraft.create(address=host, port=port)

    def player_pos(self) -> Tuple[int, int, int]:
        pos = self.mc.player.getTilePos()
        return int(pos.x), int(pos.y), int(pos.z)

    def set_block(self, x: int, y: int, z: int, block_id: int) -> None:
        self.mc.setBlock(x, y, z, block_id)

    def get_block(self, x: int, y: int, z: int) -> int:
        return int(self.mc.getBlock(x, y, z))

    @property
    def block(self):
        return _block
