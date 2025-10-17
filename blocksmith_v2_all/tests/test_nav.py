from blocksmith.world import GridWorld
from blocksmith.nav import astar_2d

def test_astar_basic():
    gw = GridWorld(20,20,3, start=(1,1,1), floor_y=0)
    for x in range(gw.w):
        for z in range(gw.d):
            gw.set_block(x,0,z,1)
    for x in range(2,15):
        gw.set_block(x,1,5,1)
    gw.set_block(8,1,5,0)
    path = astar_2d(gw, (1,1,1), (10,1,10))
    assert path is not None
    assert path[0] == (1,1,1) and path[-1] == (10,1,10)
