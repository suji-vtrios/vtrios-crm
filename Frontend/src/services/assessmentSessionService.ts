import api from './api'

export async function getSessions() {

  const response =
    await api.get(
      '/assessment-sessions/'
    )

  return response.data
}

export async function createSession(
  session: any
) {

  const response =
    await api.post(
      '/assessment-sessions/',
      session
    )

  return response.data
}