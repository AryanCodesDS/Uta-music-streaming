<script>
export default {
  data() {
    return {
      sactive: "",
      showPassword: false,
      user: {
        name: null,
        username: null,
        email: null,
        msg: [],
        password: null,
        repassword: null,
      },
    };
  },
  watch: {
    "user.username": function (value) {
      this.user.username = value;
      if (value.length < 8) {
        this.user.msg["username"] = "*Must be 8 characters!";
      } else if (value.length >= 8) {
        this.validateUsername(value);
      } else {
        this.user.msg["username"] = "";
      }
    },
    "user.email": function (value) {
      this.user.email = value;
      this.validateEmail(value);
    },
    "user.password": function () {
      if (this.user.password !== this.user.repassword) {
        this.user.msg["repassword"] = "*Passwords do not match";
      } else {
        this.user.msg["repassword"] = "";
      }
    },
    "user.repassword":
      function () {
        if (this.user.password !== this.user.repassword) {
          this.user.msg["repassword"] = "*Passwords do not match";
        } else {
          this.user.msg["repassword"] = "";
        }
      },
  },
  methods: {
    validateUsername(value) {
      let pattern = /^[A-Za-z0-9_@\.]+$/;
      if (pattern.test(value)) {
        this.user.msg["username"] = "";
      } else {
        this.user.msg["username"] = "*Invalid Username";
      }
    },
    validateEmail(value) {
      if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(value)) {
        this.user.msg["email"] = "";
      } else {
        this.user.msg["email"] = "*Invalid Email Address";
      }
    },
    getActiveNavLink(link) {
      return this.$route.path === link ? "nav-link active" : "nav-link";
    },
    async createAccount() {
      if (this.user.password !== this.user.repassword) {
        return;
      } else {
        let result = await fetch("http://127.0.0.1:5000/user-signup", {
          mode: "cors",
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.user),
        });
        let data = await result.json();
        if (result.ok) {
          alert("Account Created Successfully!Please login to continue");
          this.$router.push({ name: "userlogin" });
        } else {
          alert(data.error);
        }
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
    <div style="height:100vh;">
    <div class="d-flex justify-content-center align-items-center flex-column w-100 bg-info-subtle p-5">
      <form>
        <div class="p-4 w-40 m-auto bg-white form-group">
          <div class="mb-3">
            <p class="display-6">Sign Up</p>
            <p class="text-muted">
              Create an account and dive into the world of Music🎧
            </p>
          </div>
          <div class="mb-3">
            <label for="musicInputname" class="form-label">Name</label>
            <input type="text" class="form-control input-lg" aria-label="Name" id="musicInputname" v-model="user.name" autocapitalize="on"
              aria-describedby="basic-addon1" placeholder="Your Full Name" />
          </div>
          <div class="mb-3 d-flex flex-column">
            <label for="musicInputUsername" class="form-label">Username</label>
            <div class="d-flex flex-row">
              <div class="input-group-prepend">
                <span class="input-group-text" id="basic-addon1">#</span>
              </div>
              <input type="text" class="form-control" aria-label="Username" id="musicInputUsername"
                v-model="user.username" aria-describedby="basic-addon1" minlength="8" placeholder="User@123"
                autocomplete="name"
                title="Must contain at least one  number and one uppercase and lowercase letter, and at least 8 or more characters" />
            </div>
            <span v-if="user.msg.username"><small style="color: red; font-size: 0.7em">{{
                user.msg.username
              }}</small></span>
          </div>
          <div class="mb-3">
            <label for="musicInputEmail" class="form-label">Email address</label>
            <div class="d-flex flex-row">
              <div class="input-group-prepend">
                <span class="input-group-text" id="basic-addon1">@</span>
              </div>
              <input type="email" class="form-control input-lg" id="musicInputEmail" aria-describedby="emailHelp"
                placeholder="name@example.com" v-model="user.email" autocomplete="email" />
            </div>
            <span v-if="user.msg.email"><small style="color: red; font-size: 0.7em">{{
                user.msg.email
              }}</small></span>
          </div>
          <div class="mb-3">
            <label for="musicInputPassword" class="form-label">Password</label>
            <div class="d-flex flex-row">
              <input :type="showPassword ? 'text' : 'password'" class="form-control input-lg" id="musicInputPassword"
                v-model="user.password" autocomplete="current-password" />
              <button style="margin-left: 0.5em" class="btn btn-outline-secondary" type="button"
                @click="showPassword = !showPassword">
                <img src="../assets/eye.svg" />
              </button>
            </div>
            <label for="musicInputrePassword" class="form-label">Re-enter Password</label>
            <div class="d-flex flex-row">
              <input type="text" class="form-control input-lg" id="musicInputrePassword" v-model="user.repassword"
                autocomplete="current-password" />
            </div>
            <span v-if="user.msg.repassword"><small style="color: red; font-size: 0.7em">{{
                user.msg.repassword
              }}</small></span>
          </div>
          <span class="d-flex justify-content-center align-items-center flex-column">
            <button type="submit" @click.prevent="createAccount" class="btn btn-primary">
              Signup
            </button>
            <p class="mt-3">
              Already have an account?<router-link to="/user-login">Login</router-link>
            </p>
          </span>
        </div>
      </form>
    </div>
  </div>
  </div>
</template>

<style scoped></style>
