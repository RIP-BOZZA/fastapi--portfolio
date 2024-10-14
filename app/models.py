from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped, mapped_column
import os
from dotenv import load_dotenv
import boto3


load_dotenv()


def get_ssm_parameter(param_name):
    """
    Fetch parameter from AWS SSM Parameter Store.
    """
    ssm = boto3.client('ssm', region_name='ap-south-1')
    parameter = ssm.get_parameter(Name=param_name, WithDecryption=True)
    return parameter['Parameter']['Value']


POSTGRES_USERNAME =os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME=os.getenv("DB_NAME")
DB_URL =os.getenv("DB_URL")

# if one is not defined automatically take all from aws
if not  all([POSTGRES_USERNAME ,POSTGRES_PASSWORD ,DB_NAME ,DB_URL]):
    POSTGRES_USERNAME = get_ssm_parameter("/myapp/POSTGRES_USERNAME")
    POSTGRES_PASSWORD = get_ssm_parameter("/myapp/POSTGRES_PASSWORD")
    DB_NAME = get_ssm_parameter("/myapp/DB_NAME")
    DB_URL = get_ssm_parameter("/myapp/DB_URL")

# PostgreSQL connection URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{DB_URL}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)          # Project name
    image_url: Mapped[str] = mapped_column(String)                 # URL of the project image
    role: Mapped[str] = mapped_column(String)                      # Role you worked on the project
    description: Mapped[str] = mapped_column(Text)                 # Detailed description of the project
    link: Mapped[str] = mapped_column(String, nullable=True)       # Optional link to the project
    technologies: Mapped[str] = mapped_column(String)              # Technologies used in the project

Base.metadata.create_all(bind=engine)
