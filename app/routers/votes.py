from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from . import oauth2

router = APIRouter(prefix="/votes", tags=['Votes'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    try:
        new_vote = models.Vote(**vote.model_dump(mode='json'))
        new_vote.user_id = current_user.user_id
        db.add(new_vote)
        db.commit()
        return new_vote
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Request to vote on post with id {vote.post_id} by User with id {current_user.user_id} failed")
            
