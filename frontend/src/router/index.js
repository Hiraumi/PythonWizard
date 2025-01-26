import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/views/Login.vue';
import RegisterPage from '@/views/Register.vue';
import MainPage from '@/views/MainPage.vue';
import AppDashboard from '@/views/Dashboard.vue';
import AppCourses from '@/views/Courses.vue';
import AppCoding from '@/views/Coding.vue';
import AppExams from '@/views/Exams.vue'
import MainPageStaff from '@/views/MainPageStaff.vue';
import StaffDashboard from '@/views/StaffDashboard.vue';
import UserManagement from '@/views/UserManagement.vue';
import OnCoding from "@/views/OnCoding.vue";

const routes = [
  {
    path: '/', name: 'Login', component: LoginPage,
  },
  {
    path: '/register', name: 'Register', component: RegisterPage,
  },
  {
    path: '/mainpage', name: 'MainPage', component: MainPage,
    redirect: '/mainpage/dashboard',
    children: [
      {
        path: 'dashboard', name: 'Dashboard', component: AppDashboard,
      },
      {
        path: 'courses', name: 'Courses', component: AppCourses,
      },
      {
        path: 'coding', name: 'Coding', component: AppCoding,
      },
      {
        path: 'oncoding', name: 'OnCoding', component: OnCoding,
      },
      {
        path: 'exams', name: 'Exams', component: AppExams,
      },
    ],
  },
  {
    path: '/mainpage-staff', name: 'MainPageStaff', component: MainPageStaff,
    redirect: '/mainpage-staff/dashboard',
    children: [
      {
        path: 'dashboard', name: 'StaffDashboard', component: StaffDashboard,
      },
      {
        path: 'user-management', name: 'UserManagement', component: UserManagement,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;