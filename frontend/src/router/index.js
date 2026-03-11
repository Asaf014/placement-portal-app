import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import Profile from '../views/Profile.vue'
import AdminDashboard from '../views/admin/Dashboard.vue'
import CompanyDashboard from '../views/company/Dashboard.vue'
import StudentDashboard from '../views/student/Dashboard.vue'
import CompanyProfile from '../views/company/Profile.vue'
import StudentProfile from '../views/student/Profile.vue'
import CompanyDrives from '../views/company/Drives.vue'
import StudentApply from '../views/student/Apply.vue'
import AdminCompanies from '../views/admin/Companies.vue'
import AdminStudents from '../views/admin/Students.vue'
import AdminDrives from '../views/admin/Drives.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/companies',
    name: 'AdminCompanies',
    component: AdminCompanies,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/students',
    name: 'AdminStudents',
    component: AdminStudents,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/drives',
    name: 'AdminDrives',
    component: AdminDrives,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/company/dashboard',
    name: 'CompanyDashboard',
    component: CompanyDashboard,
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/company/profile',
    name: 'CompanyProfile',
    component: CompanyProfile,
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/company/drives',
    name: 'CompanyDrives',
    component: CompanyDrives,
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/student/dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/profile',
    name: 'StudentProfile',
    component: StudentProfile,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/apply',
    name: 'StudentApply',
    component: StudentApply,
    meta: { requiresAuth: true, role: 'student' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')

  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login')
      return
    }

    if (to.meta.role && to.meta.role !== role) {
      next('/')
      return
    }
  }

  if ((to.name === 'Login' || to.name === 'Register') && token) {
    next(`/${role}/dashboard`)
    return
  }

  next()
})

export default router
