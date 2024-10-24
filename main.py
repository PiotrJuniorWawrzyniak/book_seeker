from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Ustawienia bazy danych SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./book_seeker.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Sesja bazy danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Model bazy danych
Base = declarative_base()

# Inicjalizacja aplikacji FastAPI
app = FastAPI()

# Przykładowy model książki
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)

# Utworzenie tabeli
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Book Seeker App"}

# Zależność, która będzie zwracać sesję bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BookCreate(BaseModel):
    title: str
    author: str

@app.post("/books/")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
