<template>
  <div id="app">
    <h1>Book Seeker</h1>
    <BookSearch />
  </div>
</template>

<script>
import BookSearch from "./components/BookSearch.vue";

export default {
  components: {
    BookSearch,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
