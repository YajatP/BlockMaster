import time
import numpy as np
from mcpi import block
from .io_minecraft import MC
from .blueprints import random_target, GRID_N
from .policy import Policy

def build_with_policy(block_id: int = block.BRICK_BLOCK.id, sleep_s: float = 0.02):
    mc = MC()
    pol = Policy()
    target, n, name = random_target()
    current = np.zeros_like(target, dtype=np.uint8)

    x0, y0, z0 = mc.player_pos()
    # Offset so we don't collide with the player
    x0 += 3; z0 += 3

    print(f"Deploying blueprint '{name}' of logical size {n}x{n} (padded to {GRID_N}x{GRID_N}).")
    placed = 0
    total = int(target.sum())

    while (current < target).any():
        idx = pol.next_cell(current, target)
        r, c = divmod(idx, GRID_N)
        if target[r, c] == 1 and current[r, c] == 0:
            mc.set_block(x0 + c, y0, z0 + r, block_id)
            current[r, c] = 1
            placed += 1
            if sleep_s > 0:
                time.sleep(sleep_s)

    print(f"Done. Placed {placed}/{total} blocks.")

def main():
    build_with_policy()

if __name__ == "__main__":
    main()
