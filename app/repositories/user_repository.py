from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class ExampleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: UserCreate) -> User:
        user = User(email=data.email, full_name=data.full_name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list(self) -> List[User]:
        return self.db.query(User).order_by(User.id.desc()).all()

    def get(self, user_id: int) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def update(self, user_id: int, data: UserUpdate) -> Optional[User]:
        user = self.get(user_id)
        if not user:
            return None
        if data.email is not None:
            user.email = data.email
        if data.full_name is not None:
            user.full_name = data.full_name
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
