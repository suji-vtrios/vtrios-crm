import {
  defineStore
} from 'pinia'

import { ref }
from 'vue'

import {
  getDashboardData
} from '@/services/analyticsService'

export const useAnalyticsStore =
defineStore(
  'analytics',
  () => {

    const dashboardData =
      ref<any>(null)

    async function loadDashboard() {

      dashboardData.value =
        await getDashboardData()
    }

    return {

      dashboardData,

      loadDashboard
    }
  }
)