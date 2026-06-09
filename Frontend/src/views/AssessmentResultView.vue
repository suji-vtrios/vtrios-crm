<script setup lang="ts">

import {
  onMounted
}
from 'vue'

import {
  useRoute
}
from 'vue-router'

import MainLayout
from '@/layouts/MainLayout.vue'

import Card
from 'primevue/card'

import {
  useAssessmentReportStore
}
from '@/stores/assessmentReport'

import Button
from 'primevue/button'

import {
  assessmentEnrollmentService
}
from '@/services/assessmentEnrollmentService'


const route =
  useRoute()

const reportStore =
  useAssessmentReportStore()

onMounted(async () => {

  await reportStore
    .loadReport(
      Number(
        route.params.id
      )
    )
})

async function enrollStudent() {

  const student =

    await assessmentEnrollmentService
      .enroll(
        Number(
          route.params.id
        )
      )

  router.push(
    `/students`
  )

  console.log(student)

}

</script>

<template>

<MainLayout>

<Card>

<template #title>

Assessment Result

</template>

<template #content>

<div
v-if="reportStore.report"
>

<h2>

Score:
{{ reportStore.report.overall_score }}

</h2>

<p>

Recommendation:
{{ reportStore.report.recommendation }}

</p>

<p>

Strengths:
{{ reportStore.report.strengths }}

</p>

<p>

Weaknesses:
{{ reportStore.report.weaknesses }}

</p>

<p>

Feedback:
{{ reportStore.report.gpt_feedback }}

</p>
<Button
  label="Enroll Now"
  @click="enrollStudent"
/>

</div>

</template>

</Card>

</MainLayout>

</template>