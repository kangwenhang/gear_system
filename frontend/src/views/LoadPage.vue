<template>
  <div class="load-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="page-header-left">
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
        </svg>
        <h2 class="page-title">负载参数</h2>
        <span class="page-subtitle">负载输入</span>
      </div>
    </div>

    <!-- 负载参数表格 -->
    <el-card shadow="hover" class="table-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <line x1="3" y1="9" x2="21" y2="9"/>
            <line x1="9" y1="21" x2="9" y2="9"/>
          </svg>
          <span>
            Duty Cycle 负载输入 (Input) kW
            <el-tooltip placement="top" content="TEN 和 IDR 无负载，不显示">
              <svg style="width:14px;height:14px;margin-left:4px;vertical-align:middle;color:#909399;cursor:help" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            </el-tooltip>
          </span>
          <el-tag size="small" type="info" class="count-tag">{{ tableData.length }} / 17</el-tag>
        </div>
      </template>

      <div v-if="loadColumns.length === 0" class="empty-hint">
        请先在"轮系布局参数"页面添加带轮
      </div>

      <div v-else class="table-wrapper">
        <el-table
          :data="tableData"
          border
          stripe
          :header-cell-style="headerStyle"
          :cell-style="cellStyle"
          row-class-name="table-row"
          size="default"
        >
          <!-- 占比 -->
          <el-table-column label="Duty Cycle [%]" min-width="120" align="center">
            <template #default="scope">
              <el-input-number
                v-model="tableData[scope.$index].duty_percent"
                :controls="false"
                :precision="3"
                :min="0"
                :max="100"
                size="small"
                style="width: 100%"
                placeholder="--"
              />
            </template>
          </el-table-column>

          <!-- 发动机转速 -->
          <el-table-column label="Eng.RPM" min-width="110" align="center">
            <template #default="scope">
              <el-input-number
                v-model="tableData[scope.$index].eng_rpm"
                :controls="false"
                :precision="0"
                :min="0"
                size="small"
                style="width: 100%"
                placeholder="--"
              />
            </template>
          </el-table-column>

          <!-- 车速 -->
          <el-table-column label="V [km/h]" min-width="110" align="center">
            <template #default="scope">
              <el-input-number
                v-model="tableData[scope.$index].speed"
                :controls="false"
                :precision="1"
                :min="0"
                size="small"
                style="width: 100%"
                placeholder="--"
              />
            </template>
          </el-table-column>

          <!-- 温度 -->
          <el-table-column label="T [°C]" min-width="100" align="center">
            <template #default="scope">
              <el-input-number
                v-model="tableData[scope.$index].temp"
                :controls="false"
                :precision="0"
                size="small"
                style="width: 100%"
                placeholder="--"
              />
            </template>
          </el-table-column>

          <!-- 各附件负载列（根据轮系布局页带轮数据动态生成，排除 TEN/IDR） -->
          <el-table-column
            v-for="(col, colIdx) in loadColumns"
            :key="col.code"
            :label="col.code"
            min-width="100"
            align="center"
          >
            <template #header>
              <div class="col-header">
                <span>{{ col.code }}</span>
                <el-tag v-if="colIdx === 0" size="small" type="warning" style="margin-left:4px">SUM</el-tag>
              </div>
            </template>
            <template #default="scope">
              <!-- 第一个带轮（驱动轮）：自动求和，只读 -->
              <div v-if="colIdx === 0" class="sum-cell">
                {{ formatSum(scope.$index) }}
              </div>
              <!-- 其余带轮：可输入 -->
              <el-input-number
                v-else
                v-model="tableData[scope.$index][col.code]"
                :controls="false"
                :precision="2"
                size="small"
                style="width: 100%"
                placeholder="--"
              />
            </template>
          </el-table-column>

          <!-- 操作列 -->
          <el-table-column label="操作" align="center" width="100">
            <template #default="scope">
              <div class="action-buttons">
                <el-button
                  type="primary"
                  size="small"
                  circle
                  :disabled="tableData.length >= 17"
                  @click="insertRow(scope.$index)"
                >
                  <svg style="width:12px;height:12px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  circle
                  :disabled="tableData.length <= 1"
                  @click="removeRow(scope.$index)"
                >
                  <svg style="width:12px;height:12px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/></svg>
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 发动机参数 -->
    <el-card shadow="hover" class="param-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
          <span>发动机参数</span>
        </div>
      </template>
      <el-form label-position="top" class="param-form">
        <el-row :gutter="16">
          <el-col :xs="24" :sm="12" :md="6" :lg="4" :xl="4">
            <el-form-item label="怠速范围 (RPM)">
              <div class="range-input">
                <el-input-number v-model="engineParams.idle_min" :controls="false" :precision="0" style="width:100%" placeholder="--" />
                <span class="range-sep">~</span>
                <el-input-number v-model="engineParams.idle_max" :controls="false" :precision="0" style="width:100%" placeholder="--" />
              </div>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6" :lg="4" :xl="4">
            <el-form-item label="标定转速 (RPM)">
              <el-input-number v-model="engineParams.nominal_speed" :controls="false" :precision="0" style="width:100%" placeholder="--" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6" :lg="4" :xl="4">
            <el-form-item label="极限转速 (RPM)">
              <el-input-number v-model="engineParams.limiting_speed" :controls="false" :precision="0" style="width:100%" placeholder="--" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6" :lg="4" :xl="4">
            <el-form-item label="发动机加速度 (RPM/s)">
              <el-input-number v-model="engineParams.acceleration" :controls="false" :precision="0" style="width:100%" placeholder="--" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6" :lg="4" :xl="4">
            <el-form-item label="发动机减速度 (RPM/s)">
              <el-input-number v-model="engineParams.deceleration" :controls="false" :precision="0" style="width:100%" placeholder="--" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 带轮转速 -->
    <el-card shadow="hover" class="param-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <span>带轮转速</span>
          <el-tag size="small" type="info" class="count-tag">{{ rpmColumns.length }} 个带轮</el-tag>
        </div>
      </template>

      <div v-if="rpmColumns.length === 0" class="empty-hint">
        请先在"轮系布局参数"页面添加带轮
      </div>

      <div v-else class="rpm-table-wrapper">
        <el-table
          :data="pulleyRpmData"
          border
          stripe
          :header-cell-style="headerStyle"
          size="default"
        >
          <el-table-column type="index" label="#" width="45" align="center" />
          <el-table-column label="Eng.RPM" min-width="110" align="center">
            <template #header>
              <div class="col-header">
                <span>Eng.RPM</span>
                <span class="col-unit">(RPM)</span>
              </div>
            </template>
            <template #default="scope">
              <span class="eng-rpm-cell">{{ scope.row.engRpm != null ? scope.row.engRpm : '--' }}</span>
            </template>
          </el-table-column>
          <el-table-column
            v-for="col in rpmColumns"
            :key="col.code"
            min-width="110"
            align="center"
          >
            <template #header>
              <div class="col-header">
                <span>{{ col.code }}</span>
                <span class="col-unit">(RPM)</span>
                <el-tag size="small" type="info" style="margin-left:4px;font-size:10px">i={{ col.ratio != null ? col.ratio.toFixed(3) : '--' }}</el-tag>
              </div>
            </template>
            <template #default="scope">
              <span class="rpm-cell">{{ scope.row[col.code] != null ? scope.row[col.code].toFixed(1) : '--' }}</span>
            </template>
          </el-table-column>
        </el-table>

        <div class="formula-detail">
          <span>转速 = Eng.RPM × 速比</span>
          <span style="margin-left:20px">速比 = 参考轮(第一个)有效直径 / 当前轮有效直径</span>
          <span style="margin-left:20px">槽轮有效直径 = 槽轮直径 + 2 × Pitch to Effective</span>
          <span style="margin-left:20px">平轮有效直径 = 平轮直径 + 2 × Flat to Pitch</span>
        </div>
      </div>
    </el-card>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { sharedStore } from '../store/shared.js'

