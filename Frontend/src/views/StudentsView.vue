<script setup lang="ts">
import { onMounted } from 'vue'

import MainLayout from '@/layouts/MainLayout.vue'

import { useStudentStore }
from '@/stores/student'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'

const studentStore =
  useStudentStore()

onMounted(async () => {

  await studentStore
    .loadStudents()
})

function getSeverity(
  status: string
) {

  switch (status) {

    case 'Active':
      return 'success'

    case 'Completed':
      return 'info'

    case 'Dropped':
      return 'danger'

    default:
      return 'warning'
  }
}
</script>

<template>
  <MainLayout>

    <div class="page-header">

      <h1>
        Students
      </h1>

      <p>
        Manage enrolled students
      </p>

    </div>

    <div class="table-card">

      <DataTable
        :value="
          studentStore.students
        "
        paginator
        :rows="10"
        stripedRows
      >

        <Column
          field="name"
          header="Name"
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
          field="
            enrollment_date
          "
          header="
            Enrollment Date
          "
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
                getSeverity(
                  slotProps.data
                    .status
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