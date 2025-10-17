from blocksmith.world import GridWorld
from blocksmith.blueprints import hollow_box_3d
from blocksmith.planner import plan_build
from blocksmith.actions import execute

def test_execute_hollow_box():
    target = hollow_box_3d(4,4,3)
    world = GridWorld(20,20,6, start=(1,1,1), floor_y=0)
    for x in range(world.w):
        for z in range(world.d):
            world.set_block(x,0,z,1)
    plan = plan_build((5,1,5), target, block_id=1)
    execute(world, agent_y=1, actions=plan.actions, reach=4)
    assert world.get_block(5,1,5) == 1
    assert world.get_block(8,3,8) == 1