const headerStyle = {
  background: '#f5f7fa',
  color: '#333',
  fontWeight: 600,
  fontSize: '13px',
  padding: '8px 0'
}

const cellStyle = {
  padding: '6px 4px'
}

// 根据轮系布局页的带轮数据生成负载列（排除 TEN 张紧器和 IDR 惰轮）
const loadColumns = computed(() => {
  return sharedStore.pulleys
    .filter(p => p.code !== 'TEN' && p.code !== 'IDR')
    .map(p => ({ code: p.code, name: p.name }))
})

// 第一个带轮（驱动轮）功率 = 后面所有附件功率之和
const formatSum = (rowIndex) => {
  const cols = loadColumns.value
  if (cols.length <= 1) return '--'
  let sum = 0
  let hasValue = false
  for (let i = 1; i < cols.length; i++) {
    const val = tableData.value[rowIndex]?.[cols[i].code]
    if (val != null) {
      sum += val
      hasValue = true
    }
  }
  return hasValue ? sum.toFixed(2) : '--'
}

// ===== 带轮转速计算 =====
// 带轮列（含速比），所有带轮（含 TEN/IDR，排除第一个参考轮自身显示速比1）
const rpmColumns = computed(() => {
  const pulleys = sharedStore.pulleys
  if (pulleys.length === 0) return []

  const ftp = sharedStore.beltParams.flat_to_pitch
  const pte = sharedStore.beltParams.pitch_to_effective

  const withEff = pulleys.map(p => {
    let effDia = null
    if (p.type === 'groove') {
      if (p.groove_dia != null && pte != null) effDia = p.groove_dia + 2 * pte
    } else {
      if (p.flat_dia != null && ftp != null) effDia = p.flat_dia + 2 * ftp
    }
    return { code: p.code, effDia }
  })

  const refEffDia = withEff[0]?.effDia

  return withEff.map(p => {
    let ratio = null
    if (refEffDia != null && p.effDia != null && p.effDia > 0) {
      ratio = refEffDia / p.effDia
    }
    return { code: p.code, ratio }
  })
})

