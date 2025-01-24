import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store/index";
import i18n from "./plugins/i18n";

const app = createApp(App);
app.use(router);
app.use(store);
app.use(i18n);

store.watch(
  (state) => state.lang,
  (newLang) => {
    i18n.global.locale = newLang;
  }
);

// Initialize the app
store.dispatch("initializeApp");
app.mount("#app");