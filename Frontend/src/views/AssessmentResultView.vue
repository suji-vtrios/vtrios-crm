<script setup lang="ts">

import { ref }
from 'vue'

import {
  useRoute
}
from 'vue-router'

import {
  onMounted
}
from 'vue'

import MainLayout
from '@/layouts/MainLayout.vue'

import Card
from 'primevue/card'

import Button
from 'primevue/button'

import {
  assessmentEvaluationService
}
from '@/services/assessmentEvaluationService'

const route =
  useRoute()

const sessionId =
  Number(
    route.params.sessionId
  )

const result =
  ref<any>(null)

onMounted(async () => {

  result.value =

    await assessmentEvaluationService
      .getResult(
        sessionId
      )

})

</script>

<template>

<MainLayout>

  <Card>

    <template #title>

      Assessment Result

    </template>

    <template #content>

      <div
        v-if="result"
      >

        <h2>

          Assessment Completed

        </h2>

        <h3>

          Score:
          {{ result.score }}

        </h3>

        <h3>

          Recommended Course

        </h3>

        <p>

          {{
            result.recommendation
          }}

        </p>

        <Button
          label="Enroll Now"
        />

      </div>

    </template>

  </Card>

</MainLayout>

</template>