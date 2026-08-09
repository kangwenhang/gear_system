<template>
  <div class="project-page">
    <div class="page-toolbar">
      <h2>项目管理</h2>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input v-model="searchKeyword" placeholder="搜索文件编号/客户/项目代码..." clearable
        style="width:360px" @keyup.enter="doSearch" @clear="doSearch">
        <template #prefix>
          <svg style="width:14px;height:14px" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </template>
      </el-input>
      <el-button @click="doSearch">搜索</el-button>
      <el-button type="success" @click="$emit('new-project')" style="margin-left:auto">新建轮系</el-button>
    </div>

    <!-- 项目列表 -->
    <div v-loading="loading" class="project-list">
      <el-empty v-if="!loading && projects.length === 0" description="暂无项目，请先保存" />
      <el-table v-else :data="projects" stripe border style="width:100%">
        <el-table-column label="文件编号" width="115">
          <template #default="{ row }">
            <span style="font-weight:600;color:#303133">{{ row.file_no }}</span>
          </template>
        </el-table-column>
        <el-table-column label="轮系层" width="90" align="center">
          <template #default="{ row }">
            <span>{{ row.layers || '--' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="版本" width="90" align="center">
          <template #default="{ row }">
            <el-select v-model="row.selectedVersion" size="small" style="width:65px"
              @change="(v) => onVersionChange(row, v)">
              <el-option v-for="v in row.versions" :key="v" :label="v" :value="v"/>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="customer" label="客户" width="100" />
        <el-table-column prop="displayName" label="文件名称" min-width="280">
          <template #default="{ row }">{{ row.displayName || '--' }}</template>
        </el-table-column>
        <el-table-column prop="date_modified" label="修改日期" width="120" align="center" />
        <el-table-column label="备注" min-width="200">
          <template #default="{ row }">
            <el-popover
              placement="top-start"
              :width="280"
              trigger="manual"
              v-model:visible="row.notesEditing"
            >
              <template #reference>
                <span :class="['notes-text', !row.notes && 'notes-empty']" @click="startEditNotes(row)">
                  {{ row.notes || '点击添加备注' }}
                </span>
              </template>
              <div style="padding: 4px">
                <el-input
                  v-model="row.notesDraft"
                  type="textarea"
                  :rows="3"
                  placeholder="输入备注内容"
                  maxlength="200"
                  show-word-limit
                />
                <div style="margin-top: 8px; text-align: right; display: flex; gap: 8px; justify-content: flex-end">
                  <el-button size="small" @click="cancelEditNotes(row)">取消</el-button>
                  <el-button size="small" type="primary" :loading="row.notesSaving" @click="saveNotes(row)">保存</el-button>
                </div>
              </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" align="center" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="handleLoad(row)">加载</el-button>
            <el-button size="small" type="success" link @click="handleExport(row)">导出</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页 -->
    <div v-if="total > pageSize" class="pagination">
      <el-pagination v-model:current-page="currentPage" :page-size="pageSize"
        :total="total" layout="prev, pager, next" @current-change="doSearch" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { sharedStore } from '../store/shared.js'
import { listProjects, getProjectByFile, deleteProject, exportProject, updateProject } from '../api/pulley.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const emit = defineEmits(['load-project', 'new-project'])

const props = defineProps({
  visible: { type: Boolean, default: false }
})

// 搜索
const searchKeyword = ref('')

// 列表
const loading = ref(false)
const projects = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = 20

onMounted(async () => {
  await doSearch()
})

watch(() => props.visible, (v) => {
  if (v) doSearch()
})

async function doSearch() {
  loading.value = true
  try {
    const res = await listProjects({
      keyword: searchKeyword.value,
      limit: pageSize,
      offset: (currentPage.value - 1) * pageSize
    })
    const items = (res.data.projects || []).map(p => {
      const initialVer = p.versions?.[0] || p.version || '01'
      const detail = p.version_details?.[initialVer] || {}
      // 构建文件名称: FEAD-机型-轮系层-皮带PK数-皮带类型-皮带总长
      const project = (detail.project_code || p.project_code || '').replace(/^FEAD-?/i, '')
      const layers = detail.layers || ''
      const ribs = detail.ribs || ''
      const cord = detail.cord_material || ''
      const effLength = detail.effective_length ? Math.round(detail.effective_length) : ''
      const parts = [project, layers].filter(Boolean)
      const beltDesc = [ribs + 'PK', cord, effLength].filter(p => p && p !== 'PK').join('-')
      const displayName = parts.length || beltDesc ? `FEAD-${parts.join('-')}-${beltDesc}`.replace(/^-+|-+$/g, '').replace(/--+/g, '-') : (detail.name || p.name || '')
      return {
        ...p,
        selectedVersion: initialVer,
        displayName,
        layers: detail.layers ?? '',
        name: detail.name ?? p.name,
        date_modified: detail.date_modified ?? p.date_modified,
        notes: detail.notes ?? p.notes ?? ''
      }
    })
    projects.value = items
    total.value = res.data.total || 0
  } catch (e) {
    ElMessage.error('搜索失败')
  } finally {
    loading.value = false
  }
}

async function handleLoad(row) {
  const ver = row.selectedVersion || row.versions?.[0] || '01'
  try {
    const res = await getProjectByFile(row.file_no, ver)
    const data = res.data
    if (data.form_info) Object.assign(sharedStore.formInfo, data.form_info)
    if (data.pulleys) {
      sharedStore.pulleys.splice(0, sharedStore.pulleys.length)
      data.pulleys.forEach(p => sharedStore.pulleys.push(p))
    }
    if (data.belt_params) Object.assign(sharedStore.beltFullParams, data.belt_params)
    if (data.tensioner) Object.assign(sharedStore.tensioner, data.tensioner)
    ElMessage.success(`已加载: ${row.file_no} v${ver}`)
    emit('load-project')
  } catch (e) {
    ElMessage.error('加载失败')
  }
}

// 切换版本：从 version_details 直接同步元数据（无需额外 API 请求）
function onVersionChange(row, ver) {
  row.selectedVersion = ver
  const detail = row.version_details?.[ver]
  if (!detail) return
  row.name = detail.name ?? row.name
  row.date_modified = detail.date_modified ?? row.date_modified
  row.notes = detail.notes ?? ''
  row.layers = detail.layers ?? ''
  // 重新构建 displayName
  const project = (detail.project_code || row.project_code || '').replace(/^FEAD-?/i, '')
  const layers = detail.layers || ''
  const ribs = detail.ribs || ''
  const cord = detail.cord_material || ''
  const effLength = detail.effective_length ? Math.round(detail.effective_length) : ''
  const parts = [project, layers].filter(Boolean)
  const beltDesc = [ribs + 'PK', cord, effLength].filter(p => p && p !== 'PK').join('-')
  row.displayName = parts.length || beltDesc ? `FEAD-${parts.join('-')}-${beltDesc}`.replace(/^-+|-+$/g, '').replace(/--+/g, '-') : (detail.name || row.name || '')
  // 触发表格响应式更新
  row._tick = (row._tick || 0) + 1
}

// ===== 备注编辑 =====
function startEditNotes(row) {
  row.notesDraft = row.notes || ''
  row.notesEditing = true
}

function cancelEditNotes(row) {
  row.notesEditing = false
  row.notesDraft = ''
}

async function saveNotes(row) {
  const ver = row.selectedVersion || row.versions?.[0] || '01'
  const id = row.ids?.[ver]
  if (!id) { ElMessage.error('该版本不存在'); return }
  const newNotes = (row.notesDraft || '').trim()
  if (newNotes === (row.notes || '')) {
    row.notesEditing = false
    return
  }
  row.notesSaving = true
  try {
    await updateProject(id, { notes: newNotes })
    row.notes = newNotes
    row.notesEditing = false
    ElMessage.success('备注已保存')
  } catch (e) {
    ElMessage.error('保存失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    row.notesSaving = false
  }
}

async function handleExport(row) {
  const ver = row.selectedVersion || row.versions?.[0] || '01'
  const id = row.ids?.[ver]
  if (!id) { ElMessage.error('该版本不存在'); return }
  try {
    const [projRes, exportRes] = await Promise.all([
      getProjectByFile(row.file_no, ver),
      exportProject(id)
    ])
    const data = projRes.data

    // 构建导出文件名：文件编号-版本(FEAD-机型-轮系层-皮带PK数-皮带类型-皮带总长)
    const fi = data.form_info || {}
    const bp = data.belt_params || {}
    const project = fi.project || ''
    const layers = fi.layers || ''
    const ribs = bp.ribs || bp.rib_type?.replace('PK','') || ''
    const cord = bp.cord_material || bp.belt_material || ''
    const effLength = bp.effective_length ? Math.round(bp.effective_length) : ''

    const parts = ['FEAD', project, layers]
      .filter(p => p !== '' && p != null)
    const beltDesc = [ribs + 'PK', cord, effLength]
      .filter(p => p !== '' && p != null && p !== 'PK')
      .join('-')

    const filename = `${row.file_no}-${ver}(${parts.join('-')}-${beltDesc}).xlsx`
      .replace(/[\\/:*?"<>|]/g, '_')

    const url = window.URL.createObjectURL(new Blob([exportRes.data]))
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (e) {
    ElMessage.error('导出失败')
  }
}

async function handleDelete(row) {
  const ver = row.selectedVersion || row.versions?.[0] || '01'
  const id = row.ids?.[ver]
  if (!id) { ElMessage.error('该版本不存在'); return }
  try {
    await ElMessageBox.confirm(`确定删除 "${row.file_no}" (v${ver})？`, '确认删除', {
      type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消'
    })
    await deleteProject(id)
    ElMessage.success('已删除')
    await doSearch()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}
</script>

<style scoped>
.project-page {
  padding: 24px 32px;
  max-width: 1100px;
  margin: 0 auto;
}
.page-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-toolbar h2 {
  font-size: 22px;
  color: #303133;
  margin: 0;
}
.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: center;
}
.project-list {
  min-height: 300px;
}
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
.notes-text {
  display: inline-block;
  max-width: 100%;
  color: #303133;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
  transition: background 0.15s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  vertical-align: middle;
}
.notes-text:hover {
  background: #f0f7ff;
  color: #409eff;
}
.notes-empty {
  color: #c0c4cc;
  font-style: italic;
}
.notes-empty:hover {
  color: #409eff;
  background: #f0f7ff;
}
</style>
