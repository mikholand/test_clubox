import { createRouter, createWebHistory } from 'vue-router'
import BirthdateView from '../views/BirthdateView.vue'
import ProfileView from '../views/ProfileView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'BirthdateView',
      component: BirthdateView
    },
    {
      path: '/profile/:user_id',
      name: 'ProfileView',
      component: ProfileView,
      props: true
    }
  ]
})

export default router
