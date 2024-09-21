from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db
from ..config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode['exp'] = expire
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm) # a string, not a list

def verify_and_extract_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        id: int = payload.get("user_id")
        role: str = payload.get("role")
        if not id or not role:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, role=role)
        return token_data
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"}) # fixed, standardized

    token_data = verify_and_extract_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.user_id == token_data.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    return user
