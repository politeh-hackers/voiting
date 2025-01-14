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
            50: '#f7f7f7',  
            100: '#e1e1e1', 
            200: '#cccccc', 
            300: '#999999', 
            400: '#666666', 
            500: '#333333', 
            600: '#1a1a1a', 
            700: '#000000', 
            800: '#000000', 
            900: '#000000', 
            950: '#000000'  
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
