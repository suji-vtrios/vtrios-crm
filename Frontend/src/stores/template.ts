import {
  defineStore
} from 'pinia'

import { ref }
from 'vue'

import {

  getTemplates,

  createTemplate,

  updateTemplate,

  deleteTemplate

} from '@/services/templateService'

export const useTemplateStore =
defineStore(
  'template',
  () => {

    const templates =
      ref<any[]>([])

    async function loadTemplates() {

      templates.value =
        await getTemplates()
    }

    async function addTemplate(
      template: any
    ) {

      await createTemplate(
        template
      )

      await loadTemplates()
    }

    async function editTemplate(
      id: number,
      template: any
    ) {

      await updateTemplate(
        id,
        template
      )

      await loadTemplates()
    }

    async function removeTemplate(
      id: number
    ) {

      await deleteTemplate(id)

      await loadTemplates()
    }

    return {

      templates,

      loadTemplates,

      addTemplate,

      editTemplate,

      removeTemplate
    }
  }
)