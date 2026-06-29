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
        <span class="page-indicator">共 {{ totalPages }} 页</span>
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
      <!-- ========== 第1页 ========== -->
      <div class="report-page-break">
        <div class="report-header">
          <div class="header-logo">
            <div class="logo-box">ARTIN-TECH</div>
          </div>
          <div class="header-title">FEAD Performance Analysis Report</div>
        </div>
        <div class="header-meta">
          <div class="meta-item"><span class="meta-label">File No. :</span><span class="meta-value">{{ formInfo.fileNo || '--' }}</span></div>
          <div class="meta-item"><span class="meta-label">Version :</span><span class="meta-value">{{ formInfo.version || '01' }}</span></div>
          <div class="meta-item"><span class="meta-label">Date :</span><span class="meta-value">{{ currentDate }}</span></div>
        </div>

        <h2 class="page-title">Project Information</h2>
        <table class="info-table-bordered">
          <tr>
            <th>Client :</th>
            <td>{{ formInfo.customer || '--' }}</td>
            <th>Project:</th>
            <td>{{ formInfo.project || '--' }}</td>
          </tr>
          <tr>
            <th>Number of engine cylinders:</th>
            <td>{{ formInfo.cylinders || '--' }}</td>
            <th>Engine power</th>
            <td>{{ formInfo.power || '--' }} kW</td>
          </tr>
          <tr>
            <th>Problem Statement :</th>
            <td colspan="3" class="text-left">{{ formInfo.issueDesc || '--' }}</td>
          </tr>
          <tr>
            <th>Analysis Reference :</th>
            <td colspan="3" class="text-left">{{ formInfo.updateDesc || '--' }}</td>
          </tr>
        </table>

        <h2 class="page-title">Layout Data (input)</h2>
        <div class="diagram-placeholder">
          <div class="diagram-box">
            <PulleyDiagram :data="pulleysForDiagram" :tensionerData="tensioner" :small="true" />
          </div>
        </div>

        <h2 class="page-title">Geometry Analysis (Input)</h2>
        <h3 class="sub-title">Belt Data (input)</h3>
        <div class="two-col-layout">
          <table class="info-table-bordered small-table">
            <tr><th>Belt name :</th><td>Multi- V Belt</td></tr>
            <tr><th>Belt rib Geometry type :</th><td>{{ beltFullParams?.belt_type || 'PK / EPDM' }}</td></tr>
            <tr><th>No. of Ribs/Cord Material:</th><td>{{ beltFullParams?.belt_pk || '6 PK' }} / Polyester</td></tr>
            <tr><th>Stretch and Wear Allow :</th><td>≤ {{ beltFullParams?.elongation_rate || '0.7' }} % of Length</td></tr>
          </table>
          <table class="info-table-bordered small-table">
            <tr><th colspan="2">Geometric Dimension :</th></tr>
            <tr><th>Belt Height :</th><td>{{ beltFullParams?.height || '--' }} [mm]</td></tr>
            <tr><th>Belt Flat to Pitch :</th><td>{{ beltFullParams?.flat_to_pitch || '--' }} [mm]</td></tr>
            <tr><th>Belt Pitch to Effective :</th><td>{{ beltFullParams?.pitch_to_effective || '--' }} [mm]</td></tr>
          </table>
        </div>

        <h3 class="sub-title">Tensioner Data (input)</h3>
        <div class="two-col-layout">
          <table class="info-table-bordered small-table">
            <tr><th>Tensioner Type :</th><td>{{ tensionerTypeText }}</td></tr>
            <tr v-if="tensioner?.type === 'automatic'">
              <th>Pivot Point {x,y} [mm] :</th>
              <td>{{ formatNum(tensioner?.automatic?.pivot_x) }} , {{ formatNum(tensioner?.automatic?.pivot_y) }}</td>
            </tr>
            <tr v-if="tensioner?.type === 'automatic'">
              <th>Belt Design Tension [N]:</th>
              <td>{{ formatNum(tensioner?.automatic?.tension_value) }} N</td>
            </tr>
            <tr v-else>
              <th>Tension Setting [N]:</th>
              <td>{{ formatNum(tensioner?.manual?.tension_value) }} N</td>
            </tr>
          </table>
          <table class="info-table-bordered small-table">
            <tr v-if="tensioner?.type === 'automatic'">
              <th>Tensioner Arm Length :</th>
              <td>{{ formatNum(tensioner?.automatic?.arm_length) }} [mm]</td>
            </tr>
            <tr v-if="tensioner?.type === 'automatic'">
              <th>Tensioner Arm Angle :</th>
              <td>{{ formatNum(tensioner?.automatic?.work_angle) }} [deg]</td>
            </tr>
            <tr v-if="tensioner?.type === 'automatic'">
              <th>Spring Rate Factor :</th>
              <td>{{ formatNum(tensioner?.automatic?.spring_stiffness) }} [Nm/deg]</td>
            </tr>
            <tr v-else>
              <th colspan="2">Hand Tensioner</th>
            </tr>
          </table>
        </div>

        <h3 class="sub-title">Layout Data (input)</h3>
        <table class="data-table-bordered">
          <thead>
            <tr>
              <th width="40"></th>
              <th>Pulley</th>
              <th>X Coordinate</th>
              <th>Y Coordinate</th>
              <th>Flat Diameter</th>
              <th>Pitch Diameter</th>
              <th>Effective Diameter</th>
              <th>Pulley Type</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, idx) in pulleys10" :key="idx">
              <td class="text-center">{{ idx + 1 }}</td>
              <td class="text-center">{{ p.code || 'NA' }}</td>
              <td class="text-center">{{ formatNum(p.x) }}</td>
              <td class="text-center">{{ formatNum(p.y) }}</td>
              <td class="text-center">{{ p.type === 'flat' ? formatNum(p.flat_dia) : '/' }}</td>
              <td class="text-center">{{ p.type === 'groove' ? formatNum(p.groove_dia) : formatNum(flatToPitch(p)) }}</td>
              <td class="text-center">{{ formatNum(effectiveDia(p)) }}</td>
              <td class="text-center">{{ p.type === 'flat' ? 'Flat' : 'Grooved' }}</td>
            </tr>
          </tbody>
        </table>

        <div class="page-footer">page 1 of {{ totalPages }}</div>
      </div>

      <!-- ========== 第2页 ========== -->
      <div class="report-page-break">
        <div class="report-header">
          <div class="header-logo"><div class="logo-box">ARTIN-TECH</div></div>
          <div class="header-title">FEAD Performance Analysis Report</div>
        </div>
        <div class="header-meta">
          <div class="meta-item"><span class="meta-label">File No. :</span><span class="meta-value">{{ formInfo.fileNo || '--' }}</span></div>
          <div class="meta-item"><span class="meta-label">Version :</span><span class="meta-value">{{ formInfo.version || '01' }}</span></div>
          <div class="meta-item"><span class="meta-label">Date :</span><span class="meta-value">{{ currentDate }}</span></div>
        </div>

        <h2 class="page-title">Layout Data (Results)</h2>
        <div class="four-grid-layout">
          <div class="grid-card">
            <div class="grid-card-title">Min Belt</div>
            <div class="grid-diagram">
              <div class="mini-diagram">
                <PulleyDiagram :data="pulleysForDiagram" :tensionerData="tensioner" :small="true" />
              </div>
            </div>
            <table class="grid-table">
              <tr><th>Jitter risk segment</th><td>--</td></tr>
              <tr><th>Tensioner pulley swing angle</th><td>-- [deg]</td></tr>
              <tr><th>Distance</th><td>-- [mm]</td></tr>
            </table>
          </div>
          <div class="grid-card">
            <div class="grid-card-title">Nominal Belt</div>
            <div class="grid-diagram">
              <div class="mini-diagram">
                <PulleyDiagram :data="pulleysForDiagram" :tensionerData="tensioner" :small="true" />
              </div>
            </div>
            <table class="grid-table">
              <tr><th>Jitter risk segment</th><td>--</td></tr>
              <tr><th>Tensioner pulley swing angle</th><td>-- [deg]</td></tr>
              <tr><th>Distance</th><td>-- [mm]</td></tr>
            </table>
          </div>
          <div class="grid-card">
            <div class="grid-card-title">Max Belt</div>
            <div class="grid-diagram">
              <div class="mini-diagram">
                <PulleyDiagram :data="pulleysForDiagram" :tensionerData="tensioner" :small="true" />
              </div>
            </div>
            <table class="grid-table">
              <tr><th>Jitter risk segment</th><td>--</td></tr>
              <tr><th>Tensioner pulley swing angle</th><td>-- [deg]</td></tr>
              <tr><th>Distance</th><td>-- [mm]</td></tr>
            </table>
          </div>
          <div class="grid-card">
            <div class="grid-card-title">Stretch &amp; wear</div>
            <div class="grid-diagram">
              <div class="mini-diagram">
                <PulleyDiagram :data="pulleysForDiagram" :tensionerData="tensioner" :small="true" />
              </div>
            </div>
            <table class="grid-table">
              <tr><th>Jitter risk segment</th><td>--</td></tr>
              <tr><th>Tensioner pulley swing angle</th><td>-- [deg]</td></tr>
              <tr><th>Distance</th><td>-- [mm]</td></tr>
            </table>
          </div>
        </div>

        <div class="note-box">
          Belt clearance:5%of belt span length(peak to nominal) at midspan .
        </div>

        <div class="page-footer">page 2 of {{ totalPages }}</div>
      </div>

      <!-- ========== 第3页 ========== -->
      <div class="report-page-break">
        <div class="report-header">
          <div class="header-logo"><div class="logo-box">ARTIN-TECH</div></div>
          <div class="header-title">FEAD Performance Analysis Report</div>
        </div>
        <div class="header-meta">
          <div class="meta-item"><span class="meta-label">File No. :</span><span class="meta-value">{{ formInfo.fileNo || '--' }}</span></div>
          <div class="meta-item"><span class="meta-label">Version :</span><span class="meta-value">{{ formInfo.version || '01' }}</span></div>
          <div class="meta-item"><span class="meta-label">Date :</span><span class="meta-value">{{ currentDate }}</span></div>
        </div>

        <h2 class="page-title">Geometry Analysis (Results)</h2>
        <h3 class="sub-title">Belt Data (Results)</h3>
        <div class="two-col-layout">
          <table class="info-table-bordered small-table">
            <tr><th>Eff.Drive Length (ref.ISO 9981)</th><td>-- [mm]</td></tr>
            <tr><th>Length Tolerance :</th><td>± {{ beltFullParams?.length_tolerance || '--' }} [mm]</td></tr>
          </table>
          <table class="info-table-bordered small-table">
            <tr><th>Max Stretch (Free Arm) :</th><td>-- % of Length</td></tr>
          </table>
        </div>

        <h3 class="sub-title">Tensioner Data (Results)</h3>
        <div class="two-col-layout">
          <table class="info-table-bordered small-table">
            <tr><th>Design Torque [Nm] :</th><td>-- Nm</td></tr>
            <tr><th>Belt Take-up/Arm Ratio :</th><td>-- [mm/deg]</td></tr>
          </table>
          <table class="info-table-bordered small-table">
            <tr><th>Total Travel Angle (Min) :</th><td>≥ -- [deg]</td></tr>
            <tr><th>Nominal Working Angle :</th><td>-- [deg]</td></tr>
          </table>
        </div>

        <h3 class="sub-title">Tensioner Pulley Geometry (Results)</h3>
        <table class="data-table-bordered small-text">
          <thead>
            <tr>
              <th rowspan="2">Tensioner Position</th>
              <th colspan="2">Pulley Position</th>
              <th rowspan="2">Arm Position [deg]</th>
              <th rowspan="2">Effective Belt Length [mm]</th>
              <th rowspan="2">Tensioner Torque [Nm]</th>
              <th rowspan="2">Belt Design Tension [N]</th>
              <th rowspan="2">Pulley Wrap Angle [deg]</th>
              <th rowspan="2">Pulley Hubload [N]</th>
              <th rowspan="2">Hubload Direction [deg]</th>
              <th rowspan="2">Hubload to Arm Angle [deg]</th>
            </tr>
            <tr>
              <th>X</th><th>Y</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in tensionerGeoRows" :key="row.label">
              <td class="text-center">{{ row.label }}</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
            </tr>
          </tbody>
        </table>

        <div class="two-col-layout" style="margin-top: 16px">
          <div>
            <h3 class="sub-title">Belt Drive System Geometry (Results)</h3>
            <table class="data-table-bordered small-text">
              <thead>
                <tr>
                  <th width="30"></th>
                  <th>Pulley</th>
                  <th>Span Length [mm]</th>
                  <th>Wrap Angle [deg]</th>
                  <th>Speed Ratio (Ref.Engine)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(p, idx) in pulleys10" :key="idx">
                  <td class="text-center">{{ idx + 1 }}</td>
                  <td class="text-center">{{ p.code || 'NA' }}</td>
                  <td class="text-center">--</td>
                  <td class="text-center">--</td>
                  <td class="text-center">--</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div>
            <h3 class="sub-title">Belt Take-up Ratio</h3>
            <div class="chart-placeholder">
              <div class="chart-title">Belt Take-up</div>
              <div class="chart-area">
                <div class="chart-bar">
                  <div class="bar-fill" style="height: 60%"></div>
                </div>
              </div>
              <div class="chart-legend">
                <span class="chart-x-label">△Tensioner Arm Position</span>
                <span class="chart-y-label">△Belt [mm]</span>
              </div>
            </div>
          </div>
        </div>

        <div class="two-col-layout" style="margin-top: 16px">
          <div>
            <h3 class="sub-title">Design Geometry</h3>
            <div class="design-geo-box">
              <div class="design-geo-title">Design Geometry and Clearance:</div>
              <div class="design-geo-content">
                <p>1. Span lengths (Min) to be &gt; 75 mm( &gt; 75 mm limit applies for span length fromflat pulley to grooved pulley);</p>
                <p>2. Span lengths (Max) to be &lt; 300 mm;</p>
              </div>
            </div>
          </div>
          <div>
            <h3 class="sub-title">Belt Tension Control (Results)</h3>
            <div class="chart-placeholder small-chart">
              <div class="chart-title">Arm Travel VS Belt Tension</div>
              <div class="chart-area tension-chart">
                <div class="tension-lines">
                  <div class="t-line line-1"></div>
                  <div class="t-line line-2"></div>
                  <div class="t-line line-3"></div>
                </div>
              </div>
              <div class="chart-legend">
                <span class="chart-x-label">Arm Travel</span>
                <span class="chart-y-label">Belt Tension [N]</span>
              </div>
            </div>
          </div>
        </div>

        <div class="page-footer">page 3 of {{ totalPages }}</div>
      </div>

      <!-- ========== 第4页 ========== -->
      <div class="report-page-break">
        <div class="report-header">
          <div class="header-logo"><div class="logo-box">ARTIN-TECH</div></div>
          <div class="header-title">FEAD Performance Analysis Report</div>
        </div>
        <div class="header-meta">
          <div class="meta-item"><span class="meta-label">File No. :</span><span class="meta-value">{{ formInfo.fileNo || '--' }}</span></div>
          <div class="meta-item"><span class="meta-label">Version :</span><span class="meta-value">{{ formInfo.version || '01' }}</span></div>
          <div class="meta-item"><span class="meta-label">Date :</span><span class="meta-value">{{ currentDate }}</span></div>
        </div>

        <h2 class="page-title">Geometry Analysis (Results)</h2>
        <h3 class="sub-title">Permissible Grooved Pulley Axial offset Allowance</h3>
        <table class="data-table-bordered small-text">
          <thead>
            <tr>
              <th>Adjusted Grooved Pulley</th>
              <th>Flat Pulley Angular Misalignment</th>
              <th>Perpendicularity</th>
              <th>Datum Grooved Pulley</th>
              <th>permissible grooved pulley axial offset allowance</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, idx) in alignmentPulleys" :key="idx">
              <td class="text-center">{{ p }}</td>
              <td class="text-center">/</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center gray-cell"></td>
              <td class="text-center gray-cell"></td>
            </tr>
          </tbody>
        </table>
        <div class="note-small">
          <p>Note: &nbsp;&nbsp; For &nbsp; 0.7 [deg] Belt Entry Angle</p>
          <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Approaching the accessory installation surface of the engine is marked as "-"</p>
        </div>

        <h2 class="page-title">Dynamic Analysis (Input)</h2>
        <h3 class="sub-title">Duty Cycle Rating and Accessory Loads [kW] for B10 (Input)</h3>
        <div class="two-col-layout">
          <div>
            <table class="data-table-bordered small-text compact">
              <thead>
                <tr>
                  <th>%</th>
                  <th>Eng.RPM</th>
                  <th>V [km/h]</th>
                  <th>T [C]</th>
                  <th v-for="p in loadPulleys" :key="p">{{ p }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in loadDataRows" :key="idx">
                  <td class="text-center">{{ row.percent }}</td>
                  <td class="text-center">{{ row.rpm }}</td>
                  <td class="text-center">{{ row.speed }}</td>
                  <td class="text-center">{{ row.temp }}</td>
                  <td v-for="p in loadPulleys" :key="p" class="text-center">--</td>
                </tr>
                <tr v-for="n in 10" :key="'empty-'+n">
                  <td class="text-center"></td>
                  <td class="text-center"></td>
                  <td class="text-center"></td>
                  <td class="text-center"></td>
                  <td v-for="p in loadPulleys" :key="p" class="text-center"></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div>
            <div class="chart-placeholder side-chart">
              <div class="chart-title">Accessory Data</div>
              <div class="chart-area">
                <div class="legend-inline">
                  <span><i class="dot dot-1"></i> ALT</span>
                  <span><i class="dot dot-2"></i> AC</span>
                  <span><i class="dot dot-3"></i> TEN</span>
                </div>
                <div class="curve-area">
                  <svg viewBox="0 0 200 120" class="curve-svg">
                    <line x1="20" y1="10" x2="20" y2="100" stroke="#999" stroke-width="0.5"/>
                    <line x1="20" y1="100" x2="190" y2="100" stroke="#999" stroke-width="0.5"/>
                    <path d="M20,80 Q60,40 100,45 T190,40" fill="none" stroke="#409eff" stroke-width="1.5"/>
                    <path d="M20,85 Q60,50 100,55 T190,52" fill="none" stroke="#f56c6c" stroke-width="1.5"/>
                    <path d="M20,90 Q60,60 100,65 T190,62" fill="none" stroke="#eb6ee3" stroke-width="1.5"/>
                  </svg>
                </div>
                <div class="chart-x-label-small">Engine Speed [rpm]</div>
              </div>
            </div>
          </div>
        </div>

        <h3 class="sub-title">Accessory Inertia and Acceleration Data (Input)</h3>
        <div class="three-col-layout">
          <table class="info-table-bordered small-table">
            <tr><th colspan="2">Engine Acceleration :&nbsp; 1000 [rpm/sec]</th></tr>
            <tr><th>File Name</th><th>Moment of Inertia [kgm^2]</th></tr>
            <tr v-for="p in inertiaPulleys" :key="p">
              <td class="text-center">{{ p }}</td>
              <td class="text-center">{{ getInertia(p) }}</td>
            </tr>
          </table>
          <table class="info-table-bordered small-table">
            <tr><th colspan="2">Engine Deceleration :&nbsp; 1000 [rpm/sec]</th></tr>
            <tr><th>File Name</th><th>Moment of Inertia [kgm^2]</th></tr>
            <tr v-for="n in 4" :key="n">
              <td class="text-center">NA</td>
              <td class="text-center">0</td>
            </tr>
          </table>
          <table class="info-table-bordered small-table">
            <tr><th>File Name</th><th>Moment of Inertia [kgm^2]</th></tr>
            <tr v-for="n in 4" :key="n">
              <td class="text-center">NA</td>
              <td class="text-center">0</td>
            </tr>
          </table>
        </div>

        <div class="page-footer">page 4 of {{ totalPages }}</div>
      </div>

      <!-- ========== 第5页 ========== -->
      <div class="report-page-break">
        <div class="report-header">
          <div class="header-logo"><div class="logo-box">ARTIN-TECH</div></div>
          <div class="header-title">FEAD Performance Analysis Report</div>
        </div>
        <div class="header-meta">
          <div class="meta-item"><span class="meta-label">File No. :</span><span class="meta-value">{{ formInfo.fileNo || '--' }}</span></div>
          <div class="meta-item"><span class="meta-label">Version :</span><span class="meta-value">{{ formInfo.version || '01' }}</span></div>
          <div class="meta-item"><span class="meta-label">Date :</span><span class="meta-value">{{ currentDate }}</span></div>
        </div>

        <h2 class="page-title">Dynamic Analysis (Results)</h2>
        <h3 class="sub-title">Belt Slip Safety Factor (Results)</h3>
        <div class="chart-placeholder wide-chart">
          <div class="chart-title">Belt Slip Safety factor</div>
          <div class="chart-area slip-chart">
            <svg viewBox="0 0 600 200" class="slip-svg">
              <line x1="40" y1="20" x2="40" y2="170" stroke="#999" stroke-width="0.5"/>
              <line x1="40" y1="170" x2="580" y2="170" stroke="#999" stroke-width="0.5"/>
              <line x1="40" y1="95" x2="580" y2="95" stroke="#ddd" stroke-width="0.5" stroke-dasharray="4,4"/>
              <path d="M40,100 L580,100" fill="none" stroke="#1d4ed8" stroke-width="2"/>
              <path d="M40,130 L580,130" fill="none" stroke="#db2777" stroke-width="2"/>
              <path d="M40,50 L580,50" fill="none" stroke="#facc15" stroke-width="2"/>
              <path d="M40,140 L580,140" fill="none" stroke="#22d3d3" stroke-width="2"/>
            </svg>
            <div class="slip-legend">
              <span><i class="legend-line" style="background:#1d4ed8"></i> FAN</span>
              <span><i class="legend-line" style="background:#db2777"></i> ALT</span>
              <span><i class="legend-line" style="background:#facc15"></i> AC</span>
              <span><i class="legend-line" style="background:#22d3d3"></i> TEN</span>
            </div>
          </div>
          <div class="chart-x-label">Engine Speed [rpm]</div>
          <div class="chart-y-label-side">Slip factor</div>
        </div>

        <table class="data-table-bordered small-text" style="margin-top: 12px">
          <thead>
            <tr>
              <th colspan="2">Engine Mode</th>
              <th>Minimum slipfactor</th>
              <th>Min factor pulley</th>
              <th>Min factor speed</th>
              <th>Allowable slipfactor</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="text-center">Acceleration</td>
              <td class="text-center">1000 [rpm/sec]</td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center">-- [rpm]</td>
              <td class="text-center">1.00</td>
            </tr>
            <tr>
              <td class="text-center">Steady state</td>
              <td class="text-center"></td>
              <td class="text-center">--</td>
              <td class="text-center">--</td>
              <td class="text-center">-- [rpm]</td>
              <td class="text-center">1.10</td>
            </tr>
            <tr>
              <td colspan="6" class="text-left note-cell">
                Tension Ratio: Tt / Ts &lt; or = to Kr, Equals minimum safety slip factor: &gt; or = to 1.00.For belt no slip.<br/>
                Note: ①Tt:Tight side tension, ②Ts:Slack side tension, ③Kr=e^μθ.
              </td>
            </tr>
          </tbody>
        </table>

        <h3 class="sub-title" style="margin-top: 20px">Pulley Mean Hubload [N] and Direction [deg] for bearing B10 (Results)</h3>
        <table class="data-table-bordered small-text compact">
          <thead>
            <tr>
              <th>%</th>
              <th>Eng.RPM</th>
              <th>V [m/s]</th>
              <th v-for="p in hubloadPulleys" :key="p">{{ p }}Dire.</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in loadDataRows" :key="idx">
              <td class="text-center">{{ row.percent }}</td>
              <td class="text-center">{{ row.rpm }}</td>
              <td class="text-center">{{ row.speedV }}</td>
              <td v-for="p in hubloadPulleys" :key="p" class="text-center">--/--</td>
            </tr>
            <tr v-for="n in 10" :key="'empty-'+n">
              <td v-for="m in 4 + hubloadPulleys.length" :key="m" class="text-center"></td>
            </tr>
          </tbody>
        </table>

        <div class="page-footer">page 5 of {{ totalPages }}</div>
      </div>

      <!-- ========== 第6页 ========== -->
      <div class="report-page-break">
        <div class="report-header">
          <div class="header-logo"><div class="logo-box">ARTIN-TECH</div></div>
          <div class="header-title">FEAD Performance Analysis Report</div>
        </div>
        <div class="header-meta">
          <div class="meta-item"><span class="meta-label">File No. :</span><span class="meta-value">{{ formInfo.fileNo || '--' }}</span></div>
          <div class="meta-item"><span class="meta-label">Version :</span><span class="meta-value">{{ formInfo.version || '01' }}</span></div>
          <div class="meta-item"><span class="meta-label">Date :</span><span class="meta-value">{{ currentDate }}</span></div>
        </div>

        <h2 class="page-title">Dynamic Analysis (Results)</h2>
        <h3 class="sub-title">Pulley Peak Hubloads [N] for Bracket Capability (Results)</h3>
        <div class="two-col-layout">
          <div>
            <table class="data-table-bordered small-text compact">
              <thead>
                <tr>
                  <th>Pulley</th>
                  <th>Engine [RPM]</th>
                  <th>Acceleration [n]</th>
                  <th>Hubload [N]</th>
                  <th>Direction [deg]</th>
                  <th>Tight side Tension[N]</th>
                  <th>Slack side</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in hubloadPulleys" :key="p">
                  <td class="text-center">{{ p }}</td>
                  <td class="text-center">--</td>
                  <td class="text-center">--</td>
                  <td class="text-center">--</td>
                  <td class="text-center">--</td>
                  <td class="text-center">--</td>
                  <td class="text-center">--</td>
                </tr>
                <tr v-for="n in 3" :key="n">
                  <td class="text-center">NA</td>
                  <td class="text-center"></td>
                  <td class="text-center"></td>
                  <td class="text-center"></td>
                  <td class="text-center"></td>
                  <td class="text-center"></td>
                  <td class="text-center"></td>
                </tr>
              </tbody>
            </table>
            <div class="note-xsmall">
              Note:Dexter Peak Hubloads are defined as: The highest hubloads calculates for all peak load &amp; accelerations conditions.
            </div>
          </div>
          <div>
            <div class="chart-placeholder side-chart">
              <div class="chart-title">Pulley Mean HubLoad</div>
              <div class="chart-area">
                <svg viewBox="0 0 200 120" class="curve-svg">
                  <line x1="20" y1="10" x2="20" y2="100" stroke="#999" stroke-width="0.5"/>
                  <line x1="20" y1="100" x2="190" y2="100" stroke="#999" stroke-width="0.5"/>
                  <path d="M20,30 L190,28" fill="none" stroke="#1d4ed8" stroke-width="1.5"/>
                  <path d="M20,45 L190,42" fill="none" stroke="#db2777" stroke-width="1.5"/>
                  <path d="M20,55 L190,52" fill="none" stroke="#facc15" stroke-width="1.5"/>
                  <path d="M20,70 L190,68" fill="none" stroke="#22d3d3" stroke-width="1.5"/>
                </svg>
                <div class="legend-inline">
                  <span><i class="dot dot-1"></i> FAN</span>
                  <span><i class="dot dot-2"></i> ALT</span>
                  <span><i class="dot dot-3"></i> AC</span>
                  <span><i class="dot dot-4"></i> TEN</span>
                </div>
                <div class="chart-x-label-small">Engine RPM</div>
              </div>
            </div>
          </div>
        </div>

        <h3 class="sub-title">Belt Tension [N] and Belt Life B10 Analysis</h3>
        <div class="two-col-layout">
          <div>
            <h4 class="sub-sub-title">Belt Mean Tension [N] (Results)</h4>
            <table class="data-table-bordered small-text compact">
              <thead>
                <tr>
                  <th>%</th>
                  <th>Eng.RPM</th>
                  <th>V [m/s]</th>
                  <th v-for="p in tensionPulleys" :key="p">{{ p }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in loadDataRows" :key="idx">
                  <td class="text-center">{{ row.percent }}</td>
                  <td class="text-center">{{ row.rpm }}</td>
                  <td class="text-center">{{ row.speedV }}</td>
                  <td v-for="p in tensionPulleys" :key="p" class="text-center">--</td>
                </tr>
                <tr v-for="n in 10" :key="n">
                  <td v-for="m in 3 + tensionPulleys.length" :key="m" class="text-center"></td>
                </tr>
              </tbody>
            </table>
            <div class="chart-placeholder" style="margin-top: 12px">
              <div class="chart-title">Belt Tension [N]</div>
              <div class="chart-area">
                <svg viewBox="0 0 400 100" class="curve-svg">
                  <line x1="30" y1="10" x2="30" y2="85" stroke="#999" stroke-width="0.5"/>
                  <line x1="30" y1="85" x2="390" y2="85" stroke="#999" stroke-width="0.5"/>
                  <path d="M30,30 L390,28" fill="none" stroke="#1d4ed8" stroke-width="1.5"/>
                  <path d="M30,50 L390,48" fill="none" stroke="#facc15" stroke-width="1.5"/>
                  <path d="M30,65 L390,62" fill="none" stroke="#22d3d3" stroke-width="1.5"/>
                </svg>
                <div class="legend-inline">
                  <span><i class="dot dot-1"></i> FAN</span>
                  <span><i class="dot dot-2"></i> ALT</span>
                  <span><i class="dot dot-3"></i> AC</span>
                  <span><i class="dot dot-4"></i> TEN</span>
                </div>
                <div class="chart-x-label-small">Engine Speed [rpm]</div>
              </div>
              <div class="chart-y-label-side-small">Tension [N]</div>
            </div>
          </div>
          <div>
            <h4 class="sub-sub-title">(Results) Belt Rib Fatigue [%]</h4>
            <table class="data-table-bordered small-text compact">
              <thead>
                <tr>
                  <th>%</th>
                  <th>Eng.RPM</th>
                  <th>V [m/s]</th>
                  <th>Rib Fatigue</th>
                  <th>Belt 1 [%]</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in loadDataRows" :key="idx">
                  <td class="text-center">{{ row.percent }}</td>
                  <td class="text-center">{{ row.rpm }}</td>
                  <td class="text-center">{{ row.speedV }}</td>
                  <td class="text-center">--</td>
                  <td class="text-center">--</td>
                </tr>
                <tr v-for="n in 10" :key="n">
                  <td v-for="m in 5" :key="m" class="text-center"></td>
                </tr>
              </tbody>
            </table>

            <table class="info-table-bordered small-table" style="margin-top: 12px">
              <tr><th colspan="4">(Results) Belt Flex Life</th></tr>
              <tr>
                <th>DC [%]</th>
                <th>Rib Fatigue</th>
                <th>Flex Units</th>
                <th>Belt Elect</th>
              </tr>
              <tr>
                <td class="text-center">--</td>
                <td class="text-center">--</td>
                <td class="text-center">--</td>
                <td class="text-center">{{ beltFullParams?.belt_type || 'EPDM' }}</td>
              </tr>
            </table>
            <div class="note-xsmall">
              Note:<br/>
              Belt life &gt; 1500 flex units for Neoprene(CR) belts;<br/>
              Belt life &gt; 650 flex units for EPDM belts;<br/>
              Belt life &gt; 200 flex units for hybrid Aramid/EPDM.
            </div>

            <table class="info-table-bordered small-table" style="margin-top: 8px">
              <tr><th colspan="4">(Results) Belt Life B10</th></tr>
              <tr>
                <th>Duty Cycle [%]</th>
                <th>Average Vehicle Speed [km/h]</th>
                <th>Temperature [C]</th>
                <th>B10 (km)</th>
              </tr>
              <tr>
                <td class="text-center">--</td>
                <td class="text-center">--</td>
                <td class="text-center">--</td>
                <td class="text-center">--</td>
              </tr>
            </table>
          </div>
        </div>

        <div class="page-footer">page 6 of {{ totalPages }}</div>
      </div>

      <!-- ========== 第7页 ========== -->
      <div class="report-page-break">
        <div class="report-header">
          <div class="header-logo"><div class="logo-box">ARTIN-TECH</div></div>
          <div class="header-title">FEAD Performance Analysis Report</div>
        </div>
        <div class="header-meta">
          <div class="meta-item"><span class="meta-label">File No. :</span><span class="meta-value">{{ formInfo.fileNo || '--' }}</span></div>
          <div class="meta-item"><span class="meta-label">Version :</span><span class="meta-value">{{ formInfo.version || '01' }}</span></div>
          <div class="meta-item"><span class="meta-label">Date :</span><span class="meta-value">{{ currentDate }}</span></div>
        </div>

        <h2 class="page-title">Dynamic Analysis (Results)</h2>
        <h3 class="sub-title">Belt Span Natural Frequency (Results)</h3>
        <div class="chart-placeholder wide-chart">
          <div class="chart-title">Belt Span Natural Frequency</div>
          <div class="chart-area freq-chart">
            <svg viewBox="0 0 600 220" class="freq-svg">
              <line x1="50" y1="20" x2="50" y2="190" stroke="#999" stroke-width="0.5"/>
              <line x1="50" y1="190" x2="560" y2="190" stroke="#999" stroke-width="0.5"/>
              <line x1="50" y1="105" x2="560" y2="105" stroke="#ddd" stroke-width="0.5" stroke-dasharray="4,4"/>
              <path d="M50,50 L560,45" fill="none" stroke="#1d4ed8" stroke-width="2"/>
              <path d="M50,90 L560,88" fill="none" stroke="#db2777" stroke-width="2"/>
              <path d="M50,120 L560,118" fill="none" stroke="#facc15" stroke-width="2"/>
              <path d="M50,70 L560,68" fill="none" stroke="#22d3d3" stroke-width="2"/>
              <path d="M50,150 Q100,100 150,130 T560,120" fill="none" stroke="#ef4444" stroke-width="2"/>
              <path d="M50,165 Q100,130 150,145 T560,140" fill="none" stroke="#eab308" stroke-width="2"/>
            </svg>
            <div class="freq-legend">
              <span><i class="legend-line" style="background:#1d4ed8"></i> FAN</span>
              <span><i class="legend-line" style="background:#db2777"></i> ALT</span>
              <span><i class="legend-line" style="background:#facc15"></i> AC</span>
              <span><i class="legend-line" style="background:#22d3d3"></i> TEN</span>
              <span><i class="legend-line" style="background:#eab308"></i> Engine order 2</span>
              <span><i class="legend-line" style="background:#ef4444"></i> Engine order 3</span>
            </div>
          </div>
          <div class="chart-x-label">Engine Speed [rpm]</div>
          <div class="chart-y-label-side">Belt Span Natural Frequency [Hz]</div>
        </div>

        <table class="data-table-bordered small-text" style="margin-top: 12px">
          <thead>
            <tr>
              <th colspan="7">Belt Span Natural Frequency [Hz]</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in freqPulleys" :key="p">
              <td width="60" class="text-center"><b>{{ p }}</b></td>
              <td class="text-center">-- ~ -- [Hz]</td>
              <td class="text-center">NA</td>
              <td class="text-center">0 ~ 0 [Hz]</td>
              <td class="text-center">NA</td>
              <td class="text-center">0 ~ 0 [Hz]</td>
              <td class="text-center">Tensioner (F_)</td>
            </tr>
            <tr>
              <td colspan="2" class="text-center"><b>Belt Spans Frequency Window:</b> -- ~ -- [Hz]</td>
              <td colspan="5" class="text-center"><b>Engine Idle Speed Interval:</b> -- ~ -- [rpm]</td>
            </tr>
          </tbody>
        </table>

        <div class="freq-note">
          <p>Note: If Engine Idle is near spans frequency window,then accessory drive system may have excessive vibration.</p>
          <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; If Engine Idle is within spans frequency window,then span vibration may have excessive amplitude .</p>
        </div>

        <div class="page-footer">page 7 of {{ totalPages }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { sharedStore } from '../store/shared.js'
import PulleyDiagram from '@/components/PulleyDiagram.vue'

const emit = defineEmits(['back'])

const totalPages = 7

const formInfo = computed(() => sharedStore.formInfo)
const tensioner = computed(() => sharedStore.tensioner)
const beltFullParams = computed(() => sharedStore.beltFullParams)

const currentDate = computed(() => {
  const d = new Date()
  return `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}`
})

const tensionerTypeText = computed(() => {
  return tensioner.value?.type === 'automatic' ? 'Automatic' : 'Manual'
})

const pulleys = computed(() => sharedStore.pulleys)

const pulleysForDiagram = computed(() => {
  return pulleys.value.map(p => ({ ...p }))
})

const pulleys10 = computed(() => {
  const arr = [...pulleys.value]
  while (arr.length < 10) {
    arr.push({ code: 'NA', name: '', x: null, y: null, type: 'groove', flat_dia: null, groove_dia: null, inertia: null })
  }
  return arr.slice(0, 10)
})

const alignmentPulleys = computed(() => {
  return pulleys.value.filter(p => p.type === 'groove').map(p => p.code).slice(0, 3)
})

const loadPulleys = computed(() => {
  return pulleys.value.filter(p => p.code && !['TEN', 'IDR', 'Tensioner'].includes(p.code.toUpperCase())).map(p => p.code).slice(0, 6)
})

const hubloadPulleys = computed(() => {
  return pulleys.value.filter(p => p.code).map(p => p.code).slice(0, 6)
})

const tensionPulleys = computed(() => {
  return pulleys.value.filter(p => p.code && !['IDR'].includes(p.code.toUpperCase())).map(p => p.code).slice(0, 6)
})

const inertiaPulleys = computed(() => {
  return pulleys.value.filter(p => p.code).map(p => p.code).slice(0, 4)
})

const freqPulleys = computed(() => {
  return pulleys.value.filter(p => p.code).map(p => p.code).slice(0, 4)
})

const loadDataRows = ref([
  { percent: '10', rpm: '770', speed: '5', temp: '80', speedV: '7.90' },
  { percent: '90', rpm: '2200', speed: '10', temp: '80', speedV: '22.58' }
])

const tensionerGeoRows = ref([
  { label: 'Install -/TEN' },
  { label: 'Min Belt' },
  { label: 'Nominal Belt' },
  { label: 'Max Belt' },
  { label: 'Stretch & wear' },
  { label: 'Free Arm' }
])

function formatNum(val) {
  if (val === null || val === undefined || isNaN(val) || val === '') return '--'
  return Number(val).toFixed(2)
}

function flatToPitch(p) {
  if (p.type !== 'flat' || p.flat_dia == null) return null
  const ftp = beltFullParams.value?.flat_to_pitch || 0
  return p.flat_dia - 2 * ftp
}

function effectiveDia(p) {
  let pitch = null
  if (p.type === 'groove') {
    pitch = p.groove_dia
  } else if (p.type === 'flat') {
    pitch = flatToPitch(p)
  }
  if (pitch == null) return null
  const pte = beltFullParams.value?.pitch_to_effective || 0
  return pitch - 2 * pte
}

function getInertia(code) {
  const p = pulleys.value.find(x => x.code === code)
  if (p && p.inertia != null) return p.inertia.toFixed(4)
  return '0'
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
  padding: 10px 24px;
  border-bottom: 1px solid #e8ecf1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.toolbar-center {
  font-size: 13px;
  color: #86909c;
}

.page-indicator {
  font-weight: 500;
}

.report-container {
  max-width: 900px;
  margin: 60px auto 40px;
}

.report-page-break {
  background: #fff;
  padding: 30px 35px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  position: relative;
  min-height: 1000px;
}

.report-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 8px;
}

.header-logo .logo-box {
  background: linear-gradient(180deg, #1e6fd9 0%, #0d4a9e 100%);
  color: #fff;
  padding: 6px 16px;
  font-weight: 700;
  font-size: 16px;
  border: 2px solid #000;
  letter-spacing: 1px;
}

.header-title {
  font-size: 22px;
  font-weight: 700;
  color: #000;
  letter-spacing: 1px;
}

.header-meta {
  display: flex;
  gap: 30px;
  padding: 6px 0;
  border-top: 2px solid #000;
  border-bottom: 2px solid #000;
  margin-bottom: 16px;
  font-size: 13px;
}

.meta-item {
  display: flex;
  gap: 6px;
}

.meta-label {
  font-weight: 600;
}

.meta-value {
  color: #000;
}

.page-title {
  font-size: 18px;
  font-weight: 700;
  color: #000;
  margin: 14px 0 10px 0;
  padding-bottom: 4px;
}

.sub-title {
  font-size: 14px;
  font-weight: 600;
  color: #000;
  margin: 12px 0 6px 0;
}

.sub-sub-title {
  font-size: 12px;
  font-weight: 600;
  color: #000;
  margin: 8px 0 4px 0;
}

.info-table-bordered {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  margin-bottom: 6px;
}

.info-table-bordered th {
  background: #fff;
  color: #000;
  font-weight: 600;
  padding: 5px 10px;
  text-align: left;
  border: 1.5px solid #000;
  white-space: nowrap;
}

.info-table-bordered td {
  padding: 5px 10px;
  border: 1.5px solid #000;
  color: #000;
}

.text-left {
  text-align: left !important;
}

.text-center {
  text-align: center;
}

.small-table {
  font-size: 11px;
}

.small-table th,
.small-table td {
  padding: 3px 8px;
}

.data-table-bordered {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
}

.data-table-bordered th {
  background: #fff;
  color: #000;
  font-weight: 600;
  padding: 4px 6px;
  text-align: center;
  border: 1.5px solid #000;
}

.data-table-bordered td {
  padding: 4px 6px;
  border: 1.5px solid #000;
  color: #000;
}

.data-table-bordered.small-text {
  font-size: 10px;
}

.data-table-bordered.compact th,
.data-table-bordered.compact td {
  padding: 3px 4px;
}

.gray-cell {
  background: #eee;
}

.two-col-layout {
  display: flex;
  gap: 16px;
}

.two-col-layout > div {
  flex: 1;
}

.three-col-layout {
  display: flex;
  gap: 12px;
}

.three-col-layout > table {
  flex: 1;
}

.diagram-placeholder {
  margin: 8px 0;
  text-align: center;
}

.diagram-box {
  display: inline-block;
  border: 1.5px solid #000;
  padding: 8px;
  width: 80%;
}

.page-footer {
  position: absolute;
  bottom: 16px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 11px;
  color: #000;
}

.four-grid-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 10px;
}

.grid-card {
  border: 1.5px solid #000;
  padding: 8px;
}

.grid-card-title {
  font-weight: 700;
  font-size: 12px;
  text-align: center;
  border: 1.5px solid #000;
  padding: 3px;
  margin-bottom: 6px;
  display: inline-block;
}

.grid-diagram {
  height: 140px;
  border: 1px solid #999;
  margin-bottom: 6px;
  overflow: hidden;
}

.mini-diagram {
  transform: scale(0.5);
  transform-origin: top left;
  width: 200%;
  height: 200%;
}

.grid-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 10px;
}

.grid-table th {
  border: 1.5px solid #000;
  padding: 3px 6px;
  text-align: left;
  font-weight: 600;
  width: 55%;
}

.grid-table td {
  border: 1.5px solid #000;
  padding: 3px 6px;
  text-align: right;
}

.note-box {
  margin-top: 16px;
  padding: 10px 14px;
  border: 1px solid #999;
  font-size: 11px;
  color: #000;
}

.note-small {
  font-size: 10px;
  color: #000;
  margin: 6px 0;
  line-height: 1.5;
}

.note-xsmall {
  font-size: 9px;
  color: #333;
  margin: 6px 0;
  line-height: 1.5;
}

.note-cell {
  padding: 6px 10px !important;
  font-size: 10px;
  line-height: 1.6;
}

.chart-placeholder {
  border: 1px solid #999;
  padding: 8px;
  background: #fff;
}

.chart-title {
  text-align: center;
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 6px;
}

.chart-area {
  height: 120px;
  position: relative;
  background: #f5f5f5;
  border: 1px solid #ccc;
}

.chart-x-label {
  text-align: center;
  font-size: 10px;
  margin-top: 4px;
}

.chart-y-label-side {
  position: absolute;
  left: -30px;
  top: 50%;
  transform: translateY(-50%) rotate(-90deg);
  font-size: 10px;
  white-space: nowrap;
}

.wide-chart {
  position: relative;
  margin-left: 30px;
}

.wide-chart .chart-area {
  height: 180px;
}

.side-chart {
  margin-top: 16px;
}

.small-chart .chart-area {
  height: 100px;
}

.tension-chart .tension-lines {
  position: absolute;
  inset: 10px 20px 15px 30px;
}

.t-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 2px;
}

