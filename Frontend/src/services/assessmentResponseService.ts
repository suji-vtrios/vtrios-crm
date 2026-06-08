import api from './api'

export const
assessmentResponseService = {

  async createResponse(
    payload: any
  ) {

    const response =
      await api.post(
        '/assessment-responses/',
        payload
      )

    return response.data
  }
}