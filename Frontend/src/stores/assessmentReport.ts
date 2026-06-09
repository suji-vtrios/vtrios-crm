import { defineStore }
from 'pinia'

import { ref }
from 'vue'

import {
  assessmentReportService
}
from '@/services/assessmentReportService'

export const
useAssessmentReportStore =
defineStore(
  'assessmentReport',
  () => {

    const report =
      ref<any>(null)

    async function
    loadReport(
      sessionId: number
    ) {

      report.value =
        await assessmentReportService
          .getReport(
            sessionId
          )
    }

    return {

      report,

      loadReport
    }
  }
)