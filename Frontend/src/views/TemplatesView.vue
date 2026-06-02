<script setup lang="ts">
import { ref }
from 'vue'

import { onMounted }
from 'vue'

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

import Textarea
from 'primevue/textarea'

import DataTable
from 'primevue/datatable'

import Column
from 'primevue/column'

import { useTemplateStore }
from '@/stores/template'

const templateStore =
  useTemplateStore()

const dialogVisible =
  ref(false)

const editingTemplateId =
  ref<number | null>(null)

const templateForm =
  ref({

    name: '',

    channel: '',

    content: ''
  })

const channels = [

  'WhatsApp',

  'Email',

  'SMS'
]

async function saveTemplate() {

  if (
    editingTemplateId.value
  ) {

    await templateStore
      .editTemplate(

        editingTemplateId.value,

        templateForm.value
      )

  } else {

    await templateStore
      .addTemplate(
        templateForm.value
      )
  }

  closeDialog()
}

function openAddDialog() {

  editingTemplateId.value =
    null

  templateForm.value = {

    name: '',

    channel: '',

    content: ''
  }

  dialogVisible.value =
    true
}

function editTemplate(
  template: any
) {

  editingTemplateId.value =
    template.id

  templateForm.value = {

    ...template
  }

  dialogVisible.value =
    true
}

async function deleteTemplate(
  id: number
) {

  await templateStore
    .removeTemplate(id)
}

function closeDialog() {

  dialogVisible.value =
    false
}

onMounted(async () => {

  await templateStore
    .loadTemplates()
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
            Message Templates
          </span>

          <Button
            label="Add Template"
            icon="pi pi-plus"
            @click="
              openAddDialog
            "
          />

        </div>

      </template>

      <template #content>

        <DataTable

          :value="
            templateStore
            .templates
          "

          paginator

          :rows="10"

          stripedRows
        >

          <Column
            field="name"
            header="Name"
          />

          <Column
            field="channel"
            header="Channel"
          />

          <Column
            field="content"
            header="Content"
          />

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

                  icon="pi pi-pencil"

                  severity="warning"

                  rounded

                  @click="
                    editTemplate(
                      slotProps.data
                    )
                  "
                />

                <Button

                  icon="pi pi-trash"

                  severity="danger"

                  rounded

                  @click="
                    deleteTemplate(
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

      v-model:visible="
        dialogVisible
      "

      modal

      :style="{
        width: '600px'
      }"

      :header="

        editingTemplateId

        ?

        'Edit Template'

        :

        'Add Template'
      "
    >

      <div class="form-grid">

        <InputText

          v-model="
            templateForm.name
          "

          placeholder="Template Name"
        />

        <Dropdown

          v-model="
            templateForm.channel
          "

          :options="
            channels
          "

          placeholder="Channel"
        />

        <Textarea

          v-model="
            templateForm.content
          "

          rows="8"

          placeholder="Template Content"
        />

        <Button

          :label="

            editingTemplateId

            ?

            'Update'

            :

            'Save'
          "

          icon="pi pi-check"

          @click="
            saveTemplate
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