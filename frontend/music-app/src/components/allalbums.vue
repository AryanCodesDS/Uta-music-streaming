<script setup>
import Navbar from './Navbar.vue'
import { useStore } from 'vuex'
const store = useStore()
const username = store.state.username
const roles = store.state.roles
</script>

<template>
  <div class="mb-3">
    <Navbar :roles="roles" :username = "username" />
  </div>
<div>
  hello
</div>
</template>