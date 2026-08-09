<template>
  <div class="app-container" :class="{ 'report-mode': activeTab === 'report', 'project-mode': activeTab === 'projects' }">

    <!-- 页面内容 -->
    <div class="page-content">
      <InputPage v-show="activeTab === 'layout'" :key="layoutKey" />
      <LoadPage v-show="activeTab === 'load'" />
      <AlignmentPage v-show="activeTab === 'alignment'" />
      <ReportPage v-show="activeTab === 'report'" @back="backFromReport" />
      <ProjectPage v-show="activeTab === 'projects'" :visible="activeTab === 'projects'"
        @load-project="handleLoadProject" @new-project="handleNewProject" />
    </div>

    <!-- 底部步骤导航（报告页隐藏） -->
    <div class="step-nav no-print" v-show="activeTab !== 'report' && activeTab !== 'projects'">
      <div class="step-indicator">
        <div class="step-item">
          <span class="step-dot" :class="{ active: activeTab === 'layout' }">1</span>
          <span class="step-label" :class="{ current: activeTab === 'layout' }">轮系布局参数</span>
        </div>
        <span class="step-line" :class="{ active: activeTab !== 'layout' }"></span>
        <div class="step-item">
          <span class="step-dot" :class="{ active: activeTab === 'load' }">2</span>
          <span class="step-label" :class="{ current: activeTab === 'load' }">负载参数</span>
        </div>
        <span class="step-line" :class="{ active: activeTab === 'alignment' }"></span>
        <div class="step-item">
          <span class="step-dot" :class="{ active: activeTab === 'alignment' }">3</span>
          <span class="step-label" :class="{ current: activeTab === 'alignment' }">对齐度计算</span>
        </div>
      </div>
      <div class="step-buttons">
        <el-button
          v-if="activeTab === 'layout'"
          size="large"
          @click="activeTab = 'projects'"
        >
          <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
          返回
        </el-button>
        <el-button
          v-else
          size="large"
          @click="prevStep"
        >
          <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
          上一步
        </el-button>
        <el-button
          v-if="activeTab !== 'alignment'"
          type="primary"
          size="large"
          @click="nextStep"
        >
          下一步
          <svg style="width:16px;height:16px;margin-left:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        </el-button>
        <el-button
          v-else
          type="primary"
          size="large"
          @click="confirmCalculate"
        >
          <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          确认输入，进入计算
        </el-button>
        <el-button
          size="large"
          @click="showSaveDialog"
        >
          <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
          保存项目
        </el-button>
      </div>
    </div>

    <!-- 保存对话框 -->
    <el-dialog v-model="saveVisible" title="保存项目" width="560px" :close-on-click-modal="false" append-to-body>
      <el-form :model="saveForm" label-width="90px">
        <el-row :gutter="16">
          <el-col :span="24">
            <el-form-item label="文件编号" required>
              <el-input v-model="saveForm.file_no" placeholder="如：2026072002" disabled />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="客户">
              <el-input v-model="saveForm.customer" placeholder="如：YAMAZ" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="项目（机型）">
              <el-input v-model="saveForm.project" placeholder="如：FEAD-..." disabled />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="缸数">
              <el-input v-model="saveForm.cylinders" placeholder="--" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="功率">
              <el-input v-model="saveForm.power" placeholder="--" disabled />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="版本">
              <el-input v-model="saveForm.version" placeholder="01" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="轮系层">
              <el-input v-model="saveForm.layers" placeholder="如：ALT(270A)" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="备注">
          <el-input v-model="saveForm.notes" type="textarea" :rows="2" placeholder="可选" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="saveVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import InputPage from './views/InputPage.vue'
import LoadPage from './views/LoadPage.vue'
import AlignmentPage from './views/AlignmentPage.vue'
import ReportPage from './views/ReportPage.vue'
import ProjectPage from './views/ProjectPage.vue'
import { sharedStore } from './store/shared.js'
import { saveProject, getProjectByFile } from './api/pulley.js'

const steps = ['layout', 'load', 'alignment']
// 支持 URL hash 直达：http://localhost:5173/#report 直接打开报告页
const initialTab = () => {
  if (typeof window !== 'undefined' && window.location.hash === '#report') return 'report'
  return 'projects'
}
const activeTab = ref(initialTab())

const prevStep = () => {
  const idx = steps.indexOf(activeTab.value)
  if (idx > 0) activeTab.value = steps[idx - 1]
}

const nextStep = () => {
  const idx = steps.indexOf(activeTab.value)
  if (idx < steps.length - 1) activeTab.value = steps[idx + 1]
}

const confirmCalculate = () => {
  sharedStore.calcTrigger++
  activeTab.value = 'report'
}

const backFromReport = () => {
  activeTab.value = 'alignment'
}

const handleLoadProject = () => {
  layoutKey.value++
  activeTab.value = 'layout'
}

// 新建轮系：清空所有数据后跳转
const layoutKey = ref(0)
function handleNewProject() {
  sharedStore.resetAll()
  layoutKey.value++
  activeTab.value = 'layout'
}

