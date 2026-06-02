<script setup lang="ts">
import { onMounted }
from 'vue'

import MainLayout
from '@/layouts/MainLayout.vue'

import Card
from 'primevue/card'

import DataTable
from 'primevue/datatable'

import Column
from 'primevue/column'

import { useAnalyticsStore }
from '@/stores/analytics'

const analyticsStore =
  useAnalyticsStore()

onMounted(async () => {

  await analyticsStore
    .loadDashboard()
})
</script>

<template>

  <MainLayout>

    <div class="dashboard-grid">

      <Card>

        <template #title>
          Total Leads
        </template>

        <template #content>

          <h1>

            {{

              analyticsStore
              .dashboardData
              ?.total_leads || 0
            }}

          </h1>

        </template>

      </Card>

      <Card>

        <template #title>
          Converted
        </template>

        <template #content>

          <h1>

            {{

              analyticsStore
              .dashboardData
              ?.converted_leads || 0
            }}

          </h1>

        </template>

      </Card>

      <Card>

        <template #title>
          Interested
        </template>

        <template #content>

          <h1>

            {{

              analyticsStore
              .dashboardData
              ?.interested_leads || 0
            }}

          </h1>

        </template>

      </Card>

      <Card>

        <template #title>
          Follow-up
        </template>

        <template #content>

          <h1>

            {{

              analyticsStore
              .dashboardData
              ?.followup_leads || 0
            }}

          </h1>

        </template>

      </Card>

    </div>

    <Card
      class="leaderboard-card"
    >

      <template #title>

        Counselor Productivity

      </template>

      <template #content>

        <DataTable

          :value="

            Object.entries(

              analyticsStore
              .dashboardData
              ?.counselor_stats
              || {}

            ).map(

              ([name, stats]:
              any) => ({

                name,

                ...stats
              })
            )
          "
        >

          <Column
            field="name"
            header="Counselor"
          />

          <Column
            field="total"
            header="Total Leads"
          />

          <Column
            field="converted"
            header="Converted"
          />

        </DataTable>

      </template>

    </Card>

  </MainLayout>

</template>

<style scoped>
.dashboard-grid {

  display: grid;

  grid-template-columns:
    repeat(
      4,
      1fr
    );

  gap: 16px;

  margin-bottom: 24px;
}

.leaderboard-card {

  margin-top: 24px;
}

h1 {

  font-size: 32px;

  margin: 0;
}
</style>