<template>
  <div class="input-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="page-header-left">
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="3"/>
          <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>
        </svg>
        <h2 class="page-title">轮系布局参数</h2>
        <span class="page-subtitle">初始输入</span>
      </div>
    </div>

    <!-- 基础信息卡片 -->
    <el-card shadow="hover" class="info-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
          <span>基础信息</span>
        </div>
      </template>
      <el-form :model="formInfo" label-position="top" class="base-form">
        <el-row :gutter="16">
          <el-col :span="4">
            <el-form-item label="文件编号">
              <el-input v-model="formInfo.fileNo" placeholder="请输入" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="客户">
              <el-input v-model="formInfo.customer" placeholder="请输入" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="项目(机型)">
              <el-input v-model="formInfo.project" placeholder="请输入" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="缸数">
              <el-input v-model="formInfo.cylinders" placeholder="请输入" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="发动机功率">
              <el-input v-model="formInfo.power" placeholder="请输入功率" clearable />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="版本">
              <el-input-number
                v-model="formInfo.version"
                :min="1"
                :max="99"
                controls-position="right"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="轮系报告更新说明">
              <el-input
                v-model="formInfo.updateDesc"
                type="textarea"
                :rows="3"
                placeholder="请输入更新说明..."
                resize="none"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="轮系报告问题说明">
              <el-input
                v-model="formInfo.issueDesc"
                type="textarea"
                :rows="3"
                placeholder="请输入问题说明..."
                resize="none"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 主内容区：表格 + 示意图 -->
    <div class="main-content">
      <!-- 左侧：带轮表格 -->
      <div class="left-section">
        <el-card shadow="hover" class="table-card">
          <template #header>
            <div class="card-header">
              <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <line x1="3" y1="9" x2="21" y2="9"/>
                <line x1="3" y1="15" x2="21" y2="15"/>
                <line x1="9" y1="3" x2="9" y2="21"/>
                <line x1="15" y1="3" x2="15" y2="21"/>
              </svg>
              <span>带轮参数</span>
              <el-tag size="small" type="info" class="count-tag">{{ tableData.length }} / 10</el-tag>
            </div>
          </template>
          <div class="table-wrapper">
            <el-table
              :data="tableData"
              border
              stripe
              :header-cell-style="headerStyle"
              :cell-style="cellStyle"
              row-class-name="table-row"
              size="default"
            >
              <!-- 序号列 -->
              <el-table-column type="index" label="#" width="45" align="center" />

              <!-- 带轮名称 -->
              <el-table-column prop="name" label="名称" min-width="85" align="center">
                <template #default="scope">
                  <el-input v-model="scope.row.name" size="small" placeholder="--" />
                </template>
              </el-table-column>

              <!-- 带轮 -->
              <el-table-column prop="code" label="带轮" min-width="100" align="center">
                <template #default="scope">
                  <el-select
                    v-model="scope.row.code"
                    size="small"
                    placeholder="选择"
                    filterable
                    @change="(val) => handleCodeChange(val, scope.row)"
                    style="width: 100%"
                  >
                    <el-option
                      v-for="item in beltOptions"
                      :key="item.code"
                      :label="item.code"
                      :value="item.code"
                    />
                  </el-select>
                </template>
              </el-table-column>

              <!-- 带轮坐标 -->
              <el-table-column label="坐标" align="center">
                <el-table-column prop="x" label="X" min-width="100" align="center">
                  <template #default="scope">
                    <el-input-number
                      v-model="tableData[scope.$index].x"
                      :controls="false"
                      :precision="2"
                      size="small"
                      style="width: 100%"
                      placeholder="--"
                      :disabled="scope.$index === tableData.length - 1 && tensioner.type === 'automatic' && disableTensionerXY"
                      @change="onTableXYChange(scope.$index)"
                    />
                  </template>
                </el-table-column>
                <el-table-column prop="y" label="Y" min-width="100" align="center">
                  <template #default="scope">
                    <el-input-number
                      v-model="tableData[scope.$index].y"
                      :controls="false"
                      :precision="2"
                      size="small"
                      style="width: 100%"
                      placeholder="--"
                      :disabled="scope.$index === tableData.length - 1 && tensioner.type === 'automatic' && disableTensionerXY"
                      @change="onTableXYChange(scope.$index)"
                    />
                  </template>
                </el-table-column>
              </el-table-column>

              <!-- 带轮直径 -->
              <el-table-column label="直径(mm)" align="center">
                <el-table-column prop="flat_dia" label="平轮" min-width="100" align="center">
                  <template #default="scope">
                    <el-input-number
                      v-if="scope.row.type === 'flat'"
                      v-model="scope.row.flat_dia"
                      :controls="false"
                      :precision="2"
                      size="small"
                      style="width: 100%"
                      placeholder="--"
                    />
                    <span v-else class="disabled-cell">-</span>
                  </template>
                </el-table-column>
                <el-table-column prop="groove_dia" label="槽轮" min-width="100" align="center">
                  <template #default="scope">
                    <el-input-number
                      v-if="scope.row.type === 'groove'"
                      v-model="scope.row.groove_dia"
                      :controls="false"
                      :precision="2"
                      size="small"
                      style="width: 100%"
                      placeholder="--"
                    />
                    <span v-else class="disabled-cell">-</span>
                  </template>
                </el-table-column>
              </el-table-column>

              <!-- 带轮类型 -->
              <el-table-column prop="type" label="类型" min-width="90" align="center">
                <template #default="scope">
                  <el-select v-model="scope.row.type" size="small" style="width: 100%">
                    <el-option label="槽轮" value="groove">
                      <span>槽轮</span>
                    </el-option>
                    <el-option label="平轮" value="flat">
                      <span>平轮</span>
                    </el-option>
                  </el-select>
                </template>
              </el-table-column>

              <!-- 转动惯量 -->
              <el-table-column prop="inertia" label="惯量[kgm²]" min-width="105" align="center">
                <template #default="scope">
                  <el-input-number
                    v-model="scope.row.inertia"
                    :controls="false"
                    :precision="4"
                    size="small"
                    style="width: 100%"
                    placeholder="--"
                  />
                </template>
              </el-table-column>

              <!-- Service factor -->
              <el-table-column prop="service_factor" label="Service factor" min-width="80" align="center">
                <template #header>
                  <div class="tooltip-header">
                    <el-tooltip content="默认为1，轻载1.1，重载1.2" placement="top">
                      <span>Service factor <svg style="width:12px;height:12px;vertical-align:middle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg></span>
                    </el-tooltip>
                  </div>
                </template>
                <template #default="scope">
                  <el-input-number
                    v-model="scope.row.service_factor"
                    :controls="false"
                    :precision="1"
                    size="small"
                    style="width: 100%"
                    placeholder="--"
                  />
                </template>
              </el-table-column>

              <!-- 操作列 -->
              <el-table-column label="操作" align="center" width="100">
                <template #default="scope">
                  <div class="action-buttons">
                    <el-button
                      type="primary"
                      size="small"
                      circle
                      :disabled="tableData.length >= 10"
                      @click="addRow(scope.$index)"
                    >
                      <svg style="width:12px;height:12px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                    </el-button>
                    <el-button
                      type="danger"
                      size="small"
                      circle
                      :disabled="tableData.length <= 1"
                      @click="removeRow(scope.$index)"
                    >
                      <svg style="width:12px;height:12px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/></svg>
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>

      </div>

      <!-- 右侧：轮系示意图 -->
      <div class="right-section">
        <el-card shadow="hover" class="diagram-card">
          <template #header>
            <div class="card-header">
              <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <circle cx="12" cy="12" r="3"/>
                <line x1="12" y1="2" x2="12" y2="5"/>
                <line x1="12" y1="19" x2="12" y2="22"/>
                <line x1="2" y1="12" x2="5" y2="12"/>
                <line x1="19" y1="12" x2="22" y2="12"/>
              </svg>
              <span>轮系示意图</span>
            </div>
          </template>
          <PulleyDiagram 
            :data="tableData" 
            :tensionerData="tensioner"
            :beltParams="sharedStore.beltParams"
            :contactParams="sharedStore.contactParams"
          />
        </el-card>
      </div>
    </div>

    <!-- 张紧器参数卡片 -->
    <el-card shadow="hover" class="tensioner-card">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
          <span>张紧器参数</span>
          <el-tag size="small" :type="tensioner.type === 'automatic' ? 'success' : 'warning'" class="type-tag">
            {{ tensioner.type === 'automatic' ? '自动张紧轮' : '手调张紧轮' }}
          </el-tag>
          <el-popover placement="bottom-end" trigger="hover" :width="300" popper-class="tensioner-popover">
            <template #reference>
              <div class="tensioner-header-photo">
                <img v-if="tensioner.type === 'automatic'" src="/images/tensioner_auto.jpg" alt="自动张紧轮" />
                <img v-else src="/images/tensioner_manual.png" alt="手调张紧轮" />
              </div>
            </template>
            <img v-if="tensioner.type === 'automatic'" src="/images/tensioner_auto.jpg" alt="自动张紧轮" style="width:100%;border-radius:6px" />
            <img v-else src="/images/tensioner_manual.png" alt="手调张紧轮" style="width:100%;border-radius:6px" />
          </el-popover>
        </div>
      </template>
      <el-form :model="tensioner" label-position="top" class="tensioner-form">
        <!-- 类型选择行 -->
        <el-row :gutter="16" class="type-selector-row" align="middle">
          <el-col :span="9">
            <el-form-item label="张紧器类型">
              <div class="type-with-img">
                <el-radio-group v-model="tensioner.type" class="type-radio-group">
                  <el-radio-button value="automatic">
                    <svg style="width:14px;height:14px;margin-right:4px;vertical-align:middle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
                    自动张紧轮
                  </el-radio-button>
                  <el-radio-button value="manual">
                    <svg style="width:14px;height:14px;margin-right:4px;vertical-align:middle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
                    手调张紧轮
                  </el-radio-button>
                </el-radio-group>
              </div>
            </el-form-item>
          </el-col>

          <el-col :span="5" v-if="tensioner.type === 'automatic'">
            <el-form-item label="旋转方向">
              <el-select v-model="tensioner.automatic.rotation" placeholder="选择方向" style="width: 100%">
                <el-option label="顺时针" value="cw">
                  <span>顺时针</span>
                  <span v-if="autoCalculatedRotation === 'cw'" style="float:right;color:#409eff;font-size:11px">自动计算</span>
                </el-option>
                <el-option label="逆时针" value="ccw">
                  <span>逆时针</span>
                  <span v-if="autoCalculatedRotation === 'ccw'" style="float:right;color:#409eff;font-size:11px">自动计算</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="5" v-if="tensioner.type === 'automatic'">
            <el-form-item label="张力值类型">
              <el-select v-model="tensioner.automatic.valueType" placeholder="选择" style="width: 100%">
                <el-option label="张力值" value="tension" />
                <el-option label="扭矩" value="torque" />
              </el-select>
            </el-form-item>
          </el-col>

          <!-- 自动张紧轮SVG示意图 -->
          <el-col :span="5" v-if="tensioner.type === 'automatic'">
            <div class="tensioner-preview">
              <div class="tensioner-preview-title">工作示意图</div>
              <svg viewBox="0 0 120 90" class="tensioner-svg">
                <!-- 枢轴点 -->
                <circle cx="20" cy="60" r="6" fill="#409eff" stroke="#2c5aa0" stroke-width="2"/>
                <circle cx="20" cy="60" r="2" fill="#fff"/>
                <!-- 臂（角度更小，更水平） -->
                <line x1="20" y1="60" x2="90" y2="35" stroke="#606266" stroke-width="4" stroke-linecap="round"/>
                <!-- 皮带轮 -->
                <circle cx="90" cy="35" r="14" fill="none" stroke="#409eff" stroke-width="3"/>
                <circle cx="90" cy="35" r="8" fill="#e6f2ff" stroke="#409eff" stroke-width="1.5"/>
                <!-- 旋转方向箭头（围绕皮带轮外圈外侧，红色，圆心90,35 半径21） -->
                <path v-if="tensioner.automatic.rotation === 'cw'" d="M75 20 A21 21 0 0 1 111 35" fill="none" stroke="#f56c6c" stroke-width="3"/>
                <polygon v-if="tensioner.automatic.rotation === 'cw'" points="113,35 111,42 108,35" fill="#f56c6c"/>
                <path v-if="tensioner.automatic.rotation === 'ccw'" d="M75 20 A21 21 0 0 1 111 35" fill="none" stroke="#f56c6c" stroke-width="3"/>
                <polygon v-if="tensioner.automatic.rotation === 'ccw'" points="70,25 73,18 77,22" fill="#f56c6c"/>
                <!-- 标签 -->
                <text x="20" y="76" font-size="8" fill="#909399" text-anchor="middle">枢轴</text>
                <text x="90" y="57" font-size="8" fill="#909399" text-anchor="middle">皮带轮</text>
              </svg>
            </div>
          </el-col>

          <!-- 手调张紧轮SVG示意图 -->
          <el-col :span="5" v-if="tensioner.type === 'manual'">
            <div class="tensioner-preview">
              <div class="tensioner-preview-title">工作示意图</div>
              <svg viewBox="0 0 120 90" class="tensioner-svg">
                <!-- 起始点 -->
                <circle cx="20" cy="50" r="5" fill="#409eff" stroke="#2c5aa0" stroke-width="2"/>
                <text x="20" y="68" font-size="8" fill="#909399" text-anchor="middle">起始</text>
                <!-- 结束点 -->
                <circle cx="100" cy="50" r="5" fill="#409eff" stroke="#2c5aa0" stroke-width="2"/>
                <text x="100" y="68" font-size="8" fill="#909399" text-anchor="middle">结束</text>
                <!-- 直线 -->
                <line x1="20" y1="50" x2="100" y2="50" stroke="#606266" stroke-width="3" stroke-linecap="round"/>
                <!-- 皮带轮（中间） -->
                <circle cx="60" cy="50" r="14" fill="none" stroke="#409eff" stroke-width="3"/>
                <circle cx="60" cy="50" r="8" fill="#e6f2ff" stroke="#409eff" stroke-width="1.5"/>
                <text x="60" y="72" font-size="8" fill="#909399" text-anchor="middle">皮带轮</text>
                <!-- 左右双向箭头 -->
                <line x1="25" y1="25" x2="95" y2="25" stroke="#f56c6c" stroke-width="2" stroke-linecap="round"/>
                <polygon points="20,25 28,21 28,29" fill="#f56c6c"/>
                <polygon points="100,25 92,21 92,29" fill="#f56c6c"/>
              </svg>
            </div>
          </el-col>
        </el-row>

        <!-- 自动张紧轮参数 -->
        <template v-if="tensioner.type === 'automatic'">
          <div class="param-section">
            <div class="param-section-title">
              <svg style="width:14px;height:14px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/></svg>
              枢轴与臂参数
            </div>
            <div class="calc-mode-selector">
              <div class="calc-mode-label">计算模式</div>
              <div class="calc-mode-options">
                <div
                  class="calc-mode-card"
                  :class="{ active: calcMode === '1', disabled: disableMode1 }"
                  @click="!disableMode1 && (calcMode = '1')"
                >
                  <div class="mode-icon-wrapper blue">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 2l0 20M2 12l20 0M9.172 9.172l5.656 5.656M14.828 9.172l-5.656 5.656"/>
                    </svg>
                  </div>
                  <div class="mode-title">正向计算</div>
                  <div class="mode-desc">枢轴XY + 臂长 + 工作角度 → 张紧轮XY</div>
                </div>
                <div
                  class="calc-mode-card"
                  :class="{ active: calcMode === '2', disabled: disableMode2 }"
                  @click="!disableMode2 && (calcMode = '2')"
                >
                  <div class="mode-icon-wrapper green">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 19l-7-7 7-7M19 12l-7 7-7-7"/>
                    </svg>
                  </div>
                  <div class="mode-title">反向计算</div>
                  <div class="mode-desc">张紧轮XY + 臂长 + 工作角度 → 枢轴XY</div>
                </div>
                <div
                  class="calc-mode-card"
                  :class="{ active: calcMode === '3', disabled: disableMode3 }"
                  @click="!disableMode3 && (calcMode = '3')"
                >
                  <div class="mode-icon-wrapper purple">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="3"/>
                      <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>
                    </svg>
                  </div>
                  <div class="mode-title">双向反推</div>
                  <div class="mode-desc">枢轴XY + 张紧轮XY → 臂长 + 工作角度</div>
                </div>
              </div>
            </div>
            <el-row :gutter="16">
              <el-col :span="4">
                <el-form-item label="枢轴 X">
                  <el-input-number v-model="tensioner.automatic.pivot_x" :precision="2" :controls="false" style="width:100%" placeholder="--" :disabled="disablePivotXY" @change="onPivotXYChange" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="枢轴 Y">
                  <el-input-number v-model="tensioner.automatic.pivot_y" :precision="2" :controls="false" style="width:100%" placeholder="--" :disabled="disablePivotXY" @change="onPivotXYChange" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="臂长(mm)">
                  <el-input-number v-model="tensioner.automatic.arm_length" :precision="2" :controls="false" style="width:100%" placeholder="--" :disabled="disableArmAngle" @change="onArmAngleChange" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="工作角度(°)">
                  <el-input-number v-model="tensioner.automatic.work_angle" :precision="2" :controls="false" style="width:100%" placeholder="--" :disabled="disableArmAngle" :min="0" :max="360" @change="onArmAngleChange" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="枢轴端大小(mm)">
                  <el-input-number v-model="tensioner.automatic.head_size" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="" class="reset-btn-form-item">
                  <el-button type="danger" plain class="reset-pivot-btn" @click="resetPivotArmData">
                    <svg style="width:12px;height:12px;margin-right:4px;vertical-align:middle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="1 4 1 10 7 10"/>
                      <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
                    </svg>
                    重置数据
                  </el-button>
                </el-form-item>
              </el-col>
            </el-row>
          </div>

          <div class="param-section">
            <div class="param-section-title">
              <svg style="width:14px;height:14px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
              力学参数
            </div>
            <el-row :gutter="16">
              <el-col :span="4">
                <el-form-item :label="tensioner.automatic.valueType === 'torque' ? '扭矩(N·m)' : '张力值(N)'">
                  <template v-if="tensioner.automatic.valueType === 'torque'">
                    <el-input-number v-model="tensioner.automatic.torque" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                  </template>
                  <template v-else>
                    <el-input-number v-model="tensioner.automatic.tension_value" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                  </template>
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="阻尼(%)">
                  <el-input-number v-model="tensioner.automatic.damping" :precision="1" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="名义扭转角(°)">
                  <el-input-number v-model="tensioner.automatic.nominal_angle" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="安装扭转角(°)">
                  <el-input-number v-model="tensioner.automatic.install_angle" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="总行程(°)">
                  <el-input-number v-model="tensioner.automatic.stroke" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="弹簧刚度(N·m/°)">
                  <el-input-number v-model="tensioner.automatic.spring_stiffness" :precision="4" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>
        </template>

        <!-- 手调张紧轮参数 -->
        <template v-else>
          <div class="param-section">
            <div class="param-section-title">
              <svg style="width:14px;height:14px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              调节行程
            </div>
            <el-row :gutter="16">
              <el-col :span="6">
                <el-form-item label="起始 X">
                  <el-input-number v-model="tensioner.manual.start_x" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="起始 Y">
                  <el-input-number v-model="tensioner.manual.start_y" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="结束 X">
                  <el-input-number v-model="tensioner.manual.end_x" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="结束 Y">
                  <el-input-number v-model="tensioner.manual.end_y" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>

          <div class="param-section">
            <div class="param-section-title">
              <svg style="width:14px;height:14px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
              名义位置与张力
            </div>
            <el-row :gutter="16">
              <el-col :span="6">
                <el-form-item :label="isManualVertical ? '名义位置 X (计算值)' : '名义位置 X'">
                  <el-input-number v-model="tensioner.manual.nominal_x" :precision="2" :controls="false" style="width:100%" :placeholder="isManualVertical ? '自动计算' : '--'" :disabled="isManualVertical" @change="calcManualNominalY" />
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item :label="isManualVertical ? '名义位置 Y' : '名义位置 Y (计算值)'">
                  <el-input-number v-model="tensioner.manual.nominal_y" :precision="2" :controls="false" style="width:100%" :placeholder="isManualVertical ? '--' : '自动计算'" :disabled="!isManualVertical" @change="calcManualNominalX" />
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="张力设定值(N)">
                  <el-input-number v-model="tensioner.manual.tension_value" :precision="2" :controls="false" style="width:100%" placeholder="--" />
                </el-form-item>
              </el-col>
            </el-row>
          </div>
        </template>
      </el-form>
    </el-card>

    <!-- 皮带参数卡片 -->
    <el-card shadow="hover" class="tensioner-card" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="6" width="20" height="12" rx="2"/>
            <line x1="2" y1="10" x2="22" y2="10"/>
            <line x1="2" y1="14" x2="22" y2="14"/>
          </svg>
          <span>皮带参数</span>
        </div>
      </template>
      <el-form label-position="top" class="tensioner-form">
        <el-row :gutter="16">
          <el-col :span="4">
            <el-form-item label="皮带类型">
              <el-select v-model="beltParams.belt_type" placeholder="请选择类型" style="width:100%">
                <el-option label="CR" value="CR" />
                <el-option label="EPDM(Polyester)" value="EPDM(Polyester)" />
                <el-option label="EPDM(Aramid)" value="EPDM(Aramid)" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="皮带厂家">
              <el-select v-model="beltParams.manufacturer" placeholder="请选择厂家" style="width:100%" @change="handleManufacturerChange">
                <el-option v-for="item in manufacturerOptions" :key="item.name" :label="item.name" :value="item.name" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="皮带PK">
              <el-input v-model="beltParams.belt_pk" placeholder="--" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item>
              <template #label>
                <span>皮带延伸率(%)</span>
                <el-tooltip placement="top" content="EPDM: 0.8 / Aramid: 0.4">
                  <svg style="width:14px;height:14px;margin-left:4px;vertical-align:middle;color:#909399;cursor:help" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                </el-tooltip>
              </template>
              <el-input-number v-model="beltParams.elongation_rate" :precision="3" :controls="false" style="width:100%" placeholder="--" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item>
              <template #label>
                <span>皮带长度公差(mm)</span>
                <el-tooltip placement="top" width="220">
                  <template #content>
                    <div style="line-height:1.6">
                      ≤1000: ±5.0<br/>
                      >1000~1200: ±6.0<br/>
                      >1200~1500: ±7.0<br/>
                      >1500~2000: ±8.0<br/>
                      >2000~2500: ±9.0<br/>
                      >2500~3000: ±10.0
                    </div>
                  </template>
                  <svg style="width:14px;height:14px;margin-left:4px;vertical-align:middle;color:#909399;cursor:help" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                </el-tooltip>
              </template>
              <el-input v-model="beltParams.length_tolerance" placeholder="--" @input="val => beltParams.length_tolerance = String(val).replace(/[^\d.]/g, '')">
                <template #prefix><span style="color:#606266;font-weight:600">±</span></template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item>
              <template #label>
                <span>皮带寿命系数</span>
                <el-tooltip placement="top" content="CR: 1 / EPDM(Polyester): 2.308 / EPDM(Aramid): 3.25">
                  <svg style="width:14px;height:14px;margin-left:4px;vertical-align:middle;color:#909399;cursor:help" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                </el-tooltip>
              </template>
              <el-input-number v-model="beltParams.life_coefficient" :precision="3" :controls="false" style="width:100%" placeholder="--" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16" style="margin-top: 8px">
          <el-col :span="4">
            <el-form-item label="Flat to Pitch (mm)">
              <el-input-number v-model="beltParams.flat_to_pitch" :precision="2" :controls="false" style="width:100%" placeholder="选择厂家自动填入" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="Pitch to Effective (mm)">
              <el-input-number v-model="beltParams.pitch_to_effective" :precision="2" :controls="false" style="width:100%" placeholder="选择厂家自动填入" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="Height (mm)">
              <el-input-number v-model="beltParams.height" :precision="2" :controls="false" style="width:100%" placeholder="选择厂家自动填入" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>

    <!-- 调试信息卡片 -->
    <el-card shadow="hover" class="tensioner-card" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
          </svg>
          <span>调试信息</span>
        </div>
      </template>

      <div class="debug-section">
        <div class="debug-title">张紧轮几何参数</div>
        <table class="debug-table">
          <thead>
            <tr>
              <th>参数</th>
              <th>值</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>臂长</td>
              <td>{{ formatDebugNum(tensioner.automatic.arm_length) }} mm</td>
              <td>张紧器臂长</td>
            </tr>
            <tr>
              <td>节圆直径</td>
              <td>{{ formatDebugNum(tableData.length > 0 ? getPitchDiameter(tableData[tableData.length - 1]) : null) }} mm</td>
              <td>用于几何计算</td>
            </tr>
            <tr>
              <td>包角</td>
              <td style="color: #409eff; font-weight: 600">{{ formatDebugNum(tensionerGeometry?.wrapAngle) }}°</td>
              <td>累计切点角差</td>
            </tr>
            <tr>
              <td>包角平分线 (K)</td>
              <td>{{ formatDebugNum(tensionerGeometry?.bisectAngle) }}°</td>
              <td>前后切点角平均</td>
            </tr>
            <tr>
              <td>枢轴方向 (Q)</td>
              <td>{{ formatDebugNum(tensionerGeometry?.pivotAngle) }}°</td>
              <td>从张紧轮指向枢轴</td>
            </tr>
            <tr>
              <td>包角中点 (S)</td>
              <td style="color: #e6a23c; font-weight: 600">{{ formatDebugNum(tensionerGeometry?.hubloadAngle) }}°</td>
              <td>ABS(枢轴方向 - 包角平分线)</td>
            </tr>
            <tr>
              <td>力臂</td>
              <td>{{ formatDebugNum(tensioner.automatic.arm_length && tensionerGeometry?.hubloadAngle ? tensioner.automatic.arm_length * Math.sin(tensionerGeometry.hubloadAngle * Math.PI / 180) : null) }} mm</td>
              <td>臂长 × sin(包角中点)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="debug-section">
        <div class="debug-title">力值换算</div>
        <table class="debug-table">
          <thead>
            <tr>
              <th>参数</th>
              <th>值</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>输入模式</td>
              <td>{{ tensioner.automatic.valueType === 'torque' ? '扭矩' : '张力值' }}</td>
              <td>当前选择的输入类型</td>
            </tr>
            <tr>
              <td>输入值</td>
              <td>
                <template v-if="tensioner.automatic.valueType === 'torque'">
                  {{ formatDebugNum(tensioner.automatic.torque) }} N·m
                </template>
                <template v-else>
                  {{ formatDebugNum(tensioner.automatic.tension_value) }} N
                </template>
              </td>
              <td>用户输入值</td>
            </tr>
            <tr>
              <td>单段皮带张力</td>
              <td style="color: #409eff; font-weight: 600">
                <template v-if="tensioner.automatic.valueType === 'torque'">
                  {{ formatDebugNum(calcTensionFromTorque) }} N
                </template>
                <template v-else>
                  {{ formatDebugNum(tensioner.automatic.tension_value) }} N
                </template>
              </td>
              <td>
                <template v-if="tensioner.automatic.valueType === 'torque'">
                  合力 / (2 × cos((180-包角)/2)
                </template>
                <template v-else>
                  用户输入
                </template>
              </td>
            </tr>
            <tr>
              <td>合力 (Hubload)</td>
              <td style="color: #e6a23c; font-weight: 600">{{ formatDebugNum(calcHubload) }} N</td>
              <td>2 × 张力 × cos((180-包角)/2)</td>
            </tr>
            <tr>
              <td>计算结果</td>
              <td style="color: #67c23a; font-weight: 600">
                <template v-if="tensioner.automatic.valueType === 'torque' && calcTensionFromTorque !== null">
                  张力 = {{ formatDebugNum(calcTensionFromTorque) }} N
                </template>
                <template v-else-if="tensioner.automatic.valueType === 'tension' && calcTorqueFromTension !== null">
                  扭矩 = {{ formatDebugNum(calcTorqueFromTension) }} N·m
                </template>
                <template v-else>
                  --
                </template>
              </td>
              <td>
                <template v-if="tensioner.automatic.valueType === 'torque'">
                  由扭矩反推单段张力
                </template>
                <template v-else>
                  由张力计算扭矩
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="debug-section" v-if="beltLengthResult.belt_length != null">
        <div class="debug-title">皮带长度计算</div>
        <table class="debug-table">
          <thead>
            <tr>
              <th>参数</th>
              <th>值</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>皮带总长</td>
              <td style="color: #e6a23c; font-weight: 600">{{ formatDebugNum(beltLengthResult.belt_length) }} mm</td>
              <td>Σ(切线段) + Σ(包角弧长)</td>
            </tr>
            <tr>
              <td>直线段总长</td>
              <td>{{ formatDebugNum(beltLengthResult.total_straight) }} mm</td>
              <td>Σ(C × cos(E))</td>
            </tr>
            <tr>
              <td>弧长总和</td>
              <td>{{ formatDebugNum(beltLengthResult.total_arc) }} mm</td>
              <td>Σ(S × K × π / 360)</td>
            </tr>
            <tr>
              <td>带厚 (H21)</td>
              <td>{{ formatDebugNum(beltParams.flat_to_pitch) }} mm</td>
              <td>flat_to_pitch</td>
            </tr>
            <tr>
              <td>衬厚 (H22)</td>
              <td>{{ formatDebugNum(beltParams.pitch_to_effective) }} mm</td>
              <td>pitch_to_effective</td>
            </tr>
          </tbody>
        </table>

        <table class="debug-table" style="margin-top: 8px">
          <thead>
            <tr>
              <th>带轮</th>
              <th>节圆直径K</th>
              <th>中心距C</th>
              <th>上切点角E</th>
              <th>下切点角G</th>
              <th>累计角I</th>
              <th>包角S</th>
              <th>切线段Q</th>
              <th>弧长</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in beltLengthResult.details" :key="d.code">
              <td>{{ d.code }} → {{ d.next_code }}</td>
              <td>{{ formatDebugNum(d.pitch_diameter) }}</td>
              <td>{{ formatDebugNum(d.center_dist) }}</td>
              <td>{{ formatDebugNum(d.upper_tangent_angle) }}°</td>
              <td>{{ formatDebugNum(d.lower_tangent_angle) }}°</td>
              <td>{{ formatDebugNum(d.cumulative_angle) }}°</td>
              <td>{{ formatDebugNum(d.wrap_angle) }}°</td>
              <td>{{ formatDebugNum(d.tangent_length) }}</td>
              <td>{{ formatDebugNum(d.arc_length) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 短皮带长度 & 张紧轮XY坐标 -->
      <div class="debug-section" v-if="shortBeltLength != null">
        <div class="debug-title">短皮带长度 &amp; 张紧轮XY坐标（总长 - 公差）</div>
        <table class="debug-table">
          <thead>
            <tr><th>参数</th><th>值</th><th>说明</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>短皮带长度</td>
              <td style="color: #e6a23c; font-weight: 600">{{ formatDebugNum(shortBeltLength) }} mm</td>
              <td>皮带总长 - 皮带公差</td>
            </tr>
            <tr>
              <td>张紧轮 X</td>
              <td style="color: #409eff; font-weight: 600">{{ formatDebugNum(shortBeltResult.tensioner_x) }}</td>
              <td>短皮带对应张紧轮X坐标</td>
            </tr>
            <tr>
              <td>张紧轮 Y</td>
              <td style="color: #409eff; font-weight: 600">{{ formatDebugNum(shortBeltResult.tensioner_y) }}</td>
              <td>短皮带对应张紧轮Y坐标</td>
            </tr>
            <tr>
              <td>张紧轮臂角度</td>
              <td>{{ formatDebugNum(shortBeltResult.tensioner_angle) }}°</td>
              <td>相对枢轴的臂角度（0-360°）</td>
            </tr>
            <tr>
              <td>臂长</td>
              <td>{{ formatDebugNum(shortBeltResult.arm_length) }} mm</td>
              <td>枢轴到张紧轮距离</td>
            </tr>
            <tr>
              <td>达成皮带长度</td>
              <td>{{ formatDebugNum(shortBeltResult.achieved_length) }} mm</td>
              <td>求解器实际达到的长度</td>
            </tr>
            <tr>
              <td>迭代次数 / 收敛</td>
              <td>{{ shortBeltResult.iterations }} /
                <span v-if="shortBeltResult.converged" style="color: #67c23a">已收敛</span>
                <span v-else style="color: #f56c6c">未收敛</span>
              </td>
              <td>牛顿法迭代次数与收敛状态</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 长皮带长度 & 张紧轮XY坐标 -->
      <div class="debug-section" v-if="longBeltLength != null">
        <div class="debug-title">长皮带长度 &amp; 张紧轮XY坐标（总长 + 公差）</div>
        <table class="debug-table">
          <thead>
            <tr><th>参数</th><th>值</th><th>说明</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>长皮带长度</td>
              <td style="color: #e6a23c; font-weight: 600">{{ formatDebugNum(longBeltLength) }} mm</td>
              <td>皮带总长 + 皮带公差</td>
            </tr>
            <tr>
              <td>张紧轮 X</td>
              <td style="color: #409eff; font-weight: 600">{{ formatDebugNum(longBeltResult.tensioner_x) }}</td>
              <td>长皮带对应张紧轮X坐标</td>
            </tr>
            <tr>
              <td>张紧轮 Y</td>
              <td style="color: #409eff; font-weight: 600">{{ formatDebugNum(longBeltResult.tensioner_y) }}</td>
              <td>长皮带对应张紧轮Y坐标</td>
            </tr>
            <tr>
              <td>张紧轮臂角度</td>
              <td>{{ formatDebugNum(longBeltResult.tensioner_angle) }}°</td>
              <td>相对枢轴的臂角度（0-360°）</td>
            </tr>
            <tr>
              <td>臂长</td>
              <td>{{ formatDebugNum(longBeltResult.arm_length) }} mm</td>
              <td>枢轴到张紧轮距离</td>
            </tr>
            <tr>
              <td>达成皮带长度</td>
              <td>{{ formatDebugNum(longBeltResult.achieved_length) }} mm</td>
              <td>求解器实际达到的长度</td>
            </tr>
            <tr>
              <td>迭代次数 / 收敛</td>
              <td>{{ longBeltResult.iterations }} /
                <span v-if="longBeltResult.converged" style="color: #67c23a">已收敛</span>
                <span v-else style="color: #f56c6c">未收敛</span>
              </td>
              <td>牛顿法迭代次数与收敛状态</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 张紧器自由位置 -->
      <div class="debug-section" v-if="freePositionResult.free_belt_length != null">
        <div class="debug-title">张紧器自由位置（名义扭转角 {{ formatDebugNum(freePositionResult.nominal_angle) }}°，{{ freePositionResult.rotation === 'cw' ? '顺时针' : '逆时针' }}）</div>
        <table class="debug-table">
          <thead>
            <tr><th>参数</th><th>值</th><th>说明</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>自由位置皮带长度</td>
              <td style="color: #e6a23c; font-weight: 600">{{ formatDebugNum(freePositionResult.free_belt_length) }} mm</td>
              <td>张紧器在自由位置时的皮带长度</td>
            </tr>
            <tr>
              <td>自由位置张紧轮 X</td>
              <td style="color: #409eff; font-weight: 600">{{ formatDebugNum(freePositionResult.free_tensioner_x) }}</td>
              <td>自由位置张紧轮X坐标</td>
            </tr>
            <tr>
              <td>自由位置张紧轮 Y</td>
              <td style="color: #409eff; font-weight: 600">{{ formatDebugNum(freePositionResult.free_tensioner_y) }}</td>
              <td>自由位置张紧轮Y坐标</td>
            </tr>
            <tr>
              <td>自由角度</td>
              <td>{{ formatDebugNum(freePositionResult.free_angle) }}°</td>
              <td>自由位置臂角度（0-360°）</td>
            </tr>
            <tr>
              <td>工作角度</td>
              <td>{{ formatDebugNum(freePositionResult.work_angle) }}°</td>
              <td>当前工作位置臂角度（0-360°）</td>
            </tr>
            <tr>
              <td>臂长</td>
              <td>{{ formatDebugNum(freePositionResult.arm_length) }} mm</td>
              <td>枢轴到张紧轮距离</td>
            </tr>
            <tr>
              <td>名义扭转角</td>
              <td>{{ formatDebugNum(freePositionResult.nominal_angle) }}°</td>
              <td>自由位置到工作位置的旋转角度</td>
            </tr>
            <tr>
              <td>旋转方向</td>
              <td>{{ freePositionResult.rotation === 'cw' ? '顺时针 (cw)' : '逆时针 (ccw)' }}</td>
              <td>张紧器从自由位置到工作位置的旋转方向</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 张紧器安装位置 -->
      <div class="debug-section" v-if="installPositionResult.install_belt_length != null">
        <div class="debug-title">张紧器安装位置（安装扭转角 {{ formatDebugNum(installPositionResult.torsion_angle) }}°，{{ installPositionResult.rotation === 'cw' ? '顺时针' : '逆时针' }}）</div>
        <table class="debug-table">
          <thead>
            <tr><th>参数</th><th>值</th><th>说明</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>安装位置皮带长度</td>
              <td style="color: #e6a23c; font-weight: 600">{{ formatDebugNum(installPositionResult.install_belt_length) }} mm</td>
              <td>张紧器在安装位置时的皮带长度</td>
            </tr>
            <tr>
              <td>安装位置张紧轮 X</td>
              <td style="color: #409eff; font-weight: 600">{{ formatDebugNum(installPositionResult.install_tensioner_x) }}</td>
              <td>安装位置张紧轮X坐标</td>
            </tr>
            <tr>
              <td>安装位置张紧轮 Y</td>
              <td style="color: #409eff; font-weight: 600">{{ formatDebugNum(installPositionResult.install_tensioner_y) }}</td>
              <td>安装位置张紧轮Y坐标</td>
            </tr>
            <tr>
              <td>安装臂角</td>
              <td>{{ formatDebugNum(installPositionResult.install_angle) }}°</td>
              <td>安装位置臂角度（0-360°）</td>
            </tr>
            <tr>
              <td>基准臂角</td>
              <td>{{ formatDebugNum(installPositionResult.base_angle) }}°</td>
              <td>当前张紧轮（名义输入位置）臂角度（0-360°）</td>
            </tr>
            <tr>
              <td>臂长</td>
              <td>{{ formatDebugNum(installPositionResult.arm_length) }} mm</td>
              <td>枢轴到张紧轮距离</td>
            </tr>
            <tr>
              <td>安装扭转角</td>
              <td>{{ formatDebugNum(installPositionResult.torsion_angle) }}°</td>
              <td>名义输入位置到安装位置的旋转角度</td>
            </tr>
            <tr>
              <td>旋转方向</td>
              <td>{{ installPositionResult.rotation === 'cw' ? '顺时针 (cw)' : '逆时针 (ccw)' }}</td>
              <td>从名义输入位置到安装位置的旋转方向</td>
            </tr>
          </tbody>
        </table>
      </div>
    </el-card>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, watchEffect } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import PulleyDiagram from '@/components/PulleyDiagram.vue'

import api from '../api/pulley.js'
import { calcContactParams as apiCalcContactParams } from '../api/pulley.js'
import { calcTensionerCoord as apiCalcTensionerCoord } from '../api/pulley.js'
import { calcBeltLength as apiCalcBeltLength } from '../api/pulley.js'
import { calcTensionerPosition as apiCalcTensionerPosition } from '../api/pulley.js'
import { calcFreePosition as apiCalcFreePosition } from '../api/pulley.js'
import { calcInstallPosition as apiCalcInstallPosition } from '../api/pulley.js'
import { sharedStore } from '../store/shared.js'

const formInfo = ref({
  fileNo: '',
  customer: '',
  project: '',
  cylinders: '',
  power: '',
  updateDesc: '',
  issueDesc: '',
  version: 1
})

const beltParams = ref({
  belt_type: 'EPDM(Polyester)',
  manufacturer: 'Gates',
  belt_pk: '8',
  elongation_rate: 0.8,
  length_tolerance: '6',
  life_coefficient: 2.3,
  flat_to_pitch: sharedStore.beltParams.flat_to_pitch ?? null,
  pitch_to_effective: sharedStore.beltParams.pitch_to_effective ?? null,
  height: null
})

const tensioner = ref({
  type: 'automatic',
  automatic: {
    rotation: 'cw',
    pivot_x: 120,
    pivot_y: 20,
    arm_length: null,
    work_angle: null,
    spring_stiffness: 0.32,
    valueType: 'torque',
    torque: 32,
    tension_value: null,
    damping: 30,
    nominal_angle: 25,
    install_angle: 25,
    stroke: 40,
    head_size: 50
  },
  manual: {
    start_x: null,
    start_y: null,
    end_x: null,
    end_y: null,
    nominal_x: null,
    nominal_y: null,
    tension_value: null
  }
})

// 计算模式：1=枢轴+臂长+角度→张紧轮XY  2=张紧轮+臂长+角度→枢轴XY  3=枢轴+张紧轮→臂长+角度
const calcMode = ref('3')

// 标记是否正在进行自动计算，用于阻止watch循环触发
const isAutoCalculating = ref(false)

// 计算禁用状态：根据计算模式决定哪些输入框禁用
const disablePivotXY = computed(() => {
  // 模式2：枢轴XY是计算结果，禁用输入
  return calcMode.value === '2'
})

const disableArmAngle = computed(() => {
  // 模式3：臂长+角度是计算结果，禁用输入
  return calcMode.value === '3'
})

const disableTensionerXY = computed(() => {
  // 模式1：张紧轮XY是计算结果，禁用输入
  return calcMode.value === '1'
})

// Geometry 几何计算（用节圆直径）
function getPitchDiameter(pulley) {
  const ftp = beltParams.value.flat_to_pitch || 0
  const pte = beltParams.value.pitch_to_effective || 0
  if (pulley.type === 'flat') {
    return (pulley.flat_dia || 0) + 2 * (ftp + pte)
  } else {
    return pulley.groove_dia || 0
  }
}

function calcTangentAngles(pulleys) {
  if (!pulleys || pulleys.length < 2) return null
  const n = pulleys.length
  const entryAngles = new Array(n)
  const exitAngles = new Array(n)
  const cumulativeAngles = new Array(n)
  const wrapAngles = new Array(n)
  const bisectAngles = new Array(n)

  const pitchDiams = pulleys.map(p => getPitchDiameter(p))

  for (let i = 0; i < n; i++) {
    const curr = pulleys[i]
    const nextP = pulleys[(i + 1) % n]
    const rCurr = pitchDiams[i] / 2
    const rNext = pitchDiams[(i + 1) % n] / 2

    const dx = nextP.x - curr.x
    const dy = nextP.y - curr.y
    const dist = Math.sqrt(dx * dx + dy * dy)

    const cosG = dx / dist
    let G = Math.acos(Math.max(-1, Math.min(1, cosG))) * 180 / Math.PI
    if (dy < 0) {
      G = 360 - G
    }

    const sameType = curr.type === nextP.type
    let sinE
    if (sameType) {
      sinE = (rCurr - rNext) / dist
    } else {
      sinE = (rCurr + rNext) / dist
    }
    let E = Math.asin(Math.max(-1, Math.min(1, sinE))) * 180 / Math.PI
    if (curr.type === 'flat') {
      E = -E
    }

    let I = G + E
    while (I < 0) I += 360
    while (I >= 360) I -= 360
    cumulativeAngles[i] = I
    exitAngles[i] = G
  }

  for (let i = 0; i < n; i++) {
    const prevCumulative = cumulativeAngles[(i - 1 + n) % n]
    const currCumulative = cumulativeAngles[i]
    const diff = currCumulative - prevCumulative
    const isFlat = pulleys[i].type === 'flat'

    let wrap = 0
    if (isFlat) {
      if (diff < 0) {
        if (Math.abs(diff) > 360) {
          wrap = Math.abs(diff) - 360
        } else {
          wrap = -diff
        }
      } else {
        wrap = 360 - diff
      }
    } else {
      wrap = diff < 0 ? diff + 360 : diff
    }
    wrapAngles[i] = wrap

    const prevM = prevCumulative < 180 ? prevCumulative + 180 : prevCumulative - 180
    let bisect = 0
    if (Math.abs(currCumulative - prevM) < 180) {
      bisect = (prevM + currCumulative) / 2
    } else if (currCumulative + prevM > 360) {
      bisect = (currCumulative + prevM) / 2 - 180
    } else {
      bisect = (currCumulative + prevM) / 2 + 180
    }
    while (bisect < 0) bisect += 360
    while (bisect >= 360) bisect -= 360
    bisectAngles[i] = bisect
  }

  return { entryAngles, exitAngles, cumulativeAngles, wrapAngles, bisectAngles }
}

const geometryResult = computed(() => {
  const pulleys = tableData.value
  if (!pulleys || pulleys.length < 2) return null
  return calcTangentAngles(pulleys)
})

const tensionerGeometry = computed(() => {
  const gr = geometryResult.value
  if (!gr) return null
  const lastIdx = tableData.value.length - 1
  if (lastIdx < 0) return null
  const t = tensioner.value.automatic
  const lastPulley = tableData.value[lastIdx]

  let pivotAngle = null
  if (t.pivot_x != null && t.pivot_y != null && lastPulley.x != null && lastPulley.y != null) {
    pivotAngle = Math.atan2(t.pivot_y - lastPulley.y, t.pivot_x - lastPulley.x) * 180 / Math.PI
    while (pivotAngle < 0) pivotAngle += 360
    while (pivotAngle >= 360) pivotAngle -= 360
  }

  const bisect = gr.bisectAngles[lastIdx]
  let hubloadAngle = null
  if (pivotAngle != null && bisect != null) {
    hubloadAngle = Math.abs(pivotAngle - bisect)
  }

  return {
    entryAngle: gr.entryAngles[lastIdx],
    exitAngle: gr.exitAngles[lastIdx],
    cumulativeAngle: gr.cumulativeAngles[lastIdx],
    wrapAngle: gr.wrapAngles[lastIdx],
    bisectAngle: bisect,
    pivotAngle,
    hubloadAngle
  }
})

// 皮带长度计算结果
const beltLengthResult = computed(() => sharedStore.beltLengthResult || {})

// 短皮带长度计算结果（短皮带 = 总长 - 公差）
const shortBeltResult = computed(() => sharedStore.shortBeltResult || {})

// 长皮带长度计算结果（长皮带 = 总长 + 公差）
const longBeltResult = computed(() => sharedStore.longBeltResult || {})

// 张紧器自由位置计算结果
const freePositionResult = computed(() => sharedStore.freePositionResult || {})
const installPositionResult = computed(() => sharedStore.installPositionResult || {})

// 短皮带长度（计算值，用于显示）
const shortBeltLength = computed(() => {
  const total = beltLengthResult.value.belt_length
  if (total == null) return null
  const tol = Number(beltParams.value.length_tolerance) || 0
  return total - tol
})

// 长皮带长度（计算值，用于显示）
const longBeltLength = computed(() => {
  const total = beltLengthResult.value.belt_length
  if (total == null) return null
  const tol = Number(beltParams.value.length_tolerance) || 0
  return total + tol
})

// 张紧轮力值换算
const tensionerContactParams = computed(() => {
  const cp = sharedStore.contactParams
  if (!cp || typeof cp !== 'object') return null
  const lastPulley = tableData.value[tableData.value.length - 1]
  if (!lastPulley || !lastPulley.code) return null
  return cp[lastPulley.code] || null
})

const calcTensionFromTorque = computed(() => {
  const t = tensioner.value.automatic
  if (t.valueType !== 'torque') return null
  if (t.torque == null) return null
  const arm = t.arm_length
  const tg = tensionerGeometry.value
  if (!tg || arm == null || arm === 0) return null
  const wrapAngle = tg.wrapAngle
  const hubloadAngle = tg.hubloadAngle
  if (wrapAngle == null || hubloadAngle == null) return null
  const forceArm = arm * Math.sin(hubloadAngle * Math.PI / 180)
  if (forceArm === 0) return null
  const hubload = t.torque * 1000 / forceArm
  const singleTension = hubload / (2 * Math.cos((180 - wrapAngle) / 2 * Math.PI / 180))
  return Number(singleTension.toFixed(2))
})

const calcTorqueFromTension = computed(() => {
  const t = tensioner.value.automatic
  if (t.valueType !== 'tension') return null
  if (t.tension_value == null) return null
  const arm = t.arm_length
  const tg = tensionerGeometry.value
  if (!tg || arm == null) return null
  const wrapAngle = tg.wrapAngle
  const hubloadAngle = tg.hubloadAngle
  if (wrapAngle == null || hubloadAngle == null) return null
  const hubload = 2 * t.tension_value * Math.cos((180 - wrapAngle) / 2 * Math.PI / 180)
  const forceArm = arm * Math.sin(hubloadAngle * Math.PI / 180)
  const torque = hubload * forceArm / 1000
  return Number(torque.toFixed(2))
})

const calcHubload = computed(() => {
  const t = tensioner.value.automatic
  const tg = tensionerGeometry.value
  if (!tg) return null
  const wrapAngle = tg.wrapAngle
  if (wrapAngle == null) return null
  let singleTension = null
  if (t.valueType === 'torque') {
    singleTension = calcTensionFromTorque.value
  } else {
    singleTension = t.tension_value
  }
  if (singleTension == null) return null
  const hubload = 2 * singleTension * Math.cos((180 - wrapAngle) / 2 * Math.PI / 180)
  return Number(hubload.toFixed(2))
})

function formatDebugNum(val) {
  if (val == null || isNaN(val)) return '--'
  return Number(val).toFixed(2)
}

// 手调张紧轮：判断是否为垂直线（起始X == 结束X）
const isManualVertical = computed(() => {
  const manual = tensioner.value.manual
  const sx = manual.start_x, ex = manual.end_x
  return sx != null && ex != null && Math.abs(ex - sx) < 1e-9
})

// ====== 自动推导张紧轮旋转方向 ======
// 记录自动计算推导出的旋转方向值（'cw' 或 'ccw'），手动选择时置空
const autoCalculatedRotation = ref(null)

/**
 * 根据轮系布局自动推导张紧器旋转方向
 * 原理：张紧器臂绕枢轴旋转，将张紧轮推向皮带（压紧皮带）。
 * 旋转方向 = 臂绕枢轴朝皮带方向旋转的方向。
 */
function autoDetectTensionerRotation() {
  const data = tableData.value
  if (data.length < 2) return

  // 收集有效轮子数据（有坐标和半径的）
  const validPulleys = []
  for (let i = 0; i < data.length; i++) {
    const p = data[i]
    const dia = p.type === 'flat' ? p.flat_dia : p.groove_dia
    const r = dia ? dia / 2 : 0
    if (r > 0 && p.x != null && p.y != null) {
      validPulleys.push({ ...p, r, index: i })
    }
  }
  if (validPulleys.length < 2) return

  // 张紧轮是最后一个有效轮子
  const tensionerIdx = validPulleys.length - 1
  const tensionerPulley = validPulleys[tensionerIdx]

  // 获取枢轴坐标
  const pivotX = tensioner.value.automatic?.pivot_x
  const pivotY = tensioner.value.automatic?.pivot_y
  if (pivotX == null || pivotY == null) return
  if (tensionerPulley.x == null || tensionerPulley.y == null) return

  // 计算切线（与 PulleyDiagram 相同的逻辑）
  function getTangents(a, b) {
    const x1 = a.x, y1 = a.y, r1 = a.r
    const x2 = b.x, y2 = b.y, r2 = b.r
    const dx = x2 - x1, dy = y2 - y1
    const dSq = dx * dx + dy * dy
    if (dSq === 0) return []
    const d = Math.sqrt(dSq)
    const vx = dx / d, vy = dy / d
    const tangents = []
    const rDiff = r1 - r2
    const h = Math.sqrt(Math.max(0, dSq - rDiff * rDiff))
    const nx = -vy, ny = vx
    tangents.push({
      p1: { x: x1 + r1 * (vx * rDiff / d - nx * h / d), y: y1 + r1 * (vy * rDiff / d - ny * h / d) },
      p2: { x: x2 + r2 * (vx * rDiff / d - nx * h / d), y: y2 + r2 * (vy * rDiff / d - ny * h / d) },
      type: 'external'
    })
    tangents.push({
      p1: { x: x1 + r1 * (vx * rDiff / d + nx * h / d), y: y1 + r1 * (vy * rDiff / d + ny * h / d) },
      p2: { x: x2 + r2 * (vx * rDiff / d + nx * h / d), y: y2 + r2 * (vy * rDiff / d + ny * h / d) },
      type: 'external'
    })
    const rSum = r1 + r2
    const h2 = Math.sqrt(Math.max(0, dSq - rSum * rSum))
    if (h2 > 0.001) {
      tangents.push({
        p1: { x: x1 + r1 * (vx * rSum / d - nx * h2 / d), y: y1 + r1 * (vy * rSum / d - ny * h2 / d) },
        p2: { x: x2 - r2 * (vx * rSum / d - nx * h2 / d), y: y2 - r2 * (vy * rSum / d - ny * h2 / d) },
        type: 'internal'
      })
      tangents.push({
        p1: { x: x1 + r1 * (vx * rSum / d + nx * h2 / d), y: y1 + r1 * (vy * rSum / d + ny * h2 / d) },
        p2: { x: x2 - r2 * (vx * rSum / d + nx * h2 / d), y: y2 - r2 * (vy * rSum / d + ny * h2 / d) },
        type: 'internal'
      })
    }
    return tangents
  }

  function chooseTangent(a, b, tangents) {
    if (tangents.length < 2) return tangents[0] || null
    let candidates = []
    if (a.type === b.type) {
      candidates = tangents.filter(t => t.type === 'external')
      if (candidates.length === 0) candidates = tangents
    } else {
      candidates = tangents.filter(t => t.type === 'internal')
      if (candidates.length === 0) candidates = tangents
    }
    if (candidates.length >= 2) {
      return a.type === 'groove' ? candidates[1] : candidates[0]
    }
    return candidates[0] || null
  }

  // 计算所有相邻轮对的切线
  const tangentSegments = []
  for (let i = 0; i < validPulleys.length; i++) {
    const a = validPulleys[i]
    const b = validPulleys[(i + 1) % validPulleys.length]
    const tangents = getTangents(a, b)
    const chosen = chooseTangent(a, b, tangents)
    if (chosen) {
      tangentSegments.push({
        aIndex: i,
        bIndex: (i + 1) % validPulleys.length,
        entry: chosen.p1,
        exit: chosen.p2
      })
    }
  }

  if (tangentSegments.length < 2) return

  // 找到张紧轮的 entry 和 exit 切线点
  let entryPoint = null, exitPoint = null
  for (const seg of tangentSegments) {
    if (seg.bIndex === tensionerIdx) {
      entryPoint = seg.exit
    }
    if (seg.aIndex === tensionerIdx) {
      exitPoint = seg.entry
    }
  }

  if (!entryPoint || !exitPoint) return

  // 核心逻辑：
  // 张紧器臂绕枢轴旋转，将张紧轮推向皮带（压紧方向）
  // 旋转方向 = 臂从当前位置绕枢轴朝皮带方向旋转的方向
  //
  // 步骤：
  // 1. 计算臂方向角（枢轴→张紧轮）
  // 2. 计算皮带在张紧轮处需要被压紧的方向（皮带中点到张紧轮圆心的反方向）
  // 3. 臂绕枢轴从当前方向朝压紧方向旋转，判断是顺时针还是逆时针

  const px = pivotX, py = pivotY
  const tx = tensionerPulley.x, ty = tensionerPulley.y

  // 臂方向角（枢轴→张紧轮）
  const armAngle = Math.atan2(ty - py, tx - px)

  // 皮带在张紧轮处的压紧方向：
  // 皮带 entry→exit 的中点方向就是皮带运行方向
  // 张紧轮需要朝皮带中心线方向移动（压紧）
  // 皮带中心线方向 = entry→exit 的中点相对于张紧轮圆心的方向
  const beltMidX = (entryPoint.x + exitPoint.x) / 2
  const beltMidY = (entryPoint.y + exitPoint.y) / 2
  // 压紧方向：从张紧轮圆心指向皮带中点
  const pressAngle = Math.atan2(beltMidY - ty, beltMidX - tx)

  // 目标方向：臂需要旋转到的方向（枢轴出发，朝皮带压紧点方向）
  // 压紧点 = 张紧轮圆心 + 压紧方向 * 张紧轮半径（近似）
  // 但更简单：直接看臂绕枢轴旋转，张紧轮朝皮带方向移动
  // 张紧轮当前在枢轴的 armAngle 方向
  // 需要将张紧轮推向 pressAngle 方向（相对于张紧轮圆心）
  // 转换为绕枢轴的旋转：目标角度使得张紧轮更靠近皮带

  // 更直接的方法：
  // 计算从枢轴到皮带中点的方向角
  const pivotToBeltMidAngle = Math.atan2(beltMidY - py, beltMidX - px)

  // 臂需要从 armAngle 旋转到 pivotToBeltMidAngle 方向（朝皮带中点方向推）
  // 判断旋转方向
  let rotDiff = pivotToBeltMidAngle - armAngle
  while (rotDiff > Math.PI) rotDiff -= 2 * Math.PI
  while (rotDiff < -Math.PI) rotDiff += 2 * Math.PI

  // rotDiff > 0：需要逆时针旋转（数学坐标）→ 视觉顺时针（cw）
  // rotDiff < 0：需要顺时针旋转（数学坐标）→ 视觉逆时针（ccw）
  // 旋转方向与压紧皮带方向相反
  const rotation = rotDiff > 0 ? 'ccw' : 'cw'

  autoCalculatedRotation.value = rotation
  tensioner.value.automatic.rotation = rotation
}

const headerStyle = {
  backgroundColor: '#f0f5ff',
  color: '#1d2129',
  fontWeight: '600',
  textAlign: 'center',
  fontSize: '13px',
  padding: '10px 0'
}

const cellStyle = {
  padding: '6px 4px'
}

const beltOptions = ref([])
const manufacturerOptions = ref([])
const tableData = ref(
  sharedStore.pulleys.length > 0
    ? sharedStore.pulleys.map(p => ({
        name: p.name || '',
        code: p.code || '',
        x: p.x ?? null,
        y: p.y ?? null,
        flat_dia: p.flat_dia ?? null,
        groove_dia: p.groove_dia ?? null,
        type: p.type || 'groove',
        inertia: p.inertia ?? null,
        service_factor: p.service_factor ?? null
      }))
    : [createRow(), createRow()]
)

// 判断张紧轮是否已有XY值
const hasTensionerXY = computed(() => {
  if (tableData.value.length === 0) return false
  const lastRow = tableData.value[tableData.value.length - 1]
  return !!(lastRow && lastRow.x != null && lastRow.y != null)
})

// 判断枢轴是否已有XY值
const hasPivotXY = computed(() => {
  return tensioner.value.automatic.pivot_x != null && tensioner.value.automatic.pivot_y != null
})

// 判断臂长和角度是否都有值
const hasArmAngle = computed(() => {
  return tensioner.value.automatic.arm_length != null && tensioner.value.automatic.work_angle != null
})

// 模式1是否禁用：当张紧轮已有XY值时禁用
const disableMode1 = computed(() => hasTensionerXY.value)

// 模式2是否禁用：当枢轴已有XY值时禁用
const disableMode2 = computed(() => hasPivotXY.value)

// 模式3是否禁用：当臂长和角度都已有值时禁用
const disableMode3 = computed(() => hasArmAngle.value)

// 当当前模式被禁用时，自动切换到第一个可用模式
watch([disableMode1, disableMode2, disableMode3], () => {
  if (calcMode.value === '1' && disableMode1.value) {
    if (!disableMode3.value) calcMode.value = '3'
    else if (!disableMode2.value) calcMode.value = '2'
  } else if (calcMode.value === '2' && disableMode2.value) {
    if (!disableMode3.value) calcMode.value = '3'
    else if (!disableMode1.value) calcMode.value = '1'
  } else if (calcMode.value === '3' && disableMode3.value) {
    if (!disableMode1.value) calcMode.value = '1'
    else if (!disableMode2.value) calcMode.value = '2'
  }
})

// 监听表格数据变化，自动推导旋转方向（仅在自动张紧轮模式下）
watch(
  () => tableData.value.map(p => ({ x: p.x, y: p.y, flat_dia: p.flat_dia, groove_dia: p.groove_dia, type: p.type })),
  () => {
    if (tensioner.value.type === 'automatic') {
      autoDetectTensionerRotation()
    }
  },
  { deep: true }
)

// 同步带轮数据到共享 store（供负载页使用）
// pulleys: 所有带轮完整数据（含直径、类型）；beltParams: 皮带参数
watch(
  () => tableData.value.map(p => ({ code: p.code, name: p.name, x: p.x, y: p.y, flat_dia: p.flat_dia, groove_dia: p.groove_dia, type: p.type, inertia: p.inertia, service_factor: p.service_factor })),
  (newPulleys) => {
    const filtered = newPulleys.filter(p => p.code)
    // 保留已有带轮的对齐度相关字段（centerHeightDiff, perpendicularity 等）
    const existingMap = new Map(sharedStore.pulleys.map(p => [p.code, p]))
    const merged = filtered.map(p => {
      const existing = existingMap.get(p.code)
      return existing ? { ...existing, ...p } : p
    })
    sharedStore.pulleys.splice(0, sharedStore.pulleys.length, ...merged)
  },
  { deep: true, immediate: true }
)

// 同步皮带参数到共享 store
watch(
  () => ({ flat_to_pitch: beltParams.value.flat_to_pitch, pitch_to_effective: beltParams.value.pitch_to_effective }),
  (val) => {
    sharedStore.beltParams.flat_to_pitch = val.flat_to_pitch
    sharedStore.beltParams.pitch_to_effective = val.pitch_to_effective
  },
  { deep: true, immediate: true }
)

// 计算Contact参数（K/J/L/M/N/P/O/Q/U）- 调用后端API
async function calcContactParams() {
  const list = sharedStore.pulleys.filter(p => p.code && p.x != null && p.y != null)
  sharedStore.lastPulleyIndex = list.length
  if (list.length < 2) {
    sharedStore.contactParams = {}
    return
  }

  try {
    const res = await apiCalcContactParams({
      pulleys: list.map(p => ({
        code: p.code,
        name: p.name || '',
        type: p.type,
        x: Number(p.x) || 0,
        y: Number(p.y) || 0,
        groove_dia: p.groove_dia != null ? Number(p.groove_dia) : null,
        flat_dia: p.flat_dia != null ? Number(p.flat_dia) : null,
      })),
      pitch_to_effective: Number(sharedStore.beltParams.pitch_to_effective) || 0,
      flat_to_pitch: Number(sharedStore.beltParams.flat_to_pitch) || 0,
    })
    if (res.data.success) {
      sharedStore.contactParams = res.data.contact_params
    }
  } catch (e) {
    console.error('Contact参数计算失败:', e)
  }
}

watch(
  () => [sharedStore.pulleys.map(p => ({ code: p.code, x: p.x, y: p.y, type: p.type, groove_dia: p.groove_dia, flat_dia: p.flat_dia })), sharedStore.beltParams.flat_to_pitch, sharedStore.beltParams.pitch_to_effective],
  () => {
    calcContactParams()
    calcBeltLength()
  },
  { deep: true, immediate: true }
)

// 计算皮带长度 - 调用后端API
async function calcBeltLength() {
  const list = sharedStore.pulleys.filter(p => p.code && p.x != null && p.y != null)
  if (list.length < 2) {
    sharedStore.beltFullParams.effective_length = null
    sharedStore.beltLengthResult = { belt_length: null, total_straight: null, total_arc: null, details: [] }
    return
  }

  try {
    const res = await apiCalcBeltLength({
      pulleys: list.map(p => ({
        code: p.code,
        name: p.name || '',
        type: p.type,
        x: Number(p.x) || 0,
        y: Number(p.y) || 0,
        groove_dia: p.groove_dia != null ? Number(p.groove_dia) : null,
        flat_dia: p.flat_dia != null ? Number(p.flat_dia) : null,
      })),
      belt_thickness: Number(beltParams.value.flat_to_pitch) || 0,
      lining_thickness: Number(beltParams.value.pitch_to_effective) || 0,
    })
    if (res.data.success) {
      sharedStore.beltFullParams.effective_length = res.data.belt_length
      sharedStore.beltLengthResult = {
        belt_length: res.data.belt_length,
        total_straight: res.data.total_straight,
        total_arc: res.data.total_arc,
        details: res.data.details || []
      }
      // 皮带长度计算成功后，计算短/长皮带张紧轮坐标、自由位置和安装位置
      calcTensionerPosition()
      calcFreePosition()
      calcInstallPosition()
    }
  } catch (e) {
    console.error('皮带长度计算失败:', e)
  }
}

// 计算短/长皮带长度对应的张紧轮XY坐标 - 调用后端API
// 短皮带 = 总长 - 公差，长皮带 = 总长 + 公差
async function calcTensionerPosition() {
  const list = sharedStore.pulleys.filter(p => p.code && p.x != null && p.y != null)
  const emptyResult = {
    short_belt_length: null, tensioner_x: null, tensioner_y: null,
    tensioner_angle: null, achieved_length: null, arm_length: null,
    iterations: null, converged: null
  }
  const emptyLong = {
    long_belt_length: null, tensioner_x: null, tensioner_y: null,
    tensioner_angle: null, achieved_length: null, arm_length: null,
    iterations: null, converged: null
  }

  if (list.length < 2) {
    sharedStore.shortBeltResult = { ...emptyResult }
    sharedStore.longBeltResult = { ...emptyLong }
    return
  }

  const beltLength = sharedStore.beltLengthResult.belt_length
  if (beltLength == null) return

  const tol = Number(beltParams.value.length_tolerance) || 0
  const shortTarget = beltLength - tol
  const longTarget = beltLength + tol

  const pivotX = tensioner.value.automatic.pivot_x
  const pivotY = tensioner.value.automatic.pivot_y
  if (pivotX == null || pivotY == null) {
    sharedStore.shortBeltResult = { ...emptyResult, short_belt_length: shortTarget }
    sharedStore.longBeltResult = { ...emptyLong, long_belt_length: longTarget }
    return
  }

  const tensionerCode = list[list.length - 1].code
  const pulleysPayload = list.map(p => ({
    code: p.code, name: p.name || '', type: p.type,
    x: Number(p.x) || 0, y: Number(p.y) || 0,
    groove_dia: p.groove_dia != null ? Number(p.groove_dia) : null,
    flat_dia: p.flat_dia != null ? Number(p.flat_dia) : null,
  }))
  const commonParams = {
    pulleys: pulleysPayload,
    tensioner_code: tensionerCode,
    pivot_x: Number(pivotX),
    pivot_y: Number(pivotY),
    belt_thickness: Number(beltParams.value.flat_to_pitch) || 0,
    lining_thickness: Number(beltParams.value.pitch_to_effective) || 0,
  }

  // 短皮带求解
  try {
    const res = await apiCalcTensionerPosition({ ...commonParams, target_length: shortTarget })
    if (res.data.success) {
      sharedStore.shortBeltResult = {
        short_belt_length: Number(shortTarget.toFixed(4)),
        tensioner_x: res.data.tensioner_x,
        tensioner_y: res.data.tensioner_y,
        tensioner_angle: res.data.tensioner_angle,
        achieved_length: res.data.achieved_length,
        arm_length: res.data.arm_length,
        iterations: res.data.iterations,
        converged: res.data.converged
      }
    }
  } catch (e) {
    console.error('短皮带张紧轮坐标计算失败:', e)
  }

  // 长皮带求解
  try {
    const res = await apiCalcTensionerPosition({ ...commonParams, target_length: longTarget })
    if (res.data.success) {
      sharedStore.longBeltResult = {
        long_belt_length: Number(longTarget.toFixed(4)),
        tensioner_x: res.data.tensioner_x,
        tensioner_y: res.data.tensioner_y,
        tensioner_angle: res.data.tensioner_angle,
        achieved_length: res.data.achieved_length,
        arm_length: res.data.arm_length,
        iterations: res.data.iterations,
        converged: res.data.converged
      }
    }
  } catch (e) {
    console.error('长皮带张紧轮坐标计算失败:', e)
  }
}

// 计算张紧器自由位置的皮带长度和张紧轮XY坐标 - 调用后端API
async function calcFreePosition() {
  const list = sharedStore.pulleys.filter(p => p.code && p.x != null && p.y != null)
  const empty = {
    free_tensioner_x: null, free_tensioner_y: null, free_angle: null,
    free_belt_length: null, work_angle: null, arm_length: null,
    nominal_angle: null, rotation: null
  }

  if (list.length < 2) {
    sharedStore.freePositionResult = { ...empty }
    return
  }

  const pivotX = tensioner.value.automatic.pivot_x
  const pivotY = tensioner.value.automatic.pivot_y
  if (pivotX == null || pivotY == null) {
    sharedStore.freePositionResult = { ...empty }
    return
  }

  const tensionerCode = list[list.length - 1].code
  const nominalAngle = Number(tensioner.value.automatic.nominal_angle) || 0
  const rotation = tensioner.value.automatic.rotation || 'cw'

  try {
    const res = await apiCalcFreePosition({
      pulleys: list.map(p => ({
        code: p.code, name: p.name || '', type: p.type,
        x: Number(p.x) || 0, y: Number(p.y) || 0,
        groove_dia: p.groove_dia != null ? Number(p.groove_dia) : null,
        flat_dia: p.flat_dia != null ? Number(p.flat_dia) : null,
      })),
      tensioner_code: tensionerCode,
      pivot_x: Number(pivotX),
      pivot_y: Number(pivotY),
      nominal_angle: nominalAngle,
      rotation: rotation,
      belt_thickness: Number(beltParams.value.flat_to_pitch) || 0,
      lining_thickness: Number(beltParams.value.pitch_to_effective) || 0,
    })
    if (res.data.success) {
      sharedStore.freePositionResult = {
        free_tensioner_x: res.data.free_tensioner_x,
        free_tensioner_y: res.data.free_tensioner_y,
        free_angle: res.data.free_angle,
        free_belt_length: res.data.free_belt_length,
        work_angle: res.data.work_angle,
        arm_length: res.data.arm_length,
        nominal_angle: res.data.nominal_angle,
        rotation: res.data.rotation
      }
    }
  } catch (e) {
    console.error('张紧器自由位置计算失败:', e)
  }
}

// 计算张紧器安装位置的皮带长度和张紧轮XY坐标 - 调用后端API
async function calcInstallPosition() {
  const list = sharedStore.pulleys.filter(p => p.code && p.x != null && p.y != null)
  const empty = {
    install_tensioner_x: null, install_tensioner_y: null, install_angle: null,
    install_belt_length: null, base_angle: null, arm_length: null,
    torsion_angle: null, rotation: null
  }

  if (list.length < 2) {
    sharedStore.installPositionResult = { ...empty }
    return
  }

  const pivotX = tensioner.value.automatic.pivot_x
  const pivotY = tensioner.value.automatic.pivot_y
  if (pivotX == null || pivotY == null) {
    sharedStore.installPositionResult = { ...empty }
    return
  }

  const tensionerCode = list[list.length - 1].code
  const installAngle = Number(tensioner.value.automatic.install_angle) || 0
  const rotation = tensioner.value.automatic.rotation || 'cw'

  try {
    const res = await apiCalcInstallPosition({
      pulleys: list.map(p => ({
        code: p.code, name: p.name || '', type: p.type,
        x: Number(p.x) || 0, y: Number(p.y) || 0,
        groove_dia: p.groove_dia != null ? Number(p.groove_dia) : null,
        flat_dia: p.flat_dia != null ? Number(p.flat_dia) : null,
      })),
      tensioner_code: tensionerCode,
      pivot_x: Number(pivotX),
      pivot_y: Number(pivotY),
      install_angle: installAngle,
      rotation: rotation,
      belt_thickness: Number(beltParams.value.flat_to_pitch) || 0,
      lining_thickness: Number(beltParams.value.pitch_to_effective) || 0,
    })
    if (res.data.success) {
      sharedStore.installPositionResult = {
        install_tensioner_x: res.data.install_tensioner_x,
        install_tensioner_y: res.data.install_tensioner_y,
        install_angle: res.data.install_angle,
        install_belt_length: res.data.install_belt_length,
        base_angle: res.data.base_angle,
        arm_length: res.data.arm_length,
        torsion_angle: res.data.torsion_angle,
        rotation: res.data.rotation
      }
    }
  } catch (e) {
    console.error('张紧器安装位置计算失败:', e)
  }
}

// 皮带公差变化时重新计算短/长皮带张紧轮坐标
watch(
  () => beltParams.value.length_tolerance,
  () => {
    if (sharedStore.beltLengthResult.belt_length != null) {
      calcTensionerPosition()
    }
  }
)

// 枢轴坐标变化时重新计算短/长皮带张紧轮坐标和自由位置
watch(
  () => [tensioner.value.automatic.pivot_x, tensioner.value.automatic.pivot_y],
  () => {
    if (!isAutoCalculating.value && sharedStore.beltLengthResult.belt_length != null) {
      calcTensionerPosition()
      calcFreePosition()
    }
  }
)

// 名义扭转角或旋转方向变化时重新计算自由位置
watch(
  () => [tensioner.value.automatic.nominal_angle, tensioner.value.automatic.rotation],
  () => {
    if (!isAutoCalculating.value && sharedStore.beltLengthResult.belt_length != null) {
      calcFreePosition()
    }
  }
)

// 安装扭转角或旋转方向变化时重新计算安装位置
watch(
  () => [tensioner.value.automatic.install_angle, tensioner.value.automatic.rotation],
  () => {
    if (!isAutoCalculating.value && sharedStore.beltLengthResult.belt_length != null) {
      calcInstallPosition()
    }
  }
)

// 用户修改表格XY时，根据计算模式触发计算
function onTableXYChange(idx) {
  if (isAutoCalculating.value) return
  if (tableData.value.length > 0 && idx === tableData.value.length - 1) {
    if (tableData.value[idx].x != null && tableData.value[idx].y != null) {
      triggerCalc()
    }
  }
}

// 用户修改枢轴XY时，根据计算模式触发计算
function onPivotXYChange() {
  if (isAutoCalculating.value) return
  if (tensioner.value.automatic.pivot_x != null && tensioner.value.automatic.pivot_y != null) {
    triggerCalc()
  }
}

// 用户修改臂长或角度时，根据计算模式触发计算
function onArmAngleChange() {
  if (isAutoCalculating.value) return
  if (tensioner.value.automatic.arm_length != null && tensioner.value.automatic.work_angle != null) {
    triggerCalc()
  }
}

// 根据计算模式触发对应的计算
async function triggerCalc() {
  if (isAutoCalculating.value) return

  const mode = calcMode.value
  const hasPivot = tensioner.value.automatic.pivot_x != null && tensioner.value.automatic.pivot_y != null
  const lastRow = tableData.value.length > 0 ? tableData.value[tableData.value.length - 1] : null
  const hasTensioner = lastRow && lastRow.x != null && lastRow.y != null
  const hasArmAngleVal = tensioner.value.automatic.arm_length != null && tensioner.value.automatic.work_angle != null

  isAutoCalculating.value = true

  try {
    if (mode === '1') {
      // 枢轴+臂长+角度 → 张紧轮XY
      if (hasPivot && hasArmAngleVal) {
        await calculateTensionerXY()
      }
    } else if (mode === '2') {
      // 张紧轮+臂长+角度 → 枢轴XY
      if (hasTensioner && hasArmAngleVal) {
        await calculatePivotXY()
      }
    } else if (mode === '3') {
      // 枢轴+张紧轮 → 臂长+角度
      if (hasPivot && hasTensioner) {
        await calculateArmAngle()
      }
    }
  } finally {
    setTimeout(() => {
      isAutoCalculating.value = false
    }, 50)
  }
}

// 手调张紧轮：根据起始点和结束点直线方程，由名义位置X计算Y，并自动填入表格张紧轮XY
function calcManualNominalY() {
  const manual = tensioner.value.manual
  const sx = manual.start_x, sy = manual.start_y
  const ex = manual.end_x, ey = manual.end_y
  const nx = manual.nominal_x

  if (sx == null || sy == null || ex == null || ey == null || nx == null) return

  // 如果起始点和结束点X坐标相同，直线为垂直线，Y无法由X确定
  if (Math.abs(ex - sx) < 1e-9) return

  // 直线方程：y - sy = ((ey - sy) / (ex - sx)) * (x - sx)
  const slope = (ey - sy) / (ex - sx)
  const ny = sy + slope * (nx - sx)
  manual.nominal_y = Number(ny.toFixed(2))

  // 自动将名义位置X和计算后的Y填入表格最后一行（张紧轮）
  if (tableData.value.length === 0) return
  const lastRow = tableData.value[tableData.value.length - 1]
  if (!lastRow) return
  lastRow.x = Number(nx.toFixed(2))
  lastRow.y = Number(ny.toFixed(2))
}

// 手调张紧轮：垂直线时，由名义位置Y计算X（X = start_x = end_x），并自动填入表格张紧轮XY
function calcManualNominalX() {
  const manual = tensioner.value.manual
  const sx = manual.start_x, sy = manual.start_y
  const ex = manual.end_x, ey = manual.end_y
  const ny = manual.nominal_y

  if (sx == null || sy == null || ex == null || ey == null || ny == null) return

  // 只有垂直线时才计算X
  if (Math.abs(ex - sx) >= 1e-9) return

  // 垂直线：X = start_x = end_x
  const nx = sx
  manual.nominal_x = Number(nx.toFixed(2))

  // 自动将计算后的X和名义位置Y填入表格最后一行（张紧轮）
  if (tableData.value.length === 0) return
  const lastRow = tableData.value[tableData.value.length - 1]
  if (!lastRow) return
  lastRow.x = Number(nx.toFixed(2))
  lastRow.y = Number(ny.toFixed(2))
}

// 监听手调张紧轮参数变化，自动计算名义位置Y并填入表格
watch(
  () => tensioner.value.manual,
  () => {
    calcManualNominalY()
  },
  { deep: true }
)

// 正向计算：枢轴XY + 臂长 + 角度 → 张紧轮XY（调用后端）
async function calculateTensionerXY() {
  if (tableData.value.length === 0) return

  const pivotX = tensioner.value.automatic.pivot_x
  const pivotY = tensioner.value.automatic.pivot_y
  const armLength = tensioner.value.automatic.arm_length
  const workAngle = tensioner.value.automatic.work_angle

  if (pivotX == null || pivotY == null || armLength == null || workAngle == null) return

  try {
    const res = await apiCalcTensionerCoord({
      pivot_x: Number(pivotX),
      pivot_y: Number(pivotY),
      arm_length: Number(armLength),
      work_angle: Number(workAngle)
    })
    const data = res.data || {}
    if (data.pulley_x == null || data.pulley_y == null) return

    const lastRow = tableData.value[tableData.value.length - 1]
    if (!lastRow) return

    lastRow.x = Number(Number(data.pulley_x).toFixed(2))
    lastRow.y = Number(Number(data.pulley_y).toFixed(2))
  } catch (e) {
    console.error('张紧轮坐标计算失败:', e)
  }
}

// 反向计算：张紧轮XY + 臂长 + 角度 → 枢轴XY（调用后端）
async function calculatePivotXY() {
  if (tableData.value.length === 0) return

  const lastRow = tableData.value[tableData.value.length - 1]
  if (!lastRow || lastRow.x == null || lastRow.y == null) return

  const armLength = tensioner.value.automatic.arm_length
  const workAngle = tensioner.value.automatic.work_angle

  if (armLength == null || workAngle == null) return

  try {
    const res = await apiCalcTensionerCoord({
      pulley_x: Number(lastRow.x),
      pulley_y: Number(lastRow.y),
      arm_length: Number(armLength),
      work_angle: Number(workAngle)
    })
    const data = res.data || {}
    if (data.pivot_x == null || data.pivot_y == null) return

    tensioner.value.automatic.pivot_x = Number(Number(data.pivot_x).toFixed(2))
    tensioner.value.automatic.pivot_y = Number(Number(data.pivot_y).toFixed(2))
  } catch (e) {
    console.error('枢轴坐标计算失败:', e)
  }
}

// 双向反推：枢轴XY + 张紧轮XY → 臂长 + 角度（调用后端）
async function calculateArmAngle() {
  if (tableData.value.length === 0) return

  const lastRow = tableData.value[tableData.value.length - 1]
  if (!lastRow || lastRow.x == null || lastRow.y == null) return

  const pivotX = tensioner.value.automatic.pivot_x
  const pivotY = tensioner.value.automatic.pivot_y

  if (pivotX == null || pivotY == null) return

  try {
    const res = await apiCalcTensionerCoord({
      pivot_x: Number(pivotX),
      pivot_y: Number(pivotY),
      pulley_x: Number(lastRow.x),
      pulley_y: Number(lastRow.y)
    })
    const data = res.data || {}
    if (data.arm_length == null || data.work_angle == null) return

    tensioner.value.automatic.arm_length = Number(Number(data.arm_length).toFixed(2))
    tensioner.value.automatic.work_angle = Number(Number(data.work_angle).toFixed(2))
  } catch (e) {
    console.error('臂长和角度计算失败:', e)
  }
}

function resetPivotArmData() {
  ElMessageBox.confirm('确定要重置枢轴与臂参数吗？此操作不可撤销。', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 重置枢轴参数
    tensioner.value.automatic.pivot_x = null
    tensioner.value.automatic.pivot_y = null
    // 重置臂长和工作角度
    tensioner.value.automatic.arm_length = null
    tensioner.value.automatic.work_angle = null
    // 重置计算模式
    calcMode.value = '1'
    ElMessage.success('已重置')
  }).catch(() => {})
}

function createRow() {
  return {
    name: '',
    code: '',
    x: null,
    y: null,
    flat_dia: null,
    groove_dia: null,
    type: 'groove',
    inertia: null,
    service_factor: null
  }
}

function addRow(index) {
  if (tableData.value.length >= 10) {
    ElMessage.warning('最多 10 个带轮')
    return
  }
  tableData.value.splice(index + 1, 0, createRow())
}

function removeRow(index) {
  if (tableData.value.length <= 1) {
    ElMessage.warning('至少保留一个带轮')
    return
  }
  ElMessageBox.confirm('确定要删除该带轮吗？', '提示', {
    type: 'warning',
    confirmButtonText: '确认',
    cancelButtonText: '取消'
  })
    .then(() => {
      tableData.value.splice(index, 1)
      ElMessage.success('删除成功')
    })
}

onMounted(async () => {
  try {
    const res = await api.getBeltOptions()
    beltOptions.value = res.data.belt_options
  } catch (err) {
    console.error('加载带轮失败', err)
  }
  try {
    const res = await api.getManufacturerOptions()
    manufacturerOptions.value = res.data.manufacturers
    if (beltParams.value.manufacturer) {
      const mfr = res.data.manufacturers.find(item => item.name === beltParams.value.manufacturer)
      if (mfr) {
        beltParams.value.flat_to_pitch = mfr.flat_to_pitch
        beltParams.value.pitch_to_effective = mfr.pitch_to_effective
        beltParams.value.height = mfr.height
      }
    }
  } catch (err) {
    console.error('加载厂家失败', err)
  }
  runAutoCalc()
})

function runAutoCalc() {
  if (tensioner.value.type !== 'automatic') return
  const mode = calcMode.value
  const pivotX = tensioner.value.automatic.pivot_x
  const pivotY = tensioner.value.automatic.pivot_y
  const armLen = tensioner.value.automatic.arm_length
  const workAng = tensioner.value.automatic.work_angle
  const lastRow = tableData.value.length > 0 ? tableData.value[tableData.value.length - 1] : null
  const hasT = lastRow && lastRow.x != null && lastRow.y != null
  const hasP = pivotX != null && pivotY != null
  const hasAA = armLen != null && workAng != null
  if (mode === '1' && hasP && hasAA) triggerCalc()
  else if (mode === '2' && hasT && hasAA) triggerCalc()
  else if (mode === '3' && hasP && hasT) triggerCalc()
}

const handleCodeChange = (val, row) => {
  const opt = beltOptions.value.find(item => item.code === val)
  if (opt) row.name = opt.name
}

const handleManufacturerChange = (val) => {
  const mfr = manufacturerOptions.value.find(item => item.name === val)
  if (mfr) {
    beltParams.value.flat_to_pitch = mfr.flat_to_pitch
    beltParams.value.pitch_to_effective = mfr.pitch_to_effective
    beltParams.value.height = mfr.height
  }
}

const goToCalculate = async () => {
  console.log('提交数据:', formInfo.value, tableData.value)
  try {
    const submitData = {
      info: formInfo.value,
      pulleys: tableData.value,
      tensioner: tensioner.value
    }
    const response = await api.calcPulleyDiagram(submitData)
    ElMessage.success('计算任务已提交')
    console.log('计算结果:', response.data)
  } catch (error) {
    console.error('计算失败:', error)
    ElMessage.error('计算任务提交失败')
  }
}
</script>

<style scoped>
/* ===== 调试信息 ===== */
.debug-section {
  margin-bottom: 20px;
}

.debug-title {
  font-size: 14px;
  font-weight: 600;
  color: #606266;
  margin-bottom: 10px;
}

.debug-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.debug-table th,
.debug-table td {
  border: 1px solid #e4e7ed;
  padding: 6px 8px;
  text-align: center;
}

.debug-table th {
  background: #f0f5ff;
  color: #606266;
  font-weight: 600;
}

.debug-table tbody tr:hover {
  background: #f8fafc;
}

/* ===== 页面整体 ===== */
.input-page {
  padding: 24px 0;
  max-width: 1600px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
}

/* ===== 页面标题 ===== */
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
  font-size: 22px;
  font-weight: 700;
  color: #1d2129;
  margin: 0;
}

