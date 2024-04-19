import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

load_dotenv()

postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_user = os.getenv("POSTGRES_USER")

# Создание engine и сессии
engine = create_engine(
    f"postgresql+psycopg2://{postgres_user}:{postgres_password}@localhost:5432/text_analyzer"
)
Session = sessionmaker(bind=engine)
session = Session()
