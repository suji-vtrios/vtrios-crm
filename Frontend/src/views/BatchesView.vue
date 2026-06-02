<script setup lang="ts">
import {
  ref,
  onMounted
} from 'vue'

import MainLayout
from '@/layouts/MainLayout.vue'

import {
  useBatchStore
} from '@/stores/batch'

import {
  useCourseStore
} from '@/stores/course'

import Card from 'primevue/card'

import InputText
from 'primevue/inputtext'

import Select
from 'primevue/select'

import DatePicker
from 'primevue/datepicker'

import Button
from 'primevue/button'

import DataTable
from 'primevue/datatable'

import Column
from 'primevue/column'

import Tag
from 'primevue/tag'

const batchStore =
  useBatchStore()

const courseStore =
  useCourseStore()

onMounted(async () => {

  await batchStore
    .loadBatches()

  await courseStore
    .loadCourses()
})

const editingId =
  ref<number | null>(null)

const name = ref('')

const course = ref('')

const trainer = ref('')

const startDate =
  ref<Date | null>(null)

const endDate =
  ref<Date | null>(null)

const timing = ref('')

const mode = ref('Offline')

const status = ref('Active')

const trainerOptions = [

  'Suji',

  'Nived',

  'Nivitha',

  'Ahmed'
]

const timingOptions = [

  'Weekend 10AM - 1PM',

  'Weekend 2PM - 5PM',

  'Weekday 7PM - 9PM',

  'Morning Batch',

  'Evening Batch'
]

const modeOptions = [

  'Offline',

  'Online',

  'Hybrid'
]

const statusOptions = [

  'Active',

  'Completed',

  'Upcoming'
]

async function addBatch() {

  const payload = {

    name: name.value,

    course: course.value,

    trainer:
      trainer.value,

    start_date:
      startDate.value
        ?.toISOString()
        .split('T')[0],

    end_date:
      endDate.value
        ?.toISOString()
        .split('T')[0],

    timing:
      timing.value,

    mode:
      mode.value,

    status:
      status.value
  }

  if (editingId.value) {

    await batchStore
      .editBatch(
        editingId.value,
        payload
      )

  } else {

    await batchStore
      .addBatch(payload)
  }

  resetForm()
}

function editBatch(
  batch: any
) {

  editingId.value =
    batch.id

  name.value =
    batch.name

  course.value =
    batch.course

  trainer.value =
    batch.trainer

  timing.value =
    batch.timing

  mode.value =
    batch.mode

  status.value =
    batch.status

  startDate.value =
    new Date(
      batch.start_date
    )

  endDate.value =
    new Date(
      batch.end_date
    )
}

function resetForm() {

  editingId.value = null

  name.value = ''

  course.value = ''

  trainer.value = ''

  timing.value = ''

  mode.value = 'Offline'

  status.value = 'Active'

  startDate.value = null

  endDate.value = null
}

function getSeverity(
  status: string
) {

  switch (status) {

    case 'Active':
      return 'success'

    case 'Completed':
      return 'info'

    default:
      return 'warning'
  }
}
</script>

<template>
  <MainLayout>

    <div class="page-header">

      <h1>
        Batches
      </h1>

      <p>
        Manage training batches
      </p>

    </div>

    <Card class="mb-4">

      <template #title>
        Add New Batch
      </template>

      <template #content>

        <div class="form-grid">

          <InputText
            v-model="name"
            placeholder="Batch Name"
          />

          <Select
            v-model="course"
            :options="
              courseStore.courses
            "
            optionLabel="name"
            optionValue="name"
            placeholder="Select Course"
            fluid
          />

          <Select
            v-model="trainer"
            :options="
              trainerOptions
            "
            placeholder="Select Trainer"
            fluid
          />

          <DatePicker
            v-model="startDate"
            dateFormat="yy-mm-dd"
            placeholder="Start Date"
            fluid
          />

          <DatePicker
            v-model="endDate"
            dateFormat="yy-mm-dd"
            placeholder="End Date"
            fluid
          />

          <Select
            v-model="timing"
            :options="
              timingOptions
            "
            placeholder="Select Timing"
            fluid
          />

          <Select
            v-model="mode"
            :options="
              modeOptions
            "
            placeholder="Mode"
            fluid
          />

          <Select
            v-model="status"
            :options="
              statusOptions
            "
            placeholder="Status"
            fluid
          />

          <div class="button-group">

            <Button
              :label="
                editingId
                  ? 'Update Batch'
                  : 'Add Batch'
              "
              icon="pi pi-plus"
              @click="addBatch"
            />

            <Button
              label="Clear"
              severity="secondary"
              outlined
              @click="resetForm"
            />

          </div>

        </div>

      </template>

    </Card>

    <Card>

      <template #title>
        Batch List
      </template>

      <template #content>

        <DataTable
          :value="
            batchStore.batches
          "
          paginator
          :rows="10"
          stripedRows
        >

          <Column
            field="name"
            header="Batch"
          />

          <Column
            field="course"
            header="Course"
          />

          <Column
            field="trainer"
            header="Trainer"
          />

          <Column
            field="start_date"
            header="Start"
          />

          <Column
            field="end_date"
            header="End"
          />

          <Column
            field="timing"
            header="Timing"
          />

          <Column
            field="mode"
            header="Mode"
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

          <Column
            header="Actions"
          >

            <template #body="slotProps">

              <div
                class="
                  action-buttons
                "
              >

                <Button
                  icon="pi pi-pencil"
                  severity="info"
                  text
                  rounded
                  @click="
                    editBatch(
                      slotProps.data
                    )
                  "
                />

              </div>

            </template>

          </Column>

        </DataTable>

      </template>

    </Card>

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

.form-grid {
  display: grid;

  grid-template-columns:
    repeat(3, 1fr);

  gap: 16px;
}

.button-group {
  display: flex;
  gap: 12px;
}

.action-buttons {
  display: flex;
  justify-content: center;
}
</style>