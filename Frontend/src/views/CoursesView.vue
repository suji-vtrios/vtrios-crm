<script setup lang="ts">
import MainLayout from '@/layouts/MainLayout.vue'
import { ref } from 'vue'

import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const courses = ref([
  {
    id: 1,
    name: 'BIM Professional',
    duration: '3 Months',
    fee: 25000,
  },
])

const courseName = ref('')
const duration = ref('')
const fee = ref<number | null>(null)

function addCourse() {
  if (!courseName.value) return

  courses.value.push({
    id: Date.now(),
    name: courseName.value,
    duration: duration.value,
    fee: fee.value || 0,
  })

  courseName.value = ''
  duration.value = ''
  fee.value = null
}

function deleteCourse(id: number) {
  courses.value = courses.value.filter(
    (course) => course.id !== id
  )
}

function editCourse(course: any) {
  courseName.value = course.name
  duration.value = course.duration
  fee.value = course.fee

  deleteCourse(course.id)
}
</script>

<template>
  <MainLayout>
    <div class="page-header">
      <h1>Courses</h1>
      <p>Manage and organize all your courses.</p>
    </div>

    <Card class="mb-4">
      <template #title>
        Add New Course
      </template>

      <template #content>
        <div class="form-grid">

          <div>
            <label>Course Name</label>           

            <h3>Add New Course</h3>
            <InputText
              v-model="courseName"
              placeholder="Enter course name"
              fluid
            />
          </div>

          <div>
            <label>Duration</label>

            <InputText
              v-model="duration"
              placeholder="e.g. 3 Months"
              fluid
            />
          </div>

          <div>
            <label>Fee</label>

            <InputNumber
              v-model="fee"
              fluid
            />
          </div>

          <div class="button-container">
            <Button
              label="Add Course"
              icon="pi pi-plus"
              @click="addCourse"
            />
          </div>

        </div>
      </template>
    </Card>

    <Card>
      <template #title>
        Course List
      </template>

      <template #content>

        <DataTable
          :value="courses"
          paginator
          :rows="5"
          stripedRows
          class="course-datatable"
        >
          <Column
            field="name"
            header="Course Name"
            sortable
          />

          <Column
            field="duration"
            header="Duration"
            sortable
          />

          <Column
            field="fee"
            header="Fee"
            sortable
          />

          <Column header="Actions">

            <template #body="slotProps">

              <div class="action-buttons">

                <Button
                  icon="pi pi-pencil"
                  severity="info"
                  text
                  rounded
                  @click="editCourse(slotProps.data)"
                />

                <Button
                  icon="pi pi-trash"
                  severity="danger"
                  text
                  rounded
                  @click="deleteCourse(slotProps.data.id)"
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
.course-page {
  min-height: 100vh;
  padding: 24px;
  font-family: 'Inter', sans-serif;
  background: linear-gradient(180deg, #f9fafb 0%, #f1f5f9 100%);
  color: #1e293b;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  gap: 24px;
}
.page-header h1 {
  font-size: 34px;
  font-weight: 700;
  margin: 0;
}
.page-header p {
  margin-top: 6px;
  font-size: 15px;
  color: #64748b;
}

/* Stats */
.header-stats {
  display: flex;
  gap: 20px;
}
.stat-card {
  flex: 1;
  padding: 18px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.05);
  text-align: center;
}
.stat-card span {
  font-size: 13px;
  color: #64748b;
}
.stat-card strong {
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
  margin-top: 6px;
  display: block;
}

/* Form */
.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr) auto;
  gap: 20px;
  align-items: end;
}
label {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 6px;
  color: #475569;
}
.save-btn {
  height: 46px;
  font-weight: 600;
  background: #10b981;
  border: none;
  color: white;
  transition: all 0.2s ease;
}
.save-btn:hover {
  background: #059669;
  transform: translateY(-2px);
}

/* Table */
:deep(.p-datatable) {
  border-radius: 14px;
  overflow: hidden;
}
:deep(.p-datatable-thead > tr > th) {
  background: #f1f5f9;
  color: #334155;
  font-weight: 600;
  padding: 14px;
  text-align: center;
}
:deep(.p-datatable-tbody > tr > td) {
  padding: 14px;
  text-align: center;
}
:deep(.p-datatable-tbody > tr:hover) {
  background: #383b3f; /* very light tint */
  box-shadow: inset 0 0 0 9999px rgba(99, 102, 241, 0.05); /* subtle indigo overlay */
  transition: all 0.2s ease;
}
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
}


</style>