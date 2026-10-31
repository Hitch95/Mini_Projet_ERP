<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ROUTE_NAMES } from '@/router/route-names'
import { login } from '@/core/services/auth'
import Button from '@/components/ui/button/Button.vue'
import Input from '@/components/ui/input/Input.vue'

const route = useRoute()
const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')

async function onSubmit() {
  error.value = ''
  try {
    if (await login(email.value, password.value)) {
      const redirect = route.query.redirect
      router.push(typeof redirect === 'string' ? redirect : { name: ROUTE_NAMES.HOME })
    } else {
      error.value = 'Email ou mot de passe incorrect.'
    }
  } catch {
    error.value = 'Serveur injoignable.'
  }
}
</script>

<template>
  <h1 class="mb-6 text-3xl font-bold">Connexion</h1>
  <form class="flex max-w-sm flex-col gap-4" @submit.prevent="onSubmit">
    <label class="flex flex-col gap-1 text-sm font-medium">
      Email
      <Input v-model="email" type="email" required class="rounded border border-current/30 px-3 py-2 font-normal" />
    </label>
    <label class="flex flex-col gap-1 text-sm font-medium">
      Mot de passe
      <Input v-model="password" type="password" required class="rounded border border-current/30 px-3 py-2 font-normal" />
    </label>
    <Button type="submit" class="cursor-pointer rounded bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700">
      Se connecter
    </Button>
    <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
  </form>
</template>
