from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import database
from app import crud


def get_current_user(token: str, db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
