<script>
export default {
  data() {
    return {
      sactive: "",
      showPassword: false,
      user: {
        email: null,
        password: null,
      },
    };
  },

  methods: {
    getActiveNavLink(link) {
      return this.$route.path === link ? "nav-link active" : "nav-link";
    },
    async getAuthToken() {
      let result = await fetch("http://127.0.0.1:5000/admin-login", {
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
        localStorage.setItem("authtoken", data.authtoken);
        this.$router.push({ name: "admindash" });
      } else {
        console.log("failed");
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
              <router-link to="/admin-login" :class="getActiveNavLink('/admin-login')">Admin Login</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="d-flex justify-content-center align-items-center flex-column w-100 vh-100 bg-success-subtle">
      <form class="d-flex justify-content-center align-items-center flex-column 40-w p-5 bg-white form-group">
        <div class="mb-3">
          <p class="display-6">Admin🔏</p>
        </div>
        <div class="mb-3">
          <label for="musicInputEmail" class="form-label">Email address</label>
          <input type="email" class="form-control input-lg" id="musicInputEmail" aria-describedby="emailHelp"
            v-model="user.email" autocomplete="email" />
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
        <p>Not an Admin? <a href="/user-login" class="mt-3">Login</a> as User.</p>
      </form>
    </div>
  </div>
</template>
<style scoped></style>
