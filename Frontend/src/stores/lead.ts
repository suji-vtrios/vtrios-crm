import { defineStore } from 'pinia'
import { ref } from 'vue'

import {
  getLeads,
  getLead,
  createLead,
  updateLead,
  deleteLead as deleteLeadApi
} from '@/services/leadService'

export const useLeadStore =
  defineStore('lead', () => {

    const leads = ref<any[]>([])

    const selectedLead =
      ref<any>(null)

    async function loadLeads() {

      leads.value =
        await getLeads()
    }

    async function loadLead(
      id: number
    ) {

      selectedLead.value =
        await getLead(id)
    }

    async function addLead(
      lead: any
    ) {

      await createLead(
        lead
      )

      await loadLeads()
    }

    async function editLead(
      id: number,
      lead: any
    ) {

      await updateLead(
        id,
        lead
      )

      await loadLeads()

      if (
        selectedLead.value &&
        selectedLead.value.id === id
      ) {
        await loadLead(id)
      }
    }

    async function deleteLead(id: number) {
      await deleteLeadApi(id)

      await loadLeads()
    }

    return {
      leads,
      selectedLead,

      loadLeads,
      loadLead,

      addLead,
      editLead,
      deleteLead
    }
  })