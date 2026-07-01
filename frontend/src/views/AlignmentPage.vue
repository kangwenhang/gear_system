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

    <!-- 操作按钮 -->
    <div class="action-bar">
      <el-button type="primary" size="large" :disabled="pulleys.length === 0" @click="handleCalculate">
        <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 11l3 3L22-4"/>
          <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
        </svg>
        开始计算
      </el-button>
    </div>

    <!-- 计算结果 -->
    <el-card v-if="showResult" shadow="hover" class="result-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 11 12 14 22 4"/>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
          </svg>
          <span>计算结果</span>
        </div>
      </template>

      <div class="result-summary">
        <div class="result-stat">
          <span class="stat-label">总带轮数</span>
          <span class="stat-value">{{ pulleys.length }}</span>
        </div>
        <div class="result-stat">
          <span class="stat-label">最大中心高</span>
          <span class="stat-value" :class="maxDiffClass">
            {{ formatNum(maxCenterHeightDiff) }} mm
          </span>
        </div>
        <div class="result-stat">
          <span class="stat-label">最大垂直度</span>
          <span class="stat-value" :class="maxPerpClass">
            {{ formatNum(maxPerpendicularity) }}°
          </span>
        </div>
      </div>

      <div class="result-table-wrapper">
        <table class="result-table">
          <thead>
            <tr>
              <th style="width: 60px">序号</th>
              <th>带轮编号</th>
              <th>中心高 (mm)</th>
              <th>垂直度 (°)</th>
              <th>切入角度 (°)</th>
              <th>评定</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, idx) in pulleys" :key="idx">
              <td style="text-align: center; color: #909399">{{ idx + 1 }}</td>
              <td><span class="pulley-code">{{ p.code || '--' }}</span></td>
              <td>{{ formatNum(p.centerHeightDiff) }}</td>
              <td>{{ formatNum(p.perpendicularity) }}</td>
              <td>{{ formatNum(p.entryAngle) }}</td>
              <td>
                <el-tag :type="p.passed ? 'success' : 'warning'" size="small">
                  {{ p.passed ? '合格' : '待评定' }}
                </el-tag>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { sharedStore } from '../store/shared.js'
import { ElMessage } from 'element-plus'

const showResult = ref(false)

const pulleys = computed({
  get() {
    return sharedStore.pulleys.map(p => ({
      ...p,
      centerHeightDiff: p.centerHeightDiff ?? 0,
      perpendicularity: p.perpendicularity ?? 0,
      entryAngle: p.entryAngle ?? null,
      passed: p.passed ?? false
    }))
  },
  set(val) {
    sharedStore.pulleys = val
  }
})

const maxCenterHeightDiff = computed(() => {
  if (!pulleys.value.length) return 0
  return Math.max(...pulleys.value.map(p => Math.abs(p.centerHeightDiff || 0)))
})

const maxPerpendicularity = computed(() => {
  if (!pulleys.value.length) return 0
  return Math.max(...pulleys.value.map(p => p.perpendicularity || 0))
})

const maxDiffClass = computed(() => maxCenterHeightDiff.value > 0.5 ? 'value-warn' : '')
const maxPerpClass = computed(() => maxPerpendicularity.value > 0.3 ? 'value-warn' : '')

function formatNum(val) {
  if (val === null || val === undefined || isNaN(val) || val === '') return '--'
  return Number(val).toFixed(2)
}

function handleCalculate() {
  if (pulleys.value.length === 0) {
    ElMessage.warning('请先添加带轮数据')
    return
  }
  
  // TODO: 调用后端 API 计算对齐度
  // 目前先做简单的本地计算（占位）
  pulleys.value.forEach(p => {
    // 切入角度 = arctan(垂直度) * 180 / PI （占位公式，待用户提供）
    const perp = p.perpendicularity || 0
    p.entryAngle = Math.atan(perp / 1000) * 180 / Math.PI
    p.passed = Math.abs(p.centerHeightDiff || 0) <= 0.5
  })
  
  showResult.value = true
  ElMessage.success('计算完成')
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
  text-align: left;
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

.pulley-code {
  font-weight: 600;
  color: #409eff;
}

.empty-tip {
  padding: 40px 0;
}

.action-bar {
  display: flex;
  justify-content: center;
  margin: 24px 0;
}

.result-card {
  margin-top: 20px;
}

.result-summary {
  display: flex;
  gap: 24px;
  margin-bottom: 20px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
}

.result-stat {
  flex: 1;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 13px;
  color: #909399;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #1d2129;
}

.stat-value.value-warn {
  color: #f56c6c;
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

/* 移动端适配 */
@media (max-width: 768px) {
  .pulley-table th,
  .pulley-table td {
    font-size: 12px;
  }

  .pulley-table th,
  .pulley-table td {
    padding: 8px 6px;
  }

  .result-summary {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
