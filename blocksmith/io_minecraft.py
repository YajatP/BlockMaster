from mcpi.minecraft import Minecraft
from mcpi import block as _block

class MC:
    """Thin wrapper around mcpi for clarity and future extension."""
    def __init__(self, host: str = "127.0.0.1", port: int = 4711):
        self.mc = Minecraft.create(address=host, port=port)

    def player_pos(self):
        pos = self.mc.player.getTilePos()
        # Ensure ints
        return int(pos.x), int(pos.y), int(pos.z)

    def set_block(self, x: int, y: int, z: int, block_id: int):
        self.mc.setBlock(x, y, z, block_id)

    def set_blocks(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, block_id: int):
        self.mc.setBlocks(x1, y1, z1, x2, y2, z2, block_id)

    @property
    def block(self):
        return _block
