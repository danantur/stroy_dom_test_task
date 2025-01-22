from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from roles.model import Role
from schemas import RoleORM, RoleData

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=RoleORM, description="Создать роль")
def create_role(role: RoleData, db: Session = Depends(get_db)):
    db_role = Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.get("/", response_model=List[RoleORM], description="Вывести все роли")
def read_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles


@router.get("/{role_id}", response_model=RoleORM, description="Вывести конкретную роль")
def read_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/{role_id}", response_model=RoleORM, description="Обновить роль")
def update_role(role_id: int, role: RoleData, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()

    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    db_role.name = role.name
    db_role.description = role.description
    db.commit()
    db.refresh(db_role)
    return db_role


@router.delete("/{role_id}", response_model=RoleData, description="Удалить роль")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(db_role)
    db.commit()
    return db_role