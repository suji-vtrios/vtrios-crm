<script setup lang="ts">
import { ref } from 'vue'

const menuItems = ref([
  {
    label: 'Dashboard',
    icon: 'pi pi-home',
    to: '/'
  },
  {
    label: 'Leads',
    icon: 'pi pi-users',
    to: '/leads'
  },
  {
    label: 'Courses',
    icon: 'pi pi-book',
    to: '/courses'
  },
  {
    label: 'Follow-ups',
    icon: 'pi pi-calendar',
    to: '/followups'
  },
  {
    label: 'Students',
    icon: 'pi pi-graduation-cap',
    to: '/students'
  },
  {
    label: 'Batches',
    icon: 'pi pi-list',
    to: '/batches'
  },
  {
    label: 'Users',
    icon: 'pi pi-user',
    to: '/users'
  },
  {
    label: 'Templates',
    icon: 'pi pi-file',
    to: '/templates'
  },
  {
    label: 'Conversations',
    icon: 'pi pi-comments',
    to: '/conversations'
  }
])
</script>

<template>
  <div class="sidebar-menu">
    <router-link
      v-for="item in menuItems"
      :key="item.to"
      :to="item.to"
      class="menu-item"
    >
      <i :class="item.icon"></i>
      <span>{{ item.label }}</span>
    </router-link>
  </div>
</template>

<style scoped>
.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  text-decoration: none;
}

.router-link-active {
  font-weight: bold;
}
</style>