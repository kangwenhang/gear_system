<template>
  <div class="app-container">
    <div class="page-content" v-if="!showReport">
      <InputPage v-show="activeTab === 'layout'" />
      <LoadPage v-show="activeTab === 'load'" />
      <AlignmentPage v-show="activeTab === 'alignment'" />
    </div>

    <ReportPage v-else @back="showReport = false" />

    <div class="step-nav no-print" v-if="!showReport">
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
          size="large"
          @click="prevStep"
          :disabled="activeTab === 'layout'"
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
          type="success"
          size="large"
          @click="confirmCalculate"
        >
          <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <path d="M9 15l2 2 4-4"/>
          </svg>
          生成报告
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import InputPage from './views/InputPage.vue'
import LoadPage from './views/LoadPage.vue'
import AlignmentPage from './views/AlignmentPage.vue'
import ReportPage from './views/ReportPage.vue'
import { sharedStore } from './store/shared.js'

const steps = ['layout', 'load', 'alignment']
const activeTab = ref('layout')

const showReport = computed({
  get: () => sharedStore.showReport,
  set: (val) => { sharedStore.showReport = val }
})

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
  sharedStore.showReport = true
  ElMessage.success('报告已生成')
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
  padding: 0 32px 120px;
}

.page-content {
  min-height: calc(100vh - 160px);
}

.step-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-width: 1600px;
  margin: 0 auto;
  background: #ffffff;
  border-top: 2px solid #e8ecf1;
  padding: 20px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 100;
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.04);
}

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

.step-buttons {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

@media print {
  .no-print {
    display: none !important;
  }

  .app-container {
    padding: 0;
    max-width: 100%;
  }
}
</style>
