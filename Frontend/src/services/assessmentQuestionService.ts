import api from './api'

export const assessmentQuestionService = {

  async getQuestions() {
    const response =
      await api.get(
        '/assessment-questions'
      )

    return response.data
  },

  async createQuestion(
    payload: any
  ) {
    const response =
      await api.post(
        '/assessment-questions',
        payload
      )

    return response.data
  },

  async updateQuestion(
    id: number,
    payload: any
  ) {
    const response =
      await api.put(
        `/assessment-questions/${id}`,
        payload
      )

    return response.data
  },

  async deleteQuestion(
    id: number
  ) {
    await api.delete(
      `/assessment-questions/${id}`
    )
  }
}