import api from './api'

export async function getBatches() {

  const response =
    await api.get('/batches/')

  return response.data
}

export async function createBatch(
  batch: any
) {

  const response =
    await api.post(
      '/batches/',
      batch
    )

  return response.data
}

export async function updateBatch(
  id: number,
  batch: any
) {

  const response =
    await api.put(
      `/batches/${id}`,
      batch
    )

  return response.data
}