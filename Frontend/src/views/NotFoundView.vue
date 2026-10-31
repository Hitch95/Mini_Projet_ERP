<script setup lang="ts">
import { ROUTE_NAMES } from '../router/route-names'
</script>

<template>
  <h1 class="mb-2 text-3xl font-bold">Page introuvable</h1>
  <RouterLink class="text-blue-600 hover:underline" :to="{ name: ROUTE_NAMES.HOME }">Retour à l'accueil</RouterLink>
</template>
