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
      <el-button type="primary" size="large" @click="handleCalculate" :loading="calculating">
        <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        计算对齐度
      </el-button>
    </div>

    <!-- 输入参数卡片 -->
    <el-card shadow="hover" class="input-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2v20M2 12h20"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
          <span>对齐度输入参数</span>
        </div>
      </template>

      <el-form :model="formData" label-position="top" class="input-form">
        <el-row :gutter="24">
          <el-col :span="6">
            <el-form-item label="中心高差 (mm)">
              <el-input-number
                v-model="formData.centerHeight"
                :precision="2"
                :controls="false"
                style="width: 100%"
                placeholder="请输入中心高差"
                @change="handleInputChange"
              />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="垂直度 (mm/m)">
              <el-input-number
                v-model="formData.perpendicularity"
                :precision="2"
                :controls="false"
                style="width: 100%"
                placeholder="请输入垂直度"
                @change="handleInputChange"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="说明">
              <div class="hint-text">
                输入中心高差和垂直度后，点击「计算对齐度」按钮，系统将自动计算各带轮对的切入角 BEA 等对齐度参数。
              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 对齐度结果表格 -->
    <el-card shadow="hover" class="result-card" v-if="resultList.length > 0">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <line x1="3" y1="9" x2="21" y2="9"/>
            <line x1="3" y1="15" x2="21" y2="15"/>
            <line x1="9" y1="3" x2="9" y2="21"/>
            <line x1="15" y1="3" x2="15" y2="21"/>
          </svg>
          <span>对齐度计算结果</span>
          <el-tag size="small" type="info" class="count-tag">{{ resultList.length }} 对带轮</el-tag>
        </div>
      </template>

      <div class="table-wrapper">
        <el-table
          :data="resultList"
          border
          stripe
          :header-cell-style="headerStyle"
          :cell-style="cellStyle"
          size="default"
        >
          <!-- 带轮对标识 -->
          <el-table-column label="带轮对" width="140" align="center" fixed>
            <template #header>
              <div class="col-header">From → To</div>
            </template>
            <template #default="scope">
              <span class="pulley-pair">
                <span class="pulley-code">{{ scope.row.pulley_from }}</span>
                <span class="arrow">→</span>
                <span class="pulley-code">{{ scope.row.pulley_to }}</span>
              </span>
            </template>
          </el-table-column>

          <!-- Contact -->
          <el-table-column label="Contact" align="center">
            <el-table-column prop="contact_exit" label="Exit" width="90" align="center">
              <template #default="scope">
                <span v-if="scope.row.contact_exit !== null">{{ formatNum(scope.row.contact_exit) }}</span>
                <span v-else class="na-text">--</span>
              </template>
            </el-table-column>
            <el-table-column prop="contact_entry" label="Entry" width="90" align="center">
              <template #default="scope">
                <span v-if="scope.row.contact_entry !== null">{{ formatNum(scope.row.contact_entry) }}</span>
                <span v-else class="na-text">--</span>
              </template>
            </el-table-column>
          </el-table-column>

          <!-- 包角 -->
          <el-table-column prop="wrap_angle" label="包角" width="90" align="center">
            <template #default="scope">
              <span v-if="scope.row.wrap_angle !== null">{{ formatNum(scope.row.wrap_angle) }}</span>
              <span v-else class="na-text">--</span>
            </template>
          </el-table-column>

          <!-- Check -->
          <el-table-column prop="check" label="Check" width="90" align="center">
            <template #default="scope">
              <span v-if="scope.row.check !== null">{{ formatNum(scope.row.check) }}</span>
              <span v-else class="na-text">--</span>
            </template>
          </el-table-column>

          <!-- 中心高差 -->
          <el-table-column label="中心高差" width="90" align="center">
            <template #header>
              <div class="col-header-blue">中心高差</div>
            </template>
            <template #default="scope">
              <span v-if="scope.row.center_height_diff !== null">{{ formatNum(scope.row.center_height_diff) }}</span>
              <span v-else class="na-text">--</span>
            </template>
          </el-table-column>

          <!-- 垂直度 -->
          <el-table-column label="垂直度" width="90" align="center">
            <template #header>
              <div class="col-header-blue">垂直度</div>
            </template>
            <template #default="scope">
              <span v-if="scope.row.perpendicularity !== null">{{ formatNum(scope.row.perpendicularity) }}</span>
              <span v-else class="na-text">--</span>
            </template>
          </el-table-column>

          <!-- 倾斜方向 -->
          <el-table-column prop="tilt_direction" label="倾斜方向" width="90" align="center">
            <template #default="scope">
              <span v-if="scope.row.tilt_direction !== null">{{ formatNum(scope.row.tilt_direction) }}</span>
              <span v-else class="na-text">--</span>
            </template>
          </el-table-column>

          <!-- Camber -->
          <el-table-column label="Camber" align="center">
            <el-table-column prop="camber_entry" label="Entry" width="90" align="center">
              <template #default="scope">
                <span v-if="scope.row.camber_entry !== null">{{ formatNum(scope.row.camber_entry) }}</span>
                <span v-else class="na-text">--</span>
              </template>
            </el-table-column>
            <el-table-column prop="camber_exit" label="Exit" width="90" align="center">
              <template #default="scope">
                <span v-if="scope.row.camber_exit !== null">{{ formatNum(scope.row.camber_exit) }}</span>
                <span v-else class="na-text">--</span>
              </template>
            </el-table-column>
          </el-table-column>

          <!-- Toe -->
          <el-table-column label="Toe" align="center">
            <el-table-column prop="toe_entry" label="Entry" width="90" align="center">
              <template #default="scope">
                <span v-if="scope.row.toe_entry !== null">{{ formatNum(scope.row.toe_entry) }}</span>
                <span v-else class="na-text">--</span>
              </template>
            </el-table-column>
            <el-table-column prop="toe_exit" label="Exit" width="90" align="center">
              <template #default="scope">
                <span v-if="scope.row.toe_exit !== null">{{ formatNum(scope.row.toe_exit) }}</span>
                <span v-else class="na-text">--</span>
              </template>
            </el-table-column>
          </el-table-column>

          <!-- 槽轮-槽轮 -->
          <el-table-column label="槽轮-槽轮" align="center">
            <template #header>
              <div class="col-header-orange">槽轮-槽轮</div>
            </template>
            <el-table-column prop="bea_groove_groove" label="切入角BEA" width="110" align="center">
              <template #header>
                <div class="col-header-orange">切入角BEA</div>
              </template>
              <template #default="scope">
                <span v-if="scope.row.bea_groove_groove !== null" class="bea-value">{{ formatNum(scope.row.bea_groove_groove) }}</span>
                <span v-else class="na-text">N/A</span>
              </template>
            </el-table-column>
            <el-table-column prop="twist_groove_groove" label="Twist" width="90" align="center">
              <template #default="scope">
                <span v-if="scope.row.twist_groove_groove !== null">{{ formatNum(scope.row.twist_groove_groove) }}</span>
                <span v-else class="na-text">--</span>
              </template>
            </el-table-column>
            <el-table-column prop="offset_groove_groove" label="Offset" width="90" align="center">
              <template #default="scope">
                <span v-if="scope.row.offset_groove_groove !== null">{{ formatNum(scope.row.offset_groove_groove) }}</span>
                <span v-else class="na-text">--</span>
              </template>
            </el-table-column>
          </el-table-column>

          <!-- 槽轮-平轮-槽轮 -->
          <el-table-column label="槽轮-平轮-槽轮" align="center">
            <template #header>
              <div class="col-header-orange-light">槽轮-平轮-槽轮</div>
            </template>
            <el-table-column prop="bea_groove_flat" label="切入角BEA" width="110" align="center">
              <template #header>
                <div class="col-header-orange-light">切入角BEA</div>
              </template>
              <template #default="scope">
                <span v-if="scope.row.bea_groove_flat !== null" class="bea-value">{{ formatNum(scope.row.bea_groove_flat) }}</span>
                <span v-else class="na-text">N/A</span>
              </template>
            </el-table-column>
            <el-table-column label="N/A" width="80" align="center">
              <template #default>
                <span class="na-text">N/A</span>
              </template>
            </el-table-column>
            <el-table-column prop="twist_groove_flat" label="Twist" width="90" align="center">
              <template #default="scope">
                <span v-if="scope.row.twist_groove_flat !== null">{{ formatNum(scope.row.twist_groove_flat) }}</span>
                <span v-else class="na-text">--</span>
              </template>
            </el-table-column>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 空状态 -->
    <el-card shadow="hover" class="empty-card" v-else>
      <el-empty description="请输入中心高差和垂直度，点击计算按钮查看结果">
        <template #image>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="empty-icon">
            <path d="M12 2v20M2 12h20"/>
            <circle cx="12" cy="12" r="3"/>
            <circle cx="12" cy="12" r="9" stroke-dasharray="2 2"/>
          </svg>
        </template>
      </el-empty>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api/pulley.js'
