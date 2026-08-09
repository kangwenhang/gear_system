import { reactive } from 'vue'

// 全局共享状态
export const sharedStore = reactive({
  // 所有带轮数据（含直径、类型等完整信息）
  // pitch_dia / effective_dia / flat_dia 对应 Excel 报告页的 Pitch / Effective / Flat 三列
  pulleys: [
    { code: '', name: '', type: 'groove', x: null, y: null, pitch_dia: null, effective_dia: null, flat_dia: null, groove_dia: null, inertia: null, service_factor: null, rotation: 1, centerHeightDiff: 0, perpendicularity: 0, tiltAngle: '' },
    { code: '', name: '', type: 'groove', x: null, y: null, pitch_dia: null, effective_dia: null, flat_dia: null, groove_dia: null, inertia: null, service_factor: null, rotation: 1, centerHeightDiff: 0, perpendicularity: 0, tiltAngle: '' },
    { code: '', name: '', type: 'groove', x: null, y: null, pitch_dia: null, effective_dia: null, flat_dia: null, groove_dia: null, inertia: null, service_factor: null, rotation: 1, centerHeightDiff: 0, perpendicularity: 0, tiltAngle: '' }
  ],
  // 皮带参数（含 flat_to_pitch、pitch_to_effective 等）
  beltParams: {
    flat_to_pitch: null,
    pitch_to_effective: null
  },
  // 皮带完整参数（对齐 Excel 报告页第一页 Belt Data 字段）
  beltFullParams: {
    belt_name: '',
    belt_type: '',
    rib_type: '',
    belt_material: '',
    cord_material: '',
    manufacturer: '',
    ribs: null,
    belt_height: null,
    stretch_wear_allow: null,
    flat_to_pitch: null,
    pitch_to_effective: null,
    effective_length: null,
    length_tolerance: null,
    life_coefficient: null,
    last_install_type: '',
    belt_pk: null
  },
  // 皮带长度计算详细结果
  beltLengthResult: {
    belt_length: null,
    total_straight: null,
    total_arc: null,
    details: []
  },
  // 短皮带长度计算结果（短皮带 = 总长 - 公差）
  shortBeltResult: {
    short_belt_length: null, tensioner_x: null, tensioner_y: null,
    tensioner_angle: null, achieved_length: null, arm_length: null,
    iterations: null, converged: null
  },
  // 长皮带长度计算结果（长皮带 = 总长 + 公差）
  longBeltResult: {
    long_belt_length: null, tensioner_x: null, tensioner_y: null,
    tensioner_angle: null, achieved_length: null, arm_length: null,
    iterations: null, converged: null
  },
  // 张紧器自由位置计算结果
  freePositionResult: {
    free_tensioner_x: null, free_tensioner_y: null, free_angle: null,
    free_belt_length: null, work_angle: null, arm_length: null,
    nominal_angle: null, rotation: null
  },
  // 张紧器安装位置计算结果
  installPositionResult: {
    install_tensioner_x: null, install_tensioner_y: null, install_angle: null,
    install_belt_length: null, base_angle: null, arm_length: null,
    torsion_angle: null, rotation: null
  },
  // 张紧器参数（对齐 Excel 报告页 Tensioner Data）
  tensioner: {
    type: 'Automatic',
    torque: null,
    angle: null,
    arm_length: null,
    pivot_x: null,
    pivot_y: null,
    spring_stiffness: null,
    design_tension: null,
    damping: null,
    nominal_angle: null,
    install_angle: null,
    stroke: null,
    head_size: null
  },
  // 项目表单信息（对齐 Excel 报告页第一页 Project Information）
  formInfo: {
    file_no: '2026072002',
    version: '02',
    date: '2026-08-08',
    customer: 'YAMAZ',
    project: 'FEAD-652-FAN-9PK-EPDM-1391',
    cylinders: null,
    power: null,
    layers: '',
    rated_speed: null,
    idle_speed: null,
    problem_statement: '1.The FAN has a risk of slipping.（only steady state）',
    analysis_reference: 'FAN Power Update'
  },
  // 对齐度计算结果
  alignmentResults: [],
  // 触发对齐度计算的信号
  calcTrigger: 0,
  // 最后一个带轮序号
  lastPulleyIndex: 0,
  // Contact参数（每个带轮的K/J/L/M/N/P/O/Q/U）
  contactParams: {},
  // 清空所有设计数据（新建项目时调用）
  resetAll() {
    // 清空带轮数据：3行空值
    this.pulleys.splice(0, this.pulleys.length)
    for (let i = 0; i < 3; i++) {
      this.pulleys.push({
        code: '', name: '', type: 'groove',
        x: null, y: null, pitch_dia: null, effective_dia: null,
        flat_dia: null, groove_dia: null, inertia: null, service_factor: null,
        rotation: 1, centerHeightDiff: 0, perpendicularity: 0, tiltAngle: ''
      })
    }
    // 清空皮带参数（short form）
    Object.assign(this.beltParams, {
      flat_to_pitch: null,
      pitch_to_effective: null
    })
    // 清空表单项
    Object.assign(this.formInfo, {
      file_no: '',
      version: '01',
      date: '',
      customer: '',
      project: '',
      cylinders: null,
      power: null,
      layers: '',
      rated_speed: null,
      idle_speed: null,
      problem_statement: '',
      analysis_reference: ''
    })
    // 清空皮带参数
    Object.assign(this.beltFullParams, {
      belt_name: '',
      belt_type: '',
      rib_type: '',
      belt_material: '',
      cord_material: '',
      manufacturer: '',
      ribs: null,
      belt_height: null,
      stretch_wear_allow: null,
      flat_to_pitch: null,
      pitch_to_effective: null,
      effective_length: null,
      length_tolerance: null,
      life_coefficient: null,
      last_install_type: '',
      belt_pk: null
    })
    // 清空张紧器参数
    Object.assign(this.tensioner, {
      type: 'Automatic',
      torque: null,
      angle: null,
      arm_length: null,
      pivot_x: null,
      pivot_y: null,
      spring_stiffness: null,
      design_tension: null,
      damping: null,
      nominal_angle: null,
      install_angle: null,
      stroke: null,
      head_size: null
    })
    // 清空计算结果
    this.beltLengthResult = { belt_length: null, total_straight: null, total_arc: null, details: [] }
    this.shortBeltResult = {}
    this.longBeltResult = {}
    this.freePositionResult = {}
    this.installPositionResult = {}
    this.alignmentResults = []
    this.contactParams = {}
    this.lastPulleyIndex = 0
  }
})
