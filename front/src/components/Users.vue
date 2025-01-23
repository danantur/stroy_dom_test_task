<script setup>
import { Service } from '@/service/Service';
import { validateEmail, findIndexById } from '@/service/Utils';
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { ref, onMounted, inject } from 'vue';

let userService = new Service("users")

onMounted(() => {
    userService.getAll().then((data) => {
        users.value = data.data
    });
});

const toast = useToast();
const dt = ref();
const users = ref();
const userDialog = ref(false);
const deleteUserDialog = ref(false);
const deleteUsersDialog = ref(false);
const user = ref({});
const selectedUsers = ref();
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);

function openNew() {
    user.value = {};
    submitted.value = false;
    userDialog.value = true;
}

function hideDialog() {
    userDialog.value = false;
    submitted.value = false;
}

function saveUser() {
    submitted.value = true;

    if (user?.value.name?.trim() && user?.value.surname?.trim()
            && user?.value.email?.trim()) {

        if (!validateEmail(user.value.email)) return

        if (user.value.id) {

            userService.update(user.value).then(() => {
                users.value[findIndexById(users.value, user.value.id)] = user.value;
                toast.add({ severity: 'success', summary: 'Successful', detail: 'Пользователь обновлён', life: 3000 });

                userDialog.value = false;
                user.value = {};
            })
        
        } else {

            userService.add(user.value).then((data) => {
                users.value.push(
                    {
                        id: data.data.id,
                        name: user.value.name,
                        surname: user.value.surname,
                        email: user.value.email
                    }
                );
                toast.add({ severity: 'success', summary: 'Successful', detail: 'Пользователь создан', life: 3000 });

                userDialog.value = false;
                user.value = {};
            })
        
        }
    }
}

function editUser(prod) {
    console.log({ ...prod })
    user.value = { ...prod };
    userDialog.value = true;
}

function confirmDeleteUser(prod) {
    user.value = prod;
    deleteUserDialog.value = true;
}

function deleteUser() {
    userService.delete(user.value.id).then(() => {
        users.value = users.value.filter((val) => val.id !== user.value.id);
        deleteUserDialog.value = false;
        user.value = {};
        toast.add({ severity: 'success', summary: 'Successful', detail: 'user Deleted', life: 3000 });
    });
}

function exportCSV() {
    dt.value.exportCSV();
}

function confirmDeleteSelected() {
    deleteUsersDialog.value = true;
}

function deleteSelectedUsers() {
    userService.deleteMany(selectedUsers.value).then(() => {
        users.value = users.value.filter((val) => !selectedUsers.value.includes(val));
        deleteUsersDialog.value = false;
        selectedUsers.value = null;
        toast.add({ severity: 'success', summary: 'Successful', detail: 'Users Deleted', life: 3000 });
    })
}

</script>

<template>
        <div class="card">
            <Toolbar class="mb-6">
                <template #start>
                    <Button label="Создать" icon="pi pi-plus" severity="secondary" class="mr-2" @click="openNew" />
                    <Button label="Удалить" icon="pi pi-trash" severity="secondary" @click="confirmDeleteSelected" :disabled="!selectedUsers || !selectedUsers.length" />
                </template>

                <template #end>
                    <Button label="Экспорт" icon="pi pi-upload" severity="secondary" @click="exportCSV($event)" />
                </template>
            </Toolbar>

            <DataTable
                ref="dt"
                v-model:selection="selectedUsers"
                :value="users"
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
                        <h4 class="m-0">Управление пользователями</h4>
                        <IconField>
                            <InputIcon>
                                <i class="pi pi-search" />
                            </InputIcon>
                            <InputText v-model="filters['global'].value" placeholder="Поиск..." />
                        </IconField>
                    </div>
                </template>

                <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
                
                <Column field="name" header="Имя" sortable style="min-width: 16rem"></Column>
                <Column field="surname" header="Фамилия" sortable style="min-width: 10rem"></Column>
                <Column field="email" header="E-mail" sortable style="min-width: 10rem"></Column>
                
                <Column :exportable="false" style="min-width: 12rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editUser(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteUser(slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>

        <Dialog v-model:visible="userDialog" :style="{ width: '450px' }" header="Данные пользователя" :modal="true">
            <div class="flex flex-col gap-6">

                <div>
                    <label for="name" class="block font-bold mb-3">Имя</label>
                    <InputText id="name" v-model.trim="user.name" required="true" autofocus :invalid="submitted && !user.name" fluid />
                    <small v-if="submitted && !user.name" class="text-red-500">Имя обязательно.</small>
                </div>
                <div>
                    <label for="surname" class="block font-bold mb-3">Фамилия</label>
                    <InputText id="surname" v-model="user.surname" required="true" rows="3" cols="20" :invalid="submitted && !user.surname" fluid />
                    <small v-if="submitted && !user.surname" class="text-red-500">Фамилия обязательна.</small>
                </div>
                <div>
                    <label for="email" class="block font-bold mb-3">E-mail</label>
                    <InputText id="email" v-model="user.email" required="true" :invalid="submitted && !user.email" fluid />
                    <small v-if="submitted && !user.email" class="text-red-500">E-mail обязателен.<br></small>
                    <small v-else-if="submitted && !validateEmail(user.email)" class="text-red-500">Некорректный E-mail.</small>
                </div>
            </div>

            <template #footer>
                <Button label="Отмена" icon="pi pi-times" text @click="hideDialog" />
                <Button label="Сохранить" icon="pi pi-check" @click="saveUser" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteUserDialog" :style="{ width: '450px' }" header="Подтверждение" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="user"
                    >Вы уверены, что хотите удалить пользователя <b>{{ user.name }}</b
                    >?</span
                >
            </div>
            <template #footer>
                <Button label="Нет" icon="pi pi-times" text @click="deleteUserDialog = false" />
                <Button label="Да" icon="pi pi-check" @click="deleteUser" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteUsersDialog" :style="{ width: '450px' }" header="Подтверждение" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="user">Вы уверены, что хотите удалить выбранных пользователей?</span>
            </div>
            <template #footer>
                <Button label="Нет" icon="pi pi-times" text @click="deleteUsersDialog = false" />
                <Button label="Да" icon="pi pi-check" text @click="deleteSelectedUsers" />
            </template>
        </Dialog>
</template>
