from __future__ import annotations
import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, top_k_accuracy_score
from .dataset import build_dataset

def main():
    X, y = build_dataset(episodes=600)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    clf = MLPClassifier(hidden_layer_sizes=(512,256), activation="relu", max_iter=60, random_state=42, verbose=True)
    clf.fit(Xtr, ytr)
    print("Top-1:", accuracy_score(yte, clf.predict(Xte)))
    try:
        proba = clf.predict_proba(Xte)
        print("Top-5:", top_k_accuracy_score(yte, proba, k=5))
    except Exception:
        pass
    joblib.dump(clf, "blocksmith_mlp.joblib")
    print("Saved model to blocksmith_mlp.joblib")

if __name__ == "__main__":
    main()
