<script setup lang="ts">
import { ref } from 'vue'

import { useRouter }
from 'vue-router'

import Card from 'primevue/card'

import InputText
from 'primevue/inputtext'

import Password
from 'primevue/password'

import Button
from 'primevue/button'

import {
  useAuthStore
} from '@/stores/auth'

const router =
  useRouter()

const authStore =
  useAuthStore()

const email =
  ref('')

const password =
  ref('')

async function login() {

  try {

    await authStore
      .loginUser({

        email:
          email.value,

        password:
          password.value
      })

    router.push('/')

  } catch {

    alert(
      'Invalid credentials'
    )
  }
}
</script>

<template>

  <div class="login-page">

    <Card class="login-card">

      <template #title>
        Vtrios CRM Login
      </template>

      <template #content>

        <div class="form-grid">

          <InputText
            v-model="email"
            placeholder="Email"
          />

          <Password
            v-model="password"
            placeholder="Password"
            toggleMask
          />

          <Button
            label="Login"
            icon="pi pi-sign-in"
            @click="login"
          />

        </div>

      </template>

    </Card>

  </div>

</template>

<style scoped>
.login-page {

  min-height: 100vh;

  display: flex;

  align-items: center;

  justify-content: center;

  background: #f1f5f9;
}

.login-card {

  width: 400px;
}

.form-grid {

  display: flex;

  flex-direction: column;

  gap: 16px;
}
</style>