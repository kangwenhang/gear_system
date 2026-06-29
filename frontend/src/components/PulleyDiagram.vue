<template>
  <div class="wrap" ref="wrapRef"
    @wheel.prevent="handleWheel"
    @mousedown="onPanStart"
    @mousemove="onPanMove"
    @mouseup="onPanEnd"
    @mouseleave="onPanEnd"
    @touchstart.prevent="onTouchStart"
    @touchmove.prevent="onTouchMove"
    @touchend="onPanEnd"
  >
    <div class="zoom-controls">
      <button type="button" @click="zoomIn" :disabled="zoom >= maxZoom">+</button>
      <span>{{ zoomLevel }}%</span>
      <button type="button" @click="zoomOut" :disabled="zoom <= minZoom">-</button>
      <button type="button" @click="resetZoom">重置</button>
    </div>
    <svg class="diagram" :viewBox="viewBoxStr" preserveAspectRatio="xMidYMid meet">
      <!-- 定义裁剪路径，限制网格线在坐标轴内部 -->
      <defs>
        <clipPath id="axisClip">
          <rect :x="pad" :y="pad" :width="w - 2*pad" :height="h - 2*pad"/>
        </clipPath>
      </defs>
      
      <!-- 网格（只显示在坐标轴内部，应用裁剪） -->
      <g v-if="showGrid" class="grid" clip-path="url(#axisClip)">
        <!-- X方向网格线（垂直） -->
        <line v-for="x in xticks" :key="'x'+x" :x1="x" :y1="pad" :x2="x" :y2="h-pad" stroke="#eee" stroke-width="1"/>
        <!-- Y方向网格线（水平） -->
        <line v-for="y in yticks" :key="'y'+y" :x1="pad" :y1="y" :x2="w-pad" :y2="y" stroke="#eee" stroke-width="1"/>
      </g>

      <!-- 坐标轴（含箭头） -->
      <g class="axis">
        <!-- X轴线（只延长右边） -->
        <line :x1="pad" :y1="axisYZero" :x2="w-pad+10" :y2="axisYZero" stroke="#333" stroke-width="2"/>
        <!-- X 轴箭头 -->
        <path :d="xArrowPath" fill="#333"/>

        <!-- Y 轴线（只延长上边） -->
        <line :x1="axisXZero" :y1="pad-10" :x2="axisXZero" :y2="h-pad" stroke="#333" stroke-width="2"/>
        <!-- Y 轴箭头 -->
        <path :d="yArrowPath" fill="#333"/>

        <!-- X 轴刻度 & 标签 -->
        <g class="x-ticks">
          <line v-for="t in xticks" :key="'xt'+t" :x1="t" :y1="axisYZero" :x2="t" :y2="axisYZero+5" stroke="#333" stroke-width="2"/>
          <text v-for="t in xticks" :key="'xtl'+t" :x="t" :y="axisYZero+15" text-anchor="middle" font-size="12">
            {{ formatMM(t, 'x') }}
          </text>
        </g>

        <!-- Y 轴刻度 & 标签 -->
        <g class="y-ticks">
          <line v-for="t in yticks" :key="'yt'+t" :x1="axisXZero-5" :y1="t" :x2="axisXZero" :y2="t" stroke="#333" stroke-width="2"/>
          <text v-for="t in yticks" :key="'ytl'+t" :x="axisXZero-13" :y="t+4" text-anchor="middle" font-size="12">
            {{ formatMM(t, 'y') }}
          </text>
        </g>

        <!-- 轴标签 - 固定在底部和左侧 -->
        <text :x="w/2" :y="h-15" text-anchor="middle" font-size="14" font-weight="bold">X (mm)</text>
        <text :x="20" :y="h/2" text-anchor="middle" font-size="14" font-weight="bold" :transform="`rotate(-90, 20, ${h/2})`">Y (mm)</text>
      </g>

      <!-- 皮带线 -->
      <g class="belts">
        <path 
          v-for="(belt, index) in belts" 
          :key="'belt-'+index"
          :d="belt.path"
          stroke="#52c41a"
          stroke-width="3"
          fill="none"
          stroke-linecap="round"
        />
      </g>
      
      <!-- 带轮 -->
      <g v-for="p in pulleys" :key="p.name">
        <circle 
          :cx="p.cx" 
          :cy="p.cy" 
          :r="p.r" 
          :fill="p.type==='flat'?'#e6f7ff':'#fff7e6'" 
          :stroke="p.type==='flat'?'#1890ff':'#fa8c16'" 
          stroke-width="2"
        />
        
        <!-- 轮子名称（放在圆心） -->
        <text 
          :x="p.cx" 
          :y="p.cy - 5" 
          text-anchor="middle" 
          font-size="12" 
          font-weight="bold"
          fill="#333"
        >
          {{ p.name }}
        </text>
        
        <!-- 轮子直径（放在圆心下方） -->
        <text 
          :x="p.cx" 
          :y="p.cy + 15" 
          text-anchor="middle" 
          font-size="10" 
          fill="#666"
        >
          Ø{{ p.dia.toFixed(1) }}
        </text>
      </g>

      <!-- 自动张紧器臂杆连线 -->
      <g v-if="tensionerLine.show" class="tensioner-arm">
        <!-- 枢轴点 -->
        <circle 
          :cx="tensionerLine.pivotX" 
          :cy="tensionerLine.pivotY" 
          :r="Math.max(4, tensionerLine.headSize * 0.5)" 
          fill="none" 
          stroke="#000000" 
          stroke-width="2"
          stroke-dasharray="5,3"
        />
        <!-- 枢轴点标签 -->
        <text 
          :x="tensionerLine.pivotX" 
          :y="tensionerLine.pivotY - Math.max(15, tensionerLine.headSize * 0.5 + 7)" 
          text-anchor="middle" 
          font-size="10" 
          font-weight="bold"
          fill="#d4380d"
        >
          枢轴点
        </text>
        <!-- 坐标标签 -->
        <text 
          :x="tensionerLine.pivotX" 
          :y="tensionerLine.pivotY + Math.max(20, tensionerLine.headSize * 0.5 + 12)" 
          text-anchor="middle" 
          font-size="8" 
          fill="#666"
        >
          ({{ tensionerLine.pivotXDisplay }}, {{ tensionerLine.pivotYDisplay }})
        </text>
        
        <!-- 张紧器臂杆 -->
        <line 
          :x1="tensionerLine.pivotX" 
          :y1="tensionerLine.pivotY" 
          :x2="tensionerLine.pulleyX" 
          :y2="tensionerLine.pulleyY" 
          stroke="#000000" 
          stroke-width="2"
        />
      </g>

      <!-- 手调张紧轮调节行程线 -->
      <g v-if="manualLine.show" class="manual-travel-line">
        <!-- 起始点 -->
        <circle 
          :cx="manualLine.startSvgX" 
          :cy="manualLine.startSvgY" 
          r="4" 
          fill="#409eff" 
          stroke="#000000" 
          stroke-width="1.5"
        />
        <text 
          :x="manualLine.startSvgX" 
          :y="manualLine.startSvgY - 8" 
          text-anchor="middle" 
          font-size="9" 
          font-weight="bold"
          fill="#333"
        >
          起始
        </text>
        <!-- 结束点 -->
        <circle 
          :cx="manualLine.endSvgX" 
          :cy="manualLine.endSvgY" 
          r="4" 
          fill="#409eff" 
          stroke="#000000" 
          stroke-width="1.5"
        />
        <text 
          :x="manualLine.endSvgX" 
          :y="manualLine.endSvgY - 8" 
          text-anchor="middle" 
          font-size="9" 
          font-weight="bold"
          fill="#333"
        >
          结束
        </text>
        <!-- 起始到结束的直线 -->
        <line 
          :x1="manualLine.startSvgX" 
          :y1="manualLine.startSvgY" 
          :x2="manualLine.endSvgX" 
          :y2="manualLine.endSvgY" 
          stroke="#000000" 
          stroke-width="2"
        />
      </g>
    </svg>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({ 
  data: Array,
  tensionerData: Object
})

