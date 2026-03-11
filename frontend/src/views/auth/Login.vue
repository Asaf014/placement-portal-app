<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body p-5">
            <h1 class="card-title text-center mb-4">Login</h1>
            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" v-model="form.email" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="form.password" required>
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Logging in...' : 'Login' }}
              </button>
            </form>
            <p class="text-center mt-3">
              New user? <router-link to="/register">Register here</router-link>
            </p>
            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      loading: false,
      error: ''
    }
  },
  methods: {
    async login() {
      this.error = ''
      this.loading = true
      try {
        const response = await api.post('/auth/login', this.form)
        const { token, user_id, email, role } = response.data
        
        localStorage.setItem('token', token)
        localStorage.setItem('user_id', user_id)
        localStorage.setItem('email', email)
        localStorage.setItem('role', role)
        
        this.$router.push(`/${role}/dashboard`)
      } catch (error) {
        this.error = error.response?.data?.error || 'Login failed'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
