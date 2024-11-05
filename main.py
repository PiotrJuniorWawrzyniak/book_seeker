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


#Nowa funkcja DELETE do usuwania książki po ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()

    return {"message": f"Book with ID {book_id} has been deleted"}


@app.get("/fetch_books/")
def fetch_books(url: str):
    # Pobieranie strony
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail="Failed to retrieve URL") from e

    soup = BeautifulSoup(response.content, "html.parser")
    books = []

    # Próbujemy znaleźć sekcję z książkami na podstawie nagłówków
    section = soup.find(
        lambda tag: tag.name in ["h2", "h3"] and any(
            keyword in tag.get_text() for keyword in ["Twórczość", "Książki", "Powieści", "Bibliografia", "Tytuły"]
        )
    )

    # Jeśli znajdziemy sekcję, przeszukujemy tylko jej obręb
    if section:
        for sibling in section.find_all_next():
            # Stop, jeśli znajdziemy inny nagłówek
            if sibling.name in ["h2", "h3"]:
                break
            # Zbieramy pozycje z list w tej sekcji
            if sibling.name == "ul":
                for li in sibling.find_all("li"):
                    title = li.get_text(strip=True)
                    if title:
                        books.append({"title": title})
    # Jeśli brak sekcji, przeszukujemy całą stronę w poszukiwaniu wszystkich elementów `ul`
    if not books:
        for ul in soup.find_all("ul"):
            for li in ul.find_all("li"):
                title = li.get_text(strip=True)
                if title:
                    books.append({"title": title})

    # Jeśli brak wyników, zwracamy błąd 404
    if not books:
        raise HTTPException(status_code=404, detail="No books found in any section.")

    return {"books": books}
