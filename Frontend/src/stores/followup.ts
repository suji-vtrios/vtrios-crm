import { defineStore } from 'pinia'
import { ref } from 'vue'

import {
  getFollowups,
  createFollowup
} from '@/services/followupService'

export const useFollowupStore =
defineStore(
  'followup',
  () => {

    const followups =
      ref<any[]>([])

    async function loadFollowups(
      leadId: number
    ) {

      followups.value =
        await getFollowups(
          leadId
        )
    }

    async function addFollowup(
      followup: any
    ) {

      await createFollowup(
        followup
      )

      await loadFollowups(
        followup.lead_id
      )
    }

    return {
      followups,
      loadFollowups,
      addFollowup
    }
  }
)