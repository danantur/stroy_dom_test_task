from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from back.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    def __repr__(self) -> str:
        return f"User(id={self.id}, surname={self.surname}, name={self.name}, email={self.email})"
