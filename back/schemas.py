from typing import List, Optional

from pydantic import BaseModel, constr, Field, conint
from settings import ROLES_SETTINGS, USERS_SETTINGS

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+(\.[\w]+)+$'

    
class RoleData(BaseModel):
    name: constr(min_length=1, max_length=ROLES_SETTINGS["name_max_length"]) = Field(description = "Название роли", examples=["Пользователь"])
    description: constr(min_length=1, max_length=ROLES_SETTINGS["description_max_length"]) = Field(description = "Описание роли",examples=["Может выполнять только базовые функции"])

class RoleDataWithID(RoleData):
    id: int

class UserData(BaseModel):
    surname: constr(min_length=1, max_length=USERS_SETTINGS["surname_max_length"]) = Field(description = "Фамилия пользователя", examples=["Иванов"])
    name: constr(min_length=1, max_length=USERS_SETTINGS["name_max_length"]) = Field(description = "Имя пользователя", examples=["Иван"])
    email: constr(pattern=EMAIL_REGEX) = Field(description = "E-mail пользователя", examples=["test@site.com"])  # Проверка на корректный email
    role_id: Optional[int] = Field(description="ID роли пользователя", default=None, examples=[None])

class UserORM(BaseModel):
    id: int
    surname: constr(min_length=1, max_length=USERS_SETTINGS["surname_max_length"]) = Field(description = "Фамилия пользователя", examples=["Иванов"])
    name: constr(min_length=1, max_length=USERS_SETTINGS["name_max_length"]) = Field(description = "Имя пользователя", examples=["Иван"])
    email: constr(pattern=EMAIL_REGEX) = Field(description = "E-mail пользователя", examples=["test@site.com"])  # Проверка на корректный email
    role: Optional[RoleDataWithID] = Field(description="Роль пользователя", default=None)

    class Config:
        from_attributes = True


class RoleORM(RoleDataWithID):
    users: Optional[List[UserORM]] = Field(description="Пользователи с этой ролью")

    class Config:
        from_attributes = True
