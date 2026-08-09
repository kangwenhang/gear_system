// src/pulley.js
import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api',
  timeout: 15000
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

// 计算Contact参数
export const calcContactParams = (data) => {
  return api.post('/calc-contact-params', data)
}

// 计算对齐度
export const calcAlignment = (data) => {
  return api.post('/calc-alignment', data)
}

// 张紧轮/枢轴坐标互转
// 传 pivot_x/pivot_y 做正向（→张紧轮XY），传 pulley_x/pulley_y 做反向（→枢轴XY）
export const calcTensionerCoord = (data) => {
  return api.post('/calc-tensioner-coord', data)
}

// 计算皮带长度
export const calcBeltLength = (data) => {
  return api.post('/calc-belt-length', data)
}

// 计算短/长皮带长度对应的张紧轮XY坐标
export const calcTensionerPosition = (data) => {
  return api.post('/calc-tensioner-position', data)
}

// 计算张紧器自由位置的皮带长度和张紧轮XY坐标
export const calcFreePosition = (data) => {
  return api.post('/calc-free-position', data)
}

// 计算张紧器安装位置的皮带长度和张紧轮XY坐标
export const calcInstallPosition = (data) => {
  return api.post('/calc-install-position', data)
}

// 生成 Excel 报告（基于 REPORT.xlsx 模板）
export const generateReport = (data) => {
  return api.post('/generate-report', data, { responseType: 'blob' })
}

// ===== 项目管理 API =====

// 保存项目
export const saveProject = (data) => api.post('/projects', data)

// 搜索/列出项目
export const listProjects = (params) => api.get('/projects', { params })

// 获取单个项目（按 ID）
export const getProject = (id) => api.get(`/projects/${id}`)

// 获取单个项目（按文件编号+版本）
export const getProjectByFile = (fileNo, version) => api.get('/projects/by-file', { params: { file_no: fileNo, version } })

// 更新项目
export const updateProject = (id, data) => api.put(`/projects/${id}`, data)

// 删除项目
export const deleteProject = (id) => api.delete(`/projects/${id}`)

// 导出项目 Excel
export const exportProject = (id) => api.post(`/projects/${id}/export`, {}, { responseType: 'blob' })

// 获取版本列表
export const listVersions = () => api.get('/projects/versions')

// 获取客户列表
export const listCustomers = () => api.get('/projects/customers')

// 获取下一个文件编号
export const getNextFileNo = (version) => api.get('/projects/next-file-no', { params: { version } })

// 集中导出（方便在页面中一次性引入）
export default {
  getBeltOptions,
  getManufacturerOptions,
  calcPulleyDiagram,
  calcContactParams,
  calcAlignment,
  calcTensionerCoord,
  calcBeltLength,
  calcTensionerPosition,
  calcFreePosition,
  calcInstallPosition,
  generateReport
}