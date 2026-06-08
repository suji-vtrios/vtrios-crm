<script setup lang="ts">
import { ref } from 'vue'

import MainLayout
from '@/layouts/MainLayout.vue'

import Card
from 'primevue/card'

import Button
from 'primevue/button'

import Dialog
from 'primevue/dialog'

import InputText
from 'primevue/inputtext'

import Dropdown
from 'primevue/dropdown'

import DataTable
from 'primevue/datatable'

import Column
from 'primevue/column'

import Tag
from 'primevue/tag'

import { useLeadStore }
from '@/stores/lead'

import { useCourseStore }
from '@/stores/course'

import { useUserStore } from '@/stores/user'
import { computed, onMounted } from 'vue'

import {
  useAssessmentSessionStore
} from '@/stores/assessmentSession'

import {
  useRouter
} from 'vue-router'

const router =
  useRouter()


const leadStore =
  useLeadStore()

const courseStore =
  useCourseStore()

const userStore = useUserStore()


const counselors = computed(() =>
  userStore.users.filter(
    user => user.role === 'Counselor'
  )
)

const assessmentStore =
  useAssessmentSessionStore()

const dialogVisible =
  ref(false)

const editingLeadId =
  ref<number | null>(null)

const globalFilter =
  ref('')

const leadForm =
  ref({

    name: '',

    phone: '',

    email: '',

    course: '',

    source: '',

    status: 'New',

    next_followup: '',

    assigned_counselor: ''
  })

const sourceOptions = [

  'Instagram',

  'Facebook',

  'WhatsApp',

  'Website',

  'Reference',

  'Walk-in'
]

const statusOptions = [

  'New',

  'Interested',

  'Follow-up',

  'Converted',

  'Closed'
]

async function saveLead() {

  if (
    editingLeadId.value
  ) {

    await leadStore
      .editLead(

        editingLeadId.value,

        leadForm.value
      )

  } else {

    await leadStore
      .addLead(
        leadForm.value
      )
  }

  closeDialog()
}

async function startAssessment(
  lead: any
) {

  const session =
    await assessmentStore
      .addSession({

        lead_id:
          lead.id,

        specialization:
          'Architecture',

        status:
          'Pending'
      })

  router.push(
    `/assessment-session/${session.id}`
  )
}

function openAddDialog() {

  editingLeadId.value =
    null

  leadForm.value = {

    name: '',

    phone: '',

    email: '',

    course: '',

    source: '',

    status: 'New',

    next_followup: '',

    assigned_counselor: ''
  }

  dialogVisible.value =
    true
}

function editLead(
  lead: any
) {

  editingLeadId.value =
    lead.id

  leadForm.value = {

    ...lead
  }

  dialogVisible.value =
    true
}

async function deleteLead(id: number) {
  if (!confirm('Are you sure you want to delete this lead?')) {
    return
  }

  await leadStore.deleteLead(id)
}

function closeDialog() {

  dialogVisible.value =
    false
}

onMounted(async () => {

  await userStore.loadUsers()

  await leadStore.loadLeads()

  await courseStore.loadCourses()

})
</script>

