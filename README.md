# Gear System - 轮系设计系统

基于 Python FastAPI + Vue3 的皮带轮系设计与分析系统。

## 功能特性

- **轮系布局设计**：可视化添加、编辑带轮参数，支持槽轮(Grooved)和平轮(Flat)
- **皮带选型**：多种皮带型号(CR/EPDM)支持，自动计算有效长度
- **几何计算**：节圆直径、切点角、包角、包角平分线等参数计算
- **张紧器计算**：支持自动/手调张紧轮，枢轴坐标与臂长角度双向反推
- **张力/扭矩换算**：力臂计算、合力(Hubload)计算、扭矩与张力互转
- **对齐度分析**：Contact参数(K/J/L/M/N/P/O/Q/U)、BEA/Twist/Offset计算
- **振动分析**：振动频率与稳定性分析
- **调试信息**：实时显示张紧轮几何参数、力值换算过程
- **报告生成**：导出设计报告

## 技术栈

### 后端
- Python 3.10+
- FastAPI 0.139+
- Uvicorn
- NumPy / SciPy

### 前端
- Vue 3 + Vite 5
- Element Plus
- ECharts（图表可视化）
- Lucide Vue（图标）

### 桌面应用
- PyWebView
- PyInstaller

## 快速开始

### 开发模式

```bash
# 安装后端依赖
cd backend
pip install -r requirements.txt

# 启动后端（端口 8000）
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 安装前端依赖
cd frontend
npm install

# 启动前端（端口 5173，带热更新）
npm run dev
```

访问 http://localhost:5173 查看前端页面。

### 生产模式

```bash
# 构建前端
cd frontend
npm run build

# 复制构建产物到后端
cp -r dist ../backend/frontend_dist

# 启动后端（同时提供前端静态文件）
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000 查看应用。

### 启动脚本

```bash
# Linux / macOS
./start.sh start

# Windows
start.bat
```

## 项目结构

```
gear_system/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API 路由
│   │   │   ├── alignment.py   # 对齐度计算 (Contact参数/BEA/Twist/Offset)
│   │   │   ├── belts.py       # 皮带管理接口
│   │   │   └── calculate.py   # 通用计算接口
│   │   ├── services/          # 业务逻辑服务
│   │   │   ├── alignment.py   # 对齐度计算逻辑
│   │   │   ├── analysis.py    # 受力分析 (功率分配/圆周力/带段拉力)
│   │   │   ├── gear_base.py   # 基础轮系计算 (节圆/切点/包角)
│   │   │   ├── report.py      # 报告生成
│   │   │   └── vibration.py   # 振动分析
│   │   ├── data/              # 数据文件（CSV/JSON）
│   │   ├── schemas/           # 数据模型
│   │   └── main.py            # 应用入口
│   ├── frontend_dist/         # 前端构建产物
│   ├── requirements.txt       # Python 依赖
│   └── desktop_app.py         # 桌面应用入口
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── components/        # 公共组件
│   │   │   └── PulleyDiagram.vue  # 轮系布局图 (SVG渲染/悬停tooltip)
│   │   ├── views/             # 页面组件
│   │   │   ├── AlignmentPage.vue  # 对齐度页面
│   │   │   ├── InputPage.vue      # 参数输入页面 (几何/张紧器/皮带/调试)
│   │   │   └── ResultPage.vue     # 结果页面
│   │   ├── api/               # API 调用封装
│   │   │   └── pulley.js      # 前后端计算接口
│   │   └── store/             # 状态管理 (Vuex/Pinia)
│   │       └── shared.js      # 共享数据 (带轮/皮带参数/Contact结果)
│   └── package.json           # Node.js 依赖
├── .github/workflows/         # CI/CD 配置
├── 轮系计算公式手册.md          # 公式与代码映射文档
├── README.md
└── start.sh                   # 启动脚本
```

## API 文档

启动后端后，访问 http://localhost:8000/docs 查看 Swagger API 文档。

## 桌面应用打包

```bash
cd backend
pyinstaller GearSystem.spec
```

## 许可证

MIT License