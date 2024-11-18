<template>
  <div class="book-search">
    <h2>Wyszukiwarka książek</h2>
    <input
      type="text"
      v-model="author"
      placeholder="Wpisz nazwisko autora"
    />
    <button @click="fetchBooks">Szukaj</button>

    <ul v-if="books.length">
      <li v-for="book in books" :key="book.title">
        {{ book.title }}
        <button @click="saveBook(book.title, author)">Zapisz książkę</button>
      </li>
    </ul>
    <p v-else>Brak wyników</p>

    <h3>Zapisane książki:</h3>
    <ul v-if="savedBooks.length">
      <li v-for="book in savedBooks" :key="book.id">
        {{ book.title }} ({{ book.author }})
        <button @click="deleteBook(book.id)">Usuń książkę</button>
      </li>
    </ul>
    <p v-else>Brak zapisanych książek</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      author: "",
      books: [],
      savedBooks: [],
    };
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/get_books_by_author/?author=${encodeURIComponent(
            this.author
          )}`
        );
        this.books = response.data.books;
      } catch (error) {
        console.error("Błąd podczas pobierania książek:", error);
        this.books = [];
      }
    },
    async saveBook(title, author) {
      try {
        const payload = {
          title: title || "",
          author: author || "",
        };
        console.log("Wysyłam dane:", payload);
        await axios.post("http://127.0.0.1:8000/save_book/", payload, {
            headers: {
              "Content-Type": "application/json",
            },
        });
        alert(`Książka "${title}" została zapisana!`);
        this.fetchSavedBooks();
      } catch (error) {
        console.error("Błąd podczas zapisywania książki:", error);
      }
    },
    async fetchSavedBooks() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/get_saved_books/");
        this.savedBooks = response.data.books;
      } catch (error) {
        console.error("Błąd podczas pobierania zapisanych książek:", error);
        this.savedBooks = [];
      }
    },
    async deleteBook(id) {
      try {
        await axios.delete(`http://127.0.0.1:8000/delete_book/?book_id=${id}`);
        alert("Książka została usunięta!");
        this.fetchSavedBooks();
      } catch (error) {
        console.error("Błąd podczas usuwania książki:", error);
      }
    },
  },
  mounted() {
    this.fetchSavedBooks();
  },
};
</script>

<style scoped>
.book-search {
  max-width: 600px;
  margin: auto;
  text-align: center;
}

input {
  padding: 8px;
  width: 80%;
  margin-bottom: 10px;
}

button {
  padding: 10px;
  margin: 5px;
  cursor: pointer;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 5px;
  border-bottom: 1px solid #ddd;
}
</style>
