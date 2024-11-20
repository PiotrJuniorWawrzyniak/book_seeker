<template>
  <div class="book-search">
    <h2>{{ $t('title') }}</h2>
    <input
      type="text"
      v-model="author"
      :placeholder="$t('placeholder')"
      @keyup.enter="fetchBooks"
    />
    <button @click="fetchBooks">{{ $t('search') }}</button>
    <button @click="clearSearch">{{ $t('clear') }}</button>

    <ul v-if="books.length">
      <li v-for="book in books" :key="book.title">
        {{ book.title }}
        <button @click="saveBook(book.title, author)">{{ $t('save') }}</button>
      </li>
    </ul>
    <p v-else>{{ $t('noResults') }}</p>

    <h3>{{ $t('savedBooks') }}</h3>
    <ul v-if="savedBooks.length">
      <li v-for="book in savedBooks" :key="book.id">
        {{ book.title }} ({{ book.author }})
        <button @click="deleteBook(book.id, book.title)">{{ $t('deleteBook') }}</button>
      </li>
    </ul>
    <p v-else>{{ $t('noSavedBooks') }}</p>

    <div>
      <button @click="setLanguage('pl')">PL</button>
      <button @click="setLanguage('en')">EN</button>
    </div>
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
          `http://127.0.0.1:8000/get_books_by_author/?author=${encodeURIComponent(this.author)}`
        );
        this.books = response.data.books;

        if (this.books.length === 0) {
          alert(this.$t('noResultsAlert'));
        }
      } catch (error) {
        if (error.response && error.response.status === 404) {
          alert(this.$t('noResultsAlert'));
        } else {
          console.error("Błąd podczas pobierania książek:", error);
        }
        this.books = [];
      }
    },
    async saveBook(title, author) {
      try {
        const payload = { title, author };
        await axios.post("http://127.0.0.1:8000/save_book/", payload, {
          headers: { "Content-Type": "application/json" },
        });
        alert(this.$t('bookSaved', { title }));
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
    async deleteBook(id, title) {
      try {
        await axios.delete(`http://127.0.0.1:8000/delete_book/?book_id=${id}`);
        alert(this.$t('bookDeleted', { title }));
        this.fetchSavedBooks();
      } catch (error) {
        console.error("Błąd podczas usuwania książki:", error);
      }
    },
    clearSearch() {
      this.author = "";
      this.books = [];
    },
    setLanguage(lang) {
      this.$i18n.locale = lang;
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