// 保存项目
const saveVisible = ref(false)
const saving = ref(false)
const saveForm = ref({
  file_no: '', version: '01', customer: '',
  project: '', cylinders: '', power: '', layers: '', notes: ''
})

function showSaveDialog() {
  const fi = sharedStore.formInfo
  // 来自轮系设计页面的版本，补零格式化为 "01"/"02"
  const rawVersion = fi.version || '01'
  const paddedVersion = String(rawVersion).padStart(2, '0')
  saveForm.value = {
    file_no: fi.file_no || '',
    version: paddedVersion,
    customer: fi.customer || '',
    project: fi.project || '',
    cylinders: fi.cylinders ?? '',
    power: fi.power ?? '',
    layers: fi.layers ?? '',
    notes: ''
  }
  saveVisible.value = true
}

async function handleSave() {
  if (!saveForm.value.file_no.trim()) {
    ElMessage.warning('文件编号为空，请先在轮系设计第一页填写 File No.')
    return
  }

  // 检查是否已有同文件编号+版本的历史数据
  try {
    await getProjectByFile(saveForm.value.file_no, saveForm.value.version)
    // 找到了，询问是否覆盖
    await ElMessageBox.confirm(
      `文件编号 "${saveForm.value.file_no}" 版本 ${saveForm.value.version} 已有历史数据，是否覆盖更新？`,
      '发现历史数据',
      { type: 'warning', confirmButtonText: '覆盖更新', cancelButtonText: '取消' }
    )
  } catch (e) {
    if (e === 'cancel') return
    // 404 或其他错误 = 没有历史数据，直接保存
  }

  saving.value = true
  try {
    const fi = { ...sharedStore.formInfo, file_no: saveForm.value.file_no, layers: saveForm.value.layers }
    sharedStore.formInfo.layers = saveForm.value.layers
    await saveProject({
      name: saveForm.value.file_no,
      version: saveForm.value.version,
      customer: saveForm.value.customer,
      project_code: fi.project || saveForm.value.file_no,
      form_info: fi,
      pulleys: sharedStore.pulleys.map(p => ({ ...p })),
      belt_params: { ...sharedStore.beltFullParams },
      tensioner: { ...sharedStore.tensioner },
      notes: saveForm.value.notes
    })
    ElMessage.success('保存成功')
    saveVisible.value = false
  } catch (e) {
    ElMessage.error('保存失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    saving.value = false
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: #f5f7fa;
}

.app-container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 32px 140px;
}

.app-container.report-mode {
  padding: 0;
}

.app-container.project-mode {
  padding: 0 32px 80px;
}

/* ===== 顶部导航 ===== */
.top-nav {
  display: flex;
  align-items: center;
  padding: 12px 0 0 0;
  margin-bottom: 8px;
  border-bottom: 2px solid #e8ecf1;
}
.nav-tabs {
  display: flex;
  gap: 0;
}
.nav-tab {
  padding: 10px 24px;
  font-size: 15px;
  font-weight: 500;
  color: #909399;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
  user-select: none;
}
.nav-tab:hover { color: #409eff; }
.nav-tab.active {
  color: #409eff;
  border-bottom-color: #409eff;
}

/* ===== 页面内容 ===== */
.page-content {
  min-height: calc(100vh - 160px);
}

/* ===== 底部步骤导航 ===== */
.step-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-width: 1600px;
  margin: 0 auto;
  background: #ffffff;
  border-top: 2px solid #e8ecf1;
  padding: 16px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 100;
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.04);
}

/* 步骤指示器 */
.step-indicator {
  display: flex;
  align-items: flex-start;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.step-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e5e6eb;
  color: #86909c;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  transition: all 0.3s;
  flex-shrink: 0;
}

.step-dot.active {
  background: #409eff;
  color: #ffffff;
}

.step-label {
  font-size: 12px;
  color: #c9cdd4;
  white-space: nowrap;
  transition: all 0.3s;
}

.step-label.current {
  color: #409eff;
  font-weight: 600;
}

.step-line {
  width: 48px;
  height: 2px;
  background: #e5e6eb;
  margin: 13px 8px 0;
  transition: all 0.3s;
  flex-shrink: 0;
}

.step-line.active {
  background: #409eff;
}

/* 按钮 */
.step-buttons {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

/* ===== 移动端响应式 ===== */
@media (max-width: 768px) {
  .app-container {
    padding: 0 16px 160px;
  }

  .step-nav {
    flex-direction: column;
    gap: 12px;
    padding: 12px 16px;
  }

  .step-indicator {
    width: 100%;
    justify-content: center;
  }

  .step-dot {
    width: 24px;
    height: 24px;
    font-size: 12px;
  }

  .step-label {
    font-size: 11px;
  }

  .step-line {
    width: 32px;
    margin: 11px 6px 0;
  }

  .step-buttons {
    width: 100%;
    justify-content: center;
  }

  .step-buttons .el-button {
    flex: 1;
  }
}
</style>
