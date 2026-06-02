import api from './api'

export async function getUsers() {

  const response =
    await api.get('/users')

  return response.data
}

export async function createUser(
  user: any
) {

  const response =
    await api.post(
      '/users',
      user
    )

  return response.data
}

export async function updateUser(
  id: number,
  user: any
) {

  const response =
    await api.put(
      `/users/${id}`,
      user
    )

  return response.data
}

export async function deleteUser(
  id: number
) {

  const response =
    await api.delete(
      `/users/${id}`
    )

  return response.data
}