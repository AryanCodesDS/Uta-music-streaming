<template>
  <div class="section">
    <nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
      <div class="container-fluid">
        <a
          class="navbar-brand d-flex align-items-center justify-content-center"
          href="/"
        >
          <img
            src="../assets/music-note-beamed.svg"
            alt="uta"
            width="30"
            height="20"
          />
          UTA
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarText"
          aria-controls="navbarText"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarText">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/" :class="getActiveNavLink('/')"
                >Home</router-link
              >
            </li>
            <li class="nav-item">
              <router-link to="/about" :class="getActiveNavLink('/about')"
                >About</router-link
              >
            </li>
          </ul>
          <span>
            <button
              type="button"
              class="btn btn-secondary d-flex align-items-center justify-content-center"
              style="--bs-btn-font-size: 0.75rem; text-align: center"
            >
              <img
                src="../assets/Admin.svg"
                alt="Bootstrap"
                style="margin-right: 0.2em"
                width="11"
                height="12"
              /><router-link to="/admin-login" class="nav-link"
                >| Admin Login</router-link
              >
            </button>
          </span>
        </div>
      </div>
    </nav>
    <div style="margin-top: 5em">
      <div class="h-100 d-flex align-items-center justify-content-center">
        <h1 class="display-1" style="color:violet">Welcome to UTA🧑‍🎤</h1>
      </div>
      <div class="h-100 d-flex align-items-center justify-content-center">
        <p class="lead" style="color: white">
          The best place to find your favorite music
        </p>
      </div>
    </div>
    <div style="margin-top: 3em" class="d-flex align-items-center justify-content-center">
      <div class="row">
        <div class="col px-md-5">
          <button type="button" class="btn btn-outline-light btn-lg ml-2 px-5">
            <router-link to="/user-login" class="nav-link">Login</router-link>
          </button>
        </div>
        <div class="col px-md-5">
          <button type="button" class="btn btn-outline-light btn-lg ml-2 px-5">
            <router-link to="/user-signup" class="nav-link">Signup</router-link>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sactive: "",
    };
  },

methods: {
    getActiveNavLink(link) {
      return this.$route.path === link ? "nav-link active" : "nav-link";
    },
},
};
</script>
<style scoped>
.section {
  background-image: url("../assets/banner1.png");
  background-size: cover;
  height: 100vh;
}
</style>
