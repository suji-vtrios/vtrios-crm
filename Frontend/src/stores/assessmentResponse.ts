import { defineStore }
from 'pinia'

import {
  assessmentResponseService
}
from '@/services/assessmentResponseService'

export const
useAssessmentResponseStore =
defineStore(
  'assessmentResponse',
  {

    actions: {

      async addResponse(
        payload: any
      ) {

        return await
          assessmentResponseService
            .createResponse(
              payload
            )
      }
    }
  }
)