.page-subtitle {
  font-size: 13px;
  color: #86909c;
  background: #f2f3f5;
  padding: 2px 10px;
  border-radius: 10px;
}

/* ===== 卡片通用 ===== */
.info-card,
.table-card,
.diagram-card,
.tensioner-card {
  margin-bottom: 20px;
  border-radius: 12px;
  border: none;
  transition: box-shadow 0.3s ease;
}

.info-card :deep(.el-card__body),
.table-card :deep(.el-card__body),
.diagram-card :deep(.el-card__body),
.tensioner-card :deep(.el-card__body) {
  padding: 20px 24px;
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
  margin-left: auto;
}

.type-tag {
  margin-left: 8px;
}

.tensioner-header-photo {
  margin-left: 12px;
  display: inline-flex;
  align-items: center;
}

.tensioner-header-photo img {
  height: 40px;
  width: auto;
  object-fit: contain;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid #e5e6eb;
}

/* ===== 基础信息表单 ===== */
.base-form :deep(.el-form-item__label) {
  font-size: 13px;
  font-weight: 500;
  color: #4e5969;
  padding-bottom: 4px;
}

.base-form :deep(.el-input__wrapper),
.base-form :deep(.el-input-number) {
  border-radius: 8px;
}

/* ===== 主内容区 ===== */
.main-content {
  display: flex;
  gap: 20px;
  margin-top: 0;
}

