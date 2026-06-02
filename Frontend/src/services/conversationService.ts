import api from './api'

export async function getConversations() {

  const response =
    await api.get(
      '/conversations/'
    )

  return response.data
}

export async function createConversation(
  conversation: any
) {

  const response =
    await api.post(
      '/conversations/',
      conversation
    )

  return response.data
}

export async function markConversationRead(
  id: number
) {

  const response =
    await api.put(
      `/conversations/${id}/read`
    )

  return response.data
}