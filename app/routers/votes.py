from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql.expression import and_

from ..logging import logging
from .. import models, schemas
from ..database import get_db
from . import oauth2

router = APIRouter(prefix="/votes", tags=['Votes'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VoteResponse)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_exists = db.query(models.Post).filter(models.Post.post_id == vote.post_id).first()
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")
    
    try:
        new_vote = models.Vote(**vote.model_dump(mode='json'))
        new_vote.user_id = current_user.user_id
        db.add(new_vote)
        db.commit()
        return new_vote
    except IntegrityError as e:
        print(e)
        db.rollback()
        previous_vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.user_id, models.Vote.post_id == vote.post_id)
        previous_vote = previous_vote_query.first()
        if previous_vote.upvote == vote.upvote:
            # db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id {current_user.user_id} has already voted on post with id {vote.post_id} with the same upvote status")
        else:
            previous_vote_query.update({"upvote": vote.upvote}, synchronize_session=False)
            db.commit()
            db.refresh(previous_vote)
            return previous_vote
    except (Exception, SQLAlchemyError) as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Request to vote on post with id {vote.post_id} by User with id {current_user.user_id} failed")

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_vote(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(and_(models.Vote.user_id == current_user.user_id, models.Vote.post_id == post_id))
    if not vote_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {current_user.user_id} has not voted on post with id {post_id}")
    else:
        try:
            vote_query.delete(synchronize_session=False)
            db.commit()
        except (Exception, SQLAlchemyError) as e:
            db.rollback()
            logging.error(f"Request to delete vote on post with id {post_id} by User with id {current_user.user_id} failed", exc_info=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Request to delete vote on post with id {post_id} by User with id {current_user.user_id} failed")
