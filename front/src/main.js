import { createApp } from 'vue';
import App from './App.vue';

import Aura from '@primevue/themes/aura';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';

import {ref} from 'vue'

import '@/assets/styles.scss';
import '@/assets/tailwind.css';

const app = createApp(App);

app.provide("roles", ref([]))

app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.app-dark'
        }
    }
});
app.use(ToastService);
app.use(ConfirmationService);

app.mount('#app');
