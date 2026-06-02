import { createApp }
from 'vue'

import App
from './App.vue'

import router
from './router'

import PrimeVue
from 'primevue/config'

import Aura
from '@primeuix/themes/aura'

import 'primeicons/primeicons.css'

import { createPinia }
from 'pinia'

import {
  useAuthStore
} from '@/stores/auth'

const app =
  createApp(App)

const pinia =
  createPinia()

app.use(pinia)

const authStore =
  useAuthStore()

authStore.loadUser()

app.use(router)

app.use(PrimeVue, {

  theme: {
    preset: Aura
  }
})

app.mount('#app')