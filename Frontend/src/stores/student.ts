import { defineStore } from 'pinia'
import { ref } from 'vue'

import {
  getStudents,
  createStudent
} from '@/services/studentService'

export const useStudentStore =
defineStore(
  'student',
  () => {

    const students =
      ref<any[]>([])

    async function loadStudents() {

      students.value =
        await getStudents()
    }

    async function addStudent(
      student: any
    ) {

      await createStudent(
        student
      )

      await loadStudents()
    }

    return {
      students,
      loadStudents,
      addStudent
    }
  }
)