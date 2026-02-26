from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user import User
from app.core.security import decode_access_token, oauth2_scheme


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_id = decode_access_token(token)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user