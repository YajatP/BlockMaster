from __future__ import annotations
import argparse
from .blueprints import hollow_box_3d, grid2d_perimeter, to_3d_from_2d
from .planner import plan_build
from .world import GridWorld
from .actions import execute

def plan_cmd(args):
    target = hollow_box_3d(args.w,args.d,args.h) if args.shape=="hollow_box" else to_3d_from_2d(grid2d_perimeter(args.w),1)
    plan = plan_build((0,1,0), target, block_id=1)
    print(f"Plan has {len(plan.actions)} actions.")

def simulate_cmd(args):
    target = hollow_box_3d(args.w,args.d,args.h) if args.shape=="hollow_box" else to_3d_from_2d(grid2d_perimeter(args.w),1)
    world = GridWorld(args.w+10, args.d+10, max(args.h+5,5), start=(1,1,1), floor_y=0)
    for x in range(world.w):
        for z in range(world.d):
            world.set_block(x,0,z,1)
    plan = plan_build((2,1,2), target, block_id=1)
    execute(world, agent_y=1, actions=plan.actions, reach=4)
    print("Simulation done.")

def main():
    ap = argparse.ArgumentParser(prog="blocksmith")
    sub = ap.add_subparsers()

    p1 = sub.add_parser("plan", help="Plan actions for a shape")
    p1.add_argument("--shape", default="hollow_box", choices=["hollow_box","perimeter2d"])
    p1.add_argument("--w", type=int, default=8)
    p1.add_argument("--d", type=int, default=8)
    p1.add_argument("--h", type=int, default=4)
    p1.set_defaults(func=plan_cmd)

    p2 = sub.add_parser("simulate", help="Run plan in GridWorld")
    p2.add_argument("--shape", default="hollow_box", choices=["hollow_box","perimeter2d"])
    p2.add_argument("--w", type=int, default=8)
    p2.add_argument("--d", type=int, default=8)
    p2.add_argument("--h", type=int, default=4)
    p2.set_defaults(func=simulate_cmd)

    args = ap.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
