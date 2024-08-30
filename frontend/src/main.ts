import './assets/index.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';

import { VueTelegramPlugin } from 'vue-tg';

import VueScrollPicker from "vue-scroll-picker";
import "vue-scroll-picker/lib/style.css";


const app = createApp(App);

app.use(VueTelegramPlugin);
app.use(VueScrollPicker);

app.use(createPinia());
app.use(router);

app.mount('#app');
