<script setup lang="ts">

import { ref }
from 'vue'

import { useRoute }
from 'vue-router'

import MainLayout
from '@/layouts/MainLayout.vue'

import Card
from 'primevue/card'

import Button
from 'primevue/button'

import RadioButton
from 'primevue/radiobutton'

import Textarea
from 'primevue/textarea'

import {
  useAssessmentQuestionStore
} from '@/stores/assessmentQuestion'

import {
  onMounted
} from 'vue'

import {
  useAssessmentResponseStore
}
from '@/stores/assessmentResponse'

import {
  useRouter
}
from 'vue-router'

import {
  assessmentEvaluationService
}
from '@/services/assessmentEvaluationService'

const router =
  useRouter()

const responseStore =
  useAssessmentResponseStore()

const questionStore =
  useAssessmentQuestionStore()

const currentQuestion =
  ref(0)

const startedAssessment =
  ref(false)

const answer =
  ref('')

onMounted(async () => {

  await questionStore
    .loadQuestions()

})

const route =
  useRoute()

const sessionId =
  route.params.id

const selectedSector =
  ref('')

function continueAssessment() {

  startedAssessment.value =
    true
}

async function nextQuestion() {

  const question =

    questionStore.questions[
      currentQuestion.value
    ]

  await responseStore
    .addResponse({

      session_id:
        Number(sessionId),

      question_id:
        question.id,

      response:
        answer.value
    })

  if (

    currentQuestion.value <

    questionStore.questions.length - 1

  ) {

    currentQuestion.value++

    answer.value = ''

  } else {

    await assessmentEvaluationService
        .evaluate(
            Number(sessionId)
        )

        router.push(
        `/assessment-result/${sessionId}`
        )

  }
}

</script>

<template>

<MainLayout>

  <Card>

    <template #title>

      Assessment Session

    </template>

    <template #content>

  <h3>
    Welcome to Vtrios Assessment
  </h3>

  <p>
    Session ID: {{ sessionId }}
  </p>

  <div
    v-if="!startedAssessment"
    class="sector-group"
  >

    <div>

      <RadioButton
        v-model="selectedSector"
        inputId="arch"
        value="Architecture"
      />

      <label for="arch">
        Architecture
      </label>

    </div>

    <div>

      <RadioButton
        v-model="selectedSector"
        inputId="struct"
        value="Structure"
      />

      <label for="struct">
        Structure
      </label>

    </div>

    <div>

      <RadioButton
        v-model="selectedSector"
        inputId="mep"
        value="MEP"
      />

      <label for="mep">
        MEP
      </label>

    </div>

    <div>

      <RadioButton
        v-model="selectedSector"
        inputId="const"
        value="Construction"
      />

      <label for="const">
        Construction
      </label>

    </div>

    <Button
      label="Continue"
      @click="continueAssessment"
    />

  </div>

  <div
    v-else
  >

    <h3>
      Question {{ currentQuestion + 1 }}
    </h3>

    <p>
      {{
        questionStore.questions[
          currentQuestion
        ]?.question
      }}
    </p>

    <Textarea
      v-model="answer"
      rows="5"
      style="width:100%"
    />

    <Button
      label="Next"
      @click="nextQuestion"
    />

  </div>

</template>

  </Card>

</MainLayout>

</template>

<style scoped>

.sector-group {

  display: flex;

  flex-direction: column;

  gap: 12px;

}

</style>