from fastapi import FastAPI, HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import requests
from models import Book, SessionLocal

app = FastAPI()

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Możesz podać ["http://localhost:8080"] dla większego bezpieczeństwa
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model danych Pydantic
class BookSchema(BaseModel):
    title: str
    author: str

# Funkcja tworząca sesję z bazą danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint do pobierania książek z Open Library API
@app.get("/get_books_by_author/")
def get_books_by_author(author: str):
    url = f"https://openlibrary.org/search.json?author={author}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to connect to Open Library API")

    data = response.json()
    books = [{"title": doc.get("title"), "author": author} for doc in data.get("docs", []) if doc.get("title")]

    if not books:
        raise HTTPException(status_code=404, detail="No books found for the given author")

    return {"books": books}

# Endpoint do zapisywania książki do bazy danych
@app.post("/save_book/")
def save_book(book: BookSchema, db: Session = Depends(get_db)):
    new_book = Book(title=book.title, author=book.author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"message": "Book saved successfully", "book": {"title": book.title, "author": book.author}}

# Endpoint do pobierania zapisanych książek z bazy danych
@app.get("/get_saved_books/")
def get_saved_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return {"books": [{"id": book.id, "title": book.title, "author": book.author} for book in books]}

# Endpoint do usuwania książki z bazy danych
@app.delete("/delete_book/")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
