import { createRouter, createWebHistory } from 'vue-router'
import { routes } from '@/router/route'
import { registerGuards } from '@/router/guards'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior: (_to, _from, savedPosition) => savedPosition ?? { top: 0 },
})

registerGuards(router)

export default router
