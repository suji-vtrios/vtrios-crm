import { defineStore } from 'pinia'
import { ref } from 'vue'

import {

  getCategories,

  createCategory,

  updateCategory,

  deleteCategory

} from '@/services/assessmentCategoryService'

export const useAssessmentCategoryStore =
defineStore(
  'assessmentCategory',
  () => {

    const categories =
      ref<any[]>([])

    async function loadCategories() {

      categories.value =
        await getCategories()
    }

    async function addCategory(
      category: any
    ) {

      await createCategory(
        category
      )

      await loadCategories()
    }

    async function editCategory(
      id: number,
      category: any
    ) {

      await updateCategory(
        id,
        category
      )

      await loadCategories()
    }

    async function removeCategory(
      id: number
    ) {

      await deleteCategory(id)

      await loadCategories()
    }

    return {

      categories,

      loadCategories,

      addCategory,

      editCategory,

      removeCategory
    }
  }
)