import {
  defineStore
} from 'pinia'

import { ref }
from 'vue'

import {

  getNotifications,

  markAsRead

} from '@/services/notificationService'

export const useNotificationStore =
defineStore(
  'notification',
  () => {

    const notifications =
      ref<any[]>([])

    async function loadNotifications() {

      notifications.value =
        await getNotifications()
    }

    async function readNotification(
      id: number
    ) {

      await markAsRead(id)

      await loadNotifications()
    }

    return {

      notifications,

      loadNotifications,

      readNotification
    }
  }
)