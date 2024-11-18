# BOOK SEEKER

An application for tracking and managing books from your favorite authors.

## Description

- **Search books by author:** Enter the author's name to fetch a list of books written by them using the Open Library API.
- **Save books to database:** Save the books you want to track to a local database for future reference.
- **Manage saved books:** View and delete books from the saved list directly from the interface.

This project is built using **FastAPI** (for the backend) and **Vue.js** (for the frontend). FastAPI handles the server-side logic and API endpoints, while Vue.js powers the user interface. The application uses the Open Library API to fetch book data.

## Requirements

- Python 3.8 or higher
- Node.js (for frontend development)
- A virtual environment (for Python dependencies)
- npm (Node.js package manager)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd book-seeker
    ```

2. Set up a virtual environment and install the required Python packages:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Navigate to the `frontend/` folder and install Node.js dependencies:
    ```sh
    cd frontend
    npm install
    ```

4. Run the backend server:
    ```sh
    uvicorn main:app --reload
    ```

5. Run the frontend development server:
    ```sh
    npm run serve
    ```

6. Access the application:
    - Open your browser and navigate to `http://localhost:8000` for the backend API (FastAPI documentation available).
    - The frontend (Vue.js) will be accessible at `http://localhost:8080`.

## Usage

1. **Search books by author:** 
   - On the main page, enter the author's name in the input field to fetch a list of books written by them. Click the "Szukaj" (Search) button to fetch the books.

2. **Save books to database:** 
   - Click the "Zapisz książkę" (Save book) button next to a book in the list to save it to your database.

3. **View and manage saved books:** 
   - The list of saved books is displayed below the search results. You can delete books from the saved list by clicking the "Usuń książkę" (Delete book) button next to each book.
   - The saved books list is always visible, regardless of the search results.

4. **Clear the search and book list:**
   - Click the "Wyczyść" (Clear) button to reset the search results and the author's name input, while keeping the saved books list intact.

## Author

- Piotr Wawrzyniak - [piotrjuniorwawrzyniak@gmail.com](mailto:piotrjuniorwawrzyniak@gmail.com)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
