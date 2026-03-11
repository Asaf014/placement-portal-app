<template>
  <div class="container mt-5">
    <h1 class="mb-4">Manage Companies</h1>
    
    <ul class="nav nav-tabs mb-4" id="myTab" role="tablist">
      <li class="nav-item">
        <a class="nav-link active" data-bs-toggle="tab" href="#pending">Pending Approval</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" data-bs-toggle="tab" href="#all">All Companies</a>
      </li>
    </ul>

    <div class="tab-content">
      <div id="pending" class="tab-pane fade show active">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Company Name</th>
              <th>Website</th>
              <th>HR Contact</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="company in pendingCompanies" :key="company.id">
              <td>{{ company.company_name }}</td>
              <td>{{ company.website }}</td>
              <td>{{ company.hr_contact }}</td>
              <td><span class="badge bg-warning">{{ company.approval_status }}</span></td>
              <td>
                <button @click="approveCompany(company.id)" class="btn btn-sm btn-success me-2">Approve</button>
                <button @click="rejectCompany(company.id)" class="btn btn-sm btn-danger">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="pendingCompanies.length === 0" class="text-muted">No pending companies</p>
      </div>

      <div id="all" class="tab-pane fade">
        <div class="mb-3">
          <input type="text" class="form-control" v-model="searchQuery" @input="searchCompanies" placeholder="Search companies...">
        </div>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Company Name</th>
              <th>Website</th>
              <th>HR Contact</th>
              <th>Status</th>
              <th>Active</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="company in allCompanies" :key="company.id">
              <td>{{ company.company_name }}</td>
              <td>{{ company.website }}</td>
              <td>{{ company.hr_contact }}</td>
              <td><span :class="getStatusBadge(company.approval_status)">{{ company.approval_status }}</span></td>
              <td>
                <span v-if="company.is_active" class="badge bg-success">Active</span>
                <span v-else class="badge bg-danger">Inactive</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'AdminCompanies',
  data() {
    return {
      pendingCompanies: [],
      allCompanies: [],
      searchQuery: ''
    }
  },
  mounted() {
    this.loadPendingCompanies()
    this.loadAllCompanies()
  },
  methods: {
    async loadPendingCompanies() {
      try {
        const response = await api.get('/admin/companies/pending')
        this.pendingCompanies = response.data.companies
      } catch (error) {
        console.error('Error loading pending companies:', error)
      }
    },
    async loadAllCompanies() {
      try {
        const response = await api.get('/admin/companies')
        this.allCompanies = response.data.companies
      } catch (error) {
        console.error('Error loading all companies:', error)
      }
    },
    async approveCompany(companyId) {
      try {
        await api.put(`/admin/companies/${companyId}/approve`)
        this.loadPendingCompanies()
        this.loadAllCompanies()
      } catch (error) {
        console.error('Error approving company:', error)
      }
    },
    async rejectCompany(companyId) {
      try {
        await api.put(`/admin/companies/${companyId}/reject`)
        this.loadPendingCompanies()
        this.loadAllCompanies()
      } catch (error) {
        console.error('Error rejecting company:', error)
      }
    },
    async searchCompanies() {
      if (!this.searchQuery) {
        this.loadAllCompanies()
        return
      }
      try {
        const response = await api.get('/admin/companies', {
          params: { search: this.searchQuery }
        })
        this.allCompanies = response.data.companies
      } catch (error) {
        console.error('Error searching companies:', error)
      }
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
