import type { RouteRecordRaw } from 'vue-router'
import { ROUTE_NAMES } from '@/router/route-names.ts'

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('../layouts/DefaultLayout.vue'),
    children: [
      {
        path: '',
        name: ROUTE_NAMES.HOME,
        component: () => import('../views/HomeView.vue'),
      },
      {
        path: 'pieces',
        name: ROUTE_NAMES.PIECES,
        component: () => import('../views/PiecesView.vue'),
      },
    ],
  },
  {
    path: '/login',
    name: ROUTE_NAMES.LOGIN,
    component: () => import('../views/LoginView.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: ROUTE_NAMES.NOT_FOUND,
    component: () => import('../views/NotFoundView.vue'),
  },
]
