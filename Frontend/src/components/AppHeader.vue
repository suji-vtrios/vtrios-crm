<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useNotificationStore } from '@/stores/notification'

const notificationStore =
  useNotificationStore()

onMounted(async () => {
  await notificationStore.loadNotifications()
})

const unreadCount =
  computed(() => {

    const notifications =
      notificationStore.notifications

    if (
      !Array.isArray(
        notifications
      )
    ) {
      return 0
    }

    return notifications.filter(
      n => !n.is_read
    ).length
  })
</script>

<template>
  <div class="header">

    <div class="logo">
      Vtrios CRM
    </div>

    <div class="header-right">

      <div class="notification">

        <i
          class="pi pi-bell"
        />

        <span
          v-if="
            unreadCount > 0
          "
          class="badge"
        >
          {{ unreadCount }}
        </span>

      </div>

      <div class="avatar">
        VS
      </div>

    </div>

  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 16px 24px;
  border-radius: 12px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.notification {
  position: relative;
  cursor: pointer;
}

.badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: red;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 11px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
}
</style>