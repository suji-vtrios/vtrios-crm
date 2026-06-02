import {
  defineStore
} from 'pinia'

import { ref }
from 'vue'

import {

  getUsers,

  createUser,

  updateUser,

  deleteUser

} from '@/services/userService'

export const useUserStore =
defineStore(
  'user',
  () => {

    const users =
      ref<any[]>([])

    async function loadUsers() {

      users.value =
        await getUsers()
    }

    async function addUser(
      user: any
    ) {

      await createUser(
        user
      )

      await loadUsers()
    }

    async function editUser(
      id: number,
      user: any
    ) {

      await updateUser(
        id,
        user
      )

      await loadUsers()
    }

    async function removeUser(
      id: number
    ) {

      await deleteUser(id)

      await loadUsers()
    }

    return {

      users,

      loadUsers,

      addUser,

      editUser,

      removeUser
    }
  }
)