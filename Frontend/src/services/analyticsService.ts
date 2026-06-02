import api from './api'

export async function getDashboardData() {

  const response =
    await api.get(
      '/analytics/dashboard'
    )

  return response.data
}