import api from './api'

export const assessmentReportService = {

  async getReport(
    sessionId: number
  ) {

    const response =
      await api.get(
        `/assessment-reports/${sessionId}`
      )

    return response.data
  }
}