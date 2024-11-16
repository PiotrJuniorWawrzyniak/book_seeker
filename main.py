from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


# Nowy endpoint do pobierania książek po autorze
@app.get("/get_books_by_author/")
def get_books_by_author(author: str):
    # Formatujemy zapytanie do Open Library API
    url = f"https://openlibrary.org/search.json?author={author}"

    # Wysyłamy zapytanie do API
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to connect to Open Library API")

    data = response.json()
    books = []

    # Przetwarzamy odpowiedź, aby zwrócić tylko tytuły książek
    for doc in data.get("docs", []):
        title = doc.get("title")
        if title:
            books.append({"title": title})

    # Jeśli nie znaleziono książek, zwracamy odpowiedni komunikat
    if not books:
        raise HTTPException(status_code=404, detail="No books found for the given author")

    return {"books": books}
