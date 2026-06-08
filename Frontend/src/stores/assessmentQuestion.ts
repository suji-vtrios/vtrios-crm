import { defineStore }
from 'pinia'

import {
  assessmentQuestionService
}
from '@/services/assessmentQuestionService'

export const
useAssessmentQuestionStore =
defineStore(
  'assessmentQuestion',
  {

    state: () => ({

      questions: [] as any[]

    }),

    actions: {

      async loadQuestions() {

        this.questions =
          await assessmentQuestionService
            .getQuestions()
      },

      async addQuestion(
        payload: any
      ) {

        await assessmentQuestionService
          .createQuestion(
            payload
          )

        await this.loadQuestions()
      },

      async editQuestion(
        id: number,
        payload: any
      ) {

        await assessmentQuestionService
          .updateQuestion(
            id,
            payload
          )

        await this.loadQuestions()
      },

      async removeQuestion(
        id: number
      ) {

        await assessmentQuestionService
          .deleteQuestion(id)

        await this.loadQuestions()
      }
    }
  }
)