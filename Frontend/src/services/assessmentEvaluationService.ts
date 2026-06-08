import api from './api'

export const
assessmentEvaluationService = {

  async evaluate(
    sessionId: number
  ) {

    const response =
      await api.post(
        `/assessment-evaluation/${sessionId}`
      )

    return response.data
  },

  async getResult(
    sessionId: number
  ) {

    const response =
      await api.get(
        `/assessment-evaluation/${sessionId}`
      )

    return response.data
  }
}