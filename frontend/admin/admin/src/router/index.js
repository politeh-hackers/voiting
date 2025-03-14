import AppLayout from '@/layout/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { getToken, isAuthenticated } from '@/utils/auth';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: (to) => {
                const token = getToken();
                return isAuthenticated(token) ? { name: 'dashboard' } : '/auth';
            }
        },
        {
            path: '/auth',
            name: 'auth',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/admin/home',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },
                {
                    path: '/admin/media',
                    name: 'formlayout',
                    component: () => import('@/views/uikit/MediaPage.vue')
                },
                {
                    path: '/admin/actual',
                    name: 'input',
                    component: () => import('@/views/uikit/ActualPage.vue')
                },
                {
                    path: '/admin/biography',
                    name: 'button',
                    component: () => import('@/views/uikit/BiographyPage.vue')
                },
                {
                    path: '/admin/appeals',
                    name: 'list',
                    component: () => import('@/views/uikit/AppealsPage.vue')
                },
                {
                    path: '/admin/category',
                    name: 'landing',
                    component: () => import('@/views/uikit/CategoryPage.vue')
                },
            ]
        },

        {
            path: '/auth/register',
            name: 'register',
            component: () => import('@/views/pages/auth/Registration.vue')
        },
        {
            path: '/auth/access',
            name: 'accessDenied',
            component: () => import('@/views/pages/auth/Access.vue')
        },
        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/pages/auth/Error.vue')
        }
    ]
});
router.beforeEach((to, from, next) => {
    const token = getToken();
    
    if (to.path === '/auth' && isAuthenticated(token)) {
        next({ name: 'dashboard' }); // Если авторизован и пытается зайти на страницу авторизации - на дашборд
    } else if (!to.path.startsWith('/auth') && !isAuthenticated(token)) {
        next('/auth'); // Если не авторизован и пытается зайти на защищенный путь - на авторизацию
    } else {
        next();
    }
});
export default router;
