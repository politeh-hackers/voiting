import { createRouter, createWebHistory } from 'vue-router'
import Main from './components/Main.vue'
import Base from './components/Base.vue'
import Form from './components/Category.vue'
import Media from './components/Media.vue'
import Admin from './components/Admin.vue'

export default createRouter(
    {
        history: createWebHistory(),
        routes: [
            {
                name: 'Home',
                path: '/',
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
                    ],
            },
            {
                name: 'Admin',
                path: '/login',
                component: Admin,

            }
        ]
    }
)
