import api from './api'

export async function getCompetencies() {

  const response =
    await api.get(
      '/assessment-competencies/'
    )

  return response.data
}

export async function createCompetency(
  competency: any
) {

  const response =
    await api.post(
      '/assessment-competencies/',
      competency
    )

  return response.data
}

export async function updateCompetency(
  id: number,
  competency: any
) {

  const response =
    await api.put(
      `/assessment-competencies/${id}`,
      competency
    )

  return response.data
}

export async function deleteCompetency(
  id: number
) {

  const response =
    await api.delete(
      `/assessment-competencies/${id}`
    )

  return response.data
}