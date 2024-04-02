<script setup>
function getActiveNavLink(link) {
  return this.$route.path === link ? "nav-link active" : "nav-link";
}
import { defineProps } from 'vue'
import { useStore } from 'vuex'
import {useRouter} from 'vue-router'
const router = useRouter()
const props = defineProps({'roles':Array, 'username':String})
const store = useStore()
const user = {
    username: toString(store.state.username)
}
async function signupc(){
    const res = await fetch('http://127.0.0.1:5000/signup-creator', {
        method: 'POST',
        mode: "cors",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(user),
      });
      let data = await res.json();
    if(res.ok){
        router.push({name : 'creator'})
    }
    else{
        console.log("Error")
    }
}

function logout(){
  localStorage.setItem('authtoken',"null");
  store.commit('setUsername', null);
  store.commit('setRoles', []);
  store.dispatch('logoutUser');
  localStorage.removeItem('vuex');
}
</script>

<template>
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
            <a class="nav-link active" aria-current="page" href="/all-songs">Home</a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Library
            </a>
            <ul class="dropdown-menu">
              <li><router-link class="dropdown-item" to="/all-albums">Albums</router-link></li>
              <li><router-link class="dropdown-item" to="/my-playlists">My Playlists</router-link></li>
            </ul>
          </li>
          <li class="nav-item">
            <a class="nav-link" aria-current="page" href="/" @click ="logout">Logout</a>
          </li>
        </ul>
        <ul class="navbar-nav mb-2 mb-lg-0">
        <li class="nav-item dropdown">
            <a href="#" class="nav-link dropdown-toggle rounded-circle" role="button" data-bs-toggle="dropdown" aria-expanded="false"><img src="../assets/person.jpg" alt="Profile" width="30px" height="30px"
              class="rounded-circle"></a>
            <ul class="dropdown-menu">
              
              <li class="dropdown-item p-2 disabled"><p>Welcome {{username}}</p></li>
              <li><router-link class="dropdown-item p-2" to="/profile">My Profile</router-link></li>
              <li><router-link class="dropdown-item p-2" @click.prevent="signupc" to="/creator" v-if="props.roles.includes('General') && !props.roles.includes('Creator')">Sign up as Creator</router-link></li>
              <li><router-link class="dropdown-item p-2" to="/creator" v-if="props.roles.includes('Creator')">Creator Dashboard</router-link></li>

            </ul>
          </li>
            </ul>
        <form class="d-flex" role="search">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
      </div>
    </div>
  </nav>
</template>