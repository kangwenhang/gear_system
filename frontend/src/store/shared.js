import { reactive } from 'vue'

// 全局共享状态
export const sharedStore = reactive({
  // 所有带轮数据（含直径、类型等完整信息）
  pulleys: [],
  // 皮带参数（含 flat_to_pitch、pitch_to_effective 等）
  beltParams: {
    flat_to_pitch: null,
    pitch_to_effective: null
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
  calcTrigger: 0
})
