import { createRouter, createWebHistory } from 'vue-router'
import Main from './components/LoginAdmin.vue'
import Base from './components/AdminPanel.vue'
import Form from './components/Category.vue'
import Media from './components/Media.vue'
import Admin from './components/RegisterAdmin.vue'
import Appeals from './components/Appeals.vue'
import Actual from './components/Actual.vue'
import { isAuthenticated, getToken } from './utils/auth';

const router = createRouter({
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
      component: Base,
      children: [
        {
          name: 'Form',
          path: '/Form',
          component: Form,
        },
        {
          name: 'Media',
          path: '/Media',
          component: Media,
        },
        {
          name: 'Appeals',
          path: '/Appeals',
          component: Appeals,
        },
        {
          name: 'Actual',
          path: '/Actual',
          component: Actual,
        }
      ],
    },
    {
      name: 'Admin',
      path: '/Admin',
      component: Admin,
    }
  ]
});

// Глобальный навигационный охранник
router.beforeEach((to, from, next) => {
  const token = getToken(); // Получаем токен из localStorage
  
  // Если пытаемся перейти на защищённый маршрут и нет валидного токена
  if (to.name !== 'Home' && !isAuthenticated(token)) {
    next({ name: 'Home' }); // Перенаправляем на страницу логина
  } else if (to.name === 'Home' && isAuthenticated(token)) {
    // Если пользователь уже авторизован, перенаправляем его на /Base
    next({ name: 'Base' });
  } else {
    next(); // Обычный переход
  }
});

export default router;
