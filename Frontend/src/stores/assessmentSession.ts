import { defineStore }
from 'pinia'

import { ref }
from 'vue'

import {

  getSessions,

  createSession

} from '@/services/assessmentSessionService'

export const
useAssessmentSessionStore =
defineStore(
  'assessmentSession',
  () => {

    const sessions =
      ref<any[]>([])

    async function
    loadSessions() {

      sessions.value =
        await getSessions()
    }

    async function
    addSession(
      payload: any
    ) {

      await createSession(
        payload
      )

      await loadSessions()
    }

    return {

      sessions,

      loadSessions,

      addSession
    }
  }
)