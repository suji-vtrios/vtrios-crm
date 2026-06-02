import { defineStore } from 'pinia'

import { ref } from 'vue'

import {
  getBatches,
  createBatch,
  updateBatch
} from '@/services/batchService'

export const useBatchStore =
defineStore(
  'batch',
  () => {

    const batches =
      ref<any[]>([])

    async function loadBatches() {

      batches.value =
        await getBatches()
    }

    async function addBatch(
      batch: any
    ) {

      await createBatch(
        batch
      )

      await loadBatches()
    }

    async function editBatch(
      id: number,
      batch: any
    ) {

      await updateBatch(
        id,
        batch
      )

      await loadBatches()
    }

    return {

      batches,

      loadBatches,

      addBatch,

      editBatch
    }
  }
)