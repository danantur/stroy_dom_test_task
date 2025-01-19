import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declarative_base

if not os.path.exists("../data"):
    os.makedirs("../data")

DATABASE_URL = "sqlite:///../data/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session = sessionmaker(bind=engine)
Base: DeclarativeBase = declarative_base()

# Зависимость для получения сессии
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()