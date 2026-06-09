import api from './api'

export const
assessmentEnrollmentService = {

  async enroll(
    sessionId: number
  ) {

    const response =
      await api.post(
        `/assessment-sessions/${sessionId}/enroll`
      )

    return response.data
  }
}