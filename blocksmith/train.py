import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, top_k_accuracy_score
from .dataset import build_dataset

def main():
    X, y = build_dataset(episodes=600)  # a few thousand examples
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = MLPClassifier(
        hidden_layer_sizes=(512, 256),
        activation="relu",
        solver="adam",
        learning_rate_init=1e-3,
        max_iter=60,
        verbose=True,
        random_state=42
    )
    clf.fit(Xtr, ytr)
    ypred = clf.predict(Xte)
    print("Top-1:", accuracy_score(yte, ypred))
    try:
        proba = clf.predict_proba(Xte)
        print("Top-5:", top_k_accuracy_score(yte, proba, k=5))
    except Exception as e:
        print("(Note) predict_proba not available:", e)
    joblib.dump(clf, "blocksmith_mlp.joblib")
    print("Saved model to blocksmith_mlp.joblib")

if __name__ == "__main__":
    main()
