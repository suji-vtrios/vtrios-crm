import api from './api'

export async function getFollowups(
  leadId: number
) {
  const response =
    await api.get(
      `/followups/lead/${leadId}`
    )

  return response.data
}

export async function createFollowup(
  followup: any
) {
  const response =
    await api.post(
      '/followups/',
      followup
    )

  return response.data
}