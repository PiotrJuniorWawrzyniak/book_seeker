from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./database.db"

# Utwórz silnik SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Utwórz bazę dla modeli
Base = declarative_base()

# Sesja dla operacji z bazą danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Model danych dla tabeli 'books'
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)

# Utwórz tabelę w bazie danych
Base.metadata.create_all(bind=engine)
