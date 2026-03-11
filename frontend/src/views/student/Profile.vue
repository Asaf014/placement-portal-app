<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-body p-5">
            <h1 class="card-title mb-4">Student Profile</h1>
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label class="form-label">First Name</label>
                <input type="text" class="form-control" v-model="profile.first_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Last Name</label>
                <input type="text" class="form-control" v-model="profile.last_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Roll Number</label>
                <input type="text" class="form-control" v-model="profile.roll_number" disabled>
              </div>
              <div class="mb-3">
                <label class="form-label">Branch</label>
                <input type="text" class="form-control" v-model="profile.branch">
              </div>
              <div class="mb-3">
                <label class="form-label">Batch</label>
                <input type="number" class="form-control" v-model="profile.batch">
              </div>
              <div class="mb-3">
                <label class="form-label">CGPA</label>
                <input type="number" step="0.1" class="form-control" v-model="profile.cgpa">
              </div>
              <div class="mb-3">
                <label class="form-label">Phone</label>
                <input type="tel" class="form-control" v-model="profile.phone">
              </div>
              <div class="mb-3">
                <label class="form-label">Resume URL</label>
                <input type="url" class="form-control" v-model="profile.resume_url" placeholder="Link to your resume">
              </div>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? 'Updating...' : 'Update Profile' }}
              </button>
            </form>
            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
            <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'StudentProfile',
  data() {
    return {
      profile: {
        first_name: '',
        last_name: '',
        roll_number: '',
        branch: '',
        batch: '',
        cgpa: '',
        phone: '',
        resume_url: ''
      },
      loading: false,
      error: '',
      success: ''
    }
  },
  mounted() {
    this.loadProfile()
  },
  methods: {
    async loadProfile() {
      try {
        const response = await api.get('/student/profile')
        this.profile = response.data
      } catch (error) {
        this.error = 'Error loading profile'
      }
    },
    async updateProfile() {
      this.error = ''
      this.success = ''
      this.loading = true
      try {
        await api.put('/student/profile', this.profile)
        this.success = 'Profile updated successfully'
      } catch (error) {
        this.error = error.response?.data?.error || 'Update failed'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
