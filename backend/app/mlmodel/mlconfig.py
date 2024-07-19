import os

import joblib

this_dir = os.path.dirname(__file__)

def load_model(model_name):
    return joblib.load(f"{this_dir}/models/{model_name}.pkl")


def load_scaler(model_name):
    return joblib.load(f"{this_dir}/models/Scaler{model_name[-1]}.pkl")

