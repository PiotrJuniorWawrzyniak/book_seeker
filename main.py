# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# from pydantic import BaseModel
#
# # Ustawienia bazy danych SQLite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./book_seeker.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
#
# # Sesja bazy danych
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# # Model bazy danych
# Base = declarative_base()
#
# # Inicjalizacja aplikacji FastAPI
# app = FastAPI()
#
#
# # Model książki
# class Book(Base):
#     __tablename__ = "books"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     author = Column(String, index=True)
#
#
# # Utworzenie tabeli
# Base.metadata.create_all(bind=engine)
#
#
# @app.get("/")
# def read_root():
#     return {"message": "Book Seeker App"}
#
#
# # Zależność, która będzie zwracać sesję bazy danych
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# class BookCreate(BaseModel):
#     title: str
#     author: str
#
#
# @app.post("/books/")
# def create_book(book: BookCreate, db: Session = Depends(get_db)):
#     db_book = Book(title=book.title, author=book.author)
#     db.add(db_book)
#     db.commit()
#     db.refresh(db_book)
#
#     return {
#         "id": db_book.id,
#         "author": db_book.author,
#         "title": db_book.title,
#     }
#
#
# @app.get("/books/")
# def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     books = db.query(Book).offset(skip).limit(limit).all()
#     return [
#         {
#             "id": book.id,
#             "author": book.author,
#             "title": book.title,
#         } for book in books
#     ]
#
#
# # Nowa funkcja DELETE do usuwania książki po ID
# @app.delete("/books/{book_id}")
# def delete_book(book_id: int, db: Session = Depends(get_db)):
#     db_book = db.query(Book).filter(Book.id == book_id).first()
#
#     if db_book is None:
#         raise HTTPException(status_code=404, detail="Book not found")
#
#     db.delete(db_book)
#     db.commit()
#
#     return {"message": f"Book with ID {book_id} has been deleted"}

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

# Ustawienia bazy danych SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./book_seeker.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Sesja bazy danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Model bazy danych
Base = declarative_base()

# Inicjalizacja aplikacji FastAPI
app = FastAPI()


# Model książki
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

    return {
        "id": db_book.id,
        "author": db_book.author,
        "title": db_book.title,
    }


@app.get("/books/")
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return [
        {
            "id": book.id,
            "author": book.author,
            "title": book.title,
        } for book in books
    ]


# Nowa funkcja DELETE do usuwania książki po ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()

    return {"message": f"Book with ID {book_id} has been deleted"}


# Endpoint do przetwarzania URL i zwracania listy książek
@app.get("/fetch_books/")
def fetch_books(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail="Failed to retrieve URL") from e

    soup = BeautifulSoup(response.content, "html.parser")

    # Zmienne dostosowane do selektorów strony, którą chcesz przetwarzać
    book_selector = ".book"       # Zmienna do selektora CSS książki
    title_selector = ".title"     # Zmienna do selektora CSS tytułu
    author_selector = ".author"   # Zmienna do selektora CSS autora

    books = []
    for book_element in soup.select(book_selector):
        title = book_element.select_one(title_selector).get_text(strip=True)
        author = book_element.select_one(author_selector).get_text(strip=True)
        books.append({"title": title, "author": author})

    return {"books": books}
