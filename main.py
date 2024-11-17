from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Możesz podać ["http://localhost:8080"] dla większego bezpieczeństwa
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint do pobierania książek po autorze
@app.get("/get_books_by_author/")
def get_books_by_author(author: str):
    url = f"https://openlibrary.org/search.json?author={author}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to connect to Open Library API")

    data = response.json()
    books = [{"title": doc.get("title")} for doc in data.get("docs", []) if doc.get("title")]

    if not books:
        raise HTTPException(status_code=404, detail="No books found for the given author")

    return {"books": books}
