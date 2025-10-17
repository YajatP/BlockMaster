from blocksmith.blueprints import hollow_box_3d

def test_hollow_box_edges_only():
    w,d,h = 6,7,4
    g = hollow_box_3d(w,d,h)
    assert g.shape == (w,d,h)
    assert g[0,0,0] == 1 and g[w-1,d-1,h-1] == 1
    assert g[1,1,1] == 0
    expected = 4*h + 2*(w*2 + d*2)
    assert g.sum() == expected
