// src/pulley.js
import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api',
  timeout: 5000
})

// 获取带轮选项
export const getBeltOptions = () => {
  return api.get('/belt-options')
}

// 获取皮带厂家选项
export const getManufacturerOptions = () => {
  return api.get('/manufacturer-options')
}

// ✅ 提交计算接口（直接传递完整数据对象）
export const calcPulleyDiagram = (data) => {
  return api.post('/calculate', data)
}

// 集中导出（方便在页面中一次性引入）
export default {
  getBeltOptions,
  getManufacturerOptions,
  calcPulleyDiagram
}