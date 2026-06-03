<script setup lang="ts">
import { ref, onMounted } from 'vue'

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

const categoryStore =
  useAssessmentCategoryStore()

const subcategoryStore =
  useAssessmentSubcategoryStore()

const dialogVisible = ref(false)

const editingSubcategoryId =
  ref<number | null>(null)

const subcategoryForm = ref({
  category_id: null,
  name: '',
  description: '',
  display_order: 1,
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

async function saveSubcategory() {

  if (
    editingSubcategoryId.value
  ) {

    await subcategoryStore
      .editSubcategory(
        editingSubcategoryId.value,
        subcategoryForm.value
      )

  } else {

    await subcategoryStore
      .addSubcategory(
        subcategoryForm.value
      )
  }

  closeDialog()
}

function openAddDialog() {

  editingSubcategoryId.value =
    null

  subcategoryForm.value = {

    category_id: null,

    name: '',

    description: '',

    display_order: 1,

    is_active: true
  }

  dialogVisible.value = true
}

function editSubcategory(
  subcategory: any
) {

  editingSubcategoryId.value =
    subcategory.id

  subcategoryForm.value = {
    ...subcategory
  }

  dialogVisible.value = true
}

async function deleteSubcategory(
  id: number
) {

  if (
    !confirm(
      'Are you sure you want to delete this subcategory?'
    )
  ) {
    return
  }

  await subcategoryStore
    .removeSubcategory(id)
}

function closeDialog() {

  dialogVisible.value = false
}

function getCategoryName(
  categoryId: number
) {

  return categoryStore
    .categories
    .find(
      c => c.id === categoryId
    )?.name || '-'
}

onMounted(async () => {

  await categoryStore
    .loadCategories()

  await subcategoryStore
    .loadSubcategories()
})
</script>

<template>
  <MainLayout>

    <Card>

      <template #title>

        <div class="page-header">

          <span>
            Assessment Subcategories
          </span>

          <Button
            label="Add Subcategory"
            icon="pi pi-plus"
            @click="openAddDialog"
          />

        </div>

      </template>

      <template #content>

        <DataTable
          :value="
            subcategoryStore.subcategories
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
                  slotProps.data.category_id
                )
              }}

            </template>

          </Column>

          <Column
            field="name"
            header="Subcategory"
          />

          <Column
            field="description"
            header="Description"
          />

          <Column
            field="display_order"
            header="Order"
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
                    editSubcategory(
                      slotProps.data
                    )
                  "
                />

                <Button
                  icon="pi pi-trash"
                  severity="danger"
                  rounded
                  @click="
                    deleteSubcategory(
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
        editingSubcategoryId
          ? 'Edit Subcategory'
          : 'Add Subcategory'
      "
    >

      <div class="form-grid">

        <Dropdown

          v-model="
            subcategoryForm.category_id
          "

          :options="
            categoryStore.categories
          "

          optionLabel="name"

          optionValue="id"

          placeholder="Select Category"
        />

        <InputText
          v-model="
            subcategoryForm.name
          "
          placeholder="Subcategory Name"
        />

        <InputText
          v-model="
            subcategoryForm.description
          "
          placeholder="Description"
        />

        <InputNumber
          v-model="
            subcategoryForm.display_order
          "
          placeholder="Display Order"
        />

        <Dropdown
          v-model="
            subcategoryForm.is_active
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
            editingSubcategoryId
              ? 'Update'
              : 'Save'
          "
          icon="pi pi-check"
          @click="
            saveSubcategory
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