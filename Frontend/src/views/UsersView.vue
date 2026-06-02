<script setup lang="ts">
import { ref, onMounted } from 'vue'

import MainLayout from '@/layouts/MainLayout.vue'

import Card from 'primevue/card'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'

import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const dialogVisible = ref(false)

const editingUserId = ref<number | null>(null)

const globalFilter = ref('')

const userForm = ref({
  name: '',
  email: '',
  password: '',
  role: 'Counselor',
  status: 'Active'
})

const roleOptions = [
  'Admin',
  'Counselor',
  'Marketing'
]

const statusOptions = [
  'Active',
  'Inactive'
]

async function saveUser() {
  if (editingUserId.value) {
    await userStore.editUser(
      editingUserId.value,
      userForm.value
    )
  } else {
    await userStore.addUser(
      userForm.value
    )
  }

  closeDialog()
}

function openAddDialog() {
  editingUserId.value = null

  userForm.value = {
    name: '',
    email: '',
    password: '',
    role: 'Counselor',
    status: 'Active'
  }

  dialogVisible.value = true
}

function editUser(user: any) {
  editingUserId.value = user.id

  userForm.value = {
    ...user,
    password: ''
  }

  dialogVisible.value = true
}

async function deleteUser(id: number) {
  if (
    !confirm(
      'Are you sure you want to delete this user?'
    )
  ) {
    return
  }

  await userStore.removeUser(id)
}

function closeDialog() {
  dialogVisible.value = false
}

onMounted(async () => {

  await userStore.loadUsers()

})
</script>

<template>
  <MainLayout>
    <Card>

      <template #title>
        <div class="page-header">

          <span>
            Users Management
          </span>

          <Button
            label="Add User"
            icon="pi pi-plus"
            @click="openAddDialog"
          />

        </div>
      </template>

      <template #content>

        <div class="table-toolbar">

          <InputText
            v-model="globalFilter"
            placeholder="Search Users"
          />

        </div>

        <DataTable
          :value="userStore.users"
          paginator
          :rows="10"
          stripedRows
          responsiveLayout="scroll"
          :globalFilterFields="[
            'name',
            'email',
            'role',
            'status'
          ]"
          :filters="{
            global: {
              value: globalFilter,
              matchMode: 'contains'
            }
          }"
        >

          <Column
            field="name"
            header="Name"
          />

          <Column
            field="email"
            header="Email"
          />

          <Column
            field="role"
            header="Role"
          />

          <Column
            header="Status"
          >
            <template #body="slotProps">

              <Tag
                :value="slotProps.data.status"
                :severity="
                  slotProps.data.status === 'Active'
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
                    editUser(
                      slotProps.data
                    )
                  "
                />

                <Button
                  icon="pi pi-trash"
                  severity="danger"
                  rounded
                  @click="
                    deleteUser(
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
      v-model:visible="dialogVisible"
      modal
      :style="{ width: '500px' }"
      :header="
        editingUserId
          ? 'Edit User'
          : 'Add User'
      "
    >

      <div class="form-grid">

        <InputText
          v-model="userForm.name"
          placeholder="Name"
        />

        <InputText
          v-model="userForm.email"
          placeholder="Email"
        />

        <InputText
          v-model="userForm.password"
          type="password"
          placeholder="Password"
        />

        <Dropdown
          v-model="userForm.role"
          :options="roleOptions"
          placeholder="Role"
        />

        <Dropdown
          v-model="userForm.status"
          :options="statusOptions"
          placeholder="Status"
        />

        <Button
          :label="
            editingUserId
              ? 'Update'
              : 'Save'
          "
          icon="pi pi-check"
          @click="saveUser"
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