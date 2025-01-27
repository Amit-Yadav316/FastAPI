from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import models,database
from jwt_token import token
from sqlalchemy.orm import Session
import hashing


router=APIRouter(tags=["Login"])


@router.post("/login")
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(database.get_db)):
    log=db.query(models.User).filter(request.username==models.User.email).first()
    if not log:
        raise HTTPException(status_code=404, detail="User not found")
    if not hashing.verify(request.password,log.password):
        raise HTTPException(status_code=404, detail="Invalid Password")
    access_token=token(data={"sub":log.email})
    return {"access_token":access_token,"token_type":"bearer"}




