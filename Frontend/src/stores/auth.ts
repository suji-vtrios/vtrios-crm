import {
  defineStore
} from 'pinia'

import { ref } from 'vue'

import {
  login
} from '@/services/authService'

export const useAuthStore =
defineStore(
  'auth',
  () => {

    const user =
      ref<any>(null)

    const isAuthenticated =
      ref(false)

    async function loginUser(
      credentials: any
    ) {

      const response =
        await login(
          credentials
        )

      user.value =
        response

      isAuthenticated.value =
        true

      localStorage.setItem(
        'user',
        JSON.stringify(
          response
        )
      )
    }

    function logout() {

      user.value = null

      isAuthenticated.value =
        false

      localStorage.removeItem(
        'user'
      )
    }

    function loadUser() {

      const storedUser =
        localStorage.getItem(
          'user'
        )

      if (storedUser) {

        user.value =
          JSON.parse(
            storedUser
          )

        isAuthenticated.value =
          true
      }
    }

    return {

      user,

      isAuthenticated,

      loginUser,

      logout,

      loadUser
    }
  }
)