<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-7">
        <div class="card shadow">
          <div class="card-body p-5">
            <h1 class="card-title text-center mb-4">Register</h1>
            
            <div v-if="!roleSelected" class="text-center mb-4">
              <p class="mb-3">Select registration type:</p>
              <button type="button" class="btn btn-info me-2" @click="selectRole('student')">
                <i class="bi bi-person-fill"></i> Register as Student
              </button>
              <button type="button" class="btn btn-success" @click="selectRole('company')">
                <i class="bi bi-building"></i> Register as Company
              </button>
            </div>

            <form v-if="roleSelected" @submit.prevent="register">
              <div class="mb-3">
                <label for="email" class="form-label">Email *</label>
                <input type="email" class="form-control" id="email" v-model="form.email" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password *</label>
                <input type="password" class="form-control" id="password" v-model="form.password" required>
              </div>

              <!-- Student Registration Fields -->
              <div v-if="form.role === 'student'">
                <hr>
                <h5 class="mb-3">Student Information</h5>
                <div class="mb-3">
                  <label for="firstName" class="form-label">First Name *</label>
                  <input type="text" class="form-control" id="firstName" v-model="form.firstName" required>
                </div>
                <div class="mb-3">
                  <label for="lastName" class="form-label">Last Name *</label>
                  <input type="text" class="form-control" id="lastName" v-model="form.lastName" required>
                </div>
                <div class="mb-3">
                  <label for="rollNumber" class="form-label">Roll Number *</label>
                  <input type="text" class="form-control" id="rollNumber" v-model="form.rollNumber" required>
                </div>
                <div class="mb-3">
                  <label for="phoneStudent" class="form-label">Phone Number</label>
                  <input type="tel" class="form-control" id="phoneStudent" v-model="form.phone">
                </div>
                <div class="mb-3">
                  <label for="branch" class="form-label">Branch</label>
                  <input type="text" class="form-control" id="branch" v-model="form.branch" placeholder="e.g., Computer Science">
                </div>
                <div class="mb-3">
                  <label for="cgpa" class="form-label">CGPA</label>
                  <input type="number" class="form-control" id="cgpa" v-model="form.cgpa" step="0.01" min="0" max="10">
                </div>
                <div class="mb-3">
                  <label for="resumeUrl" class="form-label">Resume URL</label>
                  <input type="url" class="form-control" id="resumeUrl" v-model="form.resumeUrl">
                </div>
              </div>

              <!-- Company Registration Fields -->
              <div v-if="form.role === 'company'">
                <hr>
                <h5 class="mb-3">Company Information</h5>
                <div class="mb-3">
                  <label for="companyName" class="form-label">Company Name *</label>
                  <input type="text" class="form-control" id="companyName" v-model="form.companyName" required>
                </div>
                <div class="mb-3">
                  <label for="website" class="form-label">Website *</label>
                  <input type="url" class="form-control" id="website" v-model="form.website" required>
                </div>
                <div class="mb-3">
                  <label for="hrContact" class="form-label">HR Contact Name *</label>
                  <input type="text" class="form-control" id="hrContact" v-model="form.hrContact" required>
                </div>
                <div class="mb-3">
                  <label for="hrPhone" class="form-label">HR Phone Number *</label>
                  <input type="tel" class="form-control" id="hrPhone" v-model="form.hrPhone" required>
                </div>
                <div class="mb-3">
                  <label for="description" class="form-label">Company Description</label>
                  <textarea class="form-control" id="description" v-model="form.description" rows="3"></textarea>
                </div>
                <div class="mb-3">
                  <label for="industry" class="form-label">Industry</label>
                  <input type="text" class="form-control" id="industry" v-model="form.industry" placeholder="e.g., Software, Finance">
                </div>
              </div>

              <button type="submit" class="btn btn-primary w-100 mt-3" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Registering...' : 'Register' }}
              </button>
              <button v-if="roleSelected" type="button" class="btn btn-secondary w-100 mt-2" @click="backToRoleSelection">
                Back
              </button>
            </form>

            <p class="text-center mt-3">
              Already have account? <router-link to="/login">Login here</router-link>
            </p>
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
  name: 'Register',
  data() {
    return {
      roleSelected: false,
      form: {
        email: '',
        password: '',
        role: '',
        firstName: '',
        lastName: '',
        rollNumber: '',
        phone: '',
        branch: '',
        cgpa: '',
        resumeUrl: '',
        companyName: '',
        website: '',
        hrContact: '',
        hrPhone: '',
        description: '',
        industry: ''
      },
      loading: false,
      error: '',
      success: ''
    }
  },
  methods: {
    selectRole(role) {
      this.form.role = role
      this.roleSelected = true
      this.error = ''
    },
    backToRoleSelection() {
      this.roleSelected = false
      this.form.role = ''
      this.error = ''
    },
    async register() {
      this.error = ''
      this.success = ''
      this.loading = true
      try {
        const payload = {
          email: this.form.email,
          password: this.form.password,
          role: this.form.role
        }

        if (this.form.role === 'student') {
          payload.student_data = {
            first_name: this.form.firstName,
            last_name: this.form.lastName,
            roll_number: this.form.rollNumber,
            phone: this.form.phone,
            branch: this.form.branch,
            cgpa: this.form.cgpa ? parseFloat(this.form.cgpa) : null,
            resume_url: this.form.resumeUrl
          }
        } else if (this.form.role === 'company') {
          payload.company_data = {
            company_name: this.form.companyName,
            website: this.form.website,
            hr_contact: this.form.hrContact,
            hr_phone: this.form.hrPhone,
            description: this.form.description,
            industry: this.form.industry
          }
        }

        const response = await api.post('/auth/register', payload)
        this.success = 'Registration successful! Redirecting to login...'
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
      } catch (error) {
        this.error = error.response?.data?.error || 'Registration failed'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
