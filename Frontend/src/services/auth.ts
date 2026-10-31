import { computed, ref } from 'vue'
import { API_URL } from '@/services/api'

const token = ref<string | null>(localStorage.getItem('token'))

export const isAuthenticated = computed(() => token.value !== null)

export async function login(email: string, password: string): Promise<boolean> {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    body: new URLSearchParams({ username: email, password }),
  })
  if (!response.ok) return false
  const data = await response.json()
  token.value = data.access_token
  localStorage.setItem('token', data.access_token)
  return true
}

export function logout() {
  token.value = null
  localStorage.removeItem('token')
}
