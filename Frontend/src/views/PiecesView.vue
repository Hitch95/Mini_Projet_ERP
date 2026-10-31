<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { API_URL } from '@/core/services/api'
import { type ReadPiece } from '@/core/types/piece.type'

const pieces = ref<ReadPiece[]>([])
const error = ref('')

onMounted(async () => {
  try {
    const response = await fetch(`${API_URL}/pieces`)
    if (!response.ok) throw new Error(String(response.status))
    pieces.value = await response.json()
  } catch {
    error.value = 'Impossible de charger les pièces.'
  }
})
</script>

<template>
  <h1 class="mb-6 text-3xl font-bold">Pièces</h1>
  <p v-if="error" class="text-red-600">{{ error }}</p>
  <table v-else class="w-full border-collapse text-left">
    <thead class="border-b border-current/20 text-sm opacity-70">
      <tr>
        <th class="px-3 py-2 font-medium">Référence</th>
        <th class="px-3 py-2 font-medium">Nom</th>
        <th class="px-3 py-2 font-medium">Prix</th>
        <th class="px-3 py-2 font-medium">Stock</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="piece in pieces" :key="piece.id" class="border-b border-current/10">
        <td class="px-3 py-2">{{ piece.reference }}</td>
        <td class="px-3 py-2">{{ piece.name }}</td>
        <td class="px-3 py-2">{{ piece.price }} €</td>
        <td class="px-3 py-2">{{ piece.stock }}</td>
      </tr>
    </tbody>
  </table>
</template>
