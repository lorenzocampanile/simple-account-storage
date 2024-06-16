import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import VerifyView from '../views/VerifyView.vue'
import AddEditAccountView from '@/views/AddEditAccountView.vue'

let requireLoginBeforeEnter = (to, from) => {
  if (!sessionStorage.getItem('privateKey')) {
    return router.push({ name: 'login' });
  }
};

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/verify-user',
      name: 'verifyUser',
      component: VerifyView,
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
      beforeEnter: requireLoginBeforeEnter,
    },
    {
      path: '/add',
      name: 'addAccount',
      component: AddEditAccountView,
      beforeEnter: requireLoginBeforeEnter,
    },
    {
      path: '/edit/:id',
      name: 'editAccount',
      component: AddEditAccountView,
      beforeEnter: requireLoginBeforeEnter,
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