import { sharedStore } from '../store/shared.js'

const calculating = ref(false)
const resultList = ref([])

const formData = ref({
  centerHeight: 0,
  perpendicularity: 0
})

const headerStyle = {
  backgroundColor: '#f0f5ff',
  color: '#1d2129',
  fontWeight: '600',
  textAlign: 'center',
  fontSize: '13px',
  padding: '10px 0'
}

const cellStyle = {
  padding: '8px 6px'
}

function formatNum(val) {
  if (val === null || val === undefined || isNaN(val)) return '--'
  return Number(val).toFixed(2)
}

function handleInputChange() {
  // 输入变化时可以做实时预览（待公式确定后实现）
}

async function handleCalculate() {
  if (sharedStore.pulleys.length < 2) {
    ElMessage.warning('请先在轮系布局页面添加至少 2 个带轮')
    return
  }

  calculating.value = true
  try {
    const response = await api.calcAlignment({
      pulleys: sharedStore.pulleys,
      center_height: formData.value.centerHeight,
      perpendicularity: formData.value.perpendicularity
    })

    if (response.data && response.data.results) {
      resultList.value = response.data.results
      sharedStore.alignmentResult = response.data.results
      sharedStore.alignmentInput = {
        centerHeight: formData.value.centerHeight,
        perpendicularity: formData.value.perpendicularity
      }
      ElMessage.success(`计算完成，共 ${response.data.count} 对带轮`)
    }
  } catch (error) {
    console.error('对齐度计算失败:', error)
    ElMessage.error('计算失败，请检查输入参数')
  } finally {
    calculating.value = false
  }
}

