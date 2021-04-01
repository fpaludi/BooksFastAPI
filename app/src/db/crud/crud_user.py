from typing import Any, Dict, Optional, Union
from sqlalchemy import schema
from sqlalchemy.orm import Session
from dependency_injector.providers import Factory
from src.db.crud.crud_base import CRUDBase
from src.db.models.user import User as UserDbModel
from src.schemas.user import User, UserCreate, UserUpdate
from src.core.security import get_password_hash


class CRUDUser(CRUDBase[UserDbModel, User, UserCreate, UserUpdate]):

    def get_by_username(self,*, username: str) -> Optional[User]:
        db_obj = self.db.query(UserDbModel).filter(UserDbModel.username == username).first()
        return self.schema.from_orm(db_obj)

    def create(self, *, obj_in: UserCreate) -> User:
        db_obj = UserDbModel(
            username=obj_in.username,
            is_superuser=obj_in.is_superuser,
            password_hash=get_password_hash(obj_in.password),
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return self.schema.from_orm(db_obj)

    def update(
        self, *, db_obj: UserDbModel, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            update_data.pop("password")
            update_data["password_hash"] = hashed_password
        return super().update(db_obj=db_obj, obj_in=update_data)

    def is_active(self, user: User) -> bool:
        return user.confirmed

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


CRUDUserFactory = Factory(
    CRUDUser,
    model=UserDbModel,
    schema=User
)
