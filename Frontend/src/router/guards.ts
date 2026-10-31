import type { Router } from 'vue-router'
import { ROUTE_NAMES } from '@/router/route-names'
import { isAuthenticated } from '@/core/services/auth'

export function registerGuards(router: Router) {
  router.beforeEach((to) => {
    if (to.meta.requiresAuth && !isAuthenticated.value) {
      return { name: ROUTE_NAMES.LOGIN, query: { redirect: to.fullPath } }
    }

    if (to.meta.guestOnly && isAuthenticated.value) {
      return { name: ROUTE_NAMES.HOME }
    }
  })
}
