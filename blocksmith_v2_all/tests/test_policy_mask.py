import numpy as np
from blocksmith.policy import Policy
from blocksmith.dataset import GRID_N
import joblib

class DummyClf:
    def predict_proba(self, X):
        import numpy as np
        return np.ones((X.shape[0], GRID_N*GRID_N)) / (GRID_N*GRID_N)

def test_policy_masking(tmp_path):
    path = tmp_path / "m.joblib"
    joblib.dump(DummyClf(), path)
    pol = Policy(str(path))
    current = np.zeros((GRID_N,GRID_N), dtype=int)
    target = current.copy(); target[0,0]=1
    idx = pol.next_cell(current, target)
    assert idx == 0
