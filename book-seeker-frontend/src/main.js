import { createApp } from 'vue';
import App from './App.vue';
import { createI18n } from 'vue-i18n';
import { lang } from './assets/lang.js';

const i18n = createI18n({
  locale: 'pl',
  messages: lang,
});

createApp(App).use(i18n).mount('#app');