const wrapRef = ref(null)
const w = 800, h = 650, pad = 80, showGrid = true
const minZoom = 0.3, maxZoom = 5, zoomStep = 0.1
const zoom = ref(1)
const zoomLevel = computed(() => Math.round(zoom.value * 100))

// 平移偏移（viewBox 坐标系）
const panX = ref(0)
const panY = ref(0)
const isPanning = ref(false)
const panStartX = ref(0)
const panStartY = ref(0)
const panStartPanX = ref(0)
const panStartPanY = ref(0)

// viewBox 字符串：通过缩放和平移控制可视区域
const viewBoxStr = computed(() => {
  const vw = w / zoom.value
  const vh = h / zoom.value
  const vx = panX.value
  const vy = panY.value
  return `${vx} ${vy} ${vw} ${vh}`
})

const zoomIn = () => {
  zoomAtCenter(1)
}

const zoomOut = () => {
  zoomAtCenter(-1)
}

// 以容器中心为锚点缩放
function zoomAtCenter(direction) {
  const oldZoom = zoom.value
  const newZoom = direction > 0
    ? Math.min(maxZoom, +(oldZoom + zoomStep).toFixed(2))
    : Math.max(minZoom, +(oldZoom - zoomStep).toFixed(2))
  if (newZoom === oldZoom) return

  // 缩放前 viewBox 中心对应的坐标
  const oldVw = w / oldZoom
  const oldVh = h / oldZoom
  const cx = panX.value + oldVw / 2
  const cy = panY.value + oldVh / 2

  // 缩放后保持中心不变
  const newVw = w / newZoom
  const newVh = h / newZoom
  panX.value = cx - newVw / 2
  panY.value = cy - newVh / 2
  zoom.value = newZoom
}

