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
          <span class="navbar-text">
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
    <div class="container">
        <h1 class="mt-4 mb-3" style="color:violet;">About UTA</h1>
        <p class="lead" style="color:whitesmoke;">UTA is a multi-user music application developed by Aryan Tiwari. It's designed with the love of music in mind, and it's built to bring people together through shared musical experiences.</p>

        <h2 class="mt-4 mb-3" style="color:violet;">Features</h2>
        <ul class="list-group">
            <li class="list-group-item"><strong>Make Playlists:</strong> Users can create their own playlists, curating their favorite songs in one place.</li>
            <li class="list-group-item"><strong>Read Lyrics:</strong> Enjoy music on a deeper level by reading the lyrics while listening to your favorite songs.</li>
            <li class="list-group-item"><strong>Upload Songs:</strong> Creators can share their music with the world by uploading their songs directly to the platform.</li>
            <li class="list-group-item"><strong>Edit Songs:</strong> Creators have the power to edit their songs after uploading, ensuring their music is always presented exactly how they want it to be.</li>
        </ul>

        <h2 class="mt-4 mb-3" style="color:violet;">Our Mission</h2>
        <p class="lead" style="color:whitesmoke;">Our mission at UTA is to create a space where music lovers can come together to discover, share, and enjoy music. Whether you're a creator or a listener, UTA is the place for you.</p>
        <p class="lead" style="color:whitesmoke;">Join us today and start your musical journey with UTA!</p>
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
  background-repeat: no-repeat;
  height: 100rem;
  widows: 100%;
}
</style>
