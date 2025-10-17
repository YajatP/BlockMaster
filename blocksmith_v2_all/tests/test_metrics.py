import numpy as np
from blocksmith.metrics import voxel_iou, precision_recall

def test_metrics_identity():
    a = np.zeros((4,4,3), dtype=int)
    a[0,0,0]=1; a[1,1,1]=1
    assert voxel_iou(a,a) == 1.0
    p,r = precision_recall(a,a)
    assert p == 1.0 and r == 1.0

def test_metrics_partial():
    t = np.zeros((3,3,2), dtype=int); b = np.zeros_like(t)
    t[0,0,0]=1; t[1,1,0]=1
    b[0,0,0]=1
    iou = voxel_iou(t,b)
    assert 0.0 < iou < 1.0
