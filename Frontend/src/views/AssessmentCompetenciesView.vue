<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

import MainLayout from '@/layouts/MainLayout.vue'

import Card from 'primevue/card'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'

import {
  useAssessmentCategoryStore
} from '@/stores/assessmentCategory'

import {
  useAssessmentSubcategoryStore
} from '@/stores/assessmentSubcategory'

import {
  useAssessmentCompetencyStore
} from '@/stores/assessmentCompetency'

const categoryStore =
  useAssessmentCategoryStore()

const subcategoryStore =
  useAssessmentSubcategoryStore()

const competencyStore =
  useAssessmentCompetencyStore()

const dialogVisible = ref(false)

const editingCompetencyId =
  ref<number | null>(null)

const competencyForm = ref({
  category_id: null,
  subcategory_id: null,
  name: '',
  description: '',
  weight: 1,
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

const filteredSubcategories =
computed(() => {

  return subcategoryStore
    .subcategories
    .filter(
      s =>
      s.category_id ===
      competencyForm.value.category_id
    )
})

async function saveCompetency() {

  const payload = {

    subcategory_id:
      competencyForm.value
      .subcategory_id,

    name:
      competencyForm.value
      .name,

    description:
      competencyForm.value
      .description,

    weight:
      competencyForm.value
      .weight,

    is_active:
      competencyForm.value
      .is_active
  }

  if (
    editingCompetencyId.value
  ) {

    await competencyStore
      .editCompetency(
        editingCompetencyId.value,
        payload
      )

  } else {

    await competencyStore
      .addCompetency(
        payload
      )
  }

  closeDialog()
}

function openAddDialog() {

  editingCompetencyId.value =
    null

  competencyForm.value = {

    category_id: null,

    subcategory_id: null,

    name: '',

    description: '',

    weight: 1,

    is_active: true
  }

  dialogVisible.value = true
}

function editCompetency(
  competency: any
) {

  const subcategory =
    subcategoryStore
      .subcategories
      .find(
        s =>
        s.id ===
        competency.subcategory_id
      )

  competencyForm.value = {

    category_id:
      subcategory
        ?.category_id || null,

    subcategory_id:
      competency.subcategory_id,

    name:
      competency.name,

    description:
      competency.description,

    weight:
      competency.weight,

    is_active:
      competency.is_active
  }

  editingCompetencyId.value =
    competency.id

  dialogVisible.value = true
}

async function deleteCompetency(
  id: number
) {

  if (
    !confirm(
      'Are you sure you want to delete this competency?'
    )
  ) {
    return
  }

  await competencyStore
    .removeCompetency(id)
}

function closeDialog() {

  dialogVisible.value = false
}

function getCategoryName(
  subcategoryId: number
) {

  const subcategory =
    subcategoryStore
      .subcategories
      .find(
        s => s.id === subcategoryId
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

function getSubcategoryName(
  subcategoryId: number
) {

  return subcategoryStore
    .subcategories
    .find(
      s => s.id === subcategoryId
    )?.name || '-'
}

onMounted(async () => {

  await categoryStore
    .loadCategories()

  await subcategoryStore
    .loadSubcategories()

  await competencyStore
    .loadCompetencies()
})
</script>

<template>
  <MainLayout>

```
<Card>

  <template #title>

    <div class="page-header">

      <span>
        Assessment Competencies
      </span>

      <Button
        label="Add Competency"
        icon="pi pi-plus"
        @click="openAddDialog"
      />

    </div>

  </template>

  <template #content>

    <DataTable
      :value="
        competencyStore.competencies
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
              slotProps.data.subcategory_id
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
              slotProps.data.subcategory_id
            )
          }}

        </template>

      </Column>

      <Column
        field="name"
        header="Competency"
      />

      <Column
        field="weight"
        header="Weight"
      />

      <Column
        header="Status"
      >

        <template #body="slotProps">

          <Tag
            :value="
              slotProps.data.is_active
                ? 'Active'
                : 'Inactive'
            "
            :severity="
              slotProps.data.is_active
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
                editCompetency(
                  slotProps.data
                )
              "
            />

            <Button
              icon="pi pi-trash"
              severity="danger"
              rounded
              @click="
                deleteCompetency(
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
    width: '500px'
  }"
  :header="
    editingCompetencyId
      ? 'Edit Competency'
      : 'Add Competency'
  "
>

  <div class="form-grid">

    <Dropdown
      v-model="
        competencyForm.category_id
      "
      :options="
        categoryStore.categories
      "
      optionLabel="name"
      optionValue="id"
      placeholder="Select Category"
    />

    <Dropdown
      v-model="
        competencyForm.subcategory_id
      "
      :options="
        filteredSubcategories
      "
      optionLabel="name"
      optionValue="id"
      placeholder="Select Subcategory"
    />

    <InputText
      v-model="
        competencyForm.name
      "
      placeholder="Competency Name"
    />

    <InputText
      v-model="
        competencyForm.description
      "
      placeholder="Description"
    />

    <InputNumber
      v-model="
        competencyForm.weight
      "
      placeholder="Weight"
    />

    <Dropdown
      v-model="
        competencyForm.is_active
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
        editingCompetencyId
          ? 'Update'
          : 'Save'
      "
      icon="pi pi-check"
      @click="
        saveCompetency
      "
    />

  </div>

</Dialog>
```

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
