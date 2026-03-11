<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-body p-5">
            <h1 class="card-title mb-4">Company Profile</h1>
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label class="form-label">Company Name</label>
                <input type="text" class="form-control" v-model="profile.company_name" disabled>
              </div>
              <div class="mb-3">
                <label class="form-label">Website</label>
                <input type="url" class="form-control" v-model="profile.website">
              </div>
              <div class="mb-3">
                <label class="form-label">HR Contact</label>
                <input type="email" class="form-control" v-model="profile.hr_contact">
              </div>
              <div class="mb-3">
                <label class="form-label">HR Phone</label>
                <input type="tel" class="form-control" v-model="profile.hr_phone">
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" v-model="profile.description" rows="5"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Status</label>
                <input type="text" class="form-control" :value="profile.approval_status" disabled>
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
  name: 'CompanyProfile',
  data() {
    return {
      profile: {
        company_name: '',
        website: '',
        hr_contact: '',
        hr_phone: '',
        description: '',
        approval_status: ''
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
        const response = await api.get('/company/profile')
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
        await api.put('/company/profile', this.profile)
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
