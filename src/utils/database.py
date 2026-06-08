# src/utils/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/inventario.db")

os.makedirs("data", exist_ok=True)

engine = create_engine(DATABASE_URL, echo=False)  # echo=True para ver SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

Base = declarative_base()

def criar_tabelas():
    Base.metadata.create_all(bind=engine)

def obter_session():
    return SessionLocal()