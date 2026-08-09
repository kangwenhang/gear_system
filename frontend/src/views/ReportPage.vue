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
        <el-button type="primary" @click="handleExportExcel" :loading="exporting" style="margin-left:8px">
          <svg style="width:16px;height:16px;margin-right:6px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="10" y1="13" x2="18" y2="13"/>
            <line x1="10" y1="17" x2="16" y2="17"/>
          </svg>
          导出报告
        </el-button>
      </div>
    </div>

    <div class="report-container" id="reportContent">
      <!-- 第1页：Excel 布局 1:1 还原（EN_REPORT） -->
      <div class="report-page-break excel-page">
        <div class="excel-scaler">
        <div class="excel-grid-wrapper">
          <div class="excel-grid">
            <!-- 标题栏 -->
            <div class="cell bl-medium br-medium bt-medium bb-medium" style="grid-column: 1 / 8; grid-row: 1 / 4; justify-content: center; align-items: center; font-size: 21px; white-space: normal; word-break: break-word"></div>
            <div class="cell bt-medium bb-thin" style="grid-column: 8 / 26; grid-row: 1 / 5; justify-content: center; align-items: center; font-size: 22px; font-weight: bold; white-space: normal; word-break: break-word">FEAD Performance  Analysis Report</div>
            <!-- 行4 底边框 -->
            <div v-for="c in 7" :key="'r4c'+c" class="cell bb-thin" :style="{ gridColumn: c + ' / ' + (c+1), gridRow: '4 / 5' }"></div>
            <!-- 行5: File No / Version / Date -->
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 1 / 4; grid-row: 5 / 6; justify-content: flex-end; align-items: center; font-size: 14px">File No. :</div>
            <div class="cell bt-thin bb-thin" style="grid-column: 4 / 8; grid-row: 5 / 6; justify-content: center; align-items: center; font-size: 14px; white-space: normal; word-break: break-word">{{ formInfo.file_no || '--' }}</div>
            <div class="cell bt-thin bb-thin" style="grid-column: 8 / 11; grid-row: 5 / 6; justify-content: flex-end; align-items: center; font-size: 14px">Version : </div>
            <div class="cell bt-thin bb-thin" style="grid-column: 11 / 12; grid-row: 5 / 6; justify-content: flex-start; align-items: center">{{ formInfo.version || '--' }}</div>
            <div class="cell bt-thin bb-thin" style="grid-column: 12 / 14; grid-row: 5 / 6"></div>
            <div class="cell bt-thin bb-thin" style="grid-column: 14 / 16; grid-row: 5 / 6; justify-content: center; align-items: center; font-size: 14px">Date :</div>
            <div class="cell bt-thin bb-thin" style="grid-column: 16 / 20; grid-row: 5 / 6; justify-content: center; align-items: center; font-size: 14px">{{ formInfo.date || '--' }}</div>
            <div class="cell bt-thin bb-thin" style="grid-column: 20 / 23; grid-row: 5 / 6"></div>
            <div class="cell bt-thin bb-thin" style="grid-column: 23 / 25; grid-row: 5 / 6"></div>
            <div class="cell bt-thin bb-thin" style="grid-column: 25 / 26; grid-row: 5 / 6"></div>
            <!-- 行7-8: Project Information 标题 -->
            <div class="cell" style="grid-column: 1 / 22; grid-row: 7 / 9; justify-content: flex-start; align-items: center; font-size: 22px">Project Information</div>
            <div class="cell" style="grid-column: 23 / 25; grid-row: 8 / 9; justify-content: flex-end; align-items: center; font-size: 10px"></div>
            <!-- 行10: Client / Project -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 1 / 5; grid-row: 10 / 11; justify-content: flex-start; align-items: center; font-size: 14px">Client :</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 5 / 11; grid-row: 10 / 11; justify-content: flex-start; align-items: center; font-size: 14px">{{ formInfo.customer || '--' }}</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 11 / 17; grid-row: 10 / 11; justify-content: center; align-items: center; font-size: 14px">Project:</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 17 / 26; grid-row: 10 / 11; justify-content: flex-start; align-items: center; font-size: 11.5px; white-space: normal; word-break: break-word">{{ formInfo.project || '--' }}</div>
            <!-- 行11: Cylinders / Engine power -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 1 / 9; grid-row: 11 / 12; justify-content: flex-start; align-items: center; font-size: 14px">Number of engine cylinders：</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 9 / 11; grid-row: 11 / 12; justify-content: flex-start; align-items: center; font-size: 14px">{{ formInfo.cylinders || '' }}</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 11 / 17; grid-row: 11 / 12; justify-content: center; align-items: center; font-size: 14px">Engine power</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 17 / 26; grid-row: 11 / 12; justify-content: flex-start; align-items: center; font-size: 14px">{{ formInfo.power ? formInfo.power + ' kW' : '' }}</div>
            <!-- 行12: Problem Statement -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 1 / 7; grid-row: 12 / 13; justify-content: flex-end; align-items: center; font-size: 14px">Problem Statement :</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 7 / 26; grid-row: 12 / 13; justify-content: flex-start; align-items: center; font-size: 9px; white-space: normal; word-break: break-word">{{ formInfo.problem_statement || '--' }}</div>
            <!-- 行13: Analysis Reference -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 1 / 7; grid-row: 13 / 14; justify-content: center; align-items: center; font-size: 14px">Analysis Reference :</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 7 / 26; grid-row: 13 / 14; justify-content: flex-start; align-items: center; font-size: 9px; white-space: normal; word-break: break-word">{{ formInfo.analysis_reference || '--' }}</div>
            <!-- 行14-29: 布局示意图 -->
            <div class="cell" style="grid-column: 1 / 26; grid-row: 14 / 30; justify-content: center; align-items: center; overflow: hidden">
              <PulleyDiagram :data="reportPulleys" :tensionerData="reportTensioner" :beltParams="reportBeltParams" :contactParams="reportContactParams" static-mode />
            </div>
            <!-- 行30-32: Geometry Analysis (Input) -->
            <div class="cell" style="grid-column: 2 / 23; grid-row: 30 / 33; justify-content: flex-start; align-items: center; font-size: 22px">Geometry Analysis (Input）</div>
            <div class="cell" style="grid-column: 23 / 25; grid-row: 31 / 32; justify-content: flex-end; align-items: center; font-size: 10px"></div>
            <!-- 行33: Belt Data (input) -->
            <div class="cell" style="grid-column: 2 / 8; grid-row: 33 / 34; justify-content: flex-start; align-items: center; font-size: 16px"> Belt Data (input)</div>
            <!-- 行35: Belt name / Geometric Dimension -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 2 / 8; grid-row: 35 / 36; justify-content: flex-start; align-items: center; font-size: 12px">Belt name :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 8 / 9; grid-row: 35 / 36"></div>
            <div class="cell bt-thin bb-thin" style="grid-column: 9 / 12; grid-row: 35 / 36; justify-content: center; align-items: center; font-size: 12px">{{ beltFullParams.belt_name || beltFullParams.belt_type || '--' }}</div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 12 / 13; grid-row: 35 / 36"></div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 14 / 24; grid-row: 35 / 36; justify-content: flex-start; align-items: center; font-size: 12px">Geometric Dimension :</div>
            <!-- 行36: Rib type / Belt Height -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 2 / 8; grid-row: 36 / 37; justify-content: flex-start; align-items: center; font-size: 12px">Belt rib Geometry type : </div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 8 / 9; grid-row: 36 / 37"></div>
            <div class="cell bt-thin bb-thin" style="grid-column: 9 / 10; grid-row: 36 / 37"></div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 10 / 13; grid-row: 36 / 37; justify-content: flex-start; align-items: center; font-size: 12px">{{ (beltFullParams.rib_type || '--') + (beltFullParams.belt_material ? ' / ' + beltFullParams.belt_material : '') }}</div>
            <div class="cell bl-thin br-thin bb-thin" style="grid-column: 14 / 20; grid-row: 36 / 37; justify-content: flex-start; align-items: center; font-size: 12px">Belt Height :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 20 / 22; grid-row: 36 / 37; justify-content: center; align-items: center; font-size: 12px">{{ beltFullParams.belt_height != null ? beltFullParams.belt_height : '--' }}</div>
            <div class="cell br-thin bb-thin" style="grid-column: 22 / 24; grid-row: 36 / 37; justify-content: flex-start; align-items: center; font-size: 12px">[mm]</div>
            <!-- 行37: Ribs/Cord / Flat to Pitch -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 2 / 8; grid-row: 37 / 38; justify-content: flex-start; align-items: center; font-size: 12px">No.of Ribs/Cord Material:</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 8 / 9; grid-row: 37 / 38"></div>
            <div class="cell bt-thin bb-thin" style="grid-column: 9 / 10; grid-row: 37 / 38"></div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 10 / 13; grid-row: 37 / 38; justify-content: flex-start; align-items: center; font-size: 12px">{{ (beltFullParams.ribs != null ? beltFullParams.ribs : '--') + (beltFullParams.cord_material ? ' / ' + beltFullParams.cord_material : '') }}</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 14 / 20; grid-row: 37 / 38; justify-content: flex-start; align-items: center; font-size: 12px">Belt Flat to Pitch :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 20 / 22; grid-row: 37 / 38; justify-content: center; align-items: center; font-size: 12px">{{ beltFullParams.flat_to_pitch != null ? beltFullParams.flat_to_pitch : '--' }}</div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 22 / 24; grid-row: 37 / 38; justify-content: flex-start; align-items: center; font-size: 12px">[mm]</div>
            <!-- 行38: Stretch&Wear / Pitch to Effective -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 2 / 8; grid-row: 38 / 39; justify-content: flex-start; align-items: center; font-size: 12px">Stretch and Wear Allow :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 8 / 10; grid-row: 38 / 39; justify-content: flex-end; align-items: center; font-size: 12px">{{ beltFullParams.stretch_wear_allow != null ? '≤ ' + beltFullParams.stretch_wear_allow : '--' }} % of Length</div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 10 / 13; grid-row: 38 / 39; justify-content: flex-start; align-items: center; font-size: 12px">%  of Length</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 14 / 20; grid-row: 38 / 39; justify-content: flex-start; align-items: center; font-size: 12px">Belt Pitch to Effective :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 20 / 22; grid-row: 38 / 39; justify-content: center; align-items: center; font-size: 12px">{{ beltFullParams.pitch_to_effective != null ? beltFullParams.pitch_to_effective : '--' }}</div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 22 / 24; grid-row: 38 / 39; justify-content: flex-start; align-items: center; font-size: 12px">[mm]</div>
            <!-- 行40: Tensioner Data (input) -->
            <div class="cell" style="grid-column: 2 / 11; grid-row: 40 / 41; justify-content: flex-start; align-items: center; font-size: 16px">Tensioner Data (input)</div>
            <!-- 行42: Tensioner Type / Arm Length -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 2 / 8; grid-row: 42 / 43; justify-content: flex-start; align-items: center; font-size: 12px">Tensioner Type :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 8 / 9; grid-row: 42 / 43"></div>
            <div class="cell bt-thin bb-thin" style="grid-column: 9 / 12; grid-row: 42 / 43; justify-content: center; align-items: center; font-size: 12px">{{ tensioner.type || '--' }}</div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 12 / 13; grid-row: 42 / 43"></div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 14 / 20; grid-row: 42 / 43; justify-content: flex-start; align-items: center; font-size: 12px">Tensioner Arm Length :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 20 / 22; grid-row: 42 / 43; justify-content: flex-end; align-items: center; font-size: 12px">{{ formatNum(tensioner.arm_length) }}</div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 22 / 24; grid-row: 42 / 43; justify-content: flex-start; align-items: center; font-size: 12px">[mm]</div>
            <!-- 行43: Pivot Point / Arm Angle -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 2 / 8; grid-row: 43 / 44; justify-content: flex-start; align-items: center; font-size: 12px">Pivot Point {x,y} [mm] :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 8 / 11; grid-row: 43 / 44; justify-content: center; align-items: center; font-size: 12px">{{ tensioner.pivot_x != null ? tensioner.pivot_x : '--' }}</div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 11 / 13; grid-row: 43 / 44; justify-content: flex-start; align-items: center; font-size: 12px">{{ tensioner.pivot_y != null ? tensioner.pivot_y : '--' }}</div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 14 / 20; grid-row: 43 / 44; justify-content: flex-start; align-items: center; font-size: 12px">Tensioner Arm Angle :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 20 / 22; grid-row: 43 / 44; justify-content: flex-end; align-items: center; font-size: 12px">{{ formatNum(tensioner.angle) }}</div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 22 / 24; grid-row: 43 / 44; justify-content: flex-start; align-items: center; font-size: 12px">[deg]</div>
            <!-- 行44: Design Tension / Spring Rate -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 2 / 8; grid-row: 44 / 45; justify-content: flex-start; align-items: center; font-size: 12px">Belt Design Tension [N] :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 8 / 10; grid-row: 44 / 45; justify-content: flex-end; align-items: center; font-size: 12px">{{ tensioner.design_tension != null ? tensioner.design_tension : '--' }}</div>
            <div class="cell bt-thin bb-thin" style="grid-column: 10 / 12; grid-row: 44 / 45"></div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 12 / 13; grid-row: 44 / 45"></div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 14 / 20; grid-row: 44 / 45; justify-content: flex-start; align-items: center; font-size: 12px">Spring Rate Factor :</div>
            <div class="cell bl-thin bt-thin bb-thin" style="grid-column: 20 / 22; grid-row: 44 / 45; justify-content: center; align-items: center; font-size: 12px">{{ tensioner.spring_stiffness != null ? tensioner.spring_stiffness : '--' }}</div>
            <div class="cell br-thin bt-thin bb-thin" style="grid-column: 22 / 24; grid-row: 44 / 45; justify-content: flex-start; align-items: center; font-size: 12px">[Nm/deg]</div>
            <!-- 行46: Layout Data (input) -->
            <div class="cell" style="grid-column: 2 / 11; grid-row: 46 / 47; justify-content: flex-start; align-items: center; font-size: 16px">Layout Data (input)</div>
            <!-- 行48-49: 表头 -->
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 2 / 4; grid-row: 48 / 50; justify-content: center; align-items: center; font-size: 12px"></div>
            <div class="cell bl-thin br-thin bt-thin bb-thin" style="grid-column: 4 / 7; grid-row: 48 / 50; justify-content: center; align-items: center; font-size: 14px">Pulley</div>
            <div class="cell bl-thin br-thin bt-thin" style="grid-column: 7 / 10; grid-row: 48 / 49; justify-content: center; align-items: center; font-size: 12px">X</div>
            <div class="cell bl-thin br-thin bt-thin" style="grid-column: 10 / 13; grid-row: 48 / 49; justify-content: center; align-items: center; font-size: 12px">Y</div>
            <div class="cell bl-thin br-thin bt-thin" style="grid-column: 13 / 16; grid-row: 48 / 49; justify-content: center; align-items: center; font-size: 12px">Flat</div>
            <div class="cell bl-thin br-thin bt-thin" style="grid-column: 16 / 19; grid-row: 48 / 49; justify-content: center; align-items: center; font-size: 12px">Pitch</div>
            <div class="cell bl-thin br-thin bt-thin" style="grid-column: 19 / 22; grid-row: 48 / 49; justify-content: center; align-items: center; font-size: 12px">Effective</div>
            <div class="cell bl-thin br-thin bt-thin" style="grid-column: 22 / 25; grid-row: 48 / 49; justify-content: center; align-items: center; font-size: 12px">Pulley</div>
            <div class="cell bl-thin br-thin bb-thin" style="grid-column: 7 / 10; grid-row: 49 / 50; justify-content: center; align-items: center; font-size: 12px">Coordinate</div>
            <div class="cell bl-thin br-thin bb-thin" style="grid-column: 10 / 13; grid-row: 49 / 50; justify-content: center; align-items: center; font-size: 12px">Coordinate</div>
            <div class="cell bl-thin br-thin bb-thin" style="grid-column: 13 / 16; grid-row: 49 / 50; justify-content: center; align-items: center; font-size: 12px">Diameter</div>
            <div class="cell bl-thin br-thin bb-thin" style="grid-column: 16 / 19; grid-row: 49 / 50; justify-content: center; align-items: center; font-size: 12px">Diameter</div>
            <div class="cell bl-thin br-thin bb-thin" style="grid-column: 19 / 22; grid-row: 49 / 50; justify-content: center; align-items: center; font-size: 12px">Diameter</div>
            <div class="cell bl-thin br-thin bb-thin" style="grid-column: 22 / 25; grid-row: 49 / 50; justify-content: center; align-items: center; font-size: 12px">Type</div>
            <!-- 行50-59: 带轮数据行（v-for 动态绑定） -->
            <template v-for="(p, idx) in displayPulleys" :key="'pulley-'+idx">
              <div class="cell bl-thin br-thin bt-thin bb-thin" :style="{ gridColumn: '2 / 4', gridRow: (50 + idx) + ' / ' + (51 + idx), justifyContent: 'center', alignItems: 'center', fontSize: '12px' }">{{ idx + 1 }}</div>
              <div class="cell bl-thin br-thin bt-thin bb-thin" :style="{ gridColumn: '4 / 7', gridRow: (50 + idx) + ' / ' + (51 + idx), justifyContent: 'center', alignItems: 'center', fontSize: '12px' }">{{ p.code || ' ' }}</div>
              <div class="cell bl-thin br-thin bt-thin bb-thin" :style="{ gridColumn: '7 / 10', gridRow: (50 + idx) + ' / ' + (51 + idx), justifyContent: 'center', alignItems: 'center', fontSize: '12px' }">{{ p.type !== 'none' ? formatNum(p.x) : '' }}</div>
              <div class="cell bl-thin br-thin bt-thin bb-thin" :style="{ gridColumn: '10 / 13', gridRow: (50 + idx) + ' / ' + (51 + idx), justifyContent: 'center', alignItems: 'center', fontSize: '12px' }">{{ p.type !== 'none' ? formatNum(p.y) : '' }}</div>
              <div class="cell bl-thin br-thin bt-thin bb-thin" :style="{ gridColumn: '13 / 16', gridRow: (50 + idx) + ' / ' + (51 + idx), justifyContent: 'center', alignItems: 'center', fontSize: '12px' }">{{ p.type === 'groove' ? '/' : p.type === 'flat' ? p.flat_dia : '' }}</div>
              <div class="cell bl-thin br-thin bt-thin bb-thin" :style="{ gridColumn: '16 / 19', gridRow: (50 + idx) + ' / ' + (51 + idx), justifyContent: 'center', alignItems: 'center', fontSize: '12px' }">{{ p.type !== 'none' ? formatNum(p.pitch_dia) : '' }}</div>
              <div class="cell bl-thin br-thin bt-thin bb-thin" :style="{ gridColumn: '19 / 22', gridRow: (50 + idx) + ' / ' + (51 + idx), justifyContent: 'center', alignItems: 'center', fontSize: '12px' }">{{ p.type !== 'none' ? formatNum(p.effective_dia) : '' }}</div>
              <div class="cell bl-thin br-thin bt-thin bb-thin" :style="{ gridColumn: '22 / 25', gridRow: (50 + idx) + ' / ' + (51 + idx), justifyContent: 'center', alignItems: 'center', fontSize: '12px' }">{{ p.type === 'flat' ? 'Flat' : p.type === 'groove' ? 'Grooved' : '' }}</div>
            </template>
            <!-- 空行占位（带轮不足10个时） -->
            <template v-for="i in Math.max(0, 10 - displayPulleys.length)" :key="'empty-'+i">
              <div v-for="(col, ci) in [[2,4],[4,7],[7,10],[10,13],[13,16],[16,19],[19,22],[22,25]]" :key="'e'+i+'-'+ci" class="cell bl-thin br-thin bt-thin bb-thin" :style="{ gridColumn: col[0] + ' / ' + col[1], gridRow: (49 + displayPulleys.length + i) + ' / ' + (50 + displayPulleys.length + i), justifyContent: 'center', alignItems: 'center', fontSize: '12px' }">&nbsp;</div>
            </template>
            <!-- 行60: 底部粗边框 -->
            <div v-for="c in 25" :key="'r60c'+c" class="cell bb-medium" :style="{ gridColumn: c + ' / ' + (c+1), gridRow: '60 / 61' }"></div>
          </div>
        </div>
        </div>
      </div>

      <!-- 第2页：布局数据结果（Layout Data Results） -->
      <div class="report-page-break">
        <div class="page-header">
          <h1>{{ t('pages.p2') }}</h1>
          <div class="page-num">{{ pageLabel(2) }} / {{ t('toolbar.pages', totalPages) }}</div>
        </div>

        <!-- Belt Length Summary（皮带长度汇总） -->
        <div class="report-section">
          <h2>Belt Length Summary &mdash; Layout Data (Results)</h2>
          <table class="data-table auto-width">
            <thead>
              <tr>
                <th></th>
                <th>Min Belt</th>
                <th>Nominal Belt</th>
                <th>Max Belt</th>
                <th>Stretch &amp; Wear</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Belt Length</td>
                <td>{{ formatNum(minBeltLen) }} mm</td>
                <td>{{ formatNum(beltFullParams.effective_length) }} mm</td>
                <td>{{ formatNum(maxBeltLen) }} mm</td>
                <td>{{ formatNum(stretchLen) }} mm</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Tensioner Pulley Geometry（张紧轮几何参数 - 模板核心对比表） -->
        <div class="report-section">
          <h2>Tensioner Pulley Geometry (Results)</h2>
          <table class="data-table wide-table">
            <thead>
              <tr>
                <th>Tensioner Position</th>
                <th>Pulley Position<br/>X / Y</th>
                <th>Arm Position<br/>[deg] / [mm]</th>
                <th>Eff. Belt Length<br/>[mm]</th>
                <th>Tensioner Torque<br/>[Nm]</th>
                <th>Belt Design<br/>Tension [N]</th>
                <th>Wrap Angle<br/>[deg]</th>
                <th>Hubload<br/>[N]</th>
                <th>Hubload<br/>Direction [deg]</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in geometryRows" :key="row.label">
                <td style="text-align:left; white-space:nowrap">- {{ row.label }} /TEN</td>
                <td>{{ row.x != null ? formatNum(row.x) : '--' }} / {{ row.y != null ? formatNum(row.y) : '--' }}</td>
                <td>{{ row.armPos != null ? formatNum(row.armPos) : '--' }}</td>
                <td>{{ row.beltLen != null ? formatNum(row.beltLen) : '--' }}</td>
                <td>{{ row.torque || '--' }}</td>
                <td>{{ row.designTension || '--' }}</td>
                <td>{{ row.wrapAngle || '--' }}</td>
                <td>{{ row.hubload || '--' }}</td>
                <td>{{ row.hubloadDir || '--' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Belt Data (Results) -->
        <div class="report-section">
          <h2>Belt Data (Results)</h2>
          <table class="data-table auto-width">
            <thead>
              <tr>
                <th>Parameter</th>
                <th>Value</th>
                <th>Unit</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Eff. Drive Length (ref. ISO 9981)</td>
                <td>{{ formatNum(beltFullParams.effective_length) }}</td>
                <td>mm</td>
              </tr>
              <tr>
                <td>Length Tolerance</td>
                <td>&plusmn; {{ formatNum(beltFullParams.length_tolerance) }}</td>
                <td>mm</td>
              </tr>
              <tr>
                <td>Max Stretch (Free Arm)</td>
                <td>{{ maxStretchPct }} %</td>
                <td>of Length</td>
              </tr>
              <tr>
                <td>Belt design tension per rib</td>
                <td>{{ formatNum(designTensionPerRib) }}</td>
                <td>N/rib</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Tensioner Data (Results) -->
        <div class="report-section">
          <h2>Tensioner Data (Results)</h2>
          <table class="data-table auto-width">
            <thead>
              <tr>
                <th>Parameter</th>
                <th>Value</th>
                <th>Unit</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Design Torque</td>
                <td>{{ formatNum(tensioner.torque) }} &plusmn; {{ formatNum(0.1 * tensioner.torque) }}</td>
                <td>Nm</td>
              </tr>
              <tr>
                <td>Belt Take-up / Arm Ratio</td>
                <td>{{ beltTakeUpRatio }} mm/deg</td>
                <td>({{ beltTakeUpPct }} %)</td>
              </tr>
              <tr>
                <td>Total Travel Angle (Min)</td>
                <td>&ge; {{ formatNum(totalTravelAngle) }}</td>
                <td>deg</td>
              </tr>
              <tr>
                <td>Nominal Working Angle</td>
                <td>{{ formatNum(nominalWorkingAngle) }}</td>
                <td>deg</td>
              </tr>
            </tbody>
          </table>
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
                <td>{{ formatNum(minBeltLen) }}</td>
                <td>{{ formatNum(beltFullParams.effective_length) }}</td>
                <td>{{ formatNum(maxBeltLen) }}</td>
                <td>mm</td>
              </tr>
              <tr>
                <td>{{ t('lengthTolerance') }}</td>
                <td colspan="3" style="text-align:center">± {{ formatNum(beltFullParams.length_tolerance) || '--' }}</td>
                <td>mm</td>
              </tr>
              <tr>
                <td>Max Stretch (Free Arm)</td>
                <td colspan="3" style="text-align:center">{{ maxStretchPct }} %</td>
                <td>%</td>
              </tr>
              <tr>
                <td>Belt design tension per rib</td>
                <td colspan="3" style="text-align:center">{{ designTensionPerRib }}</td>
                <td>N/rib</td>
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
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Design Torque</td>
                <td>{{ formatNum(tensioner.torque) }} ± {{ formatNum(0.1 * tensioner.torque) }}</td>
                <td>Nm</td>
                <td></td>
              </tr>
              <tr>
                <td>Belt Take-up / Arm Ratio</td>
                <td>{{ beltTakeUpRatio }}</td>
                <td>mm/deg</td>
                <td>({{ beltTakeUpPct }} %)</td>
              </tr>
              <tr>
                <td>Total Travel Angle (Min)</td>
                <td>≥ {{ formatNum(totalTravelAngle) }}</td>
                <td>deg</td>
                <td></td>
              </tr>
              <tr>
                <td>Nominal Working Angle</td>
                <td>{{ formatNum(nominalWorkingAngle) }}</td>
                <td>deg</td>
                <td></td>
              </tr>
              <tr>
                <td>{{ t('installAngle') }}</td>
                <td>{{ formatNum(tensioner.angle) }}</td>
                <td>deg</td>
                <td></td>
              </tr>
              <tr>
                <td>{{ t('armLength') }}</td>
                <td>{{ formatNum(tensioner.arm_length) }}</td>
                <td>mm</td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h2>{{ t('tensionerPulleyGeom') }}</h2>
          <table class="data-table auto-width">
            <thead>
              <tr>
                <th>Tensioner Position</th>
                <th>X (mm)</th>
                <th>Y (mm)</th>
                <th>Angle (deg)</th>
                <th>Belt Length (mm)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in geometryRows" :key="'g3-'+row.label">
                <td>{{ row.label }}</td>
                <td>{{ row.x != null ? formatNum(row.x) : '--' }}</td>
                <td>{{ row.y != null ? formatNum(row.y) : '--' }}</td>
                <td>{{ row.armPos != null ? formatNum(row.armPos) : '--' }}</td>
                <td>{{ row.beltLen != null ? formatNum(row.beltLen) : '--' }}</td>
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
              <tr v-for="(p, idx) in displayPulleys.filter(p => p.type !== 'none')" :key="idx">
                <td>{{ p.code || t('pulleyPlaceholder')+(idx+1) }}</td>
                <td>{{ formatNum(getWrapAngle(p.code)) }}</td>
                <td>{{ formatNum(getSpanIn(p.code)) }}</td>
                <td>{{ formatNum(getSpanOut(p.code)) }}</td>
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
import { ElMessage } from 'element-plus'
import { sharedStore } from '../store/shared.js'
import { t, getLang, setLang } from '../store/i18n.js'
import { generateReport } from '../api/pulley.js'
import PulleyDiagram from '../components/PulleyDiagram.vue'

const emit = defineEmits(['back'])
const totalPages = 7
const exporting = ref(false)

const formInfo = computed(() => sharedStore.formInfo)
const tensioner = computed(() => sharedStore.tensioner)
const beltFullParams = computed(() => sharedStore.beltFullParams)
const pulleys = computed(() => sharedStore.pulleys)

const displayPulleys = computed(() => {
  return pulleys.value || []
})

// 布局图数据（供 PulleyDiagram 静态渲染，与输入页布局一致）
const reportPulleys = computed(() => displayPulleys.value.filter(p => p.type !== 'none'))
const reportTensioner = computed(() => ({
  automatic: {
    pivot_x: tensioner.value.pivot_x,
    pivot_y: tensioner.value.pivot_y,
    head_size: 50
  },
  manual: {}
}))
const reportBeltParams = computed(() => sharedStore.beltParams)
const reportContactParams = computed(() => sharedStore.contactParams)

// ===== 第2页 Layout Data (Results) 计算数据 =====

// 皮带长度汇总
const minBeltLen = computed(() => {
  return sharedStore.shortBeltResult?.achieved_length
    || sharedStore.shortBeltResult?.short_belt_length
    || beltFullParams.value.min_length
})
const maxBeltLen = computed(() => {
  return sharedStore.longBeltResult?.achieved_length
    || sharedStore.longBeltResult?.long_belt_length
    || beltFullParams.value.max_length
})
const stretchLen = computed(() => {
  const max = maxBeltLen.value
  const eff = beltFullParams.value.effective_length
  if (max != null && eff != null) return Number(max) - Number(eff)
  return beltFullParams.value.stretch
})

// 张紧轮几何参数表（模板核心对比表：Install / Min Belt / Nominal Belt / Max Belt）
const geometryRows = computed(() => {
  const inst = sharedStore.installPositionResult || {}
  const free = sharedStore.freePositionResult || {}
  const short = sharedStore.shortBeltResult || {}
  const long = sharedStore.longBeltResult || {}
  const tenPulley = pulleys.value.find(p => p.code === 'TEN' || p.type === 'flat')
  const hasAuto = tensioner.value.type === 'Automatic'

  // Contact 参数中张紧轮数据
  const tenContact = sharedStore.contactParams?.TEN || sharedStore.contactParams?.[tenPulley?.code] || {}

  const rows = [
    {
      label: 'Install',
      x: inst.install_tensioner_x,
      y: inst.install_tensioner_y,
      armPos: hasAuto ? inst.install_angle : null,
      beltLen: inst.install_belt_length,
      torque: hasAuto ? (tensioner.value.torque != null ? formatNum(tensioner.value.torque) : '--') : null,
      designTension: null,
      wrapAngle: null,
      hubload: null,
      hubloadDir: null
    },
    {
      label: 'Min Belt',
      x: short.tensioner_x,
      y: short.tensioner_y,
      armPos: hasAuto ? short.tensioner_angle : free.free_angle,
      beltLen: short.achieved_length || short.short_belt_length,
      torque: hasAuto ? (tensioner.value.torque != null ? formatNum(tensioner.value.torque) : '--') : null,
      designTension: tenContact.design_tension || tensioner.value.design_tension,
      wrapAngle: tenContact.wrap_angle,
      hubload: tenContact.hubload,
      hubloadDir: tenContact.hubload_direction || tenContact.U
    },
    {
      label: 'Nominal Belt',
      x: free.free_tensioner_x ?? tenPulley?.x,
      y: free.free_tensioner_y ?? tenPulley?.y,
      armPos: hasAuto ? free.nominal_angle ?? tensioner.value.angle : free.free_angle,
      beltLen: beltFullParams.value.effective_length,
      torque: hasAuto ? (tensioner.value.torque != null ? formatNum(tensioner.value.torque) : '--') : null,
      designTension: tensioner.value.design_tension,
      wrapAngle: tenContact.wrap_angle,
      hubload: tenContact.hubload,
      hubloadDir: tenContact.hubload_direction || tenContact.U
    },
    {
      label: 'Max Belt',
      x: long.tensioner_x,
      y: long.tensioner_y,
      armPos: hasAuto ? long.tensioner_angle : null,
      beltLen: long.achieved_length || long.long_belt_length,
      torque: hasAuto ? (tensioner.value.torque != null ? formatNum(tensioner.value.torque) : '--') : null,
      designTension: null,
      wrapAngle: null,
      hubload: null,
      hubloadDir: null
    }
  ]
  return rows
})

// Belt Data (Results) 计算值
const maxStretchPct = computed(() => {
  const max = maxBeltLen.value
  const eff = beltFullParams.value.effective_length
  if (max != null && eff != null && Number(eff) > 0) {
    return formatNum((Number(max) / Number(eff) - 1) * 100)
  }
  return '--'
})
const designTensionPerRib = computed(() => {
  const tension = tensioner.value.design_tension
  const ribs = beltFullParams.value.ribs
  if (tension != null && ribs != null && ribs > 0) {
    return formatNum(tension / ribs)
  }
  return '--'
})

// Tensioner Data (Results) 计算值
const beltTakeUpRatio = computed(() => {
  const maxLen = maxBeltLen.value
  const minLen = minBeltLen.value
  const maxAngle = sharedStore.longBeltResult?.tensioner_angle
  const minAngle = sharedStore.shortBeltResult?.tensioner_angle
  if (maxLen != null && minLen != null && maxAngle != null && minAngle != null) {
    const deltaLen = Math.abs(Number(maxLen) - Number(minLen))
    const deltaAngleRaw = Math.abs(Number(maxAngle) - Number(minAngle))
    const deltaAngle = deltaAngleRaw > 180 ? 360 - deltaAngleRaw : deltaAngleRaw
    if (deltaAngle > 0) return formatNum(deltaLen / deltaAngle)
  }
  return '--'
})
const beltTakeUpPct = computed(() => {
  const ratio = beltTakeUpRatio.value
  const nomLen = beltFullParams.value.effective_length
  if (ratio !== '--' && nomLen != null && Number(nomLen) > 0) {
    return formatNum(100 * Number(ratio) / Number(nomLen))
  }
  return '--'
})
const totalTravelAngle = computed(() => {
  const maxAngle = sharedStore.longBeltResult?.tensioner_angle
  const minAngle = sharedStore.shortBeltResult?.tensioner_angle
  if (maxAngle != null && minAngle != null) {
    const diff = Math.abs(Number(maxAngle) - Number(minAngle))
    return diff > 180 ? 360 - diff : diff
  }
  return null
})
const nominalWorkingAngle = computed(() => {
  const maxAngle = sharedStore.longBeltResult?.tensioner_angle
  const nomAngle = tensioner.value.angle
    || sharedStore.freePositionResult?.nominal_angle
  if (maxAngle != null && nomAngle != null) {
    const diff = Math.abs(Number(maxAngle) - Number(nomAngle))
    return diff > 180 ? 360 - diff : diff
  }
  if (maxAngle != null) return Math.abs(Number(maxAngle))
  return null
})

// ===== 第一页 CSS Grid 常量 =====
// Grid 原始尺寸从 REPORT.xlsx EN_REPORT sheet 提取（25列 × 60行）
// 缩放完全由 CSS 处理（.excel-grid-wrapper transform + .excel-scaler 尺寸）
// 屏幕：scale ≈ 0.667（适配 700px 容器）；打印：scale ≈ 0.734（适配 A4 纵向）

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

// 从 contactParams 或 beltLengthResult 中提取带轮几何数据
function getWrapAngle(code) {
  const cp = sharedStore.contactParams?.[code]
  if (cp?.wrap_angle != null) return Number(cp.wrap_angle).toFixed(1)
  // fallback: 从 beltLengthResult.details 查找
  const detail = sharedStore.beltLengthResult?.details?.find(d => d.pulley_code === code)
  if (detail?.wrap_angle != null) return Number(detail.wrap_angle).toFixed(1)
  return null
}
function getSpanIn(code) {
  const detail = sharedStore.beltLengthResult?.details?.find(d => d.pulley_code === code)
  if (detail?.span_in != null) return Number(detail.span_in).toFixed(1)
  return null
}
function getSpanOut(code) {
  const detail = sharedStore.beltLengthResult?.details?.find(d => d.pulley_code === code)
  if (detail?.span_out != null) return Number(detail.span_out).toFixed(1)
  return null
}

function handleBack() {
  emit('back')
}

function handlePrint() {
  window.print()
}

async function handleExportExcel() {
  exporting.value = true
  try {
    const payload = {
      form_info: { ...sharedStore.formInfo },
      pulleys: sharedStore.pulleys.map(p => ({
        code: p.code,
        name: p.name,
        type: p.type,
        x: p.x,
        y: p.y,
        pitch_dia: p.pitch_dia,
        effective_dia: p.effective_dia,
        flat_dia: p.flat_dia,
        rotation: p.rotation
      })),
      belt_params: { ...sharedStore.beltFullParams },
      tensioner: { ...sharedStore.tensioner }
    }
    const response = await generateReport(payload)
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    const now = new Date()
    const ts = `${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}_${String(now.getHours()).padStart(2,'0')}${String(now.getMinutes()).padStart(2,'0')}${String(now.getSeconds()).padStart(2,'0')}`
    link.setAttribute('download', `FEAD_Report_${ts}.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    ElMessage.success('Excel 报告已导出')
  } catch (e) {
    console.error('Export failed:', e)
    ElMessage.error('导出失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    exporting.value = false
  }
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
  font-size: 15px;
  color: #606266;
  font-weight: 500;
}

.lang-dropdown {
  display: inline-block;
}

.report-container {
  max-width: 780px;
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
  font-size: 26px;
  color: #303133;
  margin-bottom: 8px;
}

.page-num {
  font-size: 14px;
  color: #909399;
}

/* ===== CSS Grid 布局（1:1 还原 REPORT.xlsx EN_REPORT sheet） ===== */
.excel-page {
  background: #fff;
  padding: 10px;
  overflow: hidden;
  min-height: auto;  /* 覆盖 .report-page-break 的 min-height: 1100px */
}

/* 缩放容器：尺寸 = Grid 原始尺寸 × scale，防止 transform 导致布局溢出 */
.excel-scaler {
  width: 729px;   /* 971 × 0.75 ≈ 729 */
  height: 995px;  /* 1326 × 0.75 ≈ 995 */
  margin: 0 auto;
  overflow: hidden;
}

/* Grid wrapper：固定原始尺寸，通过 transform 缩放 */
.excel-grid-wrapper {
  width: 971px;
  height: 1326px;
  transform-origin: top left;
  transform: scale(0.75);  /* 屏幕缩放 */
}

/* CSS Grid：25 列 × 60 行，尺寸从 Excel 提取 */
.excel-grid {
  display: grid;
  grid-template-columns: 28px 30px 64px 27px 40px 35px 38px 35px 38px 33px 41px 38px 33px 64px 64px 34px 32px 42px 33px 41px 27px 45px 41px 36px 32px;
  grid-template-rows: 19px 19px 19px 2px 31px 7px 15px 16px 8px 26px 26px 50px 64px 30px 6px 27px 27px 27px 27px 27px 27px 27px 27px 27px 27px 27px 27px 27px 27px 15px 16px 6px 27px 11px 21px 21px 21px 21px 16px 27px 11px 20px 21px 21px 16px 30px 12px 24px 21px 21px 21px 21px 21px 21px 21px 21px 21px 21px 21px 22px;
  font-family: 'Calibri', 'Microsoft YaHei', sans-serif;
  width: 971px;
}

.excel-grid > .cell {
  overflow: hidden;
  box-sizing: border-box;
  display: flex;
  padding: 1px 2px;
  color: #000;
}

/* 边框类（从 Excel border style 提取） */
.bl-medium { border-left: 2px solid #000 !important; }
.br-medium { border-right: 2px solid #000 !important; }
.bt-medium { border-top: 2px solid #000 !important; }
.bb-medium { border-bottom: 2px solid #000 !important; }
.bl-thin { border-left: 1px solid #000 !important; }
.br-thin { border-right: 1px solid #000 !important; }
.bt-thin { border-top: 1px solid #000 !important; }
.bb-thin { border-bottom: 1px solid #000 !important; }

/* PulleyDiagram 在 Grid 单元内填满 */
.excel-grid > .cell :deep(.wrap.static-mode) {
  width: 100%;
  height: 100%;
  padding: 4px;
}
.excel-grid > .cell :deep(svg.diagram) {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  border: none;
}

.report-section {
  margin-bottom: 28px;
}

.report-section h2 {
  font-size: 18px;
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
  font-size: 13px;
  color: #909399;
  margin-bottom: 4px;
}

.info-value {
  font-size: 15px;
  color: #303133;
  font-weight: 500;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
.data-table.auto-width {
  width: auto;
  min-width: 60%;
}
.data-table.wide-table {
  font-size: 12px;
}
.data-table.wide-table th,
.data-table.wide-table td {
  padding: 3px 4px;
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
  font-size: 12px;
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
  @page {
    size: A4 portrait;
    margin: 8mm;
    @bottom-center {
      content: "page " counter(page) " of " counter(pages);
      font-size: 9pt;
    }
  }

  html, body {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    /* 关键：强制浏览器打印渲染引擎按 1:1 像素渲染，避免浏览器自动缩放 */
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .report-page {
    background: #fff;
    padding: 0;
    width: 100%;
  }

  .no-print {
    display: none !important;
  }

  .report-container {
    max-width: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  .report-page-break {
    box-shadow: none;
    margin: 0;
    padding: 20px;
    min-height: auto;
    page-break-after: always;
    break-after: page;
    width: 100%;
    box-sizing: border-box;
  }

  .report-page-break:last-child {
    page-break-after: auto;
    break-after: auto;
  }

  /* ===== 第一页 CSS Grid 打印：缩放到 A4 纵向 ===== */
  .excel-page {
    padding: 0 10px;
    page-break-inside: avoid;
    break-inside: avoid;
    box-sizing: border-box;
  }

  /* 打印时缩放到 A4 内容区：713×974px（971×1326 × 0.7343） */
  .excel-scaler {
    width: 713px;
    height: 974px;
    margin: 0 auto;
  }

  .excel-grid-wrapper {
    transform: scale(0.7343);  /* min(713/971, 1017/1326) ≈ 0.7343 */
  }

  /* 后续报告页（非第一页）打印紧凑化，减少内容被分页到下一页 */
  .report-page-break:not(.excel-page) {
    padding: 12px;
  }

  .report-section {
    margin-bottom: 16px;
  }

  .page-header {
    margin-bottom: 16px;
    padding-bottom: 8px;
  }

  .page-header h1 {
    font-size: 20px;
  }

  .data-table {
    font-size: 11px;
  }

  .data-table th,
  .data-table td {
    padding: 4px 6px;
  }

  .layout-compare {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 10px;
  }

  .layout-card {
    padding: 8px;
  }

  .layout-card h3 {
    margin-bottom: 6px;
    font-size: 13px;
  }

  .mini-diagram {
    padding: 4px;
    margin-bottom: 6px;
  }

  .mini-diagram svg {
    max-height: 160px;
  }

  .chart-placeholder {
    min-height: 120px;
    padding: 10px;
  }

  .chart-bar {
    height: 100px;
  }

  .freq-note {
    padding: 10px;
    font-size: 12px;
  }

  .report-footer {
    margin-top: 24px;
    padding-top: 12px;
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
