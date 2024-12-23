import { createRouter, createWebHistory } from 'vue-router'
import Main from './components/LoginAdmin.vue'
import Base from './components/AdminPanel.vue'
import Form from './components/Category.vue'
import Media from './components/Media.vue'
import Admin from './components/RegisterAdmin.vue'
import Appeals from './components/Appeals.vue'
import Actual from './components/Actual.vue'

export default createRouter(
    {
        history: createWebHistory(),
        routes: [
            {
                path: '/',
                redirect: '/Main', // Начальный маршрут
            },
            {
                name: 'Home',
                path: '/Main',
                component: Main,
            },
            {
                name: 'Base',
                path: '/Base',
                component: Base, // Основной компонент
                children:
                    [
                        {
                            name: 'Form',
                            path: '/Form', // Дочерний маршрут (без начального "/")
                            component: Form, // Компонент HelloWorld.vue
                        },
                        {
                            name: 'Media',
                            path: '/Media', // Дочерний маршрут (без начального "/")
                            component: Media, // Компонент HelloWorld.vue
                        },
                        {
                            name: 'Appeals',
                            path: '/Appeals',
                            component: Appeals
                        },
                        {
                            name:'Actual',
                            path:'/Actual',
                            component: Actual
                        }
                    ],
            },
            {
                name: 'Admin',
                path: '/Admin',
                component: Admin,

            }
        ]
    }
)