.line-1 {
  top: 20%;
  background: #a855f7;
}

.line-2 {
  top: 40%;
  background: #22c55e;
}

.line-3 {
  top: 60%;
  background: #ef4444;
}

.design-geo-box {
  border: 1px solid #000;
  padding: 8px 12px;
  font-size: 11px;
  line-height: 1.7;
}

.design-geo-title {
  font-weight: 600;
  margin-bottom: 4px;
}

.design-geo-content p {
  margin: 2px 0;
}

.legend-inline {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 4px;
  font-size: 9px;
  flex-wrap: wrap;
}

.legend-inline span {
  display: flex;
  align-items: center;
  gap: 3px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.dot-1 { background: #1d4ed8; }
.dot-2 { background: #f56c6c; }
.dot-3 { background: #eb6ee3; }
.dot-4 { background: #22d3d3; }

.curve-svg {
  width: 100%;
  height: 90px;
}

.curve-area {
  padding: 4px;
}

.slip-chart {
  position: relative;
  padding-bottom: 8px;
}

.slip-svg {
  width: 100%;
  height: 100%;
}

.slip-legend {
  position: absolute;
  right: 8px;
  top: 8px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  font-size: 9px;
  background: #fff;
  padding: 4px 8px;
  border: 1px solid #ccc;
}

.slip-legend span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.legend-line {
  width: 16px;
  height: 2px;
  display: inline-block;
}

.chart-x-label-small {
  text-align: center;
  font-size: 9px;
  margin-top: 2px;
}

.chart-y-label-side-small {
  position: absolute;
  left: -25px;
  top: 50%;
  transform: translateY(-50%) rotate(-90deg);
  font-size: 9px;
  white-space: nowrap;
}

.freq-chart {
  position: relative;
  height: 220px;
}

.freq-svg {
  width: 100%;
  height: 100%;
}

.freq-legend {
  position: absolute;
  right: 8px;
  top: 8px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  font-size: 9px;
  background: #fff;
  padding: 4px 8px;
  border: 1px solid #ccc;
}

.freq-legend span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.freq-note {
  margin-top: 16px;
  font-size: 11px;
  line-height: 1.7;
}

.freq-note p {
  margin: 4px 0;
}

.bar-fill {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  background: linear-gradient(180deg, #22c55e 0%, #16a34a 100%);
}

.chart-bar {
  position: absolute;
  bottom: 10px;
  left: 0;
  right: 0;
  height: calc(100% - 20px);
  display: flex;
  justify-content: center;
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
  }

  .report-page-break {
    page-break-after: always;
    box-shadow: none;
    margin: 0;
    padding: 15mm 20mm;
    min-height: 260mm;
  }

  .report-page-break:last-child {
    page-break-after: avoid;
  }
}
</style>
