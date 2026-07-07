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
              <th style="width: 160px">垂直度 (°)</th>
              <th style="width: 160px">倾斜方向 (°)</th>
              <th style="width: 160px">Twist (°)</th>
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
              <td>
                <el-input
                v-model="p.tiltAngle"
                placeholder="请输入"
                style="width: 100%; text-align: center"
              />
              </td>
              <td style="text-align: center; color: #606266">
                {{ calcTwistDisplay(p) }}
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
              <th style="width: 60px">序号</th>
              <th>带轮对</th>
              <th style="width: 140px">类型</th>
              <th>切入角BEA (°)</th>
              <th>Offset</th>
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
              <td>{{ formatNum(pair.bea) }}</td>
              <td>{{ pair.offset === null ? 'N/A' : formatNum(pair.offset) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </el-card>

    <el-card v-else-if="pulleys.length > 0" shadow="hover" class="result-card result-empty">
      <el-empty description="带轮数量不足或无法组成带轮对，请检查带轮类型（至少需要2个槽轮）" />
    </el-card>

    <!-- 调试信息 -->
    <el-card v-if="pulleys.length > 0" shadow="hover" class="debug-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
          </svg>
          <span>调试信息</span>
        </div>
      </template>

      <div class="debug-section">
        <div class="debug-title">Contact参数（每个带轮）</div>
        <table class="debug-table">
          <thead>
            <tr>
              <th>带轮</th>
              <th>K</th>
              <th>J</th>
              <th>L</th>
              <th>M</th>
              <th>N</th>
              <th>P</th>
              <th>O</th>
              <th>Q</th>
              <th>U</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in debugPulleyList" :key="p.code">
              <td>{{ p.code }}</td>
              <td>{{ formatNum(p.K) }}</td>
              <td>{{ formatNum(p.J) }}</td>
              <td>{{ formatNum(p.L) }}</td>
              <td>{{ formatNum(p.M) }}</td>
              <td>{{ formatNum(p.N) }}</td>
              <td>{{ formatNum(p.P) }}</td>
              <td>{{ formatNum(p.O) }}</td>
              <td>{{ formatNum(p.Q) }}</td>
              <td>{{ formatNum(p.U) }}{{ p.UFromInput ? ' (输入)' : ' (计算)' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="debug-section">
        <div class="debug-title">每个带轮的V/W/X/Y值</div>
        <table class="debug-table">
          <thead>
            <tr>
              <th>带轮</th>
              <th>类型</th>
              <th>中心高S</th>
              <th>垂直度T</th>
              <th>V</th>
              <th>W</th>
              <th>X</th>
              <th>Y</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in debugVWList" :key="p.code">
              <td>{{ p.code }}</td>
              <td>{{ p.type === 'groove' ? '槽轮' : '平轮' }}</td>
              <td>{{ formatNum(p.S) }}</td>
              <td>{{ formatNum(p.T) }}</td>
              <td>{{ formatNum(p.V) }}</td>
              <td>{{ formatNum(p.W) }}</td>
              <td>{{ formatNum(p.X) }}</td>
              <td>{{ formatNum(p.Y) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="debug-section" v-if="alignmentPairs.length > 0">
        <div class="debug-title">带轮对计算详情</div>
        <div v-for="(pair, idx) in alignmentPairs" :key="idx" class="pair-debug">
          <div class="pair-debug-title">
            第{{ idx + 1 }}组：{{ pair.fromCode }} → {{ pair.middleCode || '' }} {{ pair.middleCode ? '→' : '' }} {{ pair.toCode }} ({{ pair.type === 'groove-groove' ? '槽轮-槽轮' : '槽轮-平轮-槽轮' }})
          </div>
          <div class="pair-debug-content">
            <div>BEA: {{ formatNum(pair.bea) }}°</div>
            <div>Twist: {{ formatNum(pair.twist) }}°</div>
            <div>Offset: {{ pair.offset === null ? 'N/A' : formatNum(pair.offset) }}</div>
          </div>
          <div v-if="pair.debug" class="pair-debug-details">
            <div class="debug-subtitle">详细计算过程：</div>
            <table class="debug-table">
              <thead>
                <tr>
                  <th>变量</th>
                  <th>值</th>
                  <th>说明</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, i) in pair.debug" :key="i">
                  <td>{{ item.name }}</td>
                  <td>{{ formatNum(item.value) }}</td>
                  <td style="text-align: left">{{ item.desc }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, watchEffect, watch } from 'vue'
import { sharedStore } from '../store/shared.js'
import { calcAlignment as apiCalcAlignment } from '../api/pulley.js'

const pulleys = computed(() => sharedStore.pulleys)
const contactParams = computed(() => sharedStore.contactParams)

watchEffect(() => {
  sharedStore.pulleys.forEach(p => {
    if (p.centerHeightDiff === undefined) p.centerHeightDiff = ''
    if (p.perpendicularity === undefined) p.perpendicularity = ''
    if (p.tiltAngle === undefined) p.tiltAngle = ''
  })
})

// 后端返回的计算结果
const alignmentResult = ref({ per_pulley: [], pairs: [] })

const alignmentPairs = computed(() => alignmentResult.value.pairs || [])
const debugPulleyList = computed(() => alignmentResult.value.per_pulley || [])
const debugVWList = computed(() => alignmentResult.value.per_pulley || [])

function calcTwistDisplay(p) {
  const item = alignmentResult.value.per_pulley?.find(item => item.code === p.code)
  if (!item || item.twist == null) return '--'
  return Number(item.twist).toFixed(4)
}

// 监听输入变化，调用后端API计算对齐度
async function fetchAlignment() {
  const list = sharedStore.pulleys
  const cp = sharedStore.contactParams
  if (list.length < 2 || Object.keys(cp).length === 0) {
    alignmentResult.value = { per_pulley: [], pairs: [] }
    return
  }

  try {
    const res = await apiCalcAlignment({
      pulleys: list.map(p => ({
        code: p.code,
        name: p.name || '',
        type: p.type,
        centerHeightDiff: Number(p.centerHeightDiff) || 0,
        perpendicularity: Number(p.perpendicularity) || 0,
        tiltAngle: p.tiltAngle ?? '',
      })),
      contact_params: cp,
    })
    if (res.data.success) {
      alignmentResult.value = res.data
    }
  } catch (e) {
    console.error('对齐度计算失败:', e)
  }
}

watch(
  () => [
    sharedStore.pulleys.map(p => ({ code: p.code, type: p.type, centerHeightDiff: p.centerHeightDiff, perpendicularity: p.perpendicularity, tiltAngle: p.tiltAngle })),
    sharedStore.contactParams
  ],
  () => { fetchAlignment() },
  { deep: true, immediate: true }
)

function formatNum(val) {
  if (val === null || val === undefined || isNaN(val) || val === '') return '--'
  return Number(val).toFixed(4)
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

.debug-card {
  margin-top: 20px;
}

.debug-section {
  margin-bottom: 20px;
}

.debug-title {
  font-size: 14px;
  font-weight: 600;
  color: #606266;
  margin-bottom: 10px;
}

.debug-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.debug-table th,
.debug-table td {
  border: 1px solid #e4e7ed;
  padding: 6px 8px;
  text-align: center;
}

.debug-table th {
  background: #f0f5ff;
  color: #606266;
  font-weight: 600;
}

.debug-table tbody tr:hover {
  background: #f8fafc;
}

.pair-debug {
  background: #f5f7fa;
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 10px;
}

.pair-debug-title {
  font-size: 13px;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 8px;
}

.pair-debug-content {
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: #606266;
}

.pair-debug-details {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #dcdfe6;
}

.debug-subtitle {
  font-size: 13px;
  font-weight: 600;
  color: #67c23a;
  margin-bottom: 8px;
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