.left-section {
  flex: 2;
  min-width: 0;
}

.right-section {
  flex: 1;
  min-width: 400px;
}

/* ===== 表格 ===== */
.table-wrapper {
  width: 100%;
  overflow-x: auto;
}

.table-wrapper :deep(.el-table) {
  border-radius: 8px;
  overflow: visible;
}

:deep(.el-table th.el-table__cell) {
  background-color: #f0f5ff !important;
  color: #1d2129;
  font-weight: 600;
  font-size: 13px;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) {
  background: #fafbfc;
}

:deep(.el-table td.el-table__cell) {
  padding: 8px 0;
}

:deep(.el-table .el-input-number),
:deep(.el-table .el-input),
:deep(.el-table .el-select) {
  width: 100%;
}

:deep(.el-table .el-input__wrapper) {
  border-radius: 6px;
}

:deep(.el-table .el-input-number .el-input__wrapper) {
  border-radius: 6px;
}

.disabled-cell {
  color: #c9cdd4;
  font-size: 13px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.tooltip-header {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: help;
}

/* ===== 提交按钮 ===== */
.action-bar {
  text-align: center;
  padding: 16px 0 8px;
}

.submit-btn {
  min-width: 200px;
  height: 44px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 1px;
  background: linear-gradient(135deg, #409eff 0%, #337ecc 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.35);
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.45);
}

.submit-btn:active {
  transform: translateY(0);
}

/* ===== 张紧器表单 ===== */
.tensioner-form :deep(.el-form-item__label) {
  font-size: 13px;
  font-weight: 500;
  color: #4e5969;
  padding-bottom: 4px;
}

.tensioner-form :deep(.el-input__wrapper),
.tensioner-form :deep(.el-input-number) {
  border-radius: 8px;
}

/* 皮带参数 & 张紧器参数：所有输入框文字统一居中 */
.tensioner-form :deep(.el-input__inner) {
  text-align: center;
}
.tensioner-form :deep(.el-select .el-input__inner) {
  text-align: center;
}

.type-selector-row {
  padding-bottom: 8px;
  border-bottom: 1px dashed #e5e6eb;
  margin-bottom: 16px;
}

.type-radio-group {
  width: 100%;
}

.type-radio-group :deep(.el-radio-button__inner) {
  border-radius: 8px !important;
  border: none !important;
  box-shadow: none !important;
  padding: 8px 16px;
}

.type-radio-group :deep(.el-radio-button:first-child .el-radio-button__inner) {
  border-radius: 8px !important;
}

.type-radio-group :deep(.el-radio-button:last-child .el-radio-button__inner) {
  border-radius: 8px !important;
}

/* 参数分组 */
.param-section {
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #fafbfc;
  border-radius: 10px;
  border: 1px solid #f0f0f0;
}

.param-section:last-child {
  margin-bottom: 0;
}

.reset-btn-form-item {
  margin-bottom: 18px;
}

.reset-btn-form-item :deep(.el-form-item__content) {
  line-height: 32px;
  padding-top: 34px;
}

.reset-pivot-btn {
  width: 100%;
  height: 32px;
  line-height: 30px;
  padding: 0 15px;
  border-radius: 6px;
  font-size: 14px;
  margin: 0;
  box-sizing: border-box;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.param-section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e8ecf1;
}

/* ===== 张紧器示意图 ===== */
.tensioner-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 80px;
  background: #f5f7fa;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  padding: 4px;
}

