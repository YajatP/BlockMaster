from __future__ import annotations
import numpy as np
from typing import Tuple

def voxel_iou(target: np.ndarray, built: np.ndarray) -> float:
    target = target.astype(bool); built = built.astype(bool)
    inter = np.logical_and(target, built).sum()
    union = np.logical_or(target, built).sum()
    return float(inter/union) if union>0 else 1.0

def precision_recall(target: np.ndarray, built: np.ndarray) -> Tuple[float, float]:
    t = target.astype(bool); b = built.astype(bool)
    tp = np.logical_and(t, b).sum()
    fp = np.logical_and(np.logical_not(t), b).sum()
    fn = np.logical_and(t, np.logical_not(b)).sum()
    precision = float(tp/(tp+fp)) if (tp+fp)>0 else 1.0
    recall = float(tp/(tp+fn)) if (tp+fn)>0 else 1.0
    return precision, recall
