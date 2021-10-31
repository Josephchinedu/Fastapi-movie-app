from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

import os
file_path = os.path.abspath(os.getcwd())+"\database.db"

#SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite:///'+file_path
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()