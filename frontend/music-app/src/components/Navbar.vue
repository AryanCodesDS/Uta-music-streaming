<script setup>
function getActiveNavLink(link) {
  return this.$route.path === link ? "nav-link active" : "nav-link";
}

import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const props = defineProps({ 'roles': Array, 'username': String })
const store = useStore()
const searchAttr = ref('')
const emit = defineEmits(['searchAttribute'])
const route = useRoute()
const currentroute = route.name

console.log(currentroute)
const searchSA = () => {
  emit('searchAttribute', searchAttr.value)
}

const user = {
  username: store.state.username
}

console.log(user)
const signupc = async () => {
  const res = await fetch('http://127.0.0.1:5000/signup-creator', {
    mode: "cors",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });
  let data = await res.json();
  if (res.ok) {
    alert("You are now a creator,Please Login Again to continue as a creator")
    logout()
    router.push('/')
  }
  else {
    console.log("Error")
  }
}

function logout() {
  localStorage.setItem('authtoken', "null");
  store.commit('setUsername', null);
  store.commit('setRoles', []);
  store.dispatch('logoutUser');
  localStorage.removeItem('vuex');
}
</script>

<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">
          <img src="../assets/music-note-beamed.svg" alt="Bootstrap" width="30" height="24">
          UTA
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a v-if="currentroute == 'admindash'" class="nav-link active" aria-current="page"
                href="/admin-dashboard">Dashboard</a>
                <a v-else-if="currentroute == 'profile' && props.roles.includes('Admin')" class="nav-link active" aria-current="page"
                href="/admin-dashboard">Dashboard</a>
              <a v-else class="nav-link active" aria-current="page" href="/all-songs">Home</a>
            </li>

            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="/" @click="logout">Logout</a>
            </li>
          </ul>
          <ul class="navbar-nav mb-2 mb-lg-0">
            <li v-if="currentroute == 'admindash' || currentroute == 'creator'" class="nav-item dropstart">
              <a href="#" class="nav-link dropdown-toggle rounded-circle" role="button" data-bs-toggle="dropdown"
                aria-expanded="false"><img src="../assets/person.jpg" alt="Profile" width="30px" height="30px"
                  class="rounded-circle"></a>
              <ul class="dropdown-menu">
                <li class="dropdown-header">
                  <p>Welcome {{ username }}</p>
                </li>
                <li><router-link class="dropdown-item p-2" to="/profile">My Profile</router-link></li>
                <li class="dropdown-item p-2" @click="signupc"
                  v-if="props.roles.includes('General') && !props.roles.includes('Creator')">Sign up as Creator</li>
                <li><router-link class="dropdown-item p-2" to="/creator" v-if="props.roles.includes('Creator')">Creator
                    Dashboard</router-link></li>
              </ul>
            </li>
            <li v-else-if="currentroute != 'profile'" class="nav-item dropdown">
              <a href="#" class="nav-link dropdown-toggle rounded-circle" role="button" data-bs-toggle="dropdown"
                aria-expanded="false"><img src="../assets/person.jpg" alt="Profile" width="30px" height="30px"
                  class="rounded-circle"></a>
              <ul class="dropdown-menu">
                <li class="dropdown-header">
                  <p>Welcome {{ username }}</p>
                </li>
                <li><router-link class="dropdown-item p-2" to="/profile">My Profile</router-link></li>
                <li class="dropdown-item p-2" @click="signupc"
                  v-if="props.roles.includes('General') && !props.roles.includes('Creator')">Sign up as Creator</li>
                <li><router-link class="dropdown-item p-2" to="/creator" v-if="props.roles.includes('Creator')">Creator
                    Dashboard</router-link></li>
              </ul>
            </li>
          </ul>
          <form class="d-flex" v-if="currentroute == 'songs'" role="search" @submit.prevent="searchSA">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"
              v-model="searchAttr">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
        </div>
      </div>
    </nav>
  </div>
</template>