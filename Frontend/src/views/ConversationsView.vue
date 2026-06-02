<script setup lang="ts">
import { onMounted }
from 'vue'

import MainLayout
from '@/layouts/MainLayout.vue'

import Card
from 'primevue/card'

import DataTable
from 'primevue/datatable'

import Column
from 'primevue/column'

import Tag
from 'primevue/tag'

import Button
from 'primevue/button'

import { useConversationStore }
from '@/stores/conversation'

const conversationStore =
  useConversationStore()

onMounted(async () => {

  await conversationStore
    .loadConversations()
})
</script>

<template>

  <MainLayout>

    <Card>

      <template #title>

        Unified Inbox

      </template>

      <template #content>

        <DataTable

          :value="
            conversationStore
            .conversations
          "

          paginator

          :rows="10"

          stripedRows
        >

          <Column
            field="lead_name"
            header="Lead"
          />

          <Column
            field="platform"
            header="Platform"
          >

            <template
              #body="slotProps"
            >

              <Tag

                :value="
                  slotProps.data
                  .platform
                "

                :severity="

                  slotProps.data
                  .platform
                  === 'Instagram'

                  ? 'danger'

                  :

                  slotProps.data
                  .platform
                  === 'WhatsApp'

                  ? 'success'

                  :

                  'info'
                "
              />

            </template>

          </Column>

          <Column
            field="last_message"
            header="Last Message"
          />

          <Column
            field="assigned_counselor"
            header="Counselor"
          />

          <Column
            field="status"
            header="Status"
          >

            <template
              #body="slotProps"
            >

              <Tag

                :value="
                  slotProps.data
                  .status
                "

                :severity="

                  slotProps.data
                  .status
                  === 'Open'

                  ? 'warning'

                  :

                  'success'
                "
              />

            </template>

          </Column>

          <Column
            header="Unread"
          >

            <template
              #body="slotProps"
            >

              <Tag

                v-if="
                  slotProps.data
                  .unread
                "

                value="Unread"

                severity="danger"
              />

            </template>

          </Column>

          <Column
            header="Actions"
          >

            <template
              #body="slotProps"
            >

              <Button

                v-if="
                  slotProps.data
                  .unread
                "

                label="Mark Read"

                size="small"

                @click="

                  conversationStore
                  .readConversation(
                    slotProps.data.id
                  )
                "
              />

            </template>

          </Column>

        </DataTable>

      </template>

    </Card>

  </MainLayout>

</template>