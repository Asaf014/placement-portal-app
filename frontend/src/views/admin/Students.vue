<template>
  <div class="container mt-5">
    <h1 class="mb-4">Manage Students</h1>
    
    <div class="mb-3">
      <input type="text" class="form-control" v-model="searchQuery" @input="searchStudents" placeholder="Search students...">
    </div>

    <table class="table table-striped">
      <thead>
        <tr>
          <th>Name</th>
          <th>Roll Number</th>
          <th>Branch</th>
          <th>CGPA</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.id">
          <td>{{ student.first_name }} {{ student.last_name }}</td>
          <td>{{ student.roll_number }}</td>
          <td>{{ student.branch }}</td>
          <td>{{ student.cgpa }}</td>
          <td>
            <span v-if="student.is_active" class="badge bg-success">Active</span>
            <span v-else class="badge bg-danger">Blacklisted</span>
          </td>
          <td>
            <button v-if="student.is_active" @click="blacklistStudent(student.id)" class="btn btn-sm btn-danger">
              Blacklist
            </button>
            <span v-else class="text-muted">Blacklisted</span>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="students.length === 0" class="text-muted">No students found</p>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'AdminStudents',
  data() {
    return {
      students: [],
      searchQuery: ''
    }
  },
  mounted() {
    this.loadStudents()
  },
  methods: {
    async loadStudents() {
      try {
        const response = await api.get('/admin/students')
        this.students = response.data.students
      } catch (error) {
        console.error('Error loading students:', error)
      }
    },
    async searchStudents() {
      if (!this.searchQuery) {
        this.loadStudents()
        return
      }
      try {
        const response = await api.get('/admin/students', {
          params: { search: this.searchQuery }
        })
        this.students = response.data.students
      } catch (error) {
        console.error('Error searching students:', error)
      }
    },
    async blacklistStudent(studentId) {
      try {
        await api.put(`/admin/students/${studentId}/blacklist`)
        this.loadStudents()
      } catch (error) {
        console.error('Error blacklisting student:', error)
      }
    }
  }
}
</script>
