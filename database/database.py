from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_NAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_USER


engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}')
Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
    print('Database created.')