.tensioner-preview-title {
  font-size: 11px;
  color: #909399;
  margin-bottom: 2px;
}

.tensioner-inline-photo {
  display: inline-flex;
  align-items: center;
  margin-left: 8px;
  vertical-align: middle;
}

.tensioner-inline-photo img {
  height: 56px;
  width: auto;
  object-fit: contain;
  border-radius: 4px;
  cursor: pointer;
}

.type-with-img {
  display: flex;
  align-items: center;
}

.tensioner-img {
  width: 100%;
  max-height: 100px;
  object-fit: contain;
  border-radius: 6px;
}

.tensioner-svg {
  width: 100%;
  max-width: 120px;
  height: auto;
}

/* ===== 计算模式选择器 ===== */
.calc-mode-selector {
  margin-bottom: 16px;
}

.calc-mode-label {
  font-size: 13px;
  font-weight: 500;
  color: #4e5969;
  margin-bottom: 10px;
}

.calc-mode-options {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.calc-mode-card {
  flex: 1;
  min-width: 220px;
  max-width: 280px;
  padding: 16px 18px;
  background: #ffffff;
  border-radius: 12px;
  border: 2px solid #e4e7ed;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  position: relative;
  overflow: hidden;
}

.calc-mode-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: transparent;
  transition: background 0.3s ease;
}

