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
      <li v-for="book in books" :key="book.title">{{ book.title }}</li>
    </ul>
    <p v-else>Brak wyników</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      author: "",
      books: [],
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
