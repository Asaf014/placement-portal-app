<template>
  <div class="container mt-5">
    <h1 class="mb-4">Placement Drives</h1>
    
    <ul class="nav nav-tabs mb-4" id="myTab" role="tablist">
      <li class="nav-item">
        <a class="nav-link active" data-bs-toggle="tab" href="#list">My Drives</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" data-bs-toggle="tab" href="#create">Create Drive</a>
      </li>
    </ul>

    <div class="tab-content">
      <div id="list" class="tab-pane fade show active">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Status</th>
              <th>Deadline</th>
              <th>Applicants</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in drives" :key="drive.id">
              <td>{{ drive.job_title }}</td>
              <td><span :class="getStatusBadge(drive.status)">{{ drive.status }}</span></td>
              <td>{{ formatDate(drive.application_deadline) }}</td>
              <td>{{ drive.applicants_count }}</td>
              <td>
                <button @click="viewApplications(drive.id)" class="btn btn-sm btn-info">
                  View Applications
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="drives.length === 0" class="text-muted">No drives created yet</p>
      </div>

      <div id="create" class="tab-pane fade">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Create New Drive</h5>
            <form @submit.prevent="createDrive">
              <div class="mb-3">
                <label class="form-label">Job Title</label>
                <input type="text" class="form-control" v-model="newDrive.job_title" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Job Description</label>
                <textarea class="form-control" v-model="newDrive.job_description" rows="5" required></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Minimum CGPA</label>
                <input type="number" step="0.1" class="form-control" v-model="newDrive.min_cgpa" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Application Deadline</label>
                <input type="datetime-local" class="form-control" v-model="newDrive.application_deadline" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Salary Package</label>
                <input type="number" step="0.1" class="form-control" v-model="newDrive.salary_package">
              </div>
              <div class="mb-3">
                <label class="form-label">Interview Date</label>
                <input type="datetime-local" class="form-control" v-model="newDrive.interview_date">
              </div>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? 'Creating...' : 'Create Drive' }}
              </button>
            </form>
            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
            <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showApplicationsModal" class="modal-backdrop show" @click="showApplicationsModal = false"></div>
    <div v-if="showApplicationsModal" class="modal show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Applications</h5>
            <button type="button" class="btn-close" @click="showApplicationsModal = false"></button>
          </div>
          <div class="modal-body">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Student Name</th>
                  <th>Roll Number</th>
                  <th>CGPA</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in selectedDriveApplications" :key="app.id">
                  <td>{{ app.student_name }}</td>
                  <td>{{ app.student_roll }}</td>
                  <td>{{ app.student_cgpa }}</td>
                  <td>{{ app.status }}</td>
                  <td>
                    <button @click="updateStatus(app.id, 'shortlisted')" class="btn btn-sm btn-warning me-1">Shortlist</button>
                    <button @click="updateStatus(app.id, 'selected')" class="btn btn-sm btn-success me-1">Select</button>
                    <button @click="updateStatus(app.id, 'rejected')" class="btn btn-sm btn-danger">Reject</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'CompanyDrives',
  data() {
    return {
      drives: [],
      newDrive: {
        job_title: '',
        job_description: '',
        min_cgpa: '',
        application_deadline: '',
        salary_package: '',
        interview_date: ''
      },
      loading: false,
      error: '',
      success: '',
      showApplicationsModal: false,
      selectedDriveId: null,
      selectedDriveApplications: []
    }
  },
  mounted() {
    this.loadDrives()
  },
  methods: {
    async loadDrives() {
      try {
        const response = await api.get('/company/drives')
        this.drives = response.data.drives
      } catch (error) {
        console.error('Error loading drives:', error)
      }
    },
    async createDrive() {
      this.error = ''
      this.success = ''
      this.loading = true
      try {
        await api.post('/company/drives', this.newDrive)
        this.success = 'Drive created successfully (awaiting admin approval)'
        this.newDrive = {
          job_title: '',
          job_description: '',
          min_cgpa: '',
          application_deadline: '',
          salary_package: '',
          interview_date: ''
        }
        this.loadDrives()
      } catch (error) {
        this.error = error.response?.data?.error || 'Creation failed'
      } finally {
        this.loading = false
      }
    },
    async viewApplications(driveId) {
      try {
        const response = await api.get(`/company/applications/${driveId}`)
        this.selectedDriveApplications = response.data.applications
        this.selectedDriveId = driveId
        this.showApplicationsModal = true
      } catch (error) {
        console.error('Error loading applications:', error)
      }
    },
    async updateStatus(applicationId, status) {
      try {
        const endpoint = status === 'shortlisted' ? 'shortlist' : (status === 'selected' ? 'select' : 'reject')
        await api.put(`/company/applications/${applicationId}/${endpoint}`)
        this.selectedDriveApplications = this.selectedDriveApplications.map(app => {
          if (app.id === applicationId) {
            app.status = status
          }
          return app
        })
      } catch (error) {
        console.error('Error updating status:', error)
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    getStatusBadge(status) {
      const badges = {
        approved: 'badge bg-success',
        rejected: 'badge bg-danger',
        pending: 'badge bg-warning'
      }
      return badges[status] || 'badge bg-secondary'
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}

.modal.show {
  z-index: 1050;
}
</style>
