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
  // 触发对齐度计算的信号
  calcTrigger: 0
})
