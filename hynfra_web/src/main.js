import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./assets/styles/style.css";
import "@/output.css";
import VueFeather from "vue-feather";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

createApp(App)
  .use(store)
  .use(router)
  .use(Toast, {})
  .component(VueFeather.name, VueFeather)
  .mount("#app");
