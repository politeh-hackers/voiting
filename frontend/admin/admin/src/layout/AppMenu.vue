<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { logout } from '@/utils/auth';
import AppMenuItem from './AppMenuItem.vue';

const router = useRouter();
const handleLogout = () => {
    logout(router);
};

const model = ref([
    {
        label: 'Home',
        items: [{ label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/' }]
    },
    {
        label: 'Новости',
        items: [
            { label: 'Медиа', icon: 'pi pi-fw pi-id-card', to: '/admin/media' },
            { label: 'Актуальные', icon: 'pi pi-fw pi-check-square', to: '/admin/actual' },
            { label: 'Биография', icon: 'pi pi-fw pi-mobile', to: '/admin/biography', class: 'rotated-icon' },

        ]
    },
    {
        label: 'Обращения',
        icon: 'pi pi-fw pi-briefcase',
        to: '/pages',
        items: [
            { label: 'Обращения(?)', icon: 'pi pi-fw pi-list', to: '/admin/appeals' },

        ]
    },
    {
        label: 'Настройки',
        items: [
        {
                label: 'Категории',
                icon: 'pi pi-fw pi-globe',
                to: '/admin/category'
            },
            {
                label: 'Теги',
                icon: 'pi pi-fw pi-hashtag',
                to: ''
            },
            {
                label: 'Профиль(?)',
                icon: 'pi pi-fw pi-user',
                items: [
                    {
                        label: 'Выйти',
                        icon: 'pi pi-fw pi-sign-out',
                        command: () => handleLogout()
                    },
                    {
                        label: 'Регистрация',
                        icon: 'pi pi-fw pi-user-plus',
                        to: '/auth/register'
                    },
                    {
                        label: 'Error',
                        icon: 'pi pi-fw pi-times-circle',
                        to: '/auth/error'
                    },
                    {
                        label: 'Access Denied',
                        icon: 'pi pi-fw pi-lock',
                        to: '/auth/access'
                    }
                ]
            },

        ]
    },
]);
</script>

<template>
    <ul class="layout-menu">
        <fragment v-for="(item, i) in model" :key="i">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </fragment>
    </ul>
</template>

<style lang="scss" scoped></style>
