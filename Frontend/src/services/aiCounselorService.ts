import api from './api'

export async function sendMessage(
  message: string
) {

  return fetch(
    'https://crm.vtrios.com/ai-counselor/chat',
    {
      method: 'POST',
      headers: {
        'Content-Type':
        'application/json'
      },
      body: JSON.stringify({
        message
      })
    }
  ).then(
    r => r.json()
  )
}