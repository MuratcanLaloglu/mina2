from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user, get_db
from app.models import Functions, User

router = APIRouter()


@router.post("/payment/{option}")
async def process_payment(
    option: str,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    if option not in ["model1", "model2", "model3", "all"]:
        raise HTTPException(status_code=400, detail="Invalid payment option")

    # Simulate a successful payment
    payment_successful = True  # This can be set to False to simulate a failed payment

    if payment_successful:
        # Update user's paid models and credits
        functions = session.exec(
            select(Functions).where(Functions.id == current_user.id)
        ).first()
        if not functions:
            functions = Functions(id=current_user.id)
            session.add(functions)

        if option == "model1":
            functions.model1 = True
            cost = 30
        elif option == "model2":
            functions.model2 = True
            cost = 60
        elif option == "model3":
            functions.model3 = True
            cost = 90
        elif option == "all":
            functions.model1 = True
            functions.model2 = True
            functions.model3 = True
            cost = 100

        functions.credits += cost

        session.add(functions)
        session.commit()
        session.refresh(functions)

        return {
            "message": "Payment successful",
            "paid_models": {
                k: v
                for k, v in functions.__dict__.items()
                if k in ["model1", "model2", "model3"]
            },
            "credits_added": cost,
            "total_credits": functions.credits,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Payment failed"
        )
