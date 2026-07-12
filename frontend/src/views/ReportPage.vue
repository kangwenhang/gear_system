<template>
  <div class="report-page">
    <div class="report-toolbar no-print">
      <div class="toolbar-left">
        <el-button @click="handleBack">
          <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
          返回编辑
        </el-button>
      </div>
      <div class="toolbar-center">
        <span class="page-indicator">FEAD 性能分析报告 · 共 {{ totalPages }} 页</span>
      </div>
      <div class="toolbar-right">
        <el-dropdown @command="handleLangChange" trigger="click" class="lang-dropdown">
          <el-button>
            <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="2" y1="12" x2="22" y2="12"/>
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
            </svg>
            {{ currentLangLabel }}
            <i class="el-icon-arrow-down" style="margin-left:4px"></i>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="zh-CN" :disabled="currentLang === 'zh-CN'">中文</el-dropdown-item>
              <el-dropdown-item command="en-US" :disabled="currentLang === 'en-US'">English</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button type="primary" @click="handlePrint" style="margin-left:8px">
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
      <!-- 第1页：项目信息与布局输入 -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>{{ t('pages.p1') }}</h1>
          <div class="page-num">{{ pageLabel(1) }} / {{ t('toolbar.pages', totalPages) }}</div>
        </div>

        <div class="report-section">
          <h2>{{ t('projectInfo') }}</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">{{ t('customer') }}</span>
              <span class="info-value">{{ formInfo.customer || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('projectName') }}</span>
              <span class="info-value">{{ formInfo.project || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('cylinders') }}</span>
              <span class="info-value">{{ formInfo.cylinders || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('ratedPower') }}</span>
              <span class="info-value">{{ formInfo.power ? formInfo.power + ' kW' : '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('ratedSpeed') }}</span>
              <span class="info-value">{{ formInfo.rated_speed ? formInfo.rated_speed + ' rpm' : '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('idleSpeed') }}</span>
              <span class="info-value">{{ formInfo.idle_speed ? formInfo.idle_speed + ' rpm' : '--' }}</span>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h2>{{ t('layout') }}</h2>
          <div class="diagram-box">
            <div class="diagram-placeholder">
              <svg viewBox="0 0 400 200" style="width:100%;max-width:400px">
                <circle v-for="(p, idx) in displayPulleys" :key="idx"
                  :cx="100 + p.x * 0.5" :cy="100 - p.y * 0.3"
                  :r="(p.flat_dia || p.groove_dia || 50) * 0.2"
                  fill="none" stroke="#409eff" stroke-width="2"/>
                <text v-for="(p, idx) in displayPulleys" :key="'t'+idx"
                  :x="100 + p.x * 0.5" :y="100 - p.y * 0.3"
                  text-anchor="middle" dominant-baseline="middle"
                  font-size="10" fill="#333">{{ p.code || 'P'+(idx+1) }}</text>
              </svg>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h2>{{ t('beltData') }}</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">{{ t('beltType') }}</span>
              <span class="info-value">{{ beltFullParams.belt_type || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('manufacturer') }}</span>
              <span class="info-value">{{ beltFullParams.manufacturer || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('ribs') }}</span>
              <span class="info-value">{{ beltFullParams.ribs || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('effectiveLength') }}</span>
              <span class="info-value">{{ beltFullParams.effective_length ? beltFullParams.effective_length + ' mm' : '--' }}</span>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h2>{{ t('tensionerData') }}</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">{{ t('tensionerType') }}</span>
              <span class="info-value">{{ tensioner.type || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('torque') }}</span>
              <span class="info-value">{{ tensioner.torque ? tensioner.torque + ' Nm' : '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('installAngle') }}</span>
              <span class="info-value">{{ tensioner.angle ? tensioner.angle + '°' : '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ t('armLength') }}</span>
              <span class="info-value">{{ tensioner.arm_length ? tensioner.arm_length + ' mm' : '--' }}</span>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h2>{{ t('pulleyLayout') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('pulleyTable.index') }}</th>
                <th>{{ t('pulleyTable.code') }}</th>
                <th>{{ t('pulleyTable.name') }}</th>
                <th>{{ t('pulleyTable.type') }}</th>
                <th>{{ t('pulleyTable.x') }}</th>
                <th>{{ t('pulleyTable.y') }}</th>
                <th>{{ t('pulleyTable.diameter') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys" :key="idx">
                <td>{{ idx + 1 }}</td>
                <td>{{ p.code || '--' }}</td>
                <td>{{ p.name || '--' }}</td>
                <td>{{ p.type === 'flat' ? t('pulleyTable.typeFlat') : t('pulleyTable.typeGroove') }}</td>
                <td>{{ formatNum(p.x) }}</td>
                <td>{{ formatNum(p.y) }}</td>
                <td>{{ formatNum(p.type === 'flat' ? p.flat_dia : p.groove_dia) }}</td>
              </tr>
              <tr v-if="displayPulleys.length === 0">
                <td colspan="7" style="text-align:center;color:#999">{{ t('pulleyTable.noData') }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 第2页：布局数据结果 -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>{{ t('pages.p2') }}</h1>
          <div class="page-num">{{ pageLabel(2) }} / {{ t('toolbar.pages', totalPages) }}</div>
        </div>

        <div class="layout-compare">
          <div class="layout-card">
            <h3>{{ t('minBelt') }}</h3>
            <div class="mini-diagram">
              <svg viewBox="0 0 200 150" style="width:100%">
                <circle cx="60" cy="60" r="25" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <circle cx="140" cy="90" r="20" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <line x1="60" y1="35" x2="140" y2="70" stroke="#67c23a" stroke-width="1.5"/>
                <line x1="60" y1="85" x2="140" y2="110" stroke="#67c23a" stroke-width="1.5"/>
              </svg>
            </div>
            <div class="layout-params">
              <div><span>{{ t('beltLength') }}</span><b>{{ formatNum(beltFullParams.min_length) }} mm</b></div>
              <div><span>{{ t('wrapMin') }}</span><b>--</b></div>
            </div>
          </div>

          <div class="layout-card">
            <h3>{{ t('nominalBelt') }}</h3>
            <div class="mini-diagram">
              <svg viewBox="0 0 200 150" style="width:100%">
                <circle cx="60" cy="60" r="25" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <circle cx="140" cy="85" r="20" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <line x1="60" y1="35" x2="140" y2="65" stroke="#e6a23c" stroke-width="1.5"/>
                <line x1="60" y1="85" x2="140" y2="105" stroke="#e6a23c" stroke-width="1.5"/>
              </svg>
            </div>
            <div class="layout-params">
              <div><span>{{ t('beltLength') }}</span><b>{{ formatNum(beltFullParams.effective_length) }} mm</b></div>
              <div><span>{{ t('wrapNominal') }}</span><b>--</b></div>
            </div>
          </div>

          <div class="layout-card">
            <h3>{{ t('maxBelt') }}</h3>
            <div class="mini-diagram">
              <svg viewBox="0 0 200 150" style="width:100%">
                <circle cx="60" cy="60" r="25" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <circle cx="140" cy="80" r="20" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <line x1="60" y1="35" x2="140" y2="60" stroke="#f56c6c" stroke-width="1.5"/>
                <line x1="60" y1="85" x2="140" y2="100" stroke="#f56c6c" stroke-width="1.5"/>
              </svg>
            </div>
            <div class="layout-params">
              <div><span>{{ t('beltLength') }}</span><b>{{ formatNum(beltFullParams.max_length) }} mm</b></div>
              <div><span>{{ t('wrapMax') }}</span><b>--</b></div>
            </div>
          </div>

          <div class="layout-card">
            <h3>{{ t('stretchWear') }}</h3>
            <div class="mini-diagram">
              <svg viewBox="0 0 200 150" style="width:100%">
                <circle cx="60" cy="65" r="25" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <circle cx="140" cy="85" r="20" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <line x1="60" y1="40" x2="140" y2="65" stroke="#909399" stroke-width="1.5" stroke-dasharray="4,2"/>
                <line x1="60" y1="90" x2="140" y2="105" stroke="#909399" stroke-width="1.5" stroke-dasharray="4,2"/>
              </svg>
            </div>
            <div class="layout-params">
              <div><span>{{ t('stretch') }}</span><b>{{ formatNum(beltFullParams.stretch) }} mm</b></div>
              <div><span>{{ t('wear') }}</span><b>--</b></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 第3页：几何分析结果 -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>{{ t('pages.p3') }}</h1>
          <div class="page-num">{{ pageLabel(3) }} / {{ t('toolbar.pages', totalPages) }}</div>
        </div>

        <div class="report-section">
          <h2>{{ t('beltData') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('parameter') }}</th>
                <th>{{ t('min') }}</th>
                <th>{{ t('nominal') }}</th>
                <th>{{ t('max') }}</th>
                <th>{{ t('unit') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ t('effectiveLength') }}</td>
                <td>{{ formatNum(beltFullParams.min_length) }}</td>
                <td>{{ formatNum(beltFullParams.effective_length) }}</td>
                <td>{{ formatNum(beltFullParams.max_length) }}</td>
                <td>mm</td>
              </tr>
              <tr>
                <td>{{ t('lengthTolerance') }}</td>
                <td colspan="3" style="text-align:center">{{ formatNum(beltFullParams.length_tolerance) }}</td>
                <td>mm</td>
              </tr>
              <tr>
                <td>{{ t('elongation') }}</td>
                <td colspan="3" style="text-align:center">{{ formatNum(beltFullParams.elongation) }}</td>
                <td>%</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('tensionerData') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('parameter') }}</th>
                <th>{{ t('value') }}</th>
                <th>{{ t('unit') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ t('torque') }}</td>
                <td>{{ formatNum(tensioner.torque) }}</td>
                <td>Nm</td>
              </tr>
              <tr>
                <td>{{ t('installAngle') }}</td>
                <td>{{ formatNum(tensioner.angle) }}</td>
                <td>deg</td>
              </tr>
              <tr>
                <td>{{ t('travelAngle') }}</td>
                <td>--</td>
                <td>deg</td>
              </tr>
              <tr>
                <td>{{ t('armLength') }}</td>
                <td>{{ formatNum(tensioner.arm_length) }}</td>
                <td>mm</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('tensionerPulleyGeom') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('state') }}</th>
                <th>{{ t('angle') }} (deg)</th>
                <th>X (mm)</th>
                <th>Y (mm)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ t('min') }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
              <tr>
                <td>{{ t('nominal') }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
              <tr>
                <td>{{ t('max') }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('pulleySystemGeom') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('pulley') }}</th>
                <th>{{ t('wrapAngle') }} (deg)</th>
                <th>{{ t('spanIn') }} (mm)</th>
                <th>{{ t('spanOut') }} (mm)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.slice(0, 5)" :key="idx">
                <td>{{ p.code || t('pulleyPlaceholder')+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 第4页：几何分析续 + 动态分析输入 -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>{{ t('pages.p4') }}</h1>
          <div class="page-num">{{ pageLabel(4) }} / {{ t('toolbar.pages', totalPages) }}</div>
        </div>

        <div class="report-section">
          <h2>{{ t('axialOffset') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('pulley') }}</th>
                <th>{{ t('allowOffsetMm') }}</th>
                <th>{{ t('allowOffsetDeg') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.slice(0, 5)" :key="idx">
                <td>{{ p.code || t('pulleyPlaceholder')+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('dynamicInput') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('condition') }}</th>
                <th>{{ t('dutyCycle') }}</th>
                <th>{{ t('speed') }} (rpm)</th>
                <th>{{ t('temperature') }} (°C)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ t('idle') }}</td>
                <td>--</td>
                <td>{{ formInfo.idle_speed || '--' }}</td>
                <td>--</td>
              </tr>
              <tr>
                <td>{{ t('rated') }}</td>
                <td>--</td>
                <td>{{ formInfo.rated_speed || '--' }}</td>
                <td>--</td>
              </tr>
              <tr>
                <td>{{ t('maxTorque') }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('accessoryLoad') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('accessory') }}</th>
                <th>{{ t('idle') }} (Nm)</th>
                <th>{{ t('rated') }} (Nm)</th>
                <th>{{ t('max') }} (Nm)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.filter(p => p.accessory).slice(0, 5)" :key="idx">
                <td>{{ p.name || p.code || t('accessoryPlaceholder')+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('accessoryInertia') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('accessory') }}</th>
                <th>{{ t('inertia') }} (kg·m²)</th>
                <th>{{ t('angularAccel') }} (rad/s²)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.filter(p => p.accessory).slice(0, 5)" :key="idx">
                <td>{{ p.name || p.code || t('accessoryPlaceholder')+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 第5页：动态分析结果 -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>{{ t('pages.p5') }}</h1>
          <div class="page-num">{{ pageLabel(5) }} / {{ t('toolbar.pages', totalPages) }}</div>
        </div>

        <div class="report-section">
          <h2>{{ t('slipSafetyFactor') }}</h2>
          <div class="chart-placeholder">
            <div class="chart-bar">
              <div class="bar-item" v-for="(p, idx) in displayPulleys.slice(0, 6)" :key="idx">
                <div class="bar-value" :style="{ height: (60 + Math.random()*30) + '%', background: idx < 3 ? '#67c23a' : '#e6a23c' }"></div>
                <div class="bar-label">{{ p.code || 'P'+(idx+1) }}</div>
              </div>
            </div>
            <div class="chart-legend">
              <span class="legend-item"><i style="background:#67c23a"></i>{{ t('safety') }}</span>
              <span class="legend-item"><i style="background:#e6a23c"></i>{{ t('warning') }}</span>
              <span class="legend-item"><i style="background:#f56c6c"></i>{{ t('danger') }}</span>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h2>{{ t('slipSummary') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('pulley') }}</th>
                <th>{{ t('idle') }}</th>
                <th>{{ t('rated') }}</th>
                <th>{{ t('maxTorque') }}</th>
                <th>{{ t('evaluation') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.slice(0, 5)" :key="idx">
                <td>{{ p.code || t('pulleyPlaceholder')+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
                <td><el-tag size="small" type="info">{{ t('pending') }}</el-tag></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('averageHubLoad') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('pulley') }}</th>
                <th>{{ t('idle') }} (N)</th>
                <th>{{ t('rated') }} (N)</th>
                <th>{{ t('maxTorque') }} (N)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.slice(0, 5)" :key="idx">
                <td>{{ p.code || t('pulleyPlaceholder')+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 第6页：动态分析结果（续） -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>{{ t('pages.p6') }}</h1>
          <div class="page-num">{{ pageLabel(6) }} / {{ t('toolbar.pages', totalPages) }}</div>
        </div>

        <div class="report-section">
          <h2>{{ t('peakHubLoad') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('pulley') }}</th>
                <th>{{ t('idle') }} (N)</th>
                <th>{{ t('rated') }} (N)</th>
                <th>{{ t('maxTorque') }} (N)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.slice(0, 5)" :key="idx">
                <td>{{ p.code || t('pulleyPlaceholder')+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('avgBeltTension') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('condition') }}</th>
                <th>{{ t('tightTension') }} (N)</th>
                <th>{{ t('slackTension') }} (N)</th>
                <th>{{ t('avgTension') }} (N)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ t('idle') }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
              <tr>
                <td>{{ t('rated') }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
              <tr>
                <td>{{ t('maxTorque') }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('ribFatigue') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('condition') }}</th>
                <th>{{ t('maxBendingStress') }} (MPa)</th>
                <th>{{ t('cycles') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ t('idle') }}</td>
                <td>--</td>
                <td>--</td>
              </tr>
              <tr>
                <td>{{ t('rated') }}</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('flexLife') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('parameter') }}</th>
                <th>{{ t('value') }}</th>
                <th>{{ t('unit') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ t('b10Life') }}</td>
                <td>--</td>
                <td>{{ t('hour') }}</td>
              </tr>
              <tr>
                <td>{{ t('flexLifeCycles') }}</td>
                <td>--</td>
                <td>{{ t('cycle') }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 第7页：动态分析结果（续） -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>{{ t('pages.p7') }}</h1>
          <div class="page-num">{{ pageLabel(7) }} / {{ t('toolbar.pages', totalPages) }}</div>
        </div>

        <div class="report-section">
          <h2>{{ t('freqAnalysis') }}</h2>
          <div class="chart-placeholder">
            <svg viewBox="0 0 500 200" style="width:100%">
              <line x1="40" y1="170" x2="480" y2="170" stroke="#ddd" stroke-width="1"/>
              <line x1="40" y1="20" x2="40" y2="170" stroke="#ddd" stroke-width="1"/>
              <path d="M40,150 Q100,100 160,140 T280,130 T400,120 T480,125"
                fill="none" stroke="#409eff" stroke-width="2"/>
              <text x="20" y="25" font-size="10" fill="#999">{{ t('freqLabel') }}</text>
              <text x="460" y="185" font-size="10" fill="#999">{{ t('spanLabel') }}</text>
              <line x1="40" y1="100" x2="480" y2="100" stroke="#f56c6c" stroke-width="1" stroke-dasharray="4,4"/>
              <text x="485" y="103" font-size="10" fill="#f56c6c">{{ t('idleExcitation') }}</text>
            </svg>
          </div>
        </div>

        <div class="report-section">
          <h2>{{ t('freqTable') }}</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>{{ t('span') }}</th>
                <th>{{ t('firstOrder') }} (Hz)</th>
                <th>{{ t('secondOrder') }} (Hz)</th>
                <th>{{ t('thirdOrder') }} (Hz)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="n in 5" :key="n">
                <td>{{ t('span') }} {{ n }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('freqNote') }}</h2>
          <div class="freq-note">
            <p><b>{{ t('idleExcitation') }}：</b>{{ t('idleExcitationDesc') }}</p>
            <p><b>{{ t('attention') }}：</b>{{ t('resonanceNote') }}</p>
            <p style="margin-top:10px;color:#67c23a"><b>{{ t('evalResult') }}：</b>{{ t('pending') }}</p>
          </div>
        </div>

        <div class="report-footer">
          <p>{{ t('reportEnd') }}</p>
          <p class="report-date">{{ t('generatedAt') }}：{{ currentDate }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { sharedStore } from '../store/shared.js'
import { t, getLang, setLang, SUPPORTED_LANGS } from '../store/i18n.js'

const emit = defineEmits(['back'])
const totalPages = 7

const formInfo = computed(() => sharedStore.formInfo)
const tensioner = computed(() => sharedStore.tensioner)
const beltFullParams = computed(() => sharedStore.beltFullParams)
const pulleys = computed(() => sharedStore.pulleys)

const displayPulleys = computed(() => {
  return pulleys.value || []
})

// 响应式语言
const currentLang = ref(getLang())
const currentLangLabel = computed(() => currentLang.value === 'zh-CN' ? '中文' : 'English')

function handleLangChange(cmd) {
  setLang(cmd)
  currentLang.value = getLang()
}

// 生成页码标签（中英文）
function pageLabel(n) {
  return currentLang.value === 'zh-CN' ? `第 ${n} 页` : `Page ${n}`
}

const currentDate = computed(() => {
  const now = new Date()
  if (currentLang.value === 'zh-CN') {
    return now.toLocaleString('zh-CN')
  } else {
    return now.toLocaleString('en-US')
  }
})

function formatNum(val) {
  if (val === null || val === undefined || isNaN(val) || val === '') return '--'
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
  min-height: 100vh;
  background: #f0f2f5;
  padding-bottom: 40px;
}

.report-toolbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  padding: 14px 24px 14px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e8ecf1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.toolbar-center {
  flex: 1;
  text-align: center;
  padding: 0 20px;
}

.toolbar-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-shrink: 0;
}

.toolbar-center .page-indicator {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.lang-dropdown {
  display: inline-block;
}

.report-container {
  max-width: 900px;
  margin: 24px auto;
  padding: 0 16px;
}

.report-page-break {
  background: #fff;
  padding: 40px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border-radius: 4px;
  min-height: 1100px;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 2px solid #409eff;
}

.page-header h1 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 8px;
}

.page-num {
  font-size: 13px;
  color: #909399;
}

.report-section {
  margin-bottom: 28px;
}

.report-section h2 {
  font-size: 16px;
  color: #303133;
  margin-bottom: 12px;
  padding-left: 10px;
  border-left: 4px solid #409eff;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
  padding: 10px 14px;
  background: #f8fafc;
  border-radius: 4px;
}

.info-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.info-value {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.diagram-box {
  background: #f8fafc;
  border-radius: 4px;
  padding: 20px;
  display: flex;
  justify-content: center;
}

.diagram-placeholder {
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.data-table th,
.data-table td {
  border: 1px solid #e4e7ed;
  padding: 8px 12px;
  text-align: center;
}

.data-table th {
  background: #f5f7fa;
  color: #606266;
  font-weight: 600;
}

.data-table tbody tr:hover {
  background: #f8fafc;
}

.layout-compare {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.layout-card {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e4e7ed;
}

.layout-card h3 {
  font-size: 14px;
  color: #303133;
  margin-bottom: 12px;
  text-align: center;
}

.mini-diagram {
  background: #fff;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 12px;
}

.layout-params {
  font-size: 12px;
}

.layout-params div {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
}

.layout-params span {
  color: #909399;
}

.layout-params b {
  color: #303133;
}

.chart-placeholder {
  background: #f8fafc;
  border-radius: 4px;
  padding: 20px;
  min-height: 200px;
}

.chart-bar {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 16px;
  height: 140px;
  margin-bottom: 12px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: 40px;
  height: 100%;
  justify-content: flex-end;
}

.bar-value {
  width: 100%;
  border-radius: 3px 3px 0 0;
  min-height: 8px;
}

.bar-label {
  font-size: 11px;
  color: #606266;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  font-size: 12px;
  color: #606266;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-item i {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.freq-note {
  background: #f8fafc;
  border-radius: 4px;
  padding: 16px;
  font-size: 13px;
  color: #606266;
  line-height: 1.8;
}

.report-footer {
  text-align: center;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
  color: #909399;
  font-size: 13px;
}

.report-date {
  margin-top: 8px;
  font-size: 12px;
}

/* 打印样式 */
@media print {
  .report-page {
    background: #fff;
    padding: 0;
  }

  .no-print {
    display: none !important;
  }

  .report-container {
    max-width: 100%;
    margin: 0;
    padding: 0;
  }

  .report-page-break {
    box-shadow: none;
    margin: 0;
    padding: 20px;
    min-height: auto;
    page-break-after: always;
    break-after: page;
  }

  .report-page-break:last-child {
    page-break-after: auto;
    break-after: auto;
  }
}

/* 移动端 */
@media (max-width: 768px) {
  .report-toolbar {
    padding: 10px 16px;
    flex-wrap: wrap;
    gap: 8px;
  }

  .toolbar-center {
    order: -1;
    width: 100%;
    text-align: center;
  }

  .toolbar-left,
  .toolbar-right {
    flex: 1;
  }

  .report-page-break {
    padding: 20px 16px;
    min-height: auto;
  }

  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .layout-compare {
    grid-template-columns: 1fr;
  }

  .data-table {
    font-size: 12px;
  }

  .data-table th,
  .data-table td {
    padding: 6px 8px;
  }
}
</style>
