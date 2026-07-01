<template>
  <div class="alignment-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="page-header-left">
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2v20M2 12h20"/>
          <circle cx="12" cy="12" r="3"/>
          <circle cx="12" cy="12" r="9" stroke-dasharray="2 2"/>
        </svg>
        <h2 class="page-title">对齐度计算</h2>
        <span class="page-subtitle">轮系对齐分析</span>
      </div>
    </div>

    <!-- 带轮对齐度输入 -->
    <el-card shadow="hover" class="input-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 6v6l4 2"/>
          </svg>
          <span>带轮对齐度参数</span>
          <span class="card-tip">（数据来自轮系布局，填写中心高和垂直度）</span>
        </div>
      </template>

      <div class="pulley-table-wrapper" v-if="pulleys.length > 0">
        <table class="pulley-table">
          <thead>
            <tr>
              <th style="width: 60px">序号</th>
              <th>带轮编号</th>
              <th>带轮名称</th>
              <th style="width: 160px">中心高 (mm)</th>
              <th style="width: 180px">垂直度 (°)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, idx) in pulleys" :key="idx">
              <td style="text-align: center; color: #909399">{{ idx + 1 }}</td>
              <td style="text-align: center">
                <span class="pulley-code">{{ p.code || '--' }}</span>
              </td>
              <td style="text-align: center">{{ p.name || '--' }}</td>
              <td>
                <el-input
                v-model="p.centerHeightDiff"
                placeholder="请输入"
                style="width: 100%; text-align: center"
              />
              </td>
              <td>
                <el-input
                v-model="p.perpendicularity"
                placeholder="请输入"
                style="width: 100%; text-align: center"
              />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="empty-tip" v-else>
        <el-empty description="暂无带轮数据，请先在轮系布局页面添加带轮" />
      </div>
    </el-card>

    <!-- 计算结果 -->
    <el-card v-if="alignmentPairs.length > 0" shadow="hover" class="result-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 11 12 14 22 4"/>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
          </svg>
          <span>对齐度结果</span>
          <span class="card-tip">（共 {{ alignmentPairs.length }} 组带轮对）</span>
        </div>
      </template>

      <div class="result-table-wrapper">
        <table class="result-table">
          <thead>
            <tr>
              <th rowspan="2" style="width: 60px">序号</th>
              <th rowspan="2">带轮对</th>
              <th rowspan="2" style="width: 120px">类型</th>
              <th colspan="3" class="group-header group-groove">槽轮-槽轮</th>
              <th colspan="2" class="group-header group-flat">槽轮-平轮-槽轮</th>
            </tr>
            <tr>
              <th class="group-groove">切入角BEA (°)</th>
              <th class="group-groove">Twist (°)</th>
              <th class="group-groove">Offset (mm)</th>
              <th class="group-flat">切入角BEA (°)</th>
              <th class="group-flat">Twist (°)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(pair, idx) in alignmentPairs" :key="idx">
              <td style="color: #909399">{{ idx + 1 }}</td>
              <td>
                <span class="pair-codes">
                  <span class="pulley-code">{{ pair.fromCode }}</span>
                  <span class="pair-arrow">→</span>
                  <span v-if="pair.middleCode" class="pulley-code pulley-code-flat">{{ pair.middleCode }}</span>
                  <span v-if="pair.middleCode" class="pair-arrow">→</span>
                  <span class="pulley-code">{{ pair.toCode }}</span>
                </span>
              </td>
              <td>
                <el-tag :type="pair.type === 'groove-groove' ? 'primary' : 'success'" size="small">
                  {{ pair.type === 'groove-groove' ? '槽轮-槽轮' : '槽轮-平轮-槽轮' }}
                </el-tag>
              </td>
              <td :class="{ 'cell-na': pair.type !== 'groove-groove' }">
                {{ pair.type === 'groove-groove' ? formatNum(pair.bea) : 'N/A' }}
              </td>
              <td :class="{ 'cell-na': pair.type !== 'groove-groove' }">
                {{ pair.type === 'groove-groove' ? formatNum(pair.twist) : 'N/A' }}
              </td>
              <td :class="{ 'cell-na': pair.type !== 'groove-groove' }">
                {{ pair.type === 'groove-groove' ? formatNum(pair.offset) : 'N/A' }}
              </td>
              <td :class="{ 'cell-na': pair.type !== 'groove-flat-groove' }">
                {{ pair.type === 'groove-flat-groove' ? formatNum(pair.bea) : 'N/A' }}
              </td>
              <td :class="{ 'cell-na': pair.type !== 'groove-flat-groove' }">
                {{ pair.type === 'groove-flat-groove' ? formatNum(pair.twist) : 'N/A' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </el-card>

    <el-card v-else-if="pulleys.length > 0" shadow="hover" class="result-card result-empty">
      <el-empty description="带轮数量不足或无法组成带轮对，请检查带轮类型（至少需要2个槽轮）" />
    </el-card>
  </div>
</template>

<script setup>
import { computed, watchEffect } from 'vue'
import { sharedStore } from '../store/shared.js'

// 确保每个带轮都有对齐度相关字段（副作用放在 watchEffect 中）
watchEffect(() => {
  sharedStore.pulleys.forEach(p => {
    if (p.centerHeightDiff === undefined) p.centerHeightDiff = ''
    if (p.perpendicularity === undefined) p.perpendicularity = ''
  })
})

// 直接使用共享 store 中的带轮数组
const pulleys = computed(() => sharedStore.pulleys)

// 生成带轮对（按槽轮分组，环形轮系）
// 逻辑：找到所有槽轮，每两个相邻槽轮构成一对
//   - 中间无其他带轮 → 槽轮-槽轮
//   - 中间有平轮 → 槽轮-平轮-槽轮
const alignmentPairs = computed(() => {
  const list = sharedStore.pulleys
  if (list.length < 2) return []

  // 收集所有槽轮的索引
  const grooveIndices = []
  list.forEach((p, i) => {
    if (p.type === 'groove') grooveIndices.push(i)
  })
  if (grooveIndices.length < 2) return []

  const pairs = []
  for (let i = 0; i < grooveIndices.length; i++) {
    const currIdx = grooveIndices[i]
    const nextIdx = grooveIndices[(i + 1) % grooveIndices.length]
    const curr = list[currIdx]
    const next = list[nextIdx]

    // 找两个槽轮之间的带轮（不包含两端槽轮）
    const middlePulleys = []
    let j = (currIdx + 1) % list.length
    while (j !== nextIdx) {
      middlePulleys.push({ pulley: list[j], index: j })
      j = (j + 1) % list.length
    }

    if (middlePulleys.length === 0) {
      // 槽轮-槽轮
      pairs.push({
        type: 'groove-groove',
        fromCode: curr.code || '--',
        toCode: next.code || '--',
        middleCode: null,
        fromIdx: currIdx,
        toIdx: nextIdx,
        bea: calcBEA(curr, next),
        twist: calcTwist(curr, next),
        offset: calcOffset(curr, next)
      })
    } else if (middlePulleys.length === 1 && middlePulleys[0].pulley.type === 'flat') {
      // 槽轮-平轮-槽轮
      const mid = middlePulleys[0].pulley
      pairs.push({
        type: 'groove-flat-groove',
        fromCode: curr.code || '--',
        toCode: next.code || '--',
        middleCode: mid.code || '--',
        fromIdx: currIdx,
        toIdx: nextIdx,
        middleIdx: middlePulleys[0].index,
        bea: calcBEAFlat(curr, mid, next),
        twist: calcTwistFlat(curr, mid, next),
        offset: null
      })
    }
    // 其他情况（多个平轮等）暂不处理
  }
  return pairs
})

// ===== 占位计算公式（待用户提供正式公式后替换）=====
function calcBEA(p1, p2) {
  const ch1 = Number(p1.centerHeightDiff) || 0
  const ch2 = Number(p2.centerHeightDiff) || 0
  const dx = Math.abs((p1.x || 0) - (p2.x || 0)) || 1
  return Math.atan(Math.abs(ch2 - ch1) / dx) * 180 / Math.PI
}

function calcTwist(p1, p2) {
  const perp1 = Number(p1.perpendicularity) || 0
  const perp2 = Number(p2.perpendicularity) || 0
  return Math.abs(perp1 - perp2)
}

function calcOffset(p1, p2) {
  const ch1 = Number(p1.centerHeightDiff) || 0
  const ch2 = Number(p2.centerHeightDiff) || 0
  return Math.abs(ch1 - ch2)
}

function calcBEAFlat(p1, pFlat, p2) {
  const ch1 = Number(p1.centerHeightDiff) || 0
  const ch2 = Number(p2.centerHeightDiff) || 0
  const dx = Math.abs((p1.x || 0) - (p2.x || 0)) || 1
  return Math.atan(Math.abs(ch2 - ch1) / dx) * 180 / Math.PI
}

function calcTwistFlat(p1, pFlat, p2) {
  const perp1 = Number(p1.perpendicularity) || 0
  const perp2 = Number(p2.perpendicularity) || 0
  return Math.abs(perp1 - perp2)
}

function formatNum(val) {
  if (val === null || val === undefined || isNaN(val) || val === '') return '--'
  return Number(val).toFixed(2)
}
</script>

<style scoped>
.alignment-page {
  padding: 24px 0;
  max-width: 1600px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e8ecf1;
}

.page-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 28px;
  height: 28px;
  color: #409eff;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #1d2129;
  margin: 0;
}

.page-subtitle {
  font-size: 13px;
  color: #86909c;
  margin-left: 4px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #1d2129;
}

.card-icon {
  width: 18px;
  height: 18px;
  color: #409eff;
}

.card-tip {
  font-size: 12px;
  color: #909399;
  font-weight: 400;
  margin-left: auto;
}

.input-card {
  margin-bottom: 20px;
}

.pulley-table-wrapper {
  overflow-x: auto;
}

.pulley-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.pulley-table th,
.pulley-table td {
  border: 1px solid #e4e7ed;
  padding: 10px 12px;
  text-align: center;
}

.pulley-table th {
  background: #f5f7fa;
  color: #606266;
  font-weight: 600;
  text-align: center;
}

.pulley-table tbody tr:hover {
  background: #f8fafc;
}

/* 表格内输入框文字居中 */
.pulley-table :deep(.el-input__inner) {
  text-align: center;
}

.pulley-code {
  font-weight: 600;
  color: #409eff;
}

.empty-tip {
  padding: 40px 0;
}

.result-card {
  margin-top: 20px;
}

.result-empty {
  padding: 20px 0;
}

.result-table-wrapper {
  overflow-x: auto;
}

.result-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.result-table th,
.result-table td {
  border: 1px solid #e4e7ed;
  padding: 10px 12px;
  text-align: center;
}

.result-table th {
  background: #f5f7fa;
  color: #606266;
  font-weight: 600;
}

.result-table tbody tr:hover {
  background: #f8fafc;
}

.group-header {
  font-size: 14px;
}

.group-header.group-groove {
  background: #ecf5ff;
  color: #409eff;
}

.group-header.group-flat {
  background: #f0f9eb;
  color: #67c23a;
}

th.group-groove {
  background: #f5f9ff;
}

th.group-flat {
  background: #f6fbf2;
}

.cell-na {
  background: #fff5ec;
  color: #e6a23c;
  font-weight: 500;
}

.pair-codes {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.pair-arrow {
  color: #c0c4cc;
  font-size: 12px;
}

.pulley-code-flat {
  color: #67c23a !important;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .pulley-table th,
  .pulley-table td {
    font-size: 12px;
    padding: 8px 6px;
  }

  .result-table th,
  .result-table td {
    font-size: 12px;
    padding: 8px 6px;
  }
}
</style>
