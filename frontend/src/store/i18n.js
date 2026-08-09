import { ref, computed } from 'vue'

// 支持的语言
export const SUPPORTED_LANGS = ['zh-CN', 'en-US']

// 当前语言（全局状态）
const currentLang = ref(typeof window !== 'undefined'
  ? (localStorage.getItem('report_lang') || 'zh-CN')
  : 'zh-CN')

// 中文翻译
const zhCN = {
  // 工具栏
  toolbar: {
    back: '返回编辑',
    title: 'FEAD 性能分析报告',
    pages: '共 {n} 页',
    print: '打印报告'
  },
  // 页面标题
  pages: {
    p1: 'FEAD 性能分析报告',
    p2: '布局数据结果',
    p3: '几何分析结果',
    p4: '几何分析结果（续）',
    p5: '动态分析结果',
    p6: '动态分析结果（续）',
    p7: '动态分析结果（续）'
  },
  // 项目信息
  projectInfo: 'Project Information',
  customer: '客户',
  projectName: '项目名称',
  cylinders: '发动机缸数',
  ratedPower: '额定功率',
  ratedSpeed: '额定转速',
  idleSpeed: '怠速转速',
  fileNo: 'File No. :',
  version: 'Version : ',
  date: 'Date :',
  problemStatement: 'Problem Statement :',
  analysisReference: 'Analysis Reference :',
  enginePower: 'Engine power',
  // 输入区块标题
  layoutInput: 'Layout Data (input)',
  geometryInput: 'Geometry Analysis (Input）',
  beltDataInput: 'Belt Data (input)',
  tensionerDataInput: 'Tensioner Data (input)',
  geometricDimension: 'Geometric Dimension :',
  beltHeight: 'Belt Height :',
  // 轮系布局
  layout: '轮系布局',
  // 皮带数据
  beltData: '皮带数据',
  beltType: '皮带类型',
  beltName: '皮带名称',
  ribType: '肋型',
  beltMaterial: '皮带材质',
  cordMaterial: '帘线材料',
  manufacturer: '厂家/型号',
  ribs: '肋数',
  effectiveLength: '有效长度',
  stretchWearAllow: '拉伸磨损余量',
  beltFlatToPitch: '平顶到节距',
  beltPitchToEffective: '节距到有效',
  // 张紧器
  tensionerData: '张紧器数据',
  tensionerType: '张紧器类型',
  torque: '扭矩',
  installAngle: '安装角度',
  armLength: '臂长',
  pivotPoint: 'Pivot Point {x,y} [mm]',
  tensionerArmAngle: '张紧器臂角度',
  designTension: '皮带设计张力',
  springRateFactor: '弹簧刚度系数',
  // 带轮布局数据
  pulleyLayout: '带轮布局数据',
  pulleyTable: {
    index: '序号',
    code: '编号',
    name: '名称',
    type: '类型',
    typeFlat: '平带轮',
    typeGroove: '槽轮',
    x: 'X (mm)',
    y: 'Y (mm)',
    flatDia: 'Flat 直径 (mm)',
    pitchDia: 'Pitch 直径 (mm)',
    effectiveDia: 'Effective 直径 (mm)',
    diameter: '直径 (mm)',
    noData: '暂无数据'
  },
  // 布局数据
  layoutResult: '布局数据结果',
  minBelt: 'Min Belt',
  nominalBelt: 'Nominal Belt',
  maxBelt: 'Max Belt',
  stretchWear: 'Stretch & wear',
  beltLength: '皮带长度',
  wrapMin: '包角(最小)',
  wrapNominal: '包角(名义)',
  wrapMax: '包角(最大)',
  stretch: '伸长量',
  wear: '磨损量',
  // 几何分析
  geometric: '几何分析结果',
  parameter: '参数',
  value: '数值',
  min: 'Min Belt',
  nominal: 'Nominal',
  max: 'Max Belt',
  unit: '单位',
  lengthTolerance: '长度公差',
  elongation: '延伸率',
  travelAngle: '行程角',
  tensionerPulleyGeom: '张紧轮几何参数',
  state: '状态',
  angle: '角度',
  pulleySystemGeom: '带轮系统几何参数',
  wrapAngle: '包角',
  spanIn: 'Span In',
  spanOut: 'Span Out',
  pulley: '带轮',
  pulleyPlaceholder: '轮',
  // 几何分析续
  axialOffset: '带轮轴向偏移允许值',
  allowOffsetMm: '允许偏移 (mm)',
  allowOffsetDeg: '允许偏移 (deg)',
  dynamicInput: '动态分析输入 - 负载数据',
  condition: '工况',
  dutyCycle: '占空比',
  speed: '转速',
  temperature: '温度',
  idle: '怠速',
  rated: '额定',
  maxTorque: '最大扭矩',
  accessoryLoad: '附件负载数据',
  accessory: '附件',
  accessoryPlaceholder: '附件',
  accessoryInertia: '附件惯性和加速度',
  inertia: '惯性',
  angularAccel: '角加速度',
  // 动态分析
  dynamic: '动态分析结果',
  slipSafetyFactor: '皮带打滑安全系数',
  safety: '安全',
  warning: '警告',
  danger: '危险',
  slipSummary: '打滑安全系数汇总',
  evaluation: '评定',
  pending: '待计算',
  averageHubLoad: '带轮平均轮毂载荷',
  peakHubLoad: '带轮峰值轮毂载荷',
  avgBeltTension: '皮带平均张力',
  tightTension: '紧边张力',
  slackTension: '松边张力',
  avgTension: '平均张力',
  ribFatigue: '皮带肋疲劳数据',
  maxBendingStress: '最大弯曲应力',
  cycles: '循环次数',
  flexLife: '皮带挠曲寿命和 B10 寿命',
  b10Life: 'B10 寿命',
  flexLifeCycles: '挠曲寿命',
  hour: '小时',
  cycle: '循环',
  // 频率分析
  freqAnalysis: '皮带跨度固有频率分析',
  freqLabel: '频率(Hz)',
  spanLabel: '跨度',
  idleExcitation: '怠速激励',
  freqTable: '固有频率数据表',
  firstOrder: '一阶频率',
  secondOrder: '二阶频率',
  thirdOrder: '三阶频率',
  span: '跨度',
  freqNote: '频率窗口说明',
  idleExcitationDesc: '怠速激励频率：由发动机怠速转速和气缸数决定',
  attention: '注意事项',
  resonanceNote: '皮带跨度的各阶固有频率应避开怠速激励频率及其倍频，以避免共振。',
  evalResult: '评定结果',
  reportEnd: '— 报告结束 —',
  generatedAt: '生成时间'
}

