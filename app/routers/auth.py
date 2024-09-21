from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from . import oauth2
from ..database import get_db
from .. import models, password

router = APIRouter(prefix = "/login", tags=['Authentication'])

@router.post("/", status_code=status.HTTP_200_OK)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    
    if not user or not password.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        # 404 would be easier to understand for the client if not found, but 403 is more appropriate for auth failure (security)
    
    access_token = oauth2.create_access_token(data = {"user_id": user.user_id, "role": user.role})
    
    return {"access_token": access_token, "token_type":"bearer"}
