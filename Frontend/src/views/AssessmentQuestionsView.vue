<script setup lang="ts">
import { ref, onMounted } from 'vue'

import MainLayout from '@/layouts/MainLayout.vue'

import Card from 'primevue/card'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'

import {
  useAssessmentQuestionStore
} from '@/stores/assessmentQuestion'

import {
  useAssessmentCompetencyStore
} from '@/stores/assessmentCompetency'

import {
  useAssessmentSubcategoryStore
} from '@/stores/assessmentSubcategory'

import {
  useAssessmentCategoryStore
} from '@/stores/assessmentCategory'

const questionStore =
  useAssessmentQuestionStore()

const competencyStore =
  useAssessmentCompetencyStore()

const subcategoryStore =
  useAssessmentSubcategoryStore()

const categoryStore =
  useAssessmentCategoryStore()

const dialogVisible = ref(false)

const editingQuestionId =
  ref<number | null>(null)

const questionForm = ref({

  competency_id: null,

  question: '',

  stream: 'Common',

  difficulty: 1,

  question_type: 'Knowledge',

  expected_keywords: '',

  scoring_guidance: '',

  source: 'Vtrios',

  is_active: true
})

const statusOptions = [
  {
    label: 'Active',
    value: true
  },
  {
    label: 'Inactive',
    value: false
  }
]

const questionTypeOptions = [
  {
    label: 'Knowledge',
    value: 'Knowledge'
  },
  {
    label: 'Application',
    value: 'Application'
  },
  {
    label: 'Scenario',
    value: 'Scenario'
  },
  {
    label: 'Leadership',
    value: 'Leadership'
  }
]

function getCompetencyName(
  competencyId: number
) {
  return competencyStore
    .competencies
    .find(
      c => c.id === competencyId
    )?.name || '-'
}

function getSubcategoryName(
  competencyId: number
) {

  const competency =
    competencyStore
      .competencies
      .find(
        c => c.id === competencyId
      )

  if (!competency)
    return '-'

  return subcategoryStore
    .subcategories
    .find(
      s =>
      s.id ===
      competency.subcategory_id
    )?.name || '-'
}

function getCategoryName(
  competencyId: number
) {

  const competency =
    competencyStore
      .competencies
      .find(
        c => c.id === competencyId
      )

  if (!competency)
    return '-'

  const subcategory =
    subcategoryStore
      .subcategories
      .find(
        s =>
        s.id ===
        competency.subcategory_id
      )

  if (!subcategory)
    return '-'

  return categoryStore
    .categories
    .find(
      c =>
      c.id ===
      subcategory.category_id
    )?.name || '-'
}

function openAddDialog() {

  editingQuestionId.value =
    null

  questionForm.value = {

    competency_id: null,

    question: '',

    stream: 'Common',

    difficulty: 1,

    question_type: 'Knowledge',

    expected_keywords: '',

    scoring_guidance: '',

    source: 'Vtrios',

    is_active: true
  }

  dialogVisible.value = true
}

function editQuestion(
  question: any
) {

  editingQuestionId.value =
    question.id

  questionForm.value = {

    competency_id:
      question.competency_id,

    question:
      question.question,

    stream:
      question.stream,

    difficulty:
      question.difficulty,

    question_type:
      question.question_type,

    expected_keywords:
      question.expected_keywords,

    scoring_guidance:
      question.scoring_guidance,

    source:
      question.source,

    is_active:
      question.is_active
  }

  dialogVisible.value = true
}

async function saveQuestion() {

  const payload = {

    competency_id:
      questionForm.value
        .competency_id,

    question:
      questionForm.value
        .question,

    stream:
      questionForm.value
        .stream,

    difficulty:
      questionForm.value
        .difficulty,

    question_type:
      questionForm.value
        .question_type,

    expected_keywords:
      questionForm.value
        .expected_keywords,

    scoring_guidance:
      questionForm.value
        .scoring_guidance,

    source:
      questionForm.value
        .source,

    is_active:
      questionForm.value
        .is_active
  }

  if (
    editingQuestionId.value
  ) {

    await questionStore
      .editQuestion(
        editingQuestionId.value,
        payload
      )

  } else {

    await questionStore
      .addQuestion(
        payload
      )
  }

  closeDialog()
}