const resetZoom = () => {
  zoom.value = 1
  panX.value = 0
  panY.value = 0
}

// 鼠标滚轮缩放（以鼠标位置为锚点）
const handleWheel = (event) => {
  const rect = wrapRef.value?.getBoundingClientRect()
  if (!rect) return

  // 鼠标在容器中的比例位置
  const mx = (event.clientX - rect.left) / rect.width
  const my = (event.clientY - rect.top) / rect.height

  const oldZoom = zoom.value
  const newZoom = event.deltaY < 0
    ? Math.min(maxZoom, +(oldZoom + zoomStep).toFixed(2))
    : Math.max(minZoom, +(oldZoom - zoomStep).toFixed(2))
  if (newZoom === oldZoom) return

  // 鼠标在 viewBox 坐标系中的位置
  const oldVw = w / oldZoom
  const oldVh = h / oldZoom
  const anchorX = panX.value + mx * oldVw
  const anchorY = panY.value + my * oldVh

  // 缩放后保持锚点不变
  const newVw = w / newZoom
  const newVh = h / newZoom
  panX.value = anchorX - mx * newVw
  panY.value = anchorY - my * newVh
  zoom.value = newZoom
}

// 拖拽平移 - 鼠标
function onPanStart(e) {
  if (e.button !== 0) return
  isPanning.value = true
  panStartX.value = e.clientX
  panStartY.value = e.clientY
  panStartPanX.value = panX.value
  panStartPanY.value = panY.value
  wrapRef.value.style.cursor = 'grabbing'
}

function onPanMove(e) {
  if (!isPanning.value) return
  const rect = wrapRef.value?.getBoundingClientRect()
  if (!rect) return

  const dx = e.clientX - panStartX.value
  const dy = e.clientY - panStartY.value

  // 将像素偏移转换为 viewBox 坐标偏移
  const vw = w / zoom.value
  const vh = h / zoom.value
  panX.value = panStartPanX.value - (dx / rect.width) * vw
  panY.value = panStartPanY.value - (dy / rect.height) * vh
}

function onPanEnd() {
  isPanning.value = false
  if (wrapRef.value) wrapRef.value.style.cursor = 'grab'
}

// 拖拽平移 - 触摸
function onTouchStart(e) {
  if (e.touches.length === 1) {
    isPanning.value = true
    panStartX.value = e.touches[0].clientX
    panStartY.value = e.touches[0].clientY
    panStartPanX.value = panX.value
    panStartPanY.value = panY.value
  }
}

function onTouchMove(e) {
  if (!isPanning.value || e.touches.length !== 1) return
  const rect = wrapRef.value?.getBoundingClientRect()
  if (!rect) return

  const dx = e.touches[0].clientX - panStartX.value
  const dy = e.touches[0].clientY - panStartY.value

  const vw = w / zoom.value
  const vh = h / zoom.value
  panX.value = panStartPanX.value - (dx / rect.width) * vw
  panY.value = panStartPanY.value - (dy / rect.height) * vh
}

