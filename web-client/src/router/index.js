import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import AddEditAccountView from '@/views/AddEditAccountView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
      beforeEnter: (to, from) => {
        if (!sessionStorage.getItem('encryptionKey')) {
          return router.push({ name: 'login' });
        }
      }
    },
    {
      path: '/add',
      name: 'addAccount',
      component: AddEditAccountView,
    },
    {
      path: '/edit/:id',
      name: 'editAccount',
      component: AddEditAccountView,
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
  ]
})

export default router
