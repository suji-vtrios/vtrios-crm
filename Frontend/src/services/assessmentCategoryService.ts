import api from './api'

export async function getCategories() {

  const response =
    await api.get(
      '/assessment-categories/'
    )

  return response.data
}

export async function createCategory(
  category: any
) {

  const response =
    await api.post(
      '/assessment-categories/',
      category
    )

  return response.data
}

export async function updateCategory(
  id: number,
  category: any
) {

  const response =
    await api.put(
      `/assessment-categories/${id}`,
      category
    )

  return response.data
}

export async function deleteCategory(
  id: number
) {

  const response =
    await api.delete(
      `/assessment-categories/${id}`
    )

  return response.data
}