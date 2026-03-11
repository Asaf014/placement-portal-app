<template>
  <div id="app" class="d-flex flex-column min-vh-100">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand fw-bold">Placement Portal</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/login" class="nav-link" @click="collapseNavbar">Login</router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/register" class="nav-link" @click="collapseNavbar">Register</router-link>
            </li>
            <li class="nav-item dropdown" v-if="isLoggedIn">
              <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown">{{ userEmail }}</a>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><router-link to="/profile" class="dropdown-item" @click="collapseNavbar">Profile</router-link></li>
                <li><hr class="dropdown-divider"></li>
                <li><a href="#" @click.prevent="logout" class="dropdown-item text-danger">Logout</a></li>
              </ul>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <button @click="logout" class="btn btn-sm btn-outline-light ms-2">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="flex-grow-1">
      <router-view></router-view>
    </div>

    <footer class="bg-dark text-white text-center py-3 mt-5">
      <p class="mb-0">Placement Portal Application &copy; 2026</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      userEmail: '',
      userRole: ''
    }
  },
  mounted() {
    this.checkAuth()
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('token')
      if (token) {
        this.isLoggedIn = true
        this.userEmail = localStorage.getItem('email')
        this.userRole = localStorage.getItem('role')
      }
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('email')
      localStorage.removeItem('role')
      localStorage.removeItem('user_id')
      this.isLoggedIn = false
      this.collapseNavbar()
      this.$router.push('/login')
    },
    collapseNavbar() {
      const navbarCollapse = document.getElementById('navbarNav')
      if (navbarCollapse && navbarCollapse.classList.contains('show')) {
        navbarCollapse.classList.remove('show')
      }
    }
  },
  watch: {
    '$route'() {
      this.checkAuth()
      this.collapseNavbar()
    }
  }
}
</script>

<style scoped>
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>
