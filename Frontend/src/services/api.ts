import axios from 'axios'

const api = axios.create({
  baseURL: 'https://crm.vtrios.com/api'
})

export default api