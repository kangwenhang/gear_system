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
      <!-- 第1页：项目信息与布局输入 -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>FEAD 性能分析报告</h1>
          <div class="page-num">第 1 页 / 共 {{ totalPages }} 页</div>
        </div>

        <div class="report-section">
          <h2>项目信息</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">客户</span>
              <span class="info-value">{{ formInfo.customer || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">项目名称</span>
              <span class="info-value">{{ formInfo.project || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">发动机缸数</span>
              <span class="info-value">{{ formInfo.cylinders || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">额定功率</span>
              <span class="info-value">{{ formInfo.power ? formInfo.power + ' kW' : '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">额定转速</span>
              <span class="info-value">{{ formInfo.rated_speed ? formInfo.rated_speed + ' rpm' : '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">怠速转速</span>
              <span class="info-value">{{ formInfo.idle_speed ? formInfo.idle_speed + ' rpm' : '--' }}</span>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h2>轮系布局</h2>
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
          <h2>皮带数据</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">皮带类型</span>
              <span class="info-value">{{ beltFullParams.belt_type || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">厂家/型号</span>
              <span class="info-value">{{ beltFullParams.manufacturer || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">肋数</span>
              <span class="info-value">{{ beltFullParams.ribs || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">有效长度</span>
              <span class="info-value">{{ beltFullParams.effective_length ? beltFullParams.effective_length + ' mm' : '--' }}</span>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h2>张紧器数据</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">张紧器类型</span>
              <span class="info-value">{{ tensioner.type || '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">扭矩</span>
              <span class="info-value">{{ tensioner.torque ? tensioner.torque + ' Nm' : '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">安装角度</span>
              <span class="info-value">{{ tensioner.angle ? tensioner.angle + '°' : '--' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">臂长</span>
              <span class="info-value">{{ tensioner.arm_length ? tensioner.arm_length + ' mm' : '--' }}</span>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h2>带轮布局数据</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>序号</th>
                <th>编号</th>
                <th>名称</th>
                <th>类型</th>
                <th>X (mm)</th>
                <th>Y (mm)</th>
                <th>直径 (mm)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys" :key="idx">
                <td>{{ idx + 1 }}</td>
                <td>{{ p.code || '--' }}</td>
                <td>{{ p.name || '--' }}</td>
                <td>{{ p.type === 'flat' ? '平带轮' : '槽轮' }}</td>
                <td>{{ formatNum(p.x) }}</td>
                <td>{{ formatNum(p.y) }}</td>
                <td>{{ formatNum(p.type === 'flat' ? p.flat_dia : p.groove_dia) }}</td>
              </tr>
              <tr v-if="displayPulleys.length === 0">
                <td colspan="7" style="text-align:center;color:#999">暂无数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 第2页：布局数据结果 -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>布局数据结果</h1>
          <div class="page-num">第 2 页 / 共 {{ totalPages }} 页</div>
        </div>

        <div class="layout-compare">
          <div class="layout-card">
            <h3>Min Belt</h3>
            <div class="mini-diagram">
              <svg viewBox="0 0 200 150" style="width:100%">
                <circle cx="60" cy="60" r="25" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <circle cx="140" cy="90" r="20" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <line x1="60" y1="35" x2="140" y2="70" stroke="#67c23a" stroke-width="1.5"/>
                <line x1="60" y1="85" x2="140" y2="110" stroke="#67c23a" stroke-width="1.5"/>
              </svg>
            </div>
            <div class="layout-params">
              <div><span>皮带长度</span><b>{{ formatNum(beltFullParams.min_length) }} mm</b></div>
              <div><span>包角(最小)</span><b>--</b></div>
            </div>
          </div>

          <div class="layout-card">
            <h3>Nominal Belt</h3>
            <div class="mini-diagram">
              <svg viewBox="0 0 200 150" style="width:100%">
                <circle cx="60" cy="60" r="25" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <circle cx="140" cy="85" r="20" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <line x1="60" y1="35" x2="140" y2="65" stroke="#e6a23c" stroke-width="1.5"/>
                <line x1="60" y1="85" x2="140" y2="105" stroke="#e6a23c" stroke-width="1.5"/>
              </svg>
            </div>
            <div class="layout-params">
              <div><span>皮带长度</span><b>{{ formatNum(beltFullParams.effective_length) }} mm</b></div>
              <div><span>包角(名义)</span><b>--</b></div>
            </div>
          </div>

          <div class="layout-card">
            <h3>Max Belt</h3>
            <div class="mini-diagram">
              <svg viewBox="0 0 200 150" style="width:100%">
                <circle cx="60" cy="60" r="25" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <circle cx="140" cy="80" r="20" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <line x1="60" y1="35" x2="140" y2="60" stroke="#f56c6c" stroke-width="1.5"/>
                <line x1="60" y1="85" x2="140" y2="100" stroke="#f56c6c" stroke-width="1.5"/>
              </svg>
            </div>
            <div class="layout-params">
              <div><span>皮带长度</span><b>{{ formatNum(beltFullParams.max_length) }} mm</b></div>
              <div><span>包角(最大)</span><b>--</b></div>
            </div>
          </div>

          <div class="layout-card">
            <h3>Stretch &amp; wear</h3>
            <div class="mini-diagram">
              <svg viewBox="0 0 200 150" style="width:100%">
                <circle cx="60" cy="65" r="25" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <circle cx="140" cy="85" r="20" fill="none" stroke="#409eff" stroke-width="1.5"/>
                <line x1="60" y1="40" x2="140" y2="65" stroke="#909399" stroke-width="1.5" stroke-dasharray="4,2"/>
                <line x1="60" y1="90" x2="140" y2="105" stroke="#909399" stroke-width="1.5" stroke-dasharray="4,2"/>
              </svg>
            </div>
            <div class="layout-params">
              <div><span>伸长量</span><b>{{ formatNum(beltFullParams.stretch) }} mm</b></div>
              <div><span>磨损量</span><b>--</b></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 第3页：几何分析结果 -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>几何分析结果</h1>
          <div class="page-num">第 3 页 / 共 {{ totalPages }} 页</div>
        </div>

        <div class="report-section">
          <h2>皮带数据</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>参数</th>
                <th>Min Belt</th>
                <th>Nominal</th>
                <th>Max Belt</th>
                <th>单位</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>有效长度</td>
                <td>{{ formatNum(beltFullParams.min_length) }}</td>
                <td>{{ formatNum(beltFullParams.effective_length) }}</td>
                <td>{{ formatNum(beltFullParams.max_length) }}</td>
                <td>mm</td>
              </tr>
              <tr>
                <td>长度公差</td>
                <td colspan="3" style="text-align:center">{{ formatNum(beltFullParams.length_tolerance) }}</td>
                <td>mm</td>
              </tr>
              <tr>
                <td>延伸率</td>
                <td colspan="3" style="text-align:center">{{ formatNum(beltFullParams.elongation) }}</td>
                <td>%</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>张紧器数据</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>参数</th>
                <th>数值</th>
                <th>单位</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>张紧器扭矩</td>
                <td>{{ formatNum(tensioner.torque) }}</td>
                <td>Nm</td>
              </tr>
              <tr>
                <td>安装角度</td>
                <td>{{ formatNum(tensioner.angle) }}</td>
                <td>deg</td>
              </tr>
              <tr>
                <td>行程角</td>
                <td>--</td>
                <td>deg</td>
              </tr>
              <tr>
                <td>臂长</td>
                <td>{{ formatNum(tensioner.arm_length) }}</td>
                <td>mm</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>张紧轮几何参数</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>状态</th>
                <th>角度 (deg)</th>
                <th>X (mm)</th>
                <th>Y (mm)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Min Belt</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
              <tr>
                <td>Nominal</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
              <tr>
                <td>Max Belt</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>带轮系统几何参数</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>带轮</th>
                <th>包角 (deg)</th>
                <th>Span In (mm)</th>
                <th>Span Out (mm)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.slice(0, 5)" :key="idx">
                <td>{{ p.code || '轮'+(idx+1) }}</td>
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
          <h1>几何分析结果（续）</h1>
          <div class="page-num">第 4 页 / 共 {{ totalPages }} 页</div>
        </div>

        <div class="report-section">
          <h2>带轮轴向偏移允许值</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>带轮</th>
                <th>允许偏移 (mm)</th>
                <th>允许偏移 (deg)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.slice(0, 5)" :key="idx">
                <td>{{ p.code || '轮'+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>动态分析输入 - 负载数据</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>工况</th>
                <th>占空比</th>
                <th>转速 (rpm)</th>
                <th>温度 (°C)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>怠速</td>
                <td>--</td>
                <td>{{ formInfo.idle_speed || '--' }}</td>
                <td>--</td>
              </tr>
              <tr>
                <td>额定</td>
                <td>--</td>
                <td>{{ formInfo.rated_speed || '--' }}</td>
                <td>--</td>
              </tr>
              <tr>
                <td>最大扭矩</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>附件负载数据</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>附件</th>
                <th>怠速 (Nm)</th>
                <th>额定 (Nm)</th>
                <th>最大 (Nm)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.filter(p => p.accessory).slice(0, 5)" :key="idx">
                <td>{{ p.name || p.code || '附件'+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>附件惯性和加速度</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>附件</th>
                <th>惯性 (kg·m²)</th>
                <th>角加速度 (rad/s²)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.filter(p => p.accessory).slice(0, 5)" :key="idx">
                <td>{{ p.name || p.code || '附件'+(idx+1) }}</td>
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
          <h1>动态分析结果</h1>
          <div class="page-num">第 5 页 / 共 {{ totalPages }} 页</div>
        </div>

        <div class="report-section">
          <h2>皮带打滑安全系数</h2>
          <div class="chart-placeholder">
            <div class="chart-bar">
              <div class="bar-item" v-for="(p, idx) in displayPulleys.slice(0, 6)" :key="idx">
                <div class="bar-value" :style="{ height: (60 + Math.random()*30) + '%', background: idx < 3 ? '#67c23a' : '#e6a23c' }"></div>
                <div class="bar-label">{{ p.code || 'P'+(idx+1) }}</div>
              </div>
            </div>
            <div class="chart-legend">
              <span class="legend-item"><i style="background:#67c23a"></i>安全</span>
              <span class="legend-item"><i style="background:#e6a23c"></i>警告</span>
              <span class="legend-item"><i style="background:#f56c6c"></i>危险</span>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h2>打滑安全系数汇总</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>带轮</th>
                <th>怠速</th>
                <th>额定</th>
                <th>最大扭矩</th>
                <th>评定</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.slice(0, 5)" :key="idx">
                <td>{{ p.code || '轮'+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
                <td><el-tag size="small" type="info">待计算</el-tag></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>带轮平均轮毂载荷</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>带轮</th>
                <th>怠速 (N)</th>
                <th>额定 (N)</th>
                <th>最大扭矩 (N)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.slice(0, 5)" :key="idx">
                <td>{{ p.code || '轮'+(idx+1) }}</td>
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
          <h1>动态分析结果（续）</h1>
          <div class="page-num">第 6 页 / 共 {{ totalPages }} 页</div>
        </div>

        <div class="report-section">
          <h2>带轮峰值轮毂载荷</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>带轮</th>
                <th>怠速 (N)</th>
                <th>额定 (N)</th>
                <th>最大扭矩 (N)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, idx) in displayPulleys.slice(0, 5)" :key="idx">
                <td>{{ p.code || '轮'+(idx+1) }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>皮带平均张力</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>工况</th>
                <th>紧边张力 (N)</th>
                <th>松边张力 (N)</th>
                <th>平均张力 (N)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>怠速</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
              <tr>
                <td>额定</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
              <tr>
                <td>最大扭矩</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>皮带肋疲劳数据</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>工况</th>
                <th>最大弯曲应力 (MPa)</th>
                <th>循环次数</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>怠速</td>
                <td>--</td>
                <td>--</td>
              </tr>
              <tr>
                <td>额定</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>皮带挠曲寿命和 B10 寿命</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>参数</th>
                <th>数值</th>
                <th>单位</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>B10 寿命</td>
                <td>--</td>
                <td>小时</td>
              </tr>
              <tr>
                <td>挠曲寿命</td>
                <td>--</td>
                <td>循环</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 第7页：动态分析结果（续） -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>动态分析结果（续）</h1>
          <div class="page-num">第 7 页 / 共 {{ totalPages }} 页</div>
        </div>

        <div class="report-section">
          <h2>皮带跨度固有频率分析</h2>
          <div class="chart-placeholder">
            <svg viewBox="0 0 500 200" style="width:100%">
              <line x1="40" y1="170" x2="480" y2="170" stroke="#ddd" stroke-width="1"/>
              <line x1="40" y1="20" x2="40" y2="170" stroke="#ddd" stroke-width="1"/>
              <path d="M40,150 Q100,100 160,140 T280,130 T400,120 T480,125"
                fill="none" stroke="#409eff" stroke-width="2"/>
              <text x="20" y="25" font-size="10" fill="#999">频率(Hz)</text>
              <text x="460" y="185" font-size="10" fill="#999">跨度</text>
              <line x1="40" y1="100" x2="480" y2="100" stroke="#f56c6c" stroke-width="1" stroke-dasharray="4,4"/>
              <text x="485" y="103" font-size="10" fill="#f56c6c">怠速激励</text>
            </svg>
          </div>
        </div>

        <div class="report-section">
          <h2>固有频率数据表</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>跨度</th>
                <th>一阶频率 (Hz)</th>
                <th>二阶频率 (Hz)</th>
                <th>三阶频率 (Hz)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="n in 5" :key="n">
                <td>跨度 {{ n }}</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>频率窗口说明</h2>
          <div class="freq-note">
            <p><b>怠速激励频率：</b>由发动机怠速转速和气缸数决定</p>
            <p><b>注意事项：</b>皮带跨度的各阶固有频率应避开怠速激励频率及其倍频，以避免共振。</p>
            <p style="margin-top:10px;color:#67c23a"><b>评定结果：</b>待计算</p>
          </div>
        </div>

        <div class="report-footer">
          <p>— 报告结束 —</p>
          <p class="report-date">生成时间：{{ currentDate }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { sharedStore } from '../store/shared.js'

const emit = defineEmits(['back'])
const totalPages = 7

const formInfo = computed(() => sharedStore.formInfo)
const tensioner = computed(() => sharedStore.tensioner)
const beltFullParams = computed(() => sharedStore.beltFullParams)
const pulleys = computed(() => sharedStore.pulleys)

const displayPulleys = computed(() => {
  return pulleys.value || []
})

const currentDate = computed(() => {
  const now = new Date()
  return now.toLocaleString('zh-CN')
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
  padding: 14px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e8ecf1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.toolbar-center .page-indicator {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
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
