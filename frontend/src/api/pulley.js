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
  calcFreePosition
}