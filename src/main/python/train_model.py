import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier


if __name__ == "__main__":
    
    print("Load training data...")
    aug_claims = pd.read_csv("../../../data/preprocessed_claims.csv")
    X = aug_claims["claim"].values
    y = aug_claims["truth_rating"].values
    print(f"Loaded data with shapes: {X.shape}, {y.shape}")
    
    print("Train model")
    vec = TfidfVectorizer()
    vec.fit(X)
    X_ = vec.transform(X)
    clf = PassiveAggressiveClassifier(random_state=417, n_jobs=-1, C=0.01)
    clf.fit(X_, y)
    
    print("Save trained model...")
    joblib.dump(vec, "../../../data/vectorizer_v1.pkl")
    joblib.dump(clf, "../../../data/model_v1.pkl")
    
    print("DONE")