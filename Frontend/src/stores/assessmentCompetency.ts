import { defineStore } from 'pinia'
import { ref } from 'vue'

import {

  getCompetencies,

  createCompetency,

  updateCompetency,

  deleteCompetency

} from '@/services/assessmentCompetencyService'

export const useAssessmentCompetencyStore =
defineStore(
  'assessmentCompetency',
  () => {

    const competencies =
      ref<any[]>([])

    async function loadCompetencies() {

      competencies.value =
        await getCompetencies()
    }

    async function addCompetency(
      competency: any
    ) {

      await createCompetency(
        competency
      )

      await loadCompetencies()
    }

    async function editCompetency(
      id: number,
      competency: any
    ) {

      await updateCompetency(
        id,
        competency
      )

      await loadCompetencies()
    }

    async function removeCompetency(
      id: number
    ) {

      await deleteCompetency(id)

      await loadCompetencies()
    }

    return {

      competencies,

      loadCompetencies,

      addCompetency,

      editCompetency,

      removeCompetency
    }
  }
)