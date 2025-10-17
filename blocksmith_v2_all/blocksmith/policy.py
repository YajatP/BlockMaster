from __future__ import annotations
import joblib
import numpy as np
from .dataset import GRID_N

class Policy:
    def __init__(self, path: str = "blocksmith_mlp.joblib"):
        self.clf = joblib.load(path)

    def next_cell(self, current: np.ndarray, target: np.ndarray) -> int:
        x = np.concatenate([current.flatten(), target.flatten()])[None,:]
        valid = (target.flatten()==1) & (current.flatten()==0)
        if hasattr(self.clf, "predict_proba"):
            p = self.clf.predict_proba(x)[0]
            p_mask = np.where(valid, p, -1.0)
            return int(p_mask.argmax())
        try:
            s = self.clf.decision_function(x).ravel()
            s_mask = np.where(valid, s, -1e9)
            return int(s_mask.argmax())
        except Exception:
            return int(np.where(valid)[0][0])
