<template>
  <div class="container mt-5">
    <h1 class="mb-4">Student Dashboard</h1>
    
    <div class="row">
      <div class="col-md-3 mb-4">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h5 class="card-title">Total Applications</h5>
            <p class="display-4">{{ dashboard.total_applications }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-4">
        <div class="card bg-success text-white">
          <div class="card-body">
            <h5 class="card-title">Selected</h5>
            <p class="display-4">{{ dashboard.selected }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-4">
        <div class="card bg-danger text-white">
          <div class="card-body">
            <h5 class="card-title">Rejected</h5>
            <p class="display-4">{{ dashboard.rejected }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-4">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5 class="card-title">Available Drives</h5>
            <p class="display-4">{{ dashboard.available_drives }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-5">
      <div class="col-md-3">
        <router-link to="/student/profile" class="btn btn-primary btn-lg w-100 mb-3">
          Edit Profile
        </router-link>
      </div>
      <div class="col-md-3">
        <router-link to="/student/apply" class="btn btn-success btn-lg w-100 mb-3">
          Apply to Drives
        </router-link>
      </div>
      <div class="col-md-3">
        <a href="#" @click="viewApplications" class="btn btn-info btn-lg w-100 mb-3">
          My Applications
        </a>
      </div>
      <div class="col-md-3">
        <a href="#" @click="exportApplications" class="btn btn-warning btn-lg w-100 mb-3">
          Export History
        </a>
      </div>
    </div>

    <div v-if="showApplicationsList" class="card mt-5">
      <div class="card-header">
        <h5 class="card-title mb-0">My Applications</h5>
      </div>
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Company</th>
              <th>Job Title</th>
              <th>Status</th>
              <th>Applied On</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.id">
              <td>{{ app.company_name }}</td>
              <td>{{ app.job_title }}</td>
              <td><span :class="getStatusBadge(app.status)">{{ app.status }}</span></td>
              <td>{{ formatDate(app.applied_at) }}</td>
            </tr>
          </tbody>
        </table>
        <p v-if="applications.length === 0" class="text-muted">No applications yet</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'StudentDashboard',
  data() {
    return {
      dashboard: {
        total_applications: 0,
        selected: 0,
        rejected: 0,
        available_drives: 0
      },
      showApplicationsList: false,
      applications: []
    }
  },
  mounted() {
    this.loadDashboard()
  },
  methods: {
    async loadDashboard() {
      try {
        const response = await api.get('/student/dashboard')
        this.dashboard = response.data
      } catch (error) {
        console.error('Error loading dashboard:', error)
      }
    },
    async viewApplications() {
      try {
        const response = await api.get('/student/applications')
        this.applications = response.data.applications
        this.showApplicationsList = true
      } catch (error) {
        console.error('Error loading applications:', error)
      }
    },
    async exportApplications() {
      try {
        await api.post('/student/export-applications')
        alert('Export initiated. You will receive the file via email.')
      } catch (error) {
        console.error('Error exporting applications:', error)
        alert('Export failed')
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    getStatusBadge(status) {
      const badges = {
        applied: 'badge bg-info',
        shortlisted: 'badge bg-warning',
        selected: 'badge bg-success',
        rejected: 'badge bg-danger'
      }
      return badges[status] || 'badge bg-secondary'
    }
  }
}
</script>
