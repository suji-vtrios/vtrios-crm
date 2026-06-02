import api from './api'

export async function login(
  credentials: any
) {

  const response =
    await api.post(

      '/auth/login',

      credentials
    )

  return response.data
}