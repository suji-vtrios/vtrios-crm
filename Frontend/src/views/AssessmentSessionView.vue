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

const route =
  useRoute()

const sessionId =
  route.params.id

const selectedSector =
  ref('')

function continueAssessment() {

  alert(

    `Session ${sessionId}
     Sector:
     ${selectedSector.value}`

  )
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

        Welcome to Vtrios
        Assessment

      </h3>

      <p>

        Session ID:
        {{ sessionId }}

      </p>

      <div
        class="sector-group"
      >

        <div>

          <RadioButton
            v-model="
              selectedSector
            "
            inputId="arch"
            value="Architecture"
          />

          <label for="arch">

            Architecture

          </label>

        </div>

        <div>

          <RadioButton
            v-model="
              selectedSector
            "
            inputId="struct"
            value="Structure"
          />

          <label
            for="struct"
          >

            Structure

          </label>

        </div>

        <div>

          <RadioButton
            v-model="
              selectedSector
            "
            inputId="mep"
            value="MEP"
          />

          <label for="mep">

            MEP

          </label>

        </div>

        <div>

          <RadioButton
            v-model="
              selectedSector
            "
            inputId="const"
            value="Construction"
          />

          <label
            for="const"
          >

            Construction

          </label>

        </div>

      </div>

      <Button

        label="Continue"

        @click="
          continueAssessment
        "

      />

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