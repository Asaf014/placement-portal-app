<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-body p-5">
            <h1 class="card-title mb-4">My Profile</h1>
            <div v-if="user">
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" :value="user.email" disabled>
              </div>
              <div class="mb-3">
                <label class="form-label">Role</label>
                <input type="text" class="form-control" :value="getRoleDisplay(user.role)" disabled>
              </div>
              <div class="mb-3">
                <label class="form-label">Account Status</label>
                <span class="badge" :class="user.is_active ? 'bg-success' : 'bg-danger'">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </div>
              <button @click="logout" class="btn btn-danger">Logout</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      user: null
    }
  },
  mounted() {
    this.loadUser()
  },
  methods: {
    loadUser() {
      this.user = {
        email: localStorage.getItem('email'),
        role: localStorage.getItem('role'),
        is_active: true
      }
    },
    getRoleDisplay(role) {
      const roles = {
        admin: 'Administrator',
        company: 'Company',
        student: 'Student'
      }
      return roles[role] || role
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>
