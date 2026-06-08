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

    async function addSession(
        payload: any
    ) {

        const session =
            await createSession(
                payload
        )

        await loadSessions()

        return session
    }

    return {

      sessions,

      loadSessions,

      addSession
    }
  }
)