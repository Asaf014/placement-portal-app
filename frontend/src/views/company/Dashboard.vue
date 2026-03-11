<template>
  <div class="container mt-5">
    <h1 class="mb-4">Company Dashboard</h1>
    
    <div class="row">
      <div class="col-md-3 mb-4">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h5 class="card-title">Total Drives</h5>
            <p class="display-4">{{ dashboard.total_drives }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-4">
        <div class="card bg-success text-white">
          <div class="card-body">
            <h5 class="card-title">Total Applications</h5>
            <p class="display-4">{{ dashboard.total_applications }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-4">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5 class="card-title">Shortlisted</h5>
            <p class="display-4">{{ dashboard.total_shortlisted }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-4">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <h5 class="card-title">Selected</h5>
            <p class="display-4">{{ dashboard.total_selected }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-5">
      <div class="col-md-6">
        <router-link to="/company/profile" class="btn btn-primary btn-lg w-100 mb-3">
          Edit Profile
        </router-link>
      </div>
      <div class="col-md-6">
        <router-link to="/company/drives" class="btn btn-success btn-lg w-100 mb-3">
          Manage Drives
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'CompanyDashboard',
  data() {
    return {
      dashboard: {
        total_drives: 0,
        total_applications: 0,
        total_shortlisted: 0,
        total_selected: 0
      }
    }
  },
  mounted() {
    this.loadDashboard()
  },
  methods: {
    async loadDashboard() {
      try {
        const response = await api.get('/company/dashboard')
        this.dashboard = response.data
      } catch (error) {
        console.error('Error loading dashboard:', error)
      }
    }
  }
}
</script>
