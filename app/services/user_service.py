from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories.user_repository import ExampleRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate


class ExampleUserService:
    def __init__(self, db: Session):
        self.repo = ExampleRepository(db)

    def create_user(self, data: UserCreate) -> UserRead:
        # Example business rule: unique email
        existing = self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already registered")
        user = self.repo.create(data)
        return UserRead.model_validate(user)

    def list_users(self) -> List[UserRead]:
        users = self.repo.list()
        return [UserRead.model_validate(u) for u in users]

    def get_user(self, user_id: int) -> Optional[UserRead]:
        user = self.repo.get(user_id)
        return UserRead.model_validate(user) if user else None

    def update_user(self, user_id: int, data: UserUpdate) -> Optional[UserRead]:
        user = self.repo.update(user_id, data)
        return UserRead.model_validate(user) if user else None

    def delete_user(self, user_id: int) -> bool:
        return self.repo.delete(user_id)
