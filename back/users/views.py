from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session

from back.db import get_db
from back.schemas import *
from back.users.model import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserORM, description="Добавляет пользователя")
def create_user(user: UserData, db: Session = Depends(get_db)):
    db_user = User(name=user.name, surname=user.surname, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserORM], description="Выводит всех пользователей")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserORM, description="Выводит данные об одном пользователе")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserORM, description="Обновляет данные о пользователе")
def update_user(user_id: int, user: UserData, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = user.name
    db_user.surname = user.surname
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", response_model=UserData, description="Удаляет пользователя")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user

@router.put("/{user_id}/set_role", response_model=UserORM, description="Устанавливает роль пользователя в системе")
def update_user(user_id: int, role_id: RoleID, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.role_id = role_id.role_id
    db.commit()
    db.refresh(db_user)
    return db_user