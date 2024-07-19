import joblib


def load_model(model_name):
    return joblib.load(f"./models/{model_name}.pkl")


def load_scaler(model_name):
    return joblib.load(f"backend/app/mlmodel/models/Scaler{model_name[-1]}.pkl")