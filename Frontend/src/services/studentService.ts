import api from './api'

export async function getStudents() {

  const response =
    await api.get('/students/')

  return response.data
}

export async function createStudent(
  student: any
) {

  const response =
    await api.post(
      '/students/',
      student
    )

  return response.data
}