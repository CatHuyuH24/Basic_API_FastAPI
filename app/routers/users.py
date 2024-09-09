from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db
from . import oauth2

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_a_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump(mode='json'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/admin/", response_model=list[schemas.UserResponse])
def get_all_users_for_admin(db: Session = Depends(get_db), user_token: schemas.TokenData = Depends(oauth2.get_current_user), limit: int = 5, skip: int = 0):
    print(user_token.role)
    if user_token.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    users = db.query(models.User).limit(limit).limit(limit).offset(skip).all()
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_one_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with ID {user_id} was not found")
    return user
