<script setup lang="ts">

import { ref } from 'vue'

import {
  sendMessage
}
from '@/services/aiCounselorService'

const messages = ref([
  {
    role: 'assistant',
    content:
      'Hello! I am the Vtrios AI BIM Counselor. What is your educational qualification?'
  }
])

const input =
  ref('')

async function send() {

  if (!input.value)
    return

  messages.value.push({

    role: 'user',

    content:
      input.value
  })

  const userMessage =
    input.value

  input.value = ''

  const result =
    await sendMessage(
      userMessage
    )

  messages.value.push({

    role: 'assistant',

    content:
      result.message
  })
}

</script>

<template>

<div class="p-4">

  <h2>
    AI BIM Counselor
  </h2>

  <div
    style="
      height:500px;
      overflow:auto;
      border:1px solid #ddd;
      padding:10px;
      margin-top:10px;
    "
  >

    <div
      v-for="(
        item,
        index
      ) in messages"

      :key="index"
    >

      <b>
        {{ item.role }}
      </b>

      :

      {{ item.content }}

      <hr>

    </div>

  </div>

  <input

    v-model="input"

    class="form-control mt-3"

    placeholder="Type your message"
  >

  <button

    class="btn btn-primary mt-2"

    @click="send"
  >
    Send
  </button>

</div>

</template>