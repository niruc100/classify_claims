import pandas as pd
import joblib

def add_marks(x):
    return f"\"{x}\"@en"

if __name__=="__main__":

    # laod model (and vectorizer)
    print("load resources...")
    test_set = pd.read_csv("../../../data/raw_test_claims.csv", sep=",", index_col=0)
    vec = joblib.load("../../../data/vectorizer_v1.pkl")
    model = joblib.load("../../../data/model_v1.pkl")
    
    print("Predict...")
    X = vec.transform(test_set["claim"])
    predictions = model.predict(X)
    predictions = ["NEITHER" if l == "OTHER" else l for l in predictions]
    
    print("Save predictions")
    # begin to build final format
    final_predictions = test_set[["ID", "claim"]]
    final_predictions.insert(len(final_predictions.columns), "prediction" , predictions)
    final_predictions["claim"] = final_predictions["claim"].apply(lambda x: add_marks(x))
    
    print(f"Final predictions of shape {final_predictions.shape}")
    print("Save predictions...")
    
    final_predictions.reset_index(drop=True).to_csv("../../../output_data/predictions.csv", index=False, header=None, encoding="utf8")
    print("DONE")