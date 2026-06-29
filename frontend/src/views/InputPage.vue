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
                      @change="onTableXYChange"
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
                      @change="onTableXYChange"
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
          <PulleyDiagram :data="tableData" :tensionerData="tensioner" />
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
            <el-row :gutter="16">
              <el-col :span="4">
                <el-form-item label="枢轴 X">
                  <el-input-number v-model="tensioner.automatic.pivot_x" :precision="2" :controls="false" style="width:100%" placeholder="--" :disabled="disablePivotXY" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="枢轴 Y">
                  <el-input-number v-model="tensioner.automatic.pivot_y" :precision="2" :controls="false" style="width:100%" placeholder="--" :disabled="disablePivotXY" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="臂长(mm)">
                  <el-input-number v-model="tensioner.automatic.arm_length" :precision="2" :controls="false" style="width:100%" placeholder="--" :disabled="disableArmAngle" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="工作角度(°)">
                  <el-input-number v-model="tensioner.automatic.work_angle" :precision="2" :controls="false" style="width:100%" placeholder="--" :disabled="disableArmAngle" :min="0" :max="360" />
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-form-item label="枢轴端大小(mm)">
                  <el-input-number v-model="tensioner.automatic.head_size" :precision="2" :controls="false" style="width:100%" placeholder="--" />
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

  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, watchEffect } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import PulleyDiagram from '@/components/PulleyDiagram.vue'

import api from '../api/pulley.js'
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
  belt_type: '',
  manufacturer: '',
  belt_pk: '',
  elongation_rate: null,
  length_tolerance: '',
  life_coefficient: null,
  flat_to_pitch: null,
  pitch_to_effective: null,
  height: null
})

const tensioner = ref({
  type: 'automatic',
  automatic: {
    rotation: 'cw',
    pivot_x: null,
    pivot_y: null,
    arm_length: null,
    work_angle: null,
    spring_stiffness: null,
    valueType: 'tension',
    torque: null,
    tension_value: null,
    damping: null,
    nominal_angle: null,
    stroke: null,
    head_size: null
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

// 带轮参数中张紧轮是否已输入XY坐标
const hasTensionerXY = ref(false)
const hasPivotXY = ref(false)
const hasArmAngle = ref(false)
// 标记表格XY是否由自动计算填入（而非用户手动输入）
const isAutoCalculatedXY = ref(false)

// 计算禁用状态 - 只有用户手动输入表格XY时才互斥
const disablePivotXY = computed(() => {
  return hasArmAngle.value && hasTensionerXY.value && !isAutoCalculatedXY.value
})

const disableArmAngle = computed(() => {
  return hasPivotXY.value && hasTensionerXY.value && !isAutoCalculatedXY.value
})

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
const tableData = ref([createRow(), createRow()])

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
  () => tableData.value.map(p => ({ code: p.code, name: p.name, flat_dia: p.flat_dia, groove_dia: p.groove_dia, type: p.type })),
  (newPulleys) => {
    sharedStore.pulleys.splice(0, sharedStore.pulleys.length, ...newPulleys.filter(p => p.code))
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

// 监听表格数据变化，检测张紧轮XY
function checkTensionerXY() {
  const lastRow = tableData.value[tableData.value.length - 1]
  hasTensionerXY.value = !!(lastRow && lastRow.x != null && lastRow.y != null)
}

// 用户手动修改表格XY时，清除自动计算标志，恢复互斥逻辑
function onTableXYChange() {
  isAutoCalculatedXY.value = false
  checkTensionerXY()
}

// 监听臂长和角度变化，但不触发自动计算
watch([() => tensioner.value.automatic.arm_length, () => tensioner.value.automatic.work_angle], 
() => {
  // 只有当有用户手动输入时才计算
  if (tensioner.value.automatic.arm_length != null && tensioner.value.automatic.work_angle != null) {
    calculateTensionerXY()
  }
}, { deep: true })

// 监听枢轴XY
watchEffect(() => {
  hasPivotXY.value = tensioner.value.automatic.pivot_x != null && tensioner.value.automatic.pivot_y != null
})

// 监听枢轴XY变化，但不触发自动计算
watch([() => tensioner.value.automatic.pivot_x, () => tensioner.value.automatic.pivot_y], 
() => {
  // 只有当有用户手动输入时才计算
  if (tensioner.value.automatic.pivot_x != null && tensioner.value.automatic.pivot_y != null) {
    // 如果臂长和角度也都有值，则计算
    if (tensioner.value.automatic.arm_length != null && tensioner.value.automatic.work_angle != null) {
      calculateTensionerXY()
    }
  }
})

// 监听臂长+工作角度
watchEffect(() => {
  hasArmAngle.value = tensioner.value.automatic.arm_length != null && tensioner.value.automatic.work_angle != null
})

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
  isAutoCalculatedXY.value = true
  lastRow.x = Number(nx.toFixed(2))
  lastRow.y = Number(ny.toFixed(2))
  checkTensionerXY()
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
  isAutoCalculatedXY.value = true
  lastRow.x = Number(nx.toFixed(2))
  lastRow.y = Number(ny.toFixed(2))
  checkTensionerXY()
}

// 监听手调张紧轮参数变化，自动计算名义位置Y并填入表格
watch(
  () => tensioner.value.manual,
  () => {
    calcManualNominalY()
  },
  { deep: true }
)

// 计算张紧轮坐标
function calculateTensionerXY() {
  // 确保表格中有数据
  if (tableData.value.length === 0) return
  
  const pivotX = tensioner.value.automatic.pivot_x
  const pivotY = tensioner.value.automatic.pivot_y
  const armLength = tensioner.value.automatic.arm_length
  const workAngle = tensioner.value.automatic.work_angle
  
  // 确保所有参数都有值
  if (pivotX == null || pivotY == null || armLength == null || workAngle == null) return
  
  // 角度转换为弧度（三角函数使用弧度）
  const angleRad = workAngle * Math.PI / 180
  
  // 计算皮带轮坐标
  const pulleyX = pivotX + armLength * Math.cos(angleRad)
  const pulleyY = pivotY + armLength * Math.sin(angleRad)
  
  // 获取表格最后一行（张紧轮）
  const lastRow = tableData.value[tableData.value.length - 1]
  if (!lastRow) return
  
  // 标记为自动计算，避免触发互斥逻辑
  isAutoCalculatedXY.value = true
  
  // 更新表格数据
  lastRow.x = Number(pulleyX.toFixed(2))
  lastRow.y = Number(pulleyY.toFixed(2))
  
  // 触发检测
  checkTensionerXY()
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
  } catch (err) {
    console.error('加载厂家失败', err)
  }
})

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
