import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Course } from '@/types/course'

export const useCourseStore = defineStore('course', () => {
  const courses = ref<Course[]>([
    {
      id: 1,
      name: 'BIM Professional',
      duration: '3 Months',
      fee: 25000,
      description: 'Complete BIM Training',
      status: true,
    },
  ])

  function addCourse(course: Course) {
    courses.value.push(course)
  }

  function deleteCourse(id: number) {
    courses.value = courses.value.filter((c) => c.id !== id)
  }

  async function loadCourses() {
    // later connect API
    return
  }

  return {
    courses,
    addCourse,
    deleteCourse,
    loadCourses,
  }
})