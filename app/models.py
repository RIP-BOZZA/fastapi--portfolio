from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped, mapped_column


# PostgreSQL connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/portfolio_db"

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
