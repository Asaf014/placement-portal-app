<template>
  <div class="container mt-5">
    <h1 class="mb-4">Apply to Placement Drives</h1>
    
    <div class="mb-3">
      <input type="text" class="form-control" v-model="searchQuery" @input="searchDrives" placeholder="Search drives by company or job title...">
    </div>

    <div class="row">
      <div v-for="drive in availableDrives" :key="drive.id" class="col-md-6 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ drive.job_title }}</h5>
            <p class="card-text"><strong>Company:</strong> {{ drive.company_name }}</p>
            <p class="card-text">{{ drive.job_description.substring(0, 100) }}...</p>
            <p class="card-text"><strong>Salary:</strong> ₹{{ drive.salary_package }}/annum</p>
            <p class="card-text"><strong>Min CGPA:</strong> {{ drive.min_cgpa }}</p>
            <p class="card-text"><strong>Deadline:</strong> {{ formatDate(drive.application_deadline) }}</p>
            <button @click="applyToDrive(drive.id)" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Applying...' : 'Apply Now' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <p v-if="availableDrives.length === 0" class="text-muted text-center mt-5">No eligible drives available</p>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'StudentApply',
  data() {
    return {
      availableDrives: [],
      searchQuery: '',
      loading: false,
      error: '',
      success: ''
    }
  },
  mounted() {
    this.loadAvailableDrives()
  },
  methods: {
    async loadAvailableDrives() {
      try {
        const response = await api.get('/student/available-drives')
        this.availableDrives = response.data.drives
      } catch (error) {
        this.error = 'Error loading drives'
      }
    },
    async searchDrives() {
      if (!this.searchQuery) {
        this.loadAvailableDrives()
        return
      }
      try {
        const response = await api.get('/student/search-drives', {
          params: { q: this.searchQuery }
        })
        this.availableDrives = response.data.drives
      } catch (error) {
        console.error('Error searching drives:', error)
      }
    },
    async applyToDrive(driveId) {
      this.error = ''
      this.success = ''
      this.loading = true
      try {
        await api.post(`/student/apply/${driveId}`)
        this.success = 'Application submitted successfully'
        this.loadAvailableDrives()
        setTimeout(() => {
          this.success = ''
        }, 3000)
      } catch (error) {
        this.error = error.response?.data?.error || 'Application failed'
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>
