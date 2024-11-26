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



const app = createApp(App)
app.use(router)
app.use(PrimeVue,{
    theme:{
        preset: Aura
    }
})
app.component('Button', Button);
app.component('Menu', Menu);
app.directive('ripple', Ripple);
app.component('Badge', Badge);


app.mount('#app')