// 监听共享 store 中的带轮数据变化，清除旧的计算结果
watch(
  () => sharedStore.pulleys.length,
  () => {
    resultList.value = []
  }
)
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

.count-tag {
  margin-left: 8px;
}

.input-card {
  margin-bottom: 20px;
}

.input-form {
  margin-top: 8px;
}

.hint-text {
  font-size: 13px;
  color: #86909c;
  line-height: 1.6;
  padding: 8px 12px;
  background: #f7f8fa;
  border-radius: 6px;
  border-left: 3px solid #409eff;
}

.result-card {
  margin-top: 20px;
}

.table-wrapper {
  overflow-x: auto;
}

.col-header {
  font-weight: 600;
  color: #1d2129;
}

.col-header-blue {
  font-weight: 600;
  color: #409eff;
}

.col-header-orange {
  font-weight: 600;
  color: #ff7d00;
}

.col-header-orange-light {
  font-weight: 600;
  color: #ff9a2e;
}

.pulley-pair {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 13px;
}

.pulley-code {
  font-weight: 600;
  color: #1d2129;
  background: #e8f3ff;
  padding: 2px 8px;
  border-radius: 4px;
}

.arrow {
  color: #409eff;
  font-weight: 600;
}

.bea-value {
  font-weight: 600;
  color: #ff7d00;
}

.na-text {
  color: #c9cdd4;
  font-size: 13px;
}

.empty-card {
  margin-top: 20px;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: #c9cdd4;
}
</style>