// 1. 原始数据处理
const raw = computed(() => {
  const data = props.data || []
  const result = []
  for (let i = 0; i < data.length; i++) {
    const p = data[i]
    const dia = p.type === 'flat' ? p.flat_dia : p.groove_dia
    const r = dia / 2
    if (r > 0 && p.x !== null && p.x !== undefined && p.y !== null && p.y !== undefined) {
      result.push({
        ...p,
        dia,
        r
      })
    }
  }
  return result
})

// 2. 物理边界
const physicalBounds = computed(() => {
  if (!raw.value.length) return { minX: 0, maxX: 200, minY: 0, maxY: 200 }
  
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity
  raw.value.forEach(p => {
    minX = Math.min(minX, p.x - p.r)
    maxX = Math.max(maxX, p.x + p.r)
    minY = Math.min(minY, p.y - p.r)
    maxY = Math.max(maxY, p.y + p.r)
  })
  return { minX, maxX, minY, maxY }
})

// 3. 轮系中心 = (最大值 + 最小值) / 2
const systemCenterX = computed(() => {
  const pb = physicalBounds.value
  return (pb.minX + pb.maxX) / 2
})
const systemCenterY = computed(() => {
  const pb = physicalBounds.value
  return (pb.minY + pb.maxY) / 2
})

// 4. 显示边界 - 确保0点在左下角
const displayBounds = computed(() => {
  const pb = physicalBounds.value
  
  // 计算需要的范围
  const xRange = pb.maxX - pb.minX
  const yRange = pb.maxY - pb.minY
  
  // 扩展范围，适当扩大以显示更多刻度
  const extendX = Math.max(xRange * 0.15, 50)
  const extendY = Math.max(yRange * 0.15, 50)
  
  // 确保显示范围包含0点，并且从0开始
  const minX = Math.min(pb.minX - extendX, 0)
  const maxX = pb.maxX + extendX
  const minY = Math.min(pb.minY - extendY, 0)
  const maxY = pb.maxY + extendY
  
  return { minX, maxX, minY, maxY }
})

// 5. 缩放比例
const scale = computed(() => {
  const db = displayBounds.value
  const dataW = db.maxX - db.minX || 1
  const dataH = db.maxY - db.minY || 1
  const availW = w - 2 * pad
  const availH = h - 2 * pad
  return Math.min(availW / dataW, availH / dataH)
})

// 6. 坐标映射 - 简化版，移除居中偏移
const mapX = x => {
  const db = displayBounds.value
  return Math.round(pad + (x - db.minX) / (db.maxX - db.minX) * (w - 2 * pad))
}

const mapY = y => {
  const db = displayBounds.value
  return Math.round(h - pad - (y - db.minY) / (db.maxY - db.minY) * (h - 2 * pad))
}

// 7. 坐标轴位置 - 固定在左下角
const axisXZero = computed(() => pad)
const axisYZero = computed(() => h - pad)

// 8. 箭头路径
const arrowSize = 5
const xArrowPath = computed(() => {
  const x = w - pad + 10
  const y = axisYZero.value
  return `M ${x} ${y} L ${x - arrowSize} ${y - arrowSize} L ${x - arrowSize} ${y + arrowSize} Z`
})
const yArrowPath = computed(() => {
  const x = axisXZero.value
  const y = pad - 10
  return `M ${x} ${y} L ${x - arrowSize} ${y + arrowSize} L ${x + arrowSize} ${y + arrowSize} Z`
})

// 9. 张紧器臂杆连线数据
const tensionerLine = computed(() => {
  const tensioner = props.tensionerData || {}
  const pivotX = tensioner.automatic?.pivot_x
  const pivotY = tensioner.automatic?.pivot_y
  const headSize = tensioner.automatic?.head_size || 8 // 默认值8
  
  // 需要找到张紧轮的坐标（表格最后一行）
  const tableData = props.data || []
  const lastRow = tableData[tableData.length - 1]
  const pulleyX = lastRow?.x
  const pulleyY = lastRow?.y
  
  const show = pivotX != null && pivotY != null && pulleyX != null && pulleyY != null
  
  return {
    show,
    pivotX: show ? mapX(pivotX) : 0,
    pivotY: show ? mapY(pivotY) : 0,
    pulleyX: show ? mapX(pulleyX) : 0,
    pulleyY: show ? mapY(pulleyY) : 0,
    pivotXDisplay: pivotX?.toFixed(2) || '',
    pivotYDisplay: pivotY?.toFixed(2) || '',
    headSize: headSize // 添加头部大小
  }
})

