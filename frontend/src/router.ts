import { createRouter, createWebHistory } from 'vue-router'
import Main from './components/Main.vue'
import Base from './components/Base.vue'
import Form from './components/HelloWorld.vue'

export default createRouter(
    {
        history: createWebHistory(),
        routes: [
            {
                name: 'Home',
                path: '/',
                component: Main,
            }, {
                name: 'Base',
                path: '/Base',
                component: Base, // Основной компонент
                children: [
                    {
                        name: 'Form',
                        path: '/Form', // Дочерний маршрут (без начального "/")
                        component: Form, // Компонент HelloWorld.vue
                    },
                ],
            }
        ]
    }
)
