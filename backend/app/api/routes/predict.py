from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user, get_db
from app.mlmodel.prediction import PredictionService
from app.models import Functions, InputData, User

router = APIRouter()

@router.post("/predict/{model_name}")
async def predict_endpoint(
    model_name: str,
    input_data: InputData,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if model_name not in ["model1", "model2", "model3"]:
        raise HTTPException(status_code=400, detail="Invalid model name")

    functions = session.exec(
        select(Functions).where(Functions.id == current_user.id)
    ).first()
    if not functions:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Payment required for {model_name}",
        )

    if model_name == "model1" and not functions.model1:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Payment required for model1",
        )
    elif model_name == "model2" and not functions.model2:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Payment required for model2",
        )
    elif model_name == "model3" and not functions.model3:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Payment required for model3",
        )

    if model_name == "model1" and functions.credits < 1:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Not enough credits for model1",
        )
    elif model_name == "model2" and functions.credits < 2:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Not enough credits for model2",
        )
    elif model_name == "model3" and functions.credits < 3:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Not enough credits for model3",
        )

    prediction_service = PredictionService(model_name)
    prediction = prediction_service.predict(input_data)

    # Deduct credits based on the model used
    if model_name == "model1":
        functions.credits -= 1
    elif model_name == "model2":
        functions.credits -= 2
    elif model_name == "model3":
        functions.credits -= 3

    session.add(functions)
    session.commit()
    session.refresh(functions)

    return {
        "prediction": prediction["prediction"],
        "credits_left": functions.credits,
    }
