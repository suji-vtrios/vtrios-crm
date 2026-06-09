<script setup lang="ts">

import { onMounted } from 'vue'

import MainLayout
from '@/layouts/MainLayout.vue'

import Card
from 'primevue/card'

import DataTable
from 'primevue/datatable'

import Column
from 'primevue/column'

import Button
from 'primevue/button'

import { useRouter }
from 'vue-router'

import {
  useAssessmentSessionStore
}
from '@/stores/assessmentSession'

const router =
  useRouter()

const sessionStore =
  useAssessmentSessionStore()

onMounted(async () => {

  await sessionStore
    .loadSessions()

})

function viewResult(
  session: any
) {

  router.push(
    `/assessment-result/${session.id}`
  )
}

function viewDetails(
  session: any
) {

  router.push(
    `/assessment-session-details/${session.id}`
  )
}

</script>

<template>

<MainLayout>

<Card>

  <template #title>

    Assessment Sessions

  </template>

  <template #content>

    <DataTable
      :value="sessionStore.sessions"
      paginator
      :rows="10"
    >

      <Column
        field="id"
        header="Session ID"
      />

      <Column
        field="lead_id"
        header="Lead"
      />

      <Column
        field="status"
        header="Status"
      />

      <Column
        field="overall_score"
        header="Score"
      />

      <Column
        field="recommendation"
        header="Recommendation"
      />

      <Column
        header="Actions"
      >

        <template #body="slotProps">

          <Button
            label="View Result"
            icon="pi pi-eye"
            @click="
              viewResult(
                slotProps.data
              )
            "
          />

          <Button
            label="Details"
            icon="pi pi-search"
            @click="
              viewDetails(
                slotProps.data
              )
            "
          />

        </template>

      </Column>

    </DataTable>

  </template>

</Card>

</MainLayout>

</template>