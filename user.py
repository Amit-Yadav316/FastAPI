from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jwt_token import create_token,verify_token
import schemas, models,hashing,emailed
import database
import logging




router=APIRouter(tags=["User"])

@router.post("/user")
async def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    check = db.query(models.User).filter(request.email==models.User.email).first()
    if check:
        raise HTTPException(status_code=400, detail="Email already registered")
    if request.password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Password does not match")
    new_user = models.User(name=request.name, email=request.email, password=hashing.hashed(request.password),confirm_password=hashing.hashed(request.password))
    access_token = create_token(data={"sub": new_user.email})
    verification_url = f'http://localhost:9005/user/{access_token}'
    new_user.verification_token = access_token
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    await emailed.send_email(new_user.email, "Verification for User",verification_url)
    return new_user



@router.get("/user/{token}")
def verify_user(token: str, db: Session = Depends(database.get_db)):
    logging.info(f"Received token: {token}")

    try:
        payload = verify_token(token)
        logging.info(f"Payload: {payload}")
    except HTTPException as e:
        logging.error(f"Error verifying token: {str(e)}")
        raise e
    user = db.query(models.User).filter(token==models.User.verification_token).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = 1
    user.verification_token = None
    db.commit()

    return {"message": "Email verified successfully"}



@router.post("/login")
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(database.get_db)):
    log=db.query(models.User).filter(request.username==models.User.email).first()
    if not log:
        raise HTTPException(status_code=404, detail="User not found")
    if not hashing.verify(request.password,log.password):
        raise HTTPException(status_code=404, detail="Invalid Password")
    if not verify_token(log.verification_token):
        raise HTTPException(status_code=404, detail="Email not verified")
    return {"access_token":log.verification_token,"token_type": "bearer"}