// 带轮转速数据：每行对应 Duty Cycle 表格的一行，用其 Eng.RPM 计算各带轮转速
const pulleyRpmData = computed(() => {
  const cols = rpmColumns.value
  if (cols.length === 0) return []

  return tableData.value.map(row => {
    const engRpm = row.eng_rpm
    const result = { engRpm }
    cols.forEach(col => {
      if (engRpm != null && col.ratio != null) {
        result[col.code] = engRpm * col.ratio
      } else {
        result[col.code] = null
      }
    })
    return result
  })
})

const engineParams = ref({
  idle_min: null,
  idle_max: null,
  nominal_speed: null,
  limiting_speed: null,
  acceleration: null,
  deceleration: null
})

function createRow() {
  return {
    duty_percent: null,
    eng_rpm: null,
    speed: null,
    temp: null
  }
}

const tableData = ref([createRow(), createRow(), createRow()])

// 当负载列变化时，同步已有行数据的字段
watch(loadColumns, (newCols) => {
  tableData.value.forEach(row => {
    newCols.forEach(col => {
      if (!(col.code in row)) {
        row[col.code] = null
      }
    })
    // 清理已不存在的列
    Object.keys(row).forEach(key => {
      if (!['duty_percent', 'eng_rpm', 'speed', 'temp'].includes(key) &&
          !newCols.some(c => c.code === key)) {
        delete row[key]
      }
    })
  })
}, { deep: true })

const insertRow = (index) => {
  if (tableData.value.length >= 17) return
  const newRow = createRow()
  loadColumns.value.forEach(col => {
    newRow[col.code] = null
  })
  tableData.value.splice(index + 1, 0, newRow)
}

const removeRow = (index) => {
  if (tableData.value.length <= 1) return
  tableData.value.splice(index, 1)
}

const goToCalculate = () => {
  const totalDuty = tableData.value.reduce((sum, r) => sum + (r.duty_percent || 0), 0)
  console.log('负载参数:', tableData.value, '发动机参数:', engineParams.value)
  if (Math.abs(totalDuty - 100) > 0.1) {
    ElMessage.warning(`Duty Cycle 总和为 ${totalDuty.toFixed(3)}%，建议合计 100%`)
  } else {
    ElMessage.success('负载参数已确认')
  }
}
</script>

<style scoped>
/* ===== 页面整体 ===== */
.load-page {
  padding: 24px 0;
  max-width: 1600px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
}

/* ===== 页面标题 ===== */
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

/* ===== 卡片 ===== */
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

.count-tag {
  margin-left: auto;
}

.table-card {
  margin-bottom: 20px;
}

.table-wrapper {
  overflow-x: auto;
}

.col-header {
  font-weight: 600;
}

.col-unit {
  font-size: 11px;
  font-weight: 400;
  color: #86909c;
  margin-left: 2px;
}

.sum-cell {
  font-size: 14px;
  font-weight: 700;
  color: #d48806;
  background: #fffbe6;
  border-radius: 4px;
  padding: 4px 0;
  border: 1px solid #ffe58f;
}

.action-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

/* ===== 带轮转速卡片 ===== */
.rpm-table-wrapper {
  overflow-x: auto;
}

.ratio-cell {
  font-weight: 600;
  color: #409eff;
}

.eng-rpm-cell {
  font-weight: 600;
  color: #1d2129;
}

.rpm-cell {
  font-weight: 600;
  color: #d48806;
  font-size: 14px;
}

.formula-detail {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #e5e6eb;
  font-size: 12px;
  color: #86909c;
  line-height: 1.8;
}

.empty-hint {
  padding: 40px 20px;
  text-align: center;
  color: #86909c;
  font-size: 14px;
}

:deep(.el-table .el-input-number),
:deep(.el-table .el-input),
:deep(.el-table .el-select) {
  width: 100%;
}

:deep(.el-table .el-input__wrapper) {
  border-radius: 6px;
}

:deep(.el-table .el-input-number .el-input__wrapper) {
  border-radius: 6px;
}

/* ===== 参数卡片 ===== */
.param-card {
  margin-bottom: 20px;
}

.param-form :deep(.el-form-item__label) {
  font-size: 13px;
  font-weight: 500;
  color: #4e5969;
  padding-bottom: 4px;
}

.param-form :deep(.el-input__wrapper),
.param-form :deep(.el-input-number) {
  border-radius: 8px;
}

.param-form :deep(.el-input__inner) {
  text-align: center;
}

.range-input {
  display: flex;
  align-items: center;
  gap: 4px;
}

.range-sep {
  color: #86909c;
  font-size: 14px;
}

/* ===== 操作栏 ===== */
.action-bar {
  margin-top: 24px;
  text-align: center;
}

.submit-btn {
  min-width: 200px;
}
</style>
