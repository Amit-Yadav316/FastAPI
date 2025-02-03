from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jwt_token import create_token,verify_reset_token
import schemas, models,hashing,emailed
import database
import logging

router=APIRouter(tags=["Reset"])

@router.post("/password-reset")
async def password_reset(request: schemas.PasswordReset, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(request.email == models.User.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email not found")

    reset_token = create_token({"sub": user.email})
    user.verification_token = reset_token
    verification_url = f'http://localhost:9005/reset-password/{user.id}/{reset_token}'

    await emailed.send_email(user.email, "Reset Password", f"Verification code:{verification_url}")

    return {"message": "Password reset email sent"}

@router.post("/reset-password/{id}/{token}")
async def reset_password(id: int,token: str,request: schemas.PasswordUpdate ,db: Session = Depends(database.get_db)):
    logging.info(f"Received request body: {request}")

    try:
        payload = verify_reset_token(token)
        if not payload:
            raise HTTPException(status_code=400, detail="Invalid token")
        logging.info(f"Decoded Payload: {payload}")
        user_email = payload.get("sub")
    except HTTPException as e:
        logging.error(f"Error verifying token: {str(e)}")
        raise e

    user = db.query(models.User).filter(id==models.User.id ).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if request.new_password != request.confirm_new_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    user.password = hashing.hashed(request.new_password)
    user.confirm_password = hashing.hashed(request.confirm_new_password)
    user.verification_token = None
    db.commit()

    return {"message": "Password reset successful"}