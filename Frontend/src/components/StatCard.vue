<script setup lang="ts">
defineProps<{
  title: string
  value: string | number
  icon?: string
}>()
</script>

<template>
  <div class="stat-card">

    <div class="stat-header">

      <span>
        {{ title }}
      </span>

      <i
        v-if="icon"
        :class="icon"
      />

    </div>

    <div class="stat-value">
      {{ value }}
    </div>

  </div>
</template>

<style scoped>
.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow:
    0 2px 8px
    rgba(
      0,
      0,
      0,
      0.08
    );
}

.stat-header {
  display: flex;
  justify-content: space-between;
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
}
</style>