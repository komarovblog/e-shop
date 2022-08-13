import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MyHome from '../views/MyHome.vue'
import MyCatalog from '../views/MyCatalog.vue'
import MySingleProduct from '../views/MySingleProduct.vue'
import MyLK from '../views/MyLK.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Главная',
      component: HomeView
    },
    {
      path: '/products',
      name: 'Каталог',
      component: MyCatalog
    },
    {
      path: '/products/:productid',
      name: 'Товар',
      component: MySingleProduct
    },
    {
      path: '/user',
      name: 'Личный кабинет',
      component: MyLK
    },
    {
      path: '/about',
      name: 'О проекте',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
