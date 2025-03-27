import AppLayout from '@/layout/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { getToken, isAuthenticated } from '@/utils/auth.ts';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: (to) => {
                const token = getToken();
                return isAuthenticated(token) ? { name: 'media' } : '/auth';
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
                    path: '/admin/media',
                    name: 'media',
                    component: () => import('@/views/uikit/MediaPage.vue')
                },
                {
                    path: '/admin/actual',
                    name: 'actual',
                    component: () => import('@/views/uikit/ActualPage.vue')
                },
                {
                    path: '/admin/biography',
                    name: 'biography',
                    component: () => import('@/views/uikit/BiographyPage.vue')
                },
                {
                    path: '/admin/appeals',
                    name: 'appeals',
                    component: () => import('@/views/uikit/AppealsPage.vue')
                },
                {
                    path: '/admin/category',
                    name: 'category',
                    component: () => import('@/views/uikit/CategoryPage.vue')
                },
            ]
        },

        {
            path: '/auth/register',
            name: 'register',
            component: () => import('@/views/pages/auth/Registration.vue')
        },
        
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
