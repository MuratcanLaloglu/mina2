import os
from typing import Any

import joblib  # type: ignore

this_dir: str = os.path.dirname(__file__)


def load_model(model_name: str) -> Any:
    return joblib.load(f"{this_dir}/models/{model_name}.pkl")


def load_scaler(model_name: str) -> Any:
    return joblib.load(f"{this_dir}/models/Scaler{model_name[-1]}.pkl")
