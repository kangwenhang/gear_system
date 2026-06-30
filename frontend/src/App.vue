<template>
  <div class="app-container" :class="{ 'report-mode': activeTab === 'report' }">
    <!-- 页面内容 -->
    <div class="page-content">
      <InputPage v-show="activeTab === 'layout'" />
      <LoadPage v-show="activeTab === 'load'" />
      <AlignmentPage v-show="activeTab === 'alignment'" />
      <ReportPage v-show="activeTab === 'report'" @back="backFromReport" />
    </div>

    <!-- 底部步骤导航（报告页隐藏） -->
    <div class="step-nav no-print" v-show="activeTab !== 'report'">
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
          type="primary"
          size="large"
          @click="confirmCalculate"
        >
          <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          确认输入，进入计算
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import InputPage from './views/InputPage.vue'
import LoadPage from './views/LoadPage.vue'
import AlignmentPage from './views/AlignmentPage.vue'
import ReportPage from './views/ReportPage.vue'
import { sharedStore } from './store/shared.js'

const steps = ['layout', 'load', 'alignment']
const activeTab = ref('layout')

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
