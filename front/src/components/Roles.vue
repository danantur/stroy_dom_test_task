<script setup>
import { Service } from '@/service/Service';
import { findIndexById } from '@/service/Utils';
import { FilterMatchMode } from '@primevue/core/api';
import { Accordion } from 'primevue';
import { useToast } from 'primevue/usetoast';
import { ref, onMounted, provide, computed, inject } from 'vue';

let roleService = new Service("roles")

onMounted(() => {
    roleService.getAll().then((data) => {
        roles.value = data.data
    });
});

const roles = ref([])

const toast = useToast();
const dt = ref();
const roleDialog = ref(false);
const deleteRoleDialog = ref(false);
const deleteRolesDialog = ref(false);
const role = ref({});
const selectedRoles = ref();
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);

function openNew() {
    role.value = {};
    submitted.value = false;
    roleDialog.value = true;
}

function hideDialog() {
    roleDialog.value = false;
    submitted.value = false;
}

function saveRole() {
    submitted.value = true;

    if (role?.value.name?.trim() && role?.value.description?.trim()) {

        if (role.value.id) {

            roleService.update(role.value).then(() => {
                roles.value[findIndexById(roles.value, role.value.id)] = role.value;
                toast.add({ severity: 'success', summary: 'Successful', detail: 'Пользователь обновлён', life: 3000 });

                roleDialog.value = false;
                role.value = {};
            })
        
        } else {

            roleService.add(role.value).then((data) => {
                roles.value.push(
                    {
                        id: data.data.id,
                        name: role.value.name,
                        description: role.value.description
                    }
                );
                toast.add({ severity: 'success', summary: 'Successful', detail: 'Пользователь создан', life: 3000 });

                roleDialog.value = false;
                role.value = {};
            })
        
        }
    }
}

function editRole(prod) {
    role.value = { ...prod };
    roleDialog.value = true;
}

function confirmDeleteRole(prod) {
    role.value = prod;
    deleteRoleDialog.value = true;
}

function deleteRole() {
    roleService.delete(role.value.id).then(() => {
        roles.value = roles.value.filter((val) => val.id !== role.value.id);
        deleteRoleDialog.value = false;
        role.value = {};
        toast.add({ severity: 'success', summary: 'Successful', detail: 'role Deleted', life: 3000 });
    });
}

function exportCSV() {
    dt.value.exportCSV();
}

function confirmDeleteSelected() {
    deleteRolesDialog.value = true;
}

function deleteSelectedRoles() {
    roleService.deleteMany(selectedRoles.value).then(() => {
        roles.value = roles.value.filter((val) => !selectedRoles.value.includes(val));
        deleteRolesDialog.value = false;
        selectedRoles.value = null;
        toast.add({ severity: 'success', summary: 'Successful', detail: 'Roles Deleted', life: 3000 });
    })
}

</script>

<template>
        <div class="card">
            <Toolbar class="mb-6">
                <template #start>
                    <Button label="Создать" icon="pi pi-plus" severity="secondary" class="mr-2" @click="openNew" />
                    <Button label="Удалить" icon="pi pi-trash" severity="secondary" @click="confirmDeleteSelected" :disabled="!selectedRoles || !selectedRoles.length" />
                </template>

                <template #end>
                    <Button label="Экспорт" icon="pi pi-upload" severity="secondary" @click="exportCSV($event)" />
                </template>
            </Toolbar>

            <DataTable
                ref="dt"
                v-model:selection="selectedRoles"
                :value="roles"
                dataKey="id"
                :paginator="true"
                :rows="10"
                :filters="filters"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5, 10, 25]"
                currentPageReportTemplate="Показано {first} к {last} от {totalRecords} пользователей"
            >
                <template #header>
                    <div class="flex flex-wrap gap-2 items-center justify-between">
                        <h4 class="m-0">Управление ролями</h4>
                        <IconField>
                            <InputIcon>
                                <i class="pi pi-search" />
                            </InputIcon>
                            <InputText v-model="filters['global'].value" placeholder="Поиск..." />
                        </IconField>
                    </div>
                </template>

                <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
                
                <Column field="name" header="Роль" sortable style="min-width: 16rem"></Column>
                <Column field="description" header="Описание" sortable style="min-width: 10rem"></Column>
                
                <Column :exportable="false" style="min-width: 12rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editRole(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteRole(slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>

        <Dialog v-model:visible="roleDialog" :style="{ width: '450px' }" header="Данные Роли" :modal="true">
            <div class="flex flex-col gap-6">

                <div>
                    <label for="name" class="block font-bold mb-3">Название</label>
                    <InputText id="name" v-model.trim="role.name" required="true" autofocus :invalid="submitted && !role.name" fluid />
                    <small v-if="submitted && !role.name" class="text-red-500">Название обязательно.</small>
                </div>
                <div>
                    <label for="description" class="block font-bold mb-3">Описание</label>
                    <Textarea id="description" v-model="role.description" required="true" rows="3" cols="20" :invalid="submitted && !role.description" fluid />
                    <small v-if="submitted && !role.description" class="text-red-500">Описание обязательно.</small>
                </div>
            </div>

            <template #footer>
                <Button label="Отмена" icon="pi pi-times" text @click="hideDialog" />
                <Button label="Сохранить" icon="pi pi-check" @click="saveRole" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteRoleDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="role"
                    >Вы уверены, что хотите удалить роль <b>{{ role.name }}</b
                    >?</span
                >
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteRoleDialog = false" />
                <Button label="Yes" icon="pi pi-check" @click="deleteRole" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteRolesDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="role">Вы уверены, что хотите удалить выбранные роли?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteRolesDialog = false" />
                <Button label="Yes" icon="pi pi-check" text @click="deleteSelectedRoles" />
            </template>
        </Dialog>
</template>
