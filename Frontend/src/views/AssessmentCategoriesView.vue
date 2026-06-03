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

const categoryStore =
  useAssessmentCategoryStore()

const dialogVisible = ref(false)

const editingCategoryId =
  ref<number | null>(null)

const globalFilter = ref('')

const categoryForm = ref({
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

async function saveCategory() {

  if (editingCategoryId.value) {

    await categoryStore
      .editCategory(
        editingCategoryId.value,
        categoryForm.value
      )

  } else {

    await categoryStore
      .addCategory(
        categoryForm.value
      )
  }

  closeDialog()
}

function openAddDialog() {

  editingCategoryId.value =
    null

  categoryForm.value = {

    name: '',

    description: '',

    display_order: 1,

    is_active: true
  }

  dialogVisible.value =
    true
}

function editCategory(
  category: any
) {

  editingCategoryId.value =
    category.id

  categoryForm.value = {
    ...category
  }

  dialogVisible.value =
    true
}

async function deleteCategory(
  id: number
) {

  if (
    !confirm(
      'Are you sure you want to delete this category?'
    )
  ) {
    return
  }

  await categoryStore
    .removeCategory(id)
}

function closeDialog() {

  dialogVisible.value =
    false
}

onMounted(async () => {

  await categoryStore
    .loadCategories()
})
</script>

<template>
  <MainLayout>

    <Card>

      <template #title>

        <div class="page-header">

          <span>
            Assessment Categories
          </span>

          <Button
            label="Add Category"
            icon="pi pi-plus"
            @click="openAddDialog"
          />

        </div>

      </template>

      <template #content>

        <div class="table-toolbar">

          <InputText
            v-model="globalFilter"
            placeholder="Search Categories"
          />

        </div>

        <DataTable
          :value="
            categoryStore.categories
          "
          paginator
          :rows="10"
          stripedRows
          responsiveLayout="scroll"
        >

          <Column
            field="name"
            header="Name"
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
                    editCategory(
                      slotProps.data
                    )
                  "
                />

                <Button
                  icon="pi pi-trash"
                  severity="danger"
                  rounded
                  @click="
                    deleteCategory(
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
        editingCategoryId
          ? 'Edit Category'
          : 'Add Category'
      "
    >

      <div class="form-grid">

        <InputText
          v-model="
            categoryForm.name
          "
          placeholder="Name"
        />

        <InputText
          v-model="
            categoryForm.description
          "
          placeholder="Description"
        />

        <InputNumber
          v-model="
            categoryForm.display_order
          "
          placeholder="Display Order"
        />

        <Dropdown
          v-model="
            categoryForm.is_active
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
            editingCategoryId
              ? 'Update'
              : 'Save'
          "
          icon="pi pi-check"
          @click="saveCategory"
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

.table-toolbar {
  margin-bottom: 16px;
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