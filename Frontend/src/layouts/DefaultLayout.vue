<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ROUTE_NAMES } from '../router/route-names'
import { isAuthenticated, logout } from '../services/auth'

const router = useRouter()

const onLogout = () => {
  logout()
  router.push({ name: ROUTE_NAMES.LOGIN })
}
</script>

<template>
  <header class="border-b border-current/15">
    <nav class="mx-auto flex max-w-4xl items-center gap-6 px-4 py-3">
      <RouterLink :to="{ name: ROUTE_NAMES.HOME }" class="hover:underline [&.router-link-exact-active]:font-semibold">Accueil</RouterLink>
      <RouterLink :to="{ name: ROUTE_NAMES.PIECES }" class="hover:underline [&.router-link-exact-active]:font-semibold">Pièces</RouterLink>
      <button v-if="isAuthenticated" class="ml-auto cursor-pointer hover:underline" @click="onLogout">Déconnexion</button>
      <RouterLink v-else :to="{ name: ROUTE_NAMES.LOGIN }" class="ml-auto hover:underline">Connexion</RouterLink>
    </nav>
  </header>
  <main class="mx-auto max-w-4xl px-4 py-8">
    <RouterView />
  </main>
</template>
