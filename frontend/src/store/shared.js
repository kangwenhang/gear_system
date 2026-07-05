import { reactive } from 'vue'

// 全局共享状态
export const sharedStore = reactive({
  // 所有带轮数据（含直径、类型等完整信息）
  pulleys: [
    { code: 'FAN', name: 'FAN', type: 'groove', x: 0, y: 0, groove_dia: 194, flat_dia: null, inertia: 0, service_factor: 1, rotation: 1, centerHeightDiff: '', perpendicularity: '', tiltAngle: '' },
    { code: 'ALT', name: 'ALT', type: 'groove', x: 250, y: -80, groove_dia: 75, flat_dia: null, inertia: 0, service_factor: 1, rotation: 1, centerHeightDiff: '', perpendicularity: '', tiltAngle: '' },
    { code: 'AC', name: 'AC', type: 'groove', x: 268, y: 132.5, groove_dia: 110, flat_dia: null, inertia: 0, service_factor: 1, rotation: 1, centerHeightDiff: '', perpendicularity: '', tiltAngle: '' },
    { code: 'TEN', name: 'TEN', type: 'flat', x: 171.42, y: 17.35, groove_dia: null, flat_dia: 70, inertia: 0, service_factor: 1, rotation: -1, centerHeightDiff: '', perpendicularity: '', tiltAngle: '' }
  ],
  // 皮带参数（含 flat_to_pitch、pitch_to_effective 等）
  beltParams: {
    flat_to_pitch: 1.5,
    pitch_to_effective: 0.99
  },
  // 皮带完整参数
  beltFullParams: {
    belt_type: '',
    manufacturer: '',
    ribs: null,
    effective_length: null,
    min_length: null,
    max_length: null,
    length_tolerance: null,
    elongation: null,
    stretch: null
  },
  // 张紧器参数
  tensioner: {
    type: '',
    torque: null,
    angle: null,
    arm_length: null
  },
  // 项目表单信息
  formInfo: {
    customer: '',
    project: '',
    cylinders: null,
    power: null,
    rated_speed: null,
    idle_speed: null
  },
  // 对齐度计算结果
  alignmentResults: [],
  // 触发对齐度计算的信号
  calcTrigger: 0,
  // 最后一个带轮序号
  lastPulleyIndex: 0,
  // Contact参数（每个带轮的K/J/L/M/N/P/O/Q/U）
  contactParams: {}
})
