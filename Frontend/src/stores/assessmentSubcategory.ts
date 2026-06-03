import { defineStore } from 'pinia'
import { ref } from 'vue'

import {

  getSubcategories,

  createSubcategory,

  updateSubcategory,

  deleteSubcategory

} from '@/services/assessmentSubcategoryService'

export const useAssessmentSubcategoryStore =
defineStore(
  'assessmentSubcategory',
  () => {

    const subcategories =
      ref<any[]>([])

    async function loadSubcategories() {

      subcategories.value =
        await getSubcategories()
    }

    async function addSubcategory(
      subcategory: any
    ) {

      await createSubcategory(
        subcategory
      )

      await loadSubcategories()
    }

    async function editSubcategory(
      id: number,
      subcategory: any
    ) {

      await updateSubcategory(
        id,
        subcategory
      )

      await loadSubcategories()
    }

    async function removeSubcategory(
      id: number
    ) {

      await deleteSubcategory(id)

      await loadSubcategories()
    }

    return {

      subcategories,

      loadSubcategories,

      addSubcategory,

      editSubcategory,

      removeSubcategory
    }
  }
)