import api from './api'

export async function getSubcategories() {

  const response =
    await api.get(
      '/assessment-subcategories/'
    )

  return response.data
}

export async function createSubcategory(
  subcategory: any
) {

  const response =
    await api.post(
      '/assessment-subcategories/',
      subcategory
    )

  return response.data
}

export async function updateSubcategory(
  id: number,
  subcategory: any
) {

  const response =
    await api.put(
      `/assessment-subcategories/${id}`,
      subcategory
    )

  return response.data
}

export async function deleteSubcategory(
  id: number
) {

  const response =
    await api.delete(
      `/assessment-subcategories/${id}`
    )

  return response.data
}