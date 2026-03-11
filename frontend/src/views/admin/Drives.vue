<template>
  <div class="container mt-5">
    <h1 class="mb-4">Manage Placement Drives</h1>
    
    <ul class="nav nav-tabs mb-4" id="myTab" role="tablist">
      <li class="nav-item">
        <a class="nav-link active" data-bs-toggle="tab" href="#pending">Pending Approval</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" data-bs-toggle="tab" href="#approved">Approved Drives</a>
      </li>
    </ul>

    <div class="tab-content">
      <div id="pending" class="tab-pane fade show active">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Company</th>
              <th>Job Title</th>
              <th>Deadline</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in pendingDrives" :key="drive.id">
              <td>{{ drive.company_name }}</td>
              <td>{{ drive.job_title }}</td>
              <td>{{ formatDate(drive.application_deadline) }}</td>
              <td><span class="badge bg-warning">{{ drive.status }}</span></td>
              <td>
                <button @click="approveDrive(drive.id)" class="btn btn-sm btn-success me-2">Approve</button>
                <button @click="rejectDrive(drive.id)" class="btn btn-sm btn-danger">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="pendingDrives.length === 0" class="text-muted">No pending drives</p>
      </div>

      <div id="approved" class="tab-pane fade">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Company</th>
              <th>Job Title</th>
              <th>Deadline</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in approvedDrives" :key="drive.id">
              <td>{{ drive.company_name }}</td>
              <td>{{ drive.job_title }}</td>
              <td>{{ formatDate(drive.application_deadline) }}</td>
              <td><span class="badge bg-success">{{ drive.status }}</span></td>
            </tr>
          </tbody>
        </table>
        <p v-if="approvedDrives.length === 0" class="text-muted">No approved drives</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'AdminDrives',
  data() {
    return {
      pendingDrives: [],
      approvedDrives: []
    }
  },
  mounted() {
    this.loadDrives()
  },
  methods: {
    async loadDrives() {
      try {
        const pendingResp = await api.get('/admin/drives/pending')
        this.pendingDrives = pendingResp.data.drives
        
        const allResp = await api.get('/admin/drives')
        this.approvedDrives = allResp.data.drives.filter(d => d.status === 'approved')
      } catch (error) {
        console.error('Error loading drives:', error)
      }
    },
    async approveDrive(driveId) {
      try {
        await api.put(`/admin/drives/${driveId}/approve`)
        this.loadDrives()
      } catch (error) {
        console.error('Error approving drive:', error)
      }
    },
    async rejectDrive(driveId) {
      try {
        await api.put(`/admin/drives/${driveId}/reject`)
        this.loadDrives()
      } catch (error) {
        console.error('Error rejecting drive:', error)
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>
