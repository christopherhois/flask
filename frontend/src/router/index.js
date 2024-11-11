import { createRouter, createWebHistory } from 'vue-router';
import AdminUsers from '../views/AdminUsers.vue';
import AdminPTValues from '../views/AdminPTValues.vue';
import AddUser from '../views/AddUser.vue';

const routes = [
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: AdminUsers,
    meta: { requiresAuth: true, role: 'Admin' }
  },
  {
    path: '/admin/pt-values',
    name: 'AdminPTValues',
    component: AdminPTValues,
    meta: { requiresAuth: true, role: 'Admin' }
  },
  {
    path: '/admin/add-user',
    name: 'AddUser',
    component: AddUser,
    meta: { requiresAuth: true, role: 'Admin' }
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
