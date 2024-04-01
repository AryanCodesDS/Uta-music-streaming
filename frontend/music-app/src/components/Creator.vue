<template>
  <div class="mb-3">
    <Navbar :roles="roles" :username="username" />
  </div>

</template>
<script setup>
import Navbar from './Navbar.vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
const store = useStore()
const router = useRouter()
const username = store.state.username
const roles = store.state.roles
</script>