<script setup>

import AppHeader from "@/components/Header.vue"
import AppFooter from "@/components/Footer.vue"
import AppUsers from "@/components/Users.vue"
import AppRoles from "@/components/Roles.vue"
import { provide, ref } from "vue";

provide("roles", ref([]))

</script>

<template>
    <div class="layout-wrapper">
        <app-header></app-header>
        <div class="layout-main-container">
            <div class="layout-main">
                <app-users></app-users>
                <div></div>
                <app-roles></app-roles>
            </div>
            <app-footer></app-footer>
        </div>
        <div class="layout-mask animate-fadein"></div>
    </div>
    <Toast />
</template>