// 9.1 手调张紧轮调节行程线数据
const manualLine = computed(() => {
  const tensioner = props.tensionerData || {}
  const manual = tensioner.manual || {}
  const startX = manual.start_x
  const startY = manual.start_y
  const endX = manual.end_x
  const endY = manual.end_y

  const show = startX != null && startY != null && endX != null && endY != null

  return {
    show,
    startSvgX: show ? mapX(startX) : 0,
    startSvgY: show ? mapY(startY) : 0,
    endSvgX: show ? mapX(endX) : 0,
    endSvgY: show ? mapY(endY) : 0
  }
})

// 10. 最终渲染数据
const pulleys = computed(() => 
  raw.value.map(p => ({
    ...p,
    cx: mapX(p.x),
    cy: mapY(p.y),
    r: p.r * scale.value
  }))
)

// 计算两个圆的公切线
// 返回四条切线：[外切1, 外切2, 内切1, 内切2]
const getTangents = (a, b) => {
  const x1 = a.cx, y1 = a.cy, r1 = a.r
  const x2 = b.cx, y2 = b.cy, r2 = b.r
  const dx = x2 - x1, dy = y2 - y1
  const dSq = dx * dx + dy * dy
  
  if (dSq === 0) return []
  
  const d = Math.sqrt(dSq)
  const vx = dx / d, vy = dy / d
  
  const tangents = []
  
  // 外切线
  const rDiff = r1 - r2
  const h = Math.sqrt(Math.max(0, dSq - rDiff * rDiff))
  const nx = -vy, ny = vx
  
  const c1x1 = x1 + r1 * (vx * rDiff / d - nx * h / d)
  const c1y1 = y1 + r1 * (vy * rDiff / d - ny * h / d)
  const c2x1 = x2 + r2 * (vx * rDiff / d - nx * h / d)
  const c2y1 = y2 + r2 * (vy * rDiff / d - ny * h / d)
  tangents.push({ p1: { x: c1x1, y: c1y1 }, p2: { x: c2x1, y: c2y1 }, type: 'external' })
  
  const c1x2 = x1 + r1 * (vx * rDiff / d + nx * h / d)
  const c1y2 = y1 + r1 * (vy * rDiff / d + ny * h / d)
  const c2x2 = x2 + r2 * (vx * rDiff / d + nx * h / d)
  const c2y2 = y2 + r2 * (vy * rDiff / d + ny * h / d)
  tangents.push({ p1: { x: c1x2, y: c1y2 }, p2: { x: c2x2, y: c2y2 }, type: 'external' })
  
  // 内切线
  const rSum = r1 + r2
  const h2 = Math.sqrt(Math.max(0, dSq - rSum * rSum))
  if (h2 > 0.001) {
    const c1x3 = x1 + r1 * (vx * rSum / d - nx * h2 / d)
    const c1y3 = y1 + r1 * (vy * rSum / d - ny * h2 / d)
    const c2x3 = x2 - r2 * (vx * rSum / d - nx * h2 / d)
    const c2y3 = y2 - r2 * (vy * rSum / d - ny * h2 / d)
    tangents.push({ p1: { x: c1x3, y: c1y3 }, p2: { x: c2x3, y: c2y3 }, type: 'internal' })
    
    const c1x4 = x1 + r1 * (vx * rSum / d + nx * h2 / d)
    const c1y4 = y1 + r1 * (vy * rSum / d + ny * h2 / d)
    const c2x4 = x2 - r2 * (vx * rSum / d + nx * h2 / d)
    const c2y4 = y2 - r2 * (vy * rSum / d + ny * h2 / d)
    tangents.push({ p1: { x: c1x4, y: c1y4 }, p2: { x: c2x4, y: c2y4 }, type: 'internal' })
  }
  
  return tangents
}

// 计算点到圆心的角度
const getAngle = (cx, cy, px, py) => {
  return Math.atan2(py - cy, px - cx)
}

