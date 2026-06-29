<template>
  <div class="report-page">
    <div class="report-toolbar no-print">
      <div class="toolbar-left">
        <el-button @click="handleBack">
          <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
          返回编辑
        </el-button>
      </div>
      <div class="toolbar-right">
        <el-button type="primary" size="large" @click="handlePrint">
          <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 6 2 18 2 18 9"/>
            <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
            <rect x="6" y="14" width="12" height="8"/>
          </svg>
          打印报告
        </el-button>
      </div>
    </div>

    <div class="report-container" id="reportContent">
      <div class="report-header">
        <h1 class="report-title">轮系设计分析报告</h1>
        <div class="report-subtitle">Front End Accessory Drive System Analysis Report</div>
      </div>

      <section class="report-section">
        <h2 class="section-title">
          <span class="title-number">1</span>
          项目基本信息
        </h2>
        <table class="info-table">
          <tr>
            <th>文件编号</th>
            <td>{{ formInfo.fileNo || '--' }}</td>
            <th>客户</th>
            <td>{{ formInfo.customer || '--' }}</td>
            <th>项目/机型</th>
            <td>{{ formInfo.project || '--' }}</td>
          </tr>
          <tr>
            <th>缸数</th>
            <td>{{ formInfo.cylinders || '--' }}</td>
            <th>发动机功率</th>
            <td>{{ formInfo.power || '--' }} kW</td>
            <th>版本</th>
            <td>V{{ formInfo.version || 1 }}</td>
          </tr>
        </table>
      </section>

      <section class="report-section">
        <h2 class="section-title">
          <span class="title-number">2</span>
          轮系布局参数
        </h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>序号</th>
              <th>名称</th>
              <th>带轮</th>
              <th>类型</th>
              <th>X坐标 (mm)</th>
              <th>Y坐标 (mm)</th>
              <th>平轮直径 (mm)</th>
              <th>槽轮直径 (mm)</th>
              <th>转动惯量 (kg·m²)</th>
              <th>Service Factor</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, idx) in pulleys" :key="idx">
              <td class="text-center">{{ idx + 1 }}</td>
              <td class="text-center">{{ p.name || '--' }}</td>
              <td class="text-center">{{ p.code || '--' }}</td>
              <td class="text-center">{{ p.type === 'flat' ? '平轮' : '槽轮' }}</td>
              <td class="text-center">{{ p.x != null ? p.x.toFixed(2) : '--' }}</td>
              <td class="text-center">{{ p.y != null ? p.y.toFixed(2) : '--' }}</td>
              <td class="text-center">{{ p.flat_dia != null ? p.flat_dia.toFixed(2) : '--' }}</td>
              <td class="text-center">{{ p.groove_dia != null ? p.groove_dia.toFixed(2) : '--' }}</td>
              <td class="text-center">{{ p.inertia != null ? p.inertia.toFixed(4) : '--' }}</td>
              <td class="text-center">{{ p.service_factor != null ? p.service_factor.toFixed(1) : '--' }}</td>
            </tr>
            <tr v-if="pulleys.length === 0">
              <td colspan="10" class="empty-cell">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="report-section" v-if="tensioner">
        <h2 class="section-title">
          <span class="title-number">3</span>
          张紧器参数
        </h2>
        <div class="tensioner-type-tag">
          {{ tensioner.type === 'automatic' ? '自动张紧轮' : '手调张紧轮' }}
        </div>
        <template v-if="tensioner.type === 'automatic'">
          <table class="info-table">
            <tr>
              <th>旋转方向</th>
              <td>{{ tensioner.automatic?.rotation === 'cw' ? '顺时针' : '逆时针' }}</td>
              <th>张力值类型</th>
              <td>{{ tensioner.automatic?.valueType === 'torque' ? '扭矩' : '张力值' }}</td>
              <th>阻尼</th>
              <td>{{ tensioner.automatic?.damping != null ? tensioner.automatic.damping + '%' : '--' }}</td>
            </tr>
            <tr>
              <th>枢轴 X (mm)</th>
              <td>{{ tensioner.automatic?.pivot_x != null ? tensioner.automatic.pivot_x.toFixed(2) : '--' }}</td>
              <th>枢轴 Y (mm)</th>
              <td>{{ tensioner.automatic?.pivot_y != null ? tensioner.automatic.pivot_y.toFixed(2) : '--' }}</td>
              <th>臂长 (mm)</th>
              <td>{{ tensioner.automatic?.arm_length != null ? tensioner.automatic.arm_length.toFixed(2) : '--' }}</td>
            </tr>
            <tr>
              <th>工作角度 (°)</th>
              <td>{{ tensioner.automatic?.work_angle != null ? tensioner.automatic.work_angle.toFixed(2) : '--' }}</td>
              <th>名义扭转角 (°)</th>
              <td>{{ tensioner.automatic?.nominal_angle != null ? tensioner.automatic.nominal_angle.toFixed(2) : '--' }}</td>
              <th>总行程 (°)</th>
              <td>{{ tensioner.automatic?.stroke != null ? tensioner.automatic.stroke.toFixed(2) : '--' }}</td>
            </tr>
            <tr>
              <th>张力值 (N)</th>
              <td>{{ tensioner.automatic?.tension_value != null ? tensioner.automatic.tension_value.toFixed(2) : '--' }}</td>
              <th>扭矩 (N·m)</th>
              <td>{{ tensioner.automatic?.torque != null ? tensioner.automatic.torque.toFixed(2) : '--' }}</td>
              <th>弹簧刚度 (N·m/°)</th>
              <td>{{ tensioner.automatic?.spring_stiffness != null ? tensioner.automatic.spring_stiffness.toFixed(4) : '--' }}</td>
            </tr>
          </table>
        </template>
        <template v-else>
          <table class="info-table">
            <tr>
              <th>起始 X (mm)</th>
              <td>{{ tensioner.manual?.start_x != null ? tensioner.manual.start_x.toFixed(2) : '--' }}</td>
              <th>起始 Y (mm)</th>
              <td>{{ tensioner.manual?.start_y != null ? tensioner.manual.start_y.toFixed(2) : '--' }}</td>
              <th>结束 X (mm)</th>
              <td>{{ tensioner.manual?.end_x != null ? tensioner.manual.end_x.toFixed(2) : '--' }}</td>
            </tr>
            <tr>
              <th>结束 Y (mm)</th>
              <td>{{ tensioner.manual?.end_y != null ? tensioner.manual.end_y.toFixed(2) : '--' }}</td>
              <th>名义位置 X (mm)</th>
              <td>{{ tensioner.manual?.nominal_x != null ? tensioner.manual.nominal_x.toFixed(2) : '--' }}</td>
              <th>名义位置 Y (mm)</th>
              <td>{{ tensioner.manual?.nominal_y != null ? tensioner.manual.nominal_y.toFixed(2) : '--' }}</td>
            </tr>
            <tr>
              <th>张力设定值 (N)</th>
              <td>{{ tensioner.manual?.tension_value != null ? tensioner.manual.tension_value.toFixed(2) : '--' }}</td>
              <th></th>
              <td></td>
              <th></th>
              <td></td>
            </tr>
          </table>
        </template>
      </section>

      <section class="report-section" v-if="beltFullParams">
        <h2 class="section-title">
          <span class="title-number">4</span>
          皮带参数
        </h2>
        <table class="info-table">
          <tr>
            <th>皮带类型</th>
            <td>{{ beltFullParams.belt_type || '--' }}</td>
            <th>皮带厂家</th>
            <td>{{ beltFullParams.manufacturer || '--' }}</td>
            <th>皮带PK</th>
            <td>{{ beltFullParams.belt_pk || '--' }}</td>
          </tr>
          <tr>
            <th>延伸率 (%)</th>
            <td>{{ beltFullParams.elongation_rate != null ? beltFullParams.elongation_rate.toFixed(3) : '--' }}</td>
            <th>长度公差 (mm)</th>
            <td>±{{ beltFullParams.length_tolerance || '--' }}</td>
            <th>寿命系数</th>
            <td>{{ beltFullParams.life_coefficient != null ? beltFullParams.life_coefficient.toFixed(3) : '--' }}</td>
          </tr>
          <tr>
            <th>Flat to Pitch (mm)</th>
            <td>{{ beltFullParams.flat_to_pitch != null ? beltFullParams.flat_to_pitch.toFixed(2) : '--' }}</td>
            <th>Pitch to Effective (mm)</th>
            <td>{{ beltFullParams.pitch_to_effective != null ? beltFullParams.pitch_to_effective.toFixed(2) : '--' }}</td>
            <th>Height (mm)</th>
            <td>{{ beltFullParams.height != null ? beltFullParams.height.toFixed(2) : '--' }}</td>
          </tr>
        </table>
      </section>

      <section class="report-section" v-if="alignmentResult.length > 0">
        <h2 class="section-title">
          <span class="title-number">5</span>
          对齐度计算结果
        </h2>
        <div class="alignment-input-info">
          <span>中心高差：<b>{{ alignmentInput.centerHeight.toFixed(2) }} mm</b></span>
          <span style="margin-left: 24px">垂直度：<b>{{ alignmentInput.perpendicularity.toFixed(2) }} mm/m</b></span>
        </div>
        <div class="table-wrapper">
          <table class="data-table alignment-table">
            <thead>
              <tr>
                <th rowspan="2">带轮对<br/>From→To</th>
                <th colspan="2">Contact</th>
                <th rowspan="2">包角</th>
                <th rowspan="2">Check</th>
                <th rowspan="2" class="col-blue">中心高差</th>
                <th rowspan="2" class="col-blue">垂直度</th>
                <th rowspan="2">倾斜方向</th>
                <th colspan="2">Camber</th>
                <th colspan="2">Toe</th>
                <th colspan="3">槽轮-槽轮</th>
                <th colspan="3">槽轮-平轮-槽轮</th>
              </tr>
              <tr>
                <th>Exit</th>
                <th>Entry</th>
                <th>Entry</th>
                <th>Exit</th>
                <th>Entry</th>
                <th>Exit</th>
                <th>切入角BEA</th>
                <th>Twist</th>
                <th>Offset</th>
                <th>切入角BEA</th>
                <th>N/A</th>
                <th>Twist</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in alignmentResult" :key="idx">
                <td class="text-center pulley-pair-cell">
                  <span class="pair-code">{{ item.pulley_from }}</span>
                  <span class="pair-arrow">→</span>
                  <span class="pair-code">{{ item.pulley_to }}</span>
                </td>
                <td class="text-center">{{ formatVal(item.contact_exit) }}</td>
                <td class="text-center">{{ formatVal(item.contact_entry) }}</td>
                <td class="text-center">{{ formatVal(item.wrap_angle) }}</td>
                <td class="text-center">{{ formatVal(item.check) }}</td>
                <td class="text-center">{{ formatVal(item.center_height_diff) }}</td>
                <td class="text-center">{{ formatVal(item.perpendicularity) }}</td>
                <td class="text-center">{{ formatVal(item.tilt_direction) }}</td>
                <td class="text-center">{{ formatVal(item.camber_entry) }}</td>
                <td class="text-center">{{ formatVal(item.camber_exit) }}</td>
                <td class="text-center">{{ formatVal(item.toe_entry) }}</td>
                <td class="text-center">{{ formatVal(item.toe_exit) }}</td>
                <td class="text-center bea-cell">{{ formatVal(item.bea_groove_groove, 'N/A') }}</td>
                <td class="text-center">{{ formatVal(item.twist_groove_groove) }}</td>
                <td class="text-center">{{ formatVal(item.offset_groove_groove) }}</td>
                <td class="text-center bea-cell">{{ formatVal(item.bea_groove_flat, 'N/A') }}</td>
                <td class="text-center na-cell">N/A</td>
                <td class="text-center">{{ formatVal(item.twist_groove_flat) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="report-section" v-if="formInfo.updateDesc || formInfo.issueDesc">
        <h2 class="section-title">
          <span class="title-number">6</span>
          备注说明
        </h2>
        <div v-if="formInfo.updateDesc" class="remark-block">
          <div class="remark-label">更新说明：</div>
          <div class="remark-content">{{ formInfo.updateDesc }}</div>
        </div>
        <div v-if="formInfo.issueDesc" class="remark-block">
          <div class="remark-label">问题说明：</div>
          <div class="remark-content">{{ formInfo.issueDesc }}</div>
        </div>
      </section>

      <div class="report-footer">
        <div class="footer-date">报告生成时间：{{ currentTime }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { sharedStore } from '../store/shared.js'

const emit = defineEmits(['back'])

const pulleys = computed(() => sharedStore.pulleys)
const formInfo = computed(() => sharedStore.formInfo)
const tensioner = computed(() => sharedStore.tensioner)
const beltFullParams = computed(() => sharedStore.beltFullParams)
const alignmentResult = computed(() => sharedStore.alignmentResult)
const alignmentInput = computed(() => sharedStore.alignmentInput)

const currentTime = ref(new Date().toLocaleString('zh-CN'))

function formatVal(val, emptyText = '--') {
  if (val === null || val === undefined || isNaN(val)) return emptyText
  return Number(val).toFixed(2)
}

function handleBack() {
  emit('back')
}

function handlePrint() {
  window.print()
}
</script>

<style scoped>
.report-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.report-toolbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: #fff;
  padding: 12px 24px;
  border-bottom: 1px solid #e8ecf1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.report-container {
  max-width: 1000px;
  margin: 70px auto 40px;
  background: #fff;
  padding: 40px 50px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.report-header {
  text-align: center;
  padding-bottom: 24px;
  border-bottom: 2px solid #1d2129;
  margin-bottom: 28px;
}

.report-title {
  font-size: 28px;
  font-weight: 700;
  color: #1d2129;
  margin: 0 0 8px 0;
  letter-spacing: 2px;
}

.report-subtitle {
  font-size: 13px;
  color: #86909c;
  letter-spacing: 1px;
}

.report-section {
  margin-bottom: 28px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1d2129;
  margin: 0 0 14px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #e8ecf1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: #409eff;
  color: #fff;
  border-radius: 50%;
  font-size: 13px;
  font-weight: 700;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.info-table th {
  background: #f0f5ff;
  color: #1d2129;
  font-weight: 600;
  padding: 10px 14px;
  text-align: left;
  border: 1px solid #e8ecf1;
  width: 14%;
}

.info-table td {
  padding: 10px 14px;
  border: 1px solid #e8ecf1;
  color: #4e5969;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.data-table th {
  background: #f0f5ff;
  color: #1d2129;
  font-weight: 600;
  padding: 10px 8px;
  border: 1px solid #e8ecf1;
  text-align: center;
}

.data-table td {
  padding: 8px;
  border: 1px solid #e8ecf1;
  color: #4e5969;
}

.text-center {
  text-align: center;
}

.empty-cell {
  text-align: center;
  color: #c9cdd4;
  padding: 24px !important;
}

.tensioner-type-tag {
  display: inline-block;
  background: #e8f3ff;
  color: #409eff;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 12px;
}

.alignment-input-info {
  margin-bottom: 12px;
  font-size: 13px;
  color: #4e5969;
}

.alignment-input-info b {
  color: #409eff;
  font-weight: 600;
}

.table-wrapper {
  overflow-x: auto;
}

.alignment-table {
  min-width: 1100px;
}

.alignment-table th.col-blue {
  color: #409eff;
}

.pulley-pair-cell {
  white-space: nowrap;
}

.pair-code {
  background: #e8f3ff;
  padding: 2px 6px;
  border-radius: 3px;
  font-weight: 600;
  font-size: 11px;
}

.pair-arrow {
  color: #409eff;
  margin: 0 2px;
  font-weight: 600;
}

.bea-cell {
  color: #ff7d00;
  font-weight: 600;
}

.na-cell {
  color: #c9cdd4;
}

.remark-block {
  margin-bottom: 12px;
}

.remark-label {
  font-size: 13px;
  font-weight: 600;
  color: #1d2129;
  margin-bottom: 6px;
}

.remark-content {
  font-size: 13px;
  color: #4e5969;
  line-height: 1.7;
  padding: 10px 14px;
  background: #f7f8fa;
  border-radius: 4px;
  border-left: 3px solid #409eff;
}

.report-footer {
  margin-top: 40px;
  padding-top: 16px;
  border-top: 1px solid #e8ecf1;
  text-align: right;
}

.footer-date {
  font-size: 12px;
  color: #86909c;
}

@media print {
  .no-print {
    display: none !important;
  }

  .report-page {
    padding: 0;
    background: #fff;
  }

  .report-container {
    max-width: 100%;
    margin: 0;
    padding: 20px;
    box-shadow: none;
  }
}
</style>
