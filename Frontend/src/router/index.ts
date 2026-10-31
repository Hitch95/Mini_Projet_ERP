import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './route'
import { registerGuards } from './guards'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior: (_to, _from, savedPosition) => savedPosition ?? { top: 0 },
})

registerGuards(router)

export default router