// 11. 皮带线计算 - 简化版：先连接轮子中心
const belts = computed(() => {
  const pls = pulleys.value
  if (!pls || pls.length < 2) {
    return []
  }
  
  // 先收集切线点，暂时简化为直接连接轮子边缘
  const tangentPoints = []
  
  for (let i = 0; i < pls.length; i++) {
    const a = pls[i]
    const b = pls[(i + 1) % pls.length]
    const tangents = getTangents(a, b)
    
    if (tangents.length < 2) continue
    
    // 选择切线
    let candidates = []
    if (a.type === b.type) {
      candidates = tangents.filter(t => t.type === 'external')
      if (candidates.length === 0) candidates = tangents
    } else {
      candidates = tangents.filter(t => t.type === 'internal')
      if (candidates.length === 0) candidates = tangents
    }
    
    let chosenTangent = candidates[0]
    if (candidates.length >= 2) {
      const t1 = candidates[0]
      const t2 = candidates[1]
      // 规律：起点是槽轮选第2个，起点是平轮选第1个
      if (a.type === 'groove') {
        chosenTangent = t2
      } else {
        chosenTangent = t1
      }
    }
    
    tangentPoints.push({
      a: chosenTangent.p1,
      b: chosenTangent.p2
    })
  }
  
  // 构建路径 - 先只画直线，测试切线选择
  let path = ''
  if (tangentPoints.length > 0) {
    // 依次连接所有的切线点
    path = `M ${tangentPoints[0].a.x} ${tangentPoints[0].a.y}`
    
    for (let i = 0; i < tangentPoints.length; i++) {
      const current = tangentPoints[i]
      const next = tangentPoints[(i + 1) % tangentPoints.length]
      
      // 先到 Exit 点
      path += ` L ${current.b.x} ${current.b.y}`
      // 再到下一个 Entry 点
      path += ` L ${next.a.x} ${next.a.y}`
    }
  }
  
  path += ` Z`
  
  return [{ path }]
})

// 12. 坐标轴刻度 - 确保显示0刻度
const xticks = computed(() => {
  const db = displayBounds.value
  const range = db.maxX - db.minX
  // 根据范围调整刻度间隔
  let step = 50
  if (range > 500) step = 100
  if (range > 1000) step = 200
  const ticks = []
  // 确保包含0刻度
  const start = Math.min(0, Math.floor(db.minX / step) * step)
  const end = Math.max(0, Math.ceil(db.maxX / step) * step)
  for (let x = start; x <= end; x += step) {
    ticks.push(mapX(x))
  }
  return ticks
})
const yticks = computed(() => {
  const db = displayBounds.value
  const range = db.maxY - db.minY
  // 根据范围调整刻度间隔
  let step = 50
  if (range > 500) step = 100
  if (range > 1000) step = 200
  const ticks = []
  // 确保包含0刻度
  const start = Math.min(0, Math.floor(db.minY / step) * step)
  const end = Math.max(0, Math.ceil(db.maxY / step) * step)
  for (let y = start; y <= end; y += step) {
    ticks.push(mapY(y))
  }
  return ticks
})

// 13. 刻度值转换
const formatMM = (px, axis) => {
  if (axis === 'x') {
    const db = displayBounds.value
    const range = db.maxX - db.minX
    let step = 50
    if (range > 500) step = 100
    if (range > 1000) step = 200
    const relativePos = (px - pad) / (w - 2 * pad)
    const value = db.minX + relativePos * range
    // 确保刻度值是step的倍数
    return Math.round(value / step) * step
  } else {
    const db = displayBounds.value
    const range = db.maxY - db.minY
    let step = 50
    if (range > 500) step = 100
    if (range > 1000) step = 200
    const relativePos = (h - pad - px) / (h - 2 * pad)
    const value = db.minY + relativePos * range
    // 确保刻度值是step的倍数
    return Math.round(value / step) * step
  }
}
</script>

<style scoped>
.wrap {
  background: #fafafa;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
  cursor: grab;
  user-select: none;
  -webkit-user-select: none;
  min-height: 300px;
}

.wrap:active {
  cursor: grabbing;
}

.zoom-controls {
  position: absolute;
  top: 16px;
  left: 16px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 6px;
  padding: 6px 8px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  transition: background-color 0.2s ease, opacity 0.2s ease;
  opacity: 0.2;
}

.zoom-controls:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.96);
}

.zoom-controls span {
  min-width: auto;
}

.zoom-controls button {
  min-width: 30px;
  padding: 4px 8px;
  border: 1px solid #ccc;
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.zoom-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.zoom-controls span {
  min-width: 42px;
  text-align: center;
  font-weight: 600;
  font-size: 12px;
}

svg.diagram {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 100%;
  height: 100%;
  max-height: 70vh;
}

.grid line {
  stroke-dasharray: 2,2;
}

.tensioner-arm line {
  pointer-events: none;
}
</style>