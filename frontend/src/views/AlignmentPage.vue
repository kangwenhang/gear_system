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

    <!-- 计算结果 -->
    <el-card v-if="result" shadow="hover" class="result-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 11 12 14 22 4"/>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
          </svg>
          <span>计算结果</span>
          <el-tag :type="result.passed ? 'success' : 'danger'" class="result-tag">
            {{ result.passed ? '合格' : '不合格' }}
          </el-tag>
        </div>
      </template>

      <el-row :gutter="16">
        <el-col :span="8" v-for="(item, idx) in result.items" :key="idx">
          <div class="result-item">
            <div class="result-label">{{ item.label }}</div>
            <div class="result-value" :class="{ 'value-warn': !item.pass }">
              {{ item.value }}
              <span class="result-unit">{{ item.unit }}</span>
            </div>
            <div class="result-status">
              <el-tag :type="item.pass ? 'success' : 'danger'" size="small">
                {{ item.pass ? '达标' : '超标' }}
              </el-tag>
              <span class="result-limit">限值: {{ item.limit }}{{ item.unit }}</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { sharedStore } from '../store/shared.js'

const result = ref(null)

// TODO: 后续基于前序页面数据计算对齐度
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

.result-card {
  margin-top: 20px;
}

.result-tag {
  margin-left: auto;
}

.result-item {
  background: #f7f8fa;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  margin-bottom: 12px;
  border: 1px solid #e8ecf1;
}

.result-label {
  font-size: 13px;
  color: #86909c;
  margin-bottom: 8px;
}

.result-value {
  font-size: 24px;
  font-weight: 700;
  color: #1d2129;
  margin-bottom: 8px;
}

.result-value.value-warn {
  color: #f53f3f;
}

.result-unit {
  font-size: 13px;
  font-weight: 400;
  color: #86909c;
  margin-left: 2px;
}

.result-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.result-limit {
  font-size: 12px;
  color: #c9cdd4;
}
</style>
