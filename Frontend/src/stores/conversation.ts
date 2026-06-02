import {
  defineStore
} from 'pinia'

import { ref }
from 'vue'

import {

  getConversations,

  createConversation,

  markConversationRead

} from '@/services/conversationService'

export const useConversationStore =
defineStore(
  'conversation',
  () => {

    const conversations =
      ref<any[]>([])

    async function loadConversations() {

      conversations.value =
        await getConversations()
    }

    async function addConversation(
      conversation: any
    ) {

      await createConversation(
        conversation
      )

      await loadConversations()
    }

    async function readConversation(
      id: number
    ) {

      await markConversationRead(id)

      await loadConversations()
    }

    return {

      conversations,

      loadConversations,

      addConversation,

      readConversation
    }
  }
)