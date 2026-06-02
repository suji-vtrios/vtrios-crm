import api from './api'

export async function getLeads() {
  const response =
    await api.get('/leads/')

  return response.data
}

export async function getLead(
  id: number
) {
  const response =
    await api.get(
      `/leads/${id}`
    )

  return response.data
}

export async function createLead(
  lead: any
) {
  const response =
    await api.post(
      '/leads/',
      lead
    )

  return response.data
}

export async function updateLead(
  id: number,
  lead: any
) {
  const response =
    await api.put(
      `/leads/${id}`,
      lead
    )

  return response.data
}

export async function deleteLead(
  id: number
) {
  const response =
    await api.delete(
      `/leads/${id}`
    )

  return response.data
}