// 英文翻译
const enUS = {
  toolbar: {
    back: 'Back to Edit',
    title: 'FEAD Performance Analysis Report',
    pages: 'Total {n} pages',
    print: 'Print Report'
  },
  pages: {
    p1: 'FEAD Performance Analysis Report',
    p2: 'Layout Data Results',
    p3: 'Geometric Analysis Results',
    p4: 'Geometric Analysis Results (Cont.)',
    p5: 'Dynamic Analysis Results',
    p6: 'Dynamic Analysis Results (Cont.)',
    p7: 'Dynamic Analysis Results (Cont.)'
  },
  projectInfo: 'Project Information',
  customer: 'Customer',
  projectName: 'Project Name',
  cylinders: 'Engine Cylinders',
  ratedPower: 'Rated Power',
  ratedSpeed: 'Rated Speed',
  idleSpeed: 'Idle Speed',
  fileNo: 'File No. :',
  version: 'Version : ',
  date: 'Date :',
  problemStatement: 'Problem Statement :',
  analysisReference: 'Analysis Reference :',
  enginePower: 'Engine power',
  layoutInput: 'Layout Data (input)',
  geometryInput: 'Geometry Analysis (Input）',
  beltDataInput: 'Belt Data (input)',
  tensionerDataInput: 'Tensioner Data (input)',
  geometricDimension: 'Geometric Dimension :',
  beltHeight: 'Belt Height :',
  layout: 'Pulley Layout',
  beltData: 'Belt Data',
  beltType: 'Belt Type',
  beltName: 'Belt Name',
  ribType: 'Rib Type',
  beltMaterial: 'Belt Material',
  cordMaterial: 'Cord Material',
  manufacturer: 'Manufacturer/Model',
  ribs: 'Ribs',
  effectiveLength: 'Effective Length',
  stretchWearAllow: 'Stretch & Wear Allow',
  beltFlatToPitch: 'Belt Flat to Pitch',
  beltPitchToEffective: 'Belt Pitch to Effective',
  tensionerData: 'Tensioner Data',
  tensionerType: 'Tensioner Type',
  torque: 'Torque',
  installAngle: 'Installation Angle',
  armLength: 'Arm Length',
  pivotPoint: 'Pivot Point {x,y} [mm]',
  tensionerArmAngle: 'Tensioner Arm Angle',
  designTension: 'Belt Design Tension',
  springRateFactor: 'Spring Rate Factor',
  pulleyLayout: 'Pulley Layout Data',
  pulleyTable: {
    index: 'No.',
    code: 'Code',
    name: 'Name',
    type: 'Type',
    typeFlat: 'Flat',
    typeGroove: 'Groove',
    x: 'X (mm)',
    y: 'Y (mm)',
    flatDia: 'Flat Dia. (mm)',
    pitchDia: 'Pitch Dia. (mm)',
    effectiveDia: 'Effective Dia. (mm)',
    diameter: 'Diameter (mm)',
    noData: 'No data'
  },
  layoutResult: 'Layout Data Results',
  minBelt: 'Min Belt',
  nominalBelt: 'Nominal Belt',
  maxBelt: 'Max Belt',
  stretchWear: 'Stretch & Wear',
  beltLength: 'Belt Length',
  wrapMin: 'Wrap (Min)',
  wrapNominal: 'Wrap (Nominal)',
  wrapMax: 'Wrap (Max)',
  stretch: 'Stretch',
  wear: 'Wear',
  geometric: 'Geometric Analysis Results',
  parameter: 'Parameter',
  value: 'Value',
  min: 'Min Belt',
  nominal: 'Nominal',
  max: 'Max Belt',
  unit: 'Unit',
  lengthTolerance: 'Length Tolerance',
  elongation: 'Elongation',
  travelAngle: 'Travel Angle',
  tensionerPulleyGeom: 'Tensioner Pulley Geometry',
  state: 'State',
  angle: 'Angle',
  pulleySystemGeom: 'Pulley System Geometry',
  wrapAngle: 'Wrap Angle',
  spanIn: 'Span In',
  spanOut: 'Span Out',
  pulley: 'Pulley',
  pulleyPlaceholder: 'P',
  axialOffset: 'Allowable Axial Offset of Pulleys',
  allowOffsetMm: 'Allowable Offset (mm)',
  allowOffsetDeg: 'Allowable Offset (deg)',
  dynamicInput: 'Dynamic Analysis Input - Load Data',
  condition: 'Condition',
  dutyCycle: 'Duty Cycle',
  speed: 'Speed',
  temperature: 'Temperature',
  idle: 'Idle',
  rated: 'Rated',
  maxTorque: 'Max Torque',
  accessoryLoad: 'Accessory Load Data',
  accessory: 'Accessory',
  accessoryPlaceholder: 'Acc',
  accessoryInertia: 'Accessory Inertia & Acceleration',
  inertia: 'Inertia',
  angularAccel: 'Angular Accel.',
  dynamic: 'Dynamic Analysis Results',
  slipSafetyFactor: 'Belt Slip Safety Factor',
  safety: 'Safe',
  warning: 'Warning',
  danger: 'Danger',
  slipSummary: 'Slip Safety Factor Summary',
  evaluation: 'Evaluation',
  pending: 'Pending',
  averageHubLoad: 'Average Pulley Hub Load',
  peakHubLoad: 'Peak Pulley Hub Load',
  avgBeltTension: 'Average Belt Tension',
  tightTension: 'Tight Side Tension',
  slackTension: 'Slack Side Tension',
  avgTension: 'Average Tension',
  ribFatigue: 'Belt Rib Fatigue Data',
  maxBendingStress: 'Max Bending Stress',
  cycles: 'Cycles',
  flexLife: 'Belt Flex Life & B10 Life',
  b10Life: 'B10 Life',
  flexLifeCycles: 'Flex Life',
  hour: 'hr',
  cycle: 'cyc',
  freqAnalysis: 'Belt Span Natural Frequency Analysis',
  freqLabel: 'Freq(Hz)',
  spanLabel: 'Span',
  idleExcitation: 'Idle Excitation',
  freqTable: 'Natural Frequency Data Table',
  firstOrder: '1st Order',
  secondOrder: '2nd Order',
  thirdOrder: '3rd Order',
  span: 'Span',
  freqNote: 'Frequency Window Notes',
  idleExcitationDesc: 'Idle excitation frequency is determined by engine idle speed and number of cylinders.',
  attention: 'Notes',
  resonanceNote: 'Belt span natural frequencies of all orders should avoid the idle excitation frequency and its multiples to prevent resonance.',
  evalResult: 'Evaluation Result',
  reportEnd: '— End of Report —',
  generatedAt: 'Generated at'
}

const messages = {
  'zh-CN': zhCN,
  'en-US': enUS
}

export function setLang(lang) {
  if (SUPPORTED_LANGS.includes(lang)) {
    currentLang.value = lang
    if (typeof window !== 'undefined') {
      localStorage.setItem('report_lang', lang)
    }
  }
}

export function getLang() {
  return currentLang.value
}

// 翻译函数（支持 {n} 占位符）
export function t(key) {
  const dict = messages[currentLang.value] || messages['zh-CN']
  const keys = key.split('.')
  let val = dict
  for (const k of keys) {
    if (val && typeof val === 'object' && k in val) {
      val = val[k]
    } else {
      return key
    }
  }
  if (typeof val === 'string') {
    // 替换 {n} 占位符
    const args = Array.prototype.slice.call(arguments, 1)
    return val.replace(/\{(\w+)\}/g, (_, name) => {
      if (name === 'n') return args[0] !== undefined ? args[0] : `{${name}}`
      return `{${name}}`
    })
  }
  return val
}

// 响应式当前语言
export const lang = currentLang

// 切换语言
export function toggleLang() {
  setLang(currentLang.value === 'zh-CN' ? 'en-US' : 'zh-CN')
}
