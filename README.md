# BOOK SEEKER

An application for tracking new books from favorite authors.

## Description
- **Add a URL to track books:** Enter the URL (e.g., author's main page or 'Works' tab) to scrape and retrieve a list of books.
- **Filter books:** Remove books you already own from the list, leaving only the ones you're missing.
- **Save to database:** Save the filtered or full list of books to a database for future reference, making it easier to keep track of new releases.

This project is built using FastAPI (for the backend) and Vue.js (for the frontend). FastAPI handles the server-side logic and API endpoints, while Vue.js powers the user interface. The application also uses BeautifulSoup for web scraping.

## Requirements
- Python 3.8 or higher
- Node.js (for frontend development)
- A virtual environment (for Python dependencies)

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
1. **Add a URL to scrape:** 
   - On the main page, enter the URL of the author's page to scrape for book data.
   
2. **Filter books:** 
   - Remove books from the list that you already own.

3. **Save to database:** 
   - Save the filtered list to keep track of books you're missing.

## Author
- Piotr Wawrzyniak - [piotrjuniorwawrzyniak@gmail.com](mailto:piotrjuniorwawrzyniak@gmail.com)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
