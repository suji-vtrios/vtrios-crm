<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import MainLayout from '@/layouts/MainLayout.vue'

import { useLeadStore } from '@/stores/lead'
import { useFollowupStore } from '@/stores/followup'

import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Timeline from 'primevue/timeline'
import InputText from 'primevue/inputtext'
import Calendar from 'primevue/calendar'
import { useStudentStore } from '@/stores/student'

const route = useRoute()

const leadStore = useLeadStore()
const followupStore = useFollowupStore()

const leadId = Number(route.params.id)

const remarks = ref('')
const nextFollowup = ref()
const studentStore = useStudentStore()

onMounted(async () => {
  await leadStore.loadLead(leadId)

  await followupStore.loadFollowups(
    leadId
  )
})

async function saveFollowup() {
  if (!remarks.value) return

  await followupStore.addFollowup({
    id: Date.now(),

    lead_id: leadId,

    followup_date: new Date()
      .toISOString()
      .split('T')[0],

    remarks: remarks.value,

    status:
      leadStore.selectedLead?.status ||
      'New',

    next_followup:
      nextFollowup.value
  })

  remarks.value = ''
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

async function enrollLead() {

    const lead =
      leadStore.selectedLead

    if (!lead) return

    await studentStore
      .addStudent({

        id: Date.now(),

        name: lead.name,

        phone: lead.phone,

        email: lead.email,

        course: lead.course,

        enrollment_date:
          new Date()
          .toISOString()
          .split('T')[0],

        status: 'Active'
      })

    await leadStore.editLead(
      lead.id,
      {
        ...lead,
        status: 'Enrolled'
      }
    )

    alert(
      'Student enrolled successfully'
    )
  }
</script>

<template>
  <MainLayout>
    <div
      v-if="
        leadStore.selectedLead
      "
    >
      <!-- Header -->

      <div class="lead-header">
        <div>
          <h1>
            {{
              leadStore.selectedLead
                .name
            }}
          </h1>

          <Tag
            :value="
              leadStore.selectedLead
                .status
            "
            :severity="
              getStatusSeverity(
                leadStore.selectedLead
                  .status
              )
            "
          />
        </div>
      </div>

      <!-- Info Section -->

      <div class="details-grid">
        <Card>
          <template #title>
            Lead Information
          </template>

          <template #content>
            <div
              class="info-row"
            >
              <span>Phone</span>

              <strong>
                {{
                  leadStore
                    .selectedLead
                    .phone
                }}
              </strong>
            </div>

            <div
              class="info-row"
            >
              <span>Email</span>

              <strong>
                {{
                  leadStore
                    .selectedLead
                    .email
                }}
              </strong>
            </div>

            <div
              class="info-row"
            >
              <span>Course</span>

              <strong>
                {{
                  leadStore
                    .selectedLead
                    .course
                }}
              </strong>
            </div>

            <div
              class="info-row"
            >
              <span>Source</span>

              <strong>
                {{
                  leadStore
                    .selectedLead
                    .source
                }}
              </strong>
            </div>

            <div
              class="info-row"
            >
              <span>Status</span>

              <strong>
                {{
                  leadStore
                    .selectedLead
                    .status
                }}
              </strong>
            </div>
          </template>
        </Card>

        <Card>
          <template #title>
            Follow Up
          </template>

          <template #content>
            <div
              class="followup-box"
            >
              <label>
                Next Follow-up
              </label>

              <Calendar
                v-model="
                  nextFollowup
                "
                showIcon
              />

              <label>
                Remarks
              </label>

              <InputText
                v-model="remarks"
                placeholder="Enter remarks"
              />

              <div
                class="button-group"
              >
                <Button
                  label="Add Note"
                  icon="pi pi-pencil"
                  @click="
                    saveFollowup
                  "
                />

                <Button
                  label="Schedule"
                  icon="pi pi-calendar"
                  severity="secondary"
                />

                <Button
                  label="Enroll Student"
                  icon="pi pi-check"
                  severity="success"
                  @click="enrollLead"
                />
              </div>
            </div>
          </template>
        </Card>
      </div>

      <!-- Timeline -->

      <Card class="mt-4">
        <template #title>
          Activity Timeline
        </template>

        <template #content>
          <Timeline
            :value="
              followupStore.followups
            "
          >
            <template
              #content="
                slotProps
              "
            >
              <div>
                <strong>
                  {{
                    slotProps.item
                      .remarks
                  }}
                </strong>

                <div>
                  {{
                    slotProps.item
                      .followup_date
                  }}
                </div>

                <div class="next-followup">
                    Next Follow-up:
                    {{
                        new Date(
                        slotProps.item.next_followup
                        ).toLocaleDateString()
                    }}
                </div>
              </div>
            </template>
          </Timeline>
        </template>
      </Card>
    </div>
  </MainLayout>
</template>

<style scoped>
.lead-header {
  margin-bottom: 24px;
}

.lead-header h1 {
  font-size: 42px;
  margin-bottom: 10px;
}

.details-grid {
  display: grid;
  grid-template-columns:
    1fr 1fr;
  gap: 24px;
}

.info-row {
  display: flex;
  justify-content:
    space-between;

  padding: 14px 0;

  border-bottom:
    1px solid #e5e7eb;
}

.followup-box {
  display: flex;
  flex-direction: column;

  gap: 16px;
}

.button-group {
  display: flex;
  gap: 12px;
}

.mt-4 {
  margin-top: 24px;
}
</style>