async function deleteQuestion(
  id: number
) {

  if (
    !confirm(
      'Are you sure you want to delete this question?'
    )
  ) {
    return
  }

  await questionStore
    .removeQuestion(id)
}

function closeDialog() {
  dialogVisible.value = false
}

onMounted(async () => {

  await categoryStore
    .loadCategories()

  await subcategoryStore
    .loadSubcategories()

  await competencyStore
    .loadCompetencies()

  await questionStore
    .loadQuestions()
})
</script>

<template>
  <MainLayout>

    <Card>

      <template #title>

        <div class="page-header">

          <span>
            Assessment Questions
          </span>

          <Button
            label="Add Question"
            icon="pi pi-plus"
            @click="openAddDialog"
          />

        </div>

      </template>

      <template #content>

        <DataTable
          :value="
            questionStore.questions
          "
          paginator
          :rows="10"
          stripedRows
          responsiveLayout="scroll"
        >

          <Column
            header="Category"
          >
            <template #body="slotProps">
              {{
                getCategoryName(
                  slotProps.data.competency_id
                )
              }}
            </template>
          </Column>

          <Column
            header="Subcategory"
          >
            <template #body="slotProps">
              {{
                getSubcategoryName(
                  slotProps.data.competency_id
                )
              }}
            </template>
          </Column>

          <Column
            header="Competency"
          >
            <template #body="slotProps">
              {{
                getCompetencyName(
                  slotProps.data.competency_id
                )
              }}
            </template>
          </Column>

          <Column
            field="question"
            header="Question"
          />

          <Column
            field="question_type"
            header="Type"
          />

          <Column
            field="difficulty"
            header="Difficulty"
          />

          <Column
            header="Status"
          >

            <template #body="slotProps">

              <Tag
                :value="
                  slotProps.data
                    .is_active
                  ? 'Active'
                  : 'Inactive'
                "
                :severity="
                  slotProps.data
                    .is_active
                  ? 'success'
                  : 'danger'
                "
              />

            </template>

          </Column>

          <Column
            header="Actions"
          >

            <template #body="slotProps">

              <div
                class="action-buttons"
              >

                <Button
                  icon="pi pi-pencil"
                  severity="warning"
                  rounded
                  @click="
                    editQuestion(
                      slotProps.data
                    )
                  "
                />

                <Button
                  icon="pi pi-trash"
                  severity="danger"
                  rounded
                  @click="
                    deleteQuestion(
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
        width: '700px'
      }"
      :header="
        editingQuestionId
          ? 'Edit Question'
          : 'Add Question'
      "
    >

      <div class="form-grid">

        <Dropdown
          v-model="
            questionForm.competency_id
          "
          :options="
            competencyStore.competencies
          "
          optionLabel="name"
          optionValue="id"
          placeholder="
            Select Competency
          "
        />

        <Textarea
          v-model="
            questionForm.question
          "
          rows="4"
          placeholder="
            Question
          "
        />

        <Dropdown
          v-model="
            questionForm.question_type
          "
          :options="
            questionTypeOptions
          "
          optionLabel="label"
          optionValue="value"
          placeholder="
            Question Type
          "
        />

        <InputNumber
          v-model="
            questionForm.difficulty
          "
          placeholder="
            Difficulty
          "
        />

        <Textarea
          v-model="
            questionForm.expected_keywords
          "
          rows="3"
          placeholder="
            Expected Keywords
          "
        />

        <Textarea
          v-model="
            questionForm.scoring_guidance
          "
          rows="3"
          placeholder="
            Scoring Guidance
          "
        />

        <Dropdown
          v-model="
            questionForm.is_active
          "
          :options="
            statusOptions
          "
          optionLabel="label"
          optionValue="value"
          placeholder="Status"
        />

        <Button
          :label="
            editingQuestionId
              ? 'Update'
              : 'Save'
          "
          icon="pi pi-check"
          @click="
            saveQuestion
          "
        />

      </div>

    </Dialog>

  </MainLayout>
</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
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