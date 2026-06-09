import {
  createRouter,
  createWebHistory
} from 'vue-router'

import {
  useAuthStore
} from '@/stores/auth'

import DashboardView
from '@/views/DashboardView.vue'

import LeadsView
from '@/views/LeadsView.vue'

import LeadDetailsView
from '@/views/LeadDetailsView.vue'

import FollowupsView
from '@/views/FollowupsView.vue'

import StudentsView
from '@/views/StudentsView.vue'

import BatchesView
from '@/views/BatchesView.vue'

import CoursesView
from '@/views/CoursesView.vue'

import LoginView
from '@/views/LoginView.vue'

import UsersView
from '@/views/UsersView.vue'

import TemplatesView
from '@/views/TemplatesView.vue'

import ConversationsView
from '@/views/ConversationsView.vue'

import AssessmentCategoriesView
from '@/views/AssessmentCategoriesView.vue'

import AssessmentSessionView
from '@/views/AssessmentSessionView.vue'

import AssessmentResultView
from '@/views/AssessmentResultView.vue'

import AssessmentSessionsView
from '@/views/AssessmentSessionsView.vue'

const router =
createRouter({

  history:
    createWebHistory(),

  routes: [

    {
      path: '/login',

      component:
        LoginView
    },

    {
      path: '/',

      component:
        DashboardView,

      meta: {
        roles: [

          'Admin',

          'Counselor',

          'Marketing'
        ]
      }
    },

    {
      path: '/leads',

      component:
        LeadsView,

      meta: {
        roles: [

          'Admin',

          'Counselor'
        ]
      }
    },

    {
      path:
        '/leads/:id',

      component:
        LeadDetailsView,

      meta: {
        roles: [

          'Admin',

          'Counselor'
        ]
      }
    },

    {
      path:
        '/followups',

      component:
        FollowupsView,

      meta: {
        roles: [

          'Admin',

          'Counselor'
        ]
      }
    },

    {
      path:
        '/students',

      component:
        StudentsView,

      meta: {
        roles: [

          'Admin',

          'Trainer'
        ]
      }
    },

    {
      path:
        '/batches',

      component:
        BatchesView,

      meta: {
        roles: [

          'Admin',

          'Trainer'
        ]
      }
    },

    {
      path:
        '/courses',

      component:
        CoursesView,

      meta: {
        roles: [

          'Admin'
        ]
      }
    },

    {
      path: '/users',

      component:
        UsersView,

      meta: {
        roles: ['Admin']
      }
    },

    {
      path: '/templates',

      component:
        TemplatesView,

      meta: {
        roles: ['Admin']
      }
    },

    {
      path: '/conversations',

      component:
        ConversationsView
    },

    {
      path: '/assessment-categories',
      component:
        AssessmentCategoriesView
    },

    {
      path:
      '/assessment-subcategories',

      component: () =>
        import(
          '@/views/AssessmentSubcategoriesView.vue'
        )
    },

    {
      path:
      '/assessment-competencies',

      component: () =>
        import(
          '@/views/AssessmentCompetenciesView.vue'
        )
    },
    {
      path:
        '/assessment-questions',

      name:
        'assessment-questions',

      component: () =>
        import(
          '@/views/AssessmentQuestionsView.vue'
        )
    },
    {
      path:
        '/assessment-session/:id',

      name:
        'AssessmentSession',

      component:
        AssessmentSessionView
    },
    {
      path:
        '/assessment-result/:sessionId',

      name:
        'AssessmentResult',

      component:
        AssessmentResultView
    },
    {
      path:
        '/assessment-sessions',

      name:
        'AssessmentSessions',

      component:
        AssessmentSessionsView
    },
  ]
})

router.beforeEach(
  (to) => {

    const authStore =
      useAuthStore()

    authStore.loadUser()

    const isLoggedIn =
      authStore
        .isAuthenticated

    if (

      to.path !== '/login'

      &&

      !isLoggedIn

    ) {

      return '/login'
    }

    const userRole =
      authStore
        .user?.role

    const allowedRoles = to.meta.roles as string[]

    if (

      allowedRoles

      &&

      !allowedRoles
        .includes(
          userRole
        )

    ) {

      return '/'
    }
  }
)

export default router