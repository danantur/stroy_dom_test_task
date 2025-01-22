from typing import List, Optional

from pydantic import BaseModel, constr, Field, conint

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+(\.[\w]+)+$'

    
class RoleData(BaseModel):
    name: constr(min_length=1, max_length=50) = Field(description = "Название роли", examples=["Пользователь"])
    description: constr(min_length=1, max_length=200) = Field(description = "Описание роли",examples=["Может выполнять только базовые функции"])

class RoleDataWithID(RoleData):
    id: int

class UserData(BaseModel):
    surname: constr(min_length=1, max_length=50) = Field(description = "Фамилия пользователя", examples=["Иванов"])
    name: constr(min_length=1, max_length=50) = Field(description = "Имя пользователя", examples=["Иван"])
    email: constr(pattern=EMAIL_REGEX) = Field(description = "E-mail пользователя", examples=["test@site.com"])  # Проверка на корректный email
    role_id: Optional[int] = Field(description="ID роли пользователя", default=None, examples=[None])

class UserORM(BaseModel):
    id: int
    surname: constr(min_length=1, max_length=50) = Field(description = "Фамилия пользователя", examples=["Иванов"])
    name: constr(min_length=1, max_length=50) = Field(description = "Имя пользователя", examples=["Иван"])
    email: constr(pattern=EMAIL_REGEX) = Field(description = "E-mail пользователя", examples=["test@site.com"])  # Проверка на корректный email
    role: Optional[RoleDataWithID] = Field(description="Роль пользователя", default=None)

    class Config:
        from_attributes = True


class RoleORM(RoleDataWithID):
    users: Optional[List[UserORM]] = Field(description="Пользователи с этой ролью")

    class Config:
        from_attributes = True
