from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

    users = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id}, name={self.name}, description={self.description})"
