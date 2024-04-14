<script setup>
  import { onMounted, ref } from 'vue';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  import Navbar from './Navbar.vue';
  
  const store = useStore();
  const router = useRouter();
  
  const username = store.state.username;
  const roles = store.state.roles;
  const profdet = ref({});
  
  const getProfile = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/profile/${username}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('authtoken')
        }
      });
      const data = await response.json();
      profdet.value = data;
    } catch (error) {
      console.error(error);
    }
  };
  
  onMounted(() => {
    getProfile();
  });
  </script>
  


<template>
    <div>
      <Navbar :roles="roles" :username="username" />
    </div>
    <div class="container mt-5">
      <div class="row">
        <div class="col-md-6 offset-md-3">
          <div class="card">
            <div class="card-body p-5">
              <h1 class="card-title text-center mb-4">User Profile</h1>
              <div class="mb-3">
                <p class="fw-bold">Full Name:</p>
                <p>{{ profdet.Name }}</p>
              </div>
              <div class="mb-3">
                <p class="fw-bold">Username:</p>
                <p>{{ username }}</p>
              </div>
              <div class="mb-3">
                <p class="fw-bold">Email:</p>
                <p>{{ profdet.email }}</p>
              </div>
              <div class="mb-3">
                <p class="fw-bold">Roles:</p>
                <p>{{ roles }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  