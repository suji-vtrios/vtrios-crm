<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import OverlayPanel from 'primevue/overlaypanel'

import Badge from 'primevue/badge'

import Button from 'primevue/button'

import {

  computed,

  ref,

  onMounted

} from 'vue'

import { useNotificationStore } from '@/stores/notification'

const authStore =
  useAuthStore()

const role =
computed(() => {

  return authStore
    .user?.role
})

const isAdmin =
computed(() => {

  return role.value
    === 'Admin'
})

const isCounselor =
computed(() => {

  return role.value
    === 'Counselor'
})

const isTrainer =
computed(() => {

  return role.value
    === 'Trainer'
})

const isMarketing =
computed(() => {

  return role.value
    === 'Marketing'
})

const router =
  useRouter()

const notificationStore = useNotificationStore()

const notificationPanel = ref()

onMounted(async () => {

  await notificationStore
    .loadNotifications()
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

function logout() {

  authStore.logout()

  router.push('/login')
}
</script>

<template>
  <div class="layout">

    <!-- Sidebar -->

    <aside class="sidebar">

      <div class="logo-section">
        <h2>Vtrios Hub</h2>
        <p>Admissions CRM</p>
      </div>

      <nav class="menu">

        <RouterLink
          v-if="
            isAdmin
            ||
            isCounselor
            ||
            isMarketing
          "
          to="/"
          class="menu-item"
        >

          <i class="pi pi-home"></i>

          <span>
            Dashboard
          </span>

        </RouterLink>


        <RouterLink
          v-if="isAdmin"
          to="/courses"
          class="menu-item"
        >

          <i class="pi pi-briefcase"></i>

          <span>
            Courses
          </span>

        </RouterLink>

        <RouterLink
          v-if="
            isAdmin
            ||
            isCounselor
          "
          to="/followups"
          class="menu-item"
        >

          <i class="pi pi-calendar"></i>

          <span>
            Follow-ups
          </span>

        </RouterLink>

        <RouterLink
          v-if="
            isAdmin
            ||
            isTrainer
          "
          to="/students"
          class="menu-item"
        >

          <i class="pi pi-graduation-cap"></i>

          <span>
            Students
          </span>

        </RouterLink>

        <RouterLink
          v-if="
            isAdmin
            ||
            isTrainer
          "
          to="/batches"
          class="menu-item"
        >

          <i class="pi pi-book"></i>

          <span>
            Batches
          </span>

        </RouterLink>


        <RouterLink
          v-if="isAdmin"
          to="/counselors"
          class="menu-item"
        >

          <i class="pi pi-id-card"></i>

          <span>
            Counselors
          </span>

        </RouterLink>

        <RouterLink

          v-if="!authStore.user"

          to="/login"

          class="menu-item"
        >
          <i class="pi pi-sign-in"></i>

          <span>
            Login
          </span>
        </RouterLink>

        <RouterLink
          v-if="isAdmin"
          to="/users"
          class="menu-item"
        >

          <i class="pi pi-user-edit"></i>

          <span>
            Users
          </span>

        </RouterLink>

        <RouterLink
          v-if="isAdmin"
          to="/templates"
          class="menu-item"
        >

          <i class="pi pi-comments"></i>

          <span>
            Templates
          </span>

        </RouterLink>

        <RouterLink
          to="/conversations"
          class="menu-item"
        >

          <i class="pi pi-comments"></i>

          <span>
            Conversations
          </span>

        </RouterLink>

    <div

      v-if="authStore.user"

      class="menu-item"

      @click="logout"
    >

      <i class="pi pi-sign-out"></i>

      <span>
        Logout
      </span>

    </div>

      </nav>

    </aside>

    <!-- Main Content -->

    <main class="content">

      <header class="topbar">

        <div>
          <h3>Vtrios CRM</h3>
        </div>

        <div class="topbar-right">

          <div class="notification-wrapper">

            <Button

              icon="pi pi-bell"

              text

              rounded

              @click="
                notificationPanel
                .toggle($event)
              "
            />

            <Badge

              v-if="
                unreadCount > 0
              "

              :value="
                unreadCount
              "

              severity="danger"
            />

          </div>

          <OverlayPanel
            ref="notificationPanel"
          >

            <div
              class="notification-list"
            >

              <div

                v-for="
                  notification
                  in
                  notificationStore
                  .notifications
                "

                :key="
                  notification.id
                "

                class="notification-item"
              >

                <div>

                  <strong>

                    {{

                      notification.type
                    }}

                  </strong>

                  <p>

                    {{

                      notification.message
                    }}

                  </p>

                </div>

                <Button

                  v-if="
                    !notification
                    .is_read
                  "

                  label="Read"

                  size="small"

                  @click="

                    notificationStore
                    .readNotification(
                      notification.id
                    )
                  "
                />

              </div>

            </div>

          </OverlayPanel>

          <div class="avatar">
            VS
          </div>

        </div>

      </header>

      <div class="page-content">
        <slot />
      </div>

    </main>

  </div>
</template>

<style scoped>

:deep(.p-badge) {

  position: absolute;

  top: -6px;

  right: -6px;
}

.notification-wrapper {
  display: flex;

  align-items: center;

  position: relative;
}

.notification-list {

  width: 320px;

  display: flex;

  flex-direction: column;

  gap: 12px;
}

.notification-item {

  padding: 12px;

  border-bottom:
    1px solid #eee;

  display: flex;

  justify-content:
    space-between;

  align-items: center;
}

.layout {
  display: flex;
  min-height: 100vh;

  background: #f8fafc;
}

/* Sidebar */

.sidebar {
  width: 260px;

  background:
    linear-gradient(
      180deg,
      #0f172a,
      #020617
    );

  color: white;

  padding: 24px;

  display: flex;
  flex-direction: column;
}

.logo-section {
  margin-bottom: 40px;
}

.logo-section h2 {
  font-size: 28px;
  margin-bottom: 4px;
}

.logo-section p {
  color: #94a3b8;
  font-size: 14px;
}

/* Menu */

.menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.menu-item {
  display: flex;

  align-items: center;

  gap: 12px;

  padding: 14px 18px;

  border-radius: 12px;

  text-decoration: none;

  color: #cbd5e1;

  transition: all .2s ease;
}

.menu-item:hover {
  background:
    rgba(
      255,
      255,
      255,
      .08
    );
}

.router-link-active {
  background: #2563eb;
  color: white;
}

.menu-item i {
  font-size: 1rem;
}

/* Content */

.content {
  flex: 1;

  padding: 24px;

  overflow-y: auto;
}

/* Topbar */

.topbar {
  height: 70px;

  background: white;

  border-radius: 16px;

  padding: 0 24px;

  display: flex;

  justify-content: space-between;

  align-items: center;

  box-shadow:
    0 4px 16px rgba(
      0,
      0,
      0,
      .06
    );

  margin-bottom: 24px;
}

.topbar h3 {
  color: #0f172a;
}

.topbar-right {
  display: flex;

  align-items: center;

  gap: 20px;
}

.notification {
  font-size: 1.2rem;

  cursor: pointer;
}

.avatar {
  width: 42px;
  height: 42px;

  border-radius: 50%;

  background: #2563eb;

  color: white;

  display: flex;

  align-items: center;

  justify-content: center;

  font-weight: 700;
}

.page-content {
  padding-bottom: 40px;
}
</style>