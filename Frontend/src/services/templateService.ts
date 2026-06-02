import api from './api'

export async function getTemplates() {

  const response =
    await api.get(
      '/templates'
    )

  return response.data
}

export async function createTemplate(
  template: any
) {

  const response =
    await api.post(
      '/templates',
      template
    )

  return response.data
}

export async function updateTemplate(
  id: number,
  template: any
) {

  const response =
    await api.put(
      `/templates/${id}`,
      template
    )

  return response.data
}

export async function deleteTemplate(
  id: number
) {

  const response =
    await api.delete(
      `/templates/${id}`
    )

  return response.data
}