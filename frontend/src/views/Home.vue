<template>
  <div class="container mt-5">
    <div class="row text-center">
      <div class="col-md-12">
        <h1 class="display-4 fw-bold">Placement Portal</h1>
        <p class="lead">Connecting Students with Opportunities</p>
        <div class="mt-5">
          <div class="row">
            <div class="col-md-4 mb-4" v-if="!isLoggedIn">
              <div class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">Student</h5>
                  <p class="card-text">Apply to placement drives and track your applications</p>
                  <router-link to="/register" class="btn btn-primary">Register as Student</router-link>
                </div>
              </div>
            </div>
            <div class="col-md-4 mb-4" v-if="!isLoggedIn">
              <div class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">Company</h5>
                  <p class="card-text">Create placement drives and recruit talented students</p>
                  <router-link to="/register" class="btn btn-primary">Register as Company</router-link>
                </div>
              </div>
            </div>
            <div class="col-md-4 mb-4" v-if="!isLoggedIn">
              <div class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">Admin</h5>
                  <p class="card-text">Manage the entire placement ecosystem</p>
                  <router-link to="/login" class="btn btn-primary">Admin Login</router-link>
                </div>
              </div>
            </div>
          </div>
          <div v-if="!isLoggedIn" class="mt-5">
            <router-link to="/login" class="btn btn-lg btn-success">Get Started</router-link>
          </div>
          <div v-else class="mt-5">
            <router-link :to="`/${userRole}/dashboard`" class="btn btn-lg btn-success">Go to Dashboard</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      isLoggedIn: false,
      userRole: ''
    }
  },
  mounted() {
    const token = localStorage.getItem('token')
    if (token) {
      this.isLoggedIn = true
      this.userRole = localStorage.getItem('role')
    }
  }
}
</script>
