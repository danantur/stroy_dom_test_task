from typing import List, Optional

from pydantic import BaseModel, constr, Field, conint
from back.settings import ROLES_SETTINGS, USERS_SETTINGS

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+(\.[\w]+)+$'


class UserData(BaseModel): # I - Insert
    surname: constr(min_length=1, max_length=USERS_SETTINGS["surname_max_length"]) = Field(description = "Фамилия пользователя", examples=["Иванов"])
    name: constr(min_length=1, max_length=USERS_SETTINGS["name_max_length"]) = Field(description = "Имя пользователя", examples=["Иван"])
    email: constr(pattern=EMAIL_REGEX) = Field(description = "E-mail пользователя", examples=["test@site.com"])  # Проверка на корректный email


class RoleData(BaseModel): # I - Insert
    name: constr(min_length=1, max_length=ROLES_SETTINGS["name_max_length"]) = Field(description = "Название роли", examples=["Пользователь"])
    description: constr(min_length=1, max_length=ROLES_SETTINGS["description_max_length"]) = Field(description = "Описание роли",examples=["Может выполнять только базовые функции"])

class RoleID(BaseModel):
    role_id: int = Field(description = "ID роли", examples=["1"])

class RoleDataWithID(RoleData):
    role_id: int

class UserORM(UserData):
    user_id: int
    role: Optional[RoleDataWithID]

    class Config:
        from_attributes = True


class RoleORM(RoleDataWithID):
    users: Optional[List[UserORM]]

    class Config:
        from_attributes = True