.calc-mode-card:hover:not(.disabled) {
  border-color: #c0c4cc;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.calc-mode-card.active {
  border-color: #409eff;
  background: #f0f5ff;
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.15);
}

.calc-mode-card.active::before {
  background: linear-gradient(90deg, #409eff, #66b1ff);
}

.calc-mode-card.disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.mode-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.mode-icon-wrapper svg {
  width: 22px;
  height: 22px;
  color: #ffffff;
}

.mode-icon-wrapper.blue {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
}

.mode-icon-wrapper.green {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.mode-icon-wrapper.purple {
  background: linear-gradient(135deg, #909399 0%, #b4bccc 100%);
}

.calc-mode-card.active .mode-icon-wrapper {
  transform: scale(1.1);
}

.mode-title {
  font-size: 14px;
  font-weight: 600;
  color: #1d2129;
  margin-top: 4px;
}

.mode-desc {
  font-size: 12px;
  color: #86909c;
  text-align: center;
  line-height: 1.5;
}

.calc-mode-card.active .mode-title {
  color: #409eff;
}

/* ===== 响应式 ===== */
@media (max-width: 1400px) {
  .main-content {
    flex-direction: column;
  }

  .right-section {
    width: 100%;
    min-width: auto;
  }
}

/* 平板 */
@media (max-width: 1024px) {
  .input-page {
    padding: 16px 20px;
  }

  .page-title {
    font-size: 18px;
  }

  .info-card :deep(.el-card__body),
  .table-card :deep(.el-card__body),
  .diagram-card :deep(.el-card__body),
  .tensioner-card :deep(.el-card__body) {
    padding: 16px;
  }

  .type-with-img {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .tensioner-inline-photo img {
    height: 48px;
  }
}

/* 手机 */
@media (max-width: 768px) {
  .input-page {
    padding: 12px;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 16px;
    padding-bottom: 12px;
  }

  .page-title {
    font-size: 16px;
  }

  .page-subtitle {
    font-size: 11px;
  }

  .info-card :deep(.el-card__body),
  .table-card :deep(.el-card__body),
  .diagram-card :deep(.el-card__body),
  .tensioner-card :deep(.el-card__body) {
    padding: 12px;
  }

  /* 基础信息表单：单列 */
  .base-form .el-row .el-col {
    width: 100% !important;
    flex: 0 0 100% !important;
    max-width: 100% !important;
  }

  /* 主内容区：单列 */
  .main-content {
    flex-direction: column;
    gap: 12px;
  }

  .left-section,
  .right-section {
    flex: 1 1 100%;
    min-width: auto;
    width: 100%;
  }

  /* 表格横向滚动 */
  .table-wrapper {
    overflow-x: auto;
  }

  .table-wrapper :deep(.el-table) {
    min-width: 600px;
  }

  /* 张紧器参数：单列 */
  .tensioner-form .el-row .el-col {
    width: 100% !important;
    flex: 0 0 100% !important;
    max-width: 100% !important;
  }

  .type-selector-row {
    flex-direction: column;
  }

  .type-with-img {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .type-radio-group :deep(.el-radio-button__inner) {
    padding: 6px 10px;
    font-size: 12px;
  }

  .tensioner-preview {
    min-height: 60px;
    margin-top: 8px;
  }

  .tensioner-svg {
    max-width: 100px;
  }

  .param-section {
    padding: 10px 12px;
  }

  .param-section-title {
    font-size: 12px;
    margin-bottom: 8px;
    padding-bottom: 6px;
  }

  /* 示意图缩放 */
  .diagram-card :deep(.el-card__body) {
    padding: 8px;
  }

  /* 提交按钮 */
  .submit-btn {
    min-width: 160px;
    height: 40px;
    font-size: 13px;
  }

  .action-bar {
    padding: 12px 0 4px;
  }
}

/* 小屏手机 */
@media (max-width: 480px) {
  .input-page {
    padding: 8px;
  }

  .page-title {
    font-size: 15px;
  }

  .header-icon {
    width: 22px;
    height: 22px;
  }

  .card-header {
    font-size: 13px;
  }

  .card-icon {
    width: 15px;
    height: 15px;
  }

  .tensioner-header-photo img {
    height: 30px;
  }

  .info-card :deep(.el-card__body),
  .table-card :deep(.el-card__body),
  .diagram-card :deep(.el-card__body),
  .tensioner-card :deep(.el-card__body) {
    padding: 10px;
  }

  .base-form :deep(.el-form-item__label),
  .tensioner-form :deep(.el-form-item__label) {
    font-size: 12px;
  }

  .param-section {
    padding: 8px;
  }

  .param-section-title {
    font-size: 11px;
  }

  .submit-btn {
    min-width: 140px;
    height: 36px;
    font-size: 12px;
  }
}
</style>