<template>

  <MainLayout>

    <Card>

      <template #title>

        <div
          class="page-header"
        >

          <span>
            Leads Management
          </span>

          <Button
            label="Add Lead"
            icon="pi pi-plus"
            @click="
              openAddDialog
            "
          />

        </div>

      </template>

      <template #content>

        <div
          class="table-toolbar"
        >

          <InputText
            v-model="
              globalFilter
            "
            placeholder="Search Leads"
          />

        </div>

        <DataTable

          :value="
            leadStore.leads
          "

          paginator

          :rows="10"

          stripedRows

          responsiveLayout="scroll"

          :globalFilterFields="[

            'name',

            'phone',

            'email',

            'course',

            'status'
          ]"

          :filters="{
            global: {
              value:
              globalFilter,
              matchMode:
              'contains'
            }
          }"
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
            field="email"
            header="Email"
          />

          <Column
            field="course"
            header="Course"
          />

          <Column
            field="source"
            header="Source"
          />

          <Column
            field="assigned_counselor"
            header="Counselor"
          />

          <Column
            field="next_followup"
            header="Next Follow-up"
          />

          <Column
            header="Follow-up"
          >

            <template
              #body="slotProps"
            >

              <Tag

                :value="
                  slotProps.data
                  .followup_status
                "

                :severity="

                  slotProps.data
                  .followup_status
                  === 'Overdue'

                  ? 'danger'

                  :

                  slotProps.data
                  .followup_status
                  === 'Today'

                  ? 'warning'

                  :

                  'success'
                "
              />

            </template>

          </Column>

          <Column
            field="status"
            header="Status"
          />
          <Column
            field="lead_score"
            header="Score"
          >
          </Column>

          <Column
              header="Temperature"
            >

              <template #body="slotProps">

                <Tag

                  :value="
                    slotProps.data
                    .lead_temperature
                  "

                  :severity="

                    slotProps.data
                    .lead_temperature
                    === 'Hot'

                    ? 'danger'

                    :

                    slotProps.data
                    .lead_temperature
                    === 'Warm'

                    ? 'warning'

                    :

                    'info'
                  "
                />

              </template>

            </Column>

          <Column
            header="Actions"
          >

            <template
              #body="slotProps"
            >

              <div
                class="action-buttons"
              >

                <Button
                  icon="pi pi-file-edit"
                  severity="info"
                  rounded
                  @click="
                    startAssessment(
                      slotProps.data
                    )
                  "
                />
                
                <Button

                  icon="pi pi-pencil"

                  severity="warning"

                  rounded

                  @click="
                    editLead(
                      slotProps.data
                    )
                  "
                />

                <Button

                  icon="pi pi-trash"

                  severity="danger"

                  rounded

                  @click="
                    deleteLead(
                      slotProps.data.id
                    )
                  "
                />

              </div>

            </template>

          </Column>

        </DataTable>

      </template>

    </Card>

    <Dialog
        v-model:visible="dialogVisible"
        modal
        :style="{ width: '500px' }"

      :header="

        editingLeadId

        ? 'Edit Lead'
        : 'Add Lead'
      "
    >

      <div class="form-grid">

        <InputText
          v-model="
            leadForm.name
          "
          placeholder="Name"
        />

        <InputText
          v-model="
            leadForm.phone
          "
          placeholder="Phone"
        />

        <InputText
          v-model="
            leadForm.email
          "
          placeholder="Email"
        />

        <Dropdown

          v-model="
            leadForm.course
          "

          :options="
            courseStore
            .courses
          "

          optionLabel="name"

          optionValue="name"

          placeholder="Course"
        />

        <Dropdown

          v-model="
            leadForm.source
          "

          :options="
            sourceOptions
          "

          placeholder="Source"
        />

        <Dropdown

          v-model="
            leadForm.status
          "

          :options="
            statusOptions
          "

          placeholder="Status"
        />

        <Dropdown
          v-model="leadForm.assigned_counselor"
          :options="counselors"
          optionLabel="name"
          optionValue="name"
          placeholder="Counselor"
        />

        <InputText

          v-model="
            leadForm
            .next_followup
          "

          type="date"
        />

        <Button

          :label="

            editingLeadId

            ?

            'Update'

            :

            'Save'
          "

          icon="pi pi-check"

          @click="
            saveLead
          "
        />

      </div>

    </Dialog>
    
  </MainLayout>

</template>

<style scoped>
.page-header {

  display: flex;

  justify-content:
    space-between;

  align-items: center;
}

.table-toolbar {

  margin-bottom: 16px;
}

.form-grid {

  display: flex;

  flex-direction: column;

  gap: 16px;
}

.action-buttons {

  display: flex;

  gap: 8px;
}
</style>