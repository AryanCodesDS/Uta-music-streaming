<script>
import { useStore } from 'vuex'; // Import useStore hook
export default {
  data() {
    return {
      sactive: "",
      showPassword: false,
      user: {
        email: null,
        username:null,
        password: null,
      },
    };
  },

  methods: {
    getActiveNavLink(link) {
      return this.$route.path === link ? "nav-link active" : "nav-link";
    },
    async getAuthToken() {
      let result = await fetch("http://127.0.0.1:5000/user-login", {
        mode: "cors",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.user),
      });
      let data = await result.json();
      if (result.ok) {
        console.log("yes");
        this.$store.commit("setUsername", data.uname);
        this.$store.commit("setRoles", data.roles);
        localStorage.setItem("authtoken", data.authtoken);
        this.$router.push({ name: "songs"});
      } else {
        alert("failed");
      }
    },
  },
};
</script>

<template>
  <div class="section">
    <nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
      <div class="container-fluid">
        <a class="navbar-brand d-flex align-items-center justify-content-center" href="/">
          <img src="../assets/music-note-beamed.svg" alt="uta" width="30" height="20" />
          UTA
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText"
          aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarText">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/" :class="getActiveNavLink('/')">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/about" :class="getActiveNavLink('/about')">About</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user-login" :class="getActiveNavLink('/user-login')">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user-signup" :class="getActiveNavLink('/user-signup')">Signup</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="d-flex justify-content-center align-items-center flex-column w-100 vh-100 bg-success-subtle">
      <form class="d-flex justify-content-center align-items-center flex-column 40-w p-5 bg-white">
        <div class="mb-3">
          <p class="display-6">Sign in</p>
        </div>
        <div class="mb-3">
          <label for="musicInputEmailuname" class="form-label">Email address</label>
          <input type="text" class="form-control input-lg" id="musicInputEmailuname" aria-describedby="emailHelp"
            v-model="user.email" autocomplete="email" />
          <div id="emailHelp" class="form-text">
            We'll never share your email with anyone else.
          </div>
        </div>
        <div class="mb-3">
          <label for="musicInputPassword" class="form-label">Password</label>
          <div class="d-flex flex-row">
            <input :type="showPassword ? 'text' : 'password'" class="form-control input-lg" id="musicInputPassword"
              v-model="user.password" autocomplete="current-password" />
            <button style="margin-left: 1em" class="btn btn-outline-secondary" type="button"
              @click="showPassword = !showPassword">
              <img src="../assets/eye.svg" />
            </button>
          </div>
        </div>
        <button type="submit" @click.prevent="getAuthToken" class="btn btn-primary mb-3">
          Login
        </button>
        <p>Don't have an account?<a href="/user-signup" class="mt-3">Signup</a></p>
      </form>
    </div>
  </div>
</template>
<style scoped></style>
