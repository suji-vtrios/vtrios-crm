<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import MainLayout from '@/layouts/MainLayout.vue'

import { useLeadStore } from '@/stores/lead'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Button from 'primevue/button'

const router = useRouter()

const leadStore = useLeadStore()

const today =
  new Date()
    .toISOString()
    .split('T')[0]!

const followupsToday =
  computed(() =>
    leadStore.leads.filter(
      lead =>
        lead.nextFollowUpDate ===
        today
    )
  )

const overdueFollowups =
  computed(() =>
    leadStore.leads.filter(
      lead =>
        lead.nextFollowUpDate &&
        lead.nextFollowUpDate < today
    )
  )

function openLead(
  id: number
) {
  router.push(
    `/leads/${id}`
  )
}

function getStatusSeverity(
  status: string
) {
  switch (status) {
    case 'Interested':
      return 'success'

    case 'Counseling':
      return 'warning'

    case 'Enrolled':
      return 'success'

    case 'Lost':
      return 'danger'

    default:
      return 'info'
  }
}
</script>

<template>
  <MainLayout>

    <div class="page-header">
      <h1>
        Follow-ups
      </h1>

      <p>
        Manage upcoming
        student follow-ups
      </p>
    </div>

    <!-- KPI Cards -->

    <div class="stats-grid">

      <div class="stat-card">
        <h3>
          Due Today
        </h3>

        <div class="value">
          {{
            followupsToday.length
          }}
        </div>
      </div>

      <div class="stat-card">
        <h3>
          Overdue
        </h3>

        <div class="value danger">
          {{
            overdueFollowups.length
          }}
        </div>
      </div>

    </div>

    <!-- Table -->

    <div class="table-card">

      <DataTable
        :value="
          leadStore.leads
        "
        paginator
        :rows="10"
        stripedRows
      >

        <Column
          field="name"
          header="Lead"
        />

        <Column
          field="phone"
          header="Phone"
        />

        <Column
          field="course"
          header="Course"
        />

        <Column
          field="status"
          header="Status"
        >

          <template #body="slotProps">

            <Tag
              :value="
                slotProps.data
                  .status
              "
              :severity="
                getStatusSeverity(
                  slotProps.data
                    .status
                )
              "
            />

          </template>

        </Column>

        <Column
          field="
            nextFollowUpDate
          "
          header="
            Next Follow-up
          "
        />

        <Column
          header="Actions"
        >

          <template #body="slotProps">

            <Button
              label="Open"
              icon="pi pi-eye"
              size="small"
              @click="
                openLead(
                  slotProps.data.id
                )
              "
            />

          </template>

        </Column>

      </DataTable>

    </div>

  </MainLayout>
</template>

<style scoped>
.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 36px;
  margin-bottom: 8px;
}

.page-header p {
  color: #64748b;
}

.stats-grid {
  display: grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap: 20px;

  margin-bottom: 24px;
}

.stat-card {
  background: white;

  padding: 24px;

  border-radius: 16px;

  box-shadow:
    0 4px 16px
    rgba(
      0,
      0,
      0,
      0.06
    );
}

.value {
  font-size: 36px;
  font-weight: 700;
}

.danger {
  color: #dc2626;
}

.table-card {
  background: white;

  padding: 24px;

  border-radius: 16px;

  box-shadow:
    0 4px 16px
    rgba(
      0,
      0,
      0,
      0.06
    );
}
</style>