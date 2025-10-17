import joblib
import numpy as np
from .blueprints import GRID_N

class Policy:
    def __init__(self, path: str = "blocksmith_mlp.joblib") -> None:
        self.clf = joblib.load(path)

    def next_cell(self, current: np.ndarray, target: np.ndarray) -> int:
        x = np.concatenate([current.flatten(), target.flatten()])[None, :]
        # Mask invalid moves (only cells where target==1 and current==0)
        valid_mask = (target.flatten() == 1) & (current.flatten() == 0)
        # Prefer probabilities if available, else fall back to predict on masked candidates
        if hasattr(self.clf, "predict_proba"):
            probs = self.clf.predict_proba(x)[0]
            masked = np.where(valid_mask, probs, -1.0)
            return int(masked.argmax())
        else:
            # Fallback: brute-force best among valid candidates using decision_function or predict
            try:
                scores = self.clf.decision_function(x).ravel()
                masked = np.where(valid_mask, scores, -1e9)
                return int(masked.argmax())
            except Exception:
                candidates = np.where(valid_mask)[0]
                # Just pick the first valid if no scoring available
                return int(candidates[0])
