import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import './style.css'
import App from './App.vue'
import router from './router'
import Button from 'primevue/button';
import Menu from 'primevue/menu';
import Ripple from 'primevue/ripple';
import Badge from 'primevue/badge';

import { definePreset } from '@primevue/themes';

const app = createApp(App)

const MyPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '#f7f7f7',  // светлый оттенок черного (почти белый)
            100: '#e1e1e1',  // чуть темнее
            200: '#cccccc',  // еще темнее
            300: '#999999',  // серый
            400: '#666666',  // темно-серый
            500: '#333333',  // черный
            600: '#1a1a1a',  // еще темнее
            700: '#000000',  // черный
            800: '#000000',  // черный
            900: '#000000',  // черный
            950: '#000000'   // черный
        }
    }
});
app.use(router)
app.use(PrimeVue,{
    theme: {
        preset: MyPreset
    }
})
app.component('Button', Button);
app.component('Menu', Menu);
app.directive('ripple', Ripple);
app.component('Badge', Badge);

app.mount('#app')
