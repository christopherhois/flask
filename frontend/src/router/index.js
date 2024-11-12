import { createRouter, createWebHistory } from 'vue-router';
import AdminUsers from '@/pages/AdminUsers.vue';
import AdminPTValues from '@/pages/AdminPTValues.vue';
import AddUser from '@/pages/AddUser.vue';
import NotFound from '@/pages/NotFound.vue';



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
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../pages/NotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes


});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');
  const userRole = localStorage.getItem('role');

  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      return next({ path: '/auth', query: { redirect: to.fullPath } });
    }
    if (to.meta.role && to.meta.role !== userRole) {
      return next({ path: '/unauthorized' });
    }
  }
  next();
});

export default router;
