from __future__ import annotations
import argparse, time
from .io_minecraft import MCClient
from .world import GridWorld, MCWorld
from .blueprints import hollow_box_3d, grid2d_perimeter, to_3d_from_2d
from .planner import plan_build
from .actions import execute

def run(real: bool, shape: str, w: int, d: int, h: int, origin=(0,1,0), block_id: int = 1, sleep: float = 0.0):
    if shape == "hollow_box":
        target = hollow_box_3d(w,d,h)
    elif shape == "perimeter2d":
        target = to_3d_from_2d(grid2d_perimeter(w), 1)
    else:
        raise ValueError("Unknown shape")
    if real:
        mc = MCClient()
        world = MCWorld(mc)
    else:
        world = GridWorld(w+20, d+20, max(h+5, 5), start=(1,1,1), floor_y=0)
        for x in range(world.w):
            for z in range(world.d):
                world.set_block(x,0,z,1)
    plan = plan_build(origin, target, block_id=block_id)
    execute(world, agent_y=origin[1], actions=plan.actions, reach=4)
    if sleep>0: time.sleep(sleep)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--real", action="store_true", help="Use real Minecraft via mcpi")
    ap.add_argument("--dry", action="store_true", help="Force GridWorld (dry run)")
    ap.add_argument("--shape", default="hollow_box", choices=["hollow_box","perimeter2d"])
    ap.add_argument("--w", type=int, default=8)
    ap.add_argument("--d", type=int, default=8)
    ap.add_argument("--h", type=int, default=4)
    args = ap.parse_args()
    run(real=args.real and not args.dry, shape=args.shape, w=args.w, d=args.d, h=args.h)

if __name__ == "__main__":
    main()
