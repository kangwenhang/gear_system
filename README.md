# Gear System - 轮系设计工具

一个面向发动机前端轮系设计的桌面应用，提供皮带轮布局设计、受力分析、振动计算等功能。

## 功能特性

- **轮系布局设计**：可视化配置皮带轮位置、直径、类型等参数
- **张紧轮选型**：支持自动张紧轮和手动张紧轮的选型与配置
- **受力分析**：计算各皮带轮的受力情况
- **振动分析**：轮系振动特性计算
- **对中分析**：皮带轮对中偏差计算
- **报告生成**：自动生成设计报告
- **数据导入导出**：支持 CSV 格式的皮带轮和皮带数据管理
- **跨平台**：支持 Windows 和 Linux 桌面应用

## 技术栈

### 后端
- Python 3.9+
- FastAPI - Web API 框架
- SciPy / NumPy - 科学计算
- PyWebView - 桌面应用容器
- PyInstaller - 应用打包

### 前端
- Vue 3 - 前端框架
- Element Plus - UI 组件库
- Vite - 构建工具
- Vue Router - 路由管理
- Axios - HTTP 客户端

## 项目结构

```
gear_system/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API 接口
│   │   │   ├── belts.py    # 皮带轮数据管理
│   │   │   └── calculate.py # 计算接口
│   │   ├── services/       # 业务逻辑服务
│   │   ├── schemas/        # 数据模型
│   │   ├── data/           # 数据文件 (CSV)
│   │   └── main.py         # 应用入口
│   ├── frontend_dist/      # 前端构建产物
│   ├── desktop_app.py      # 桌面应用启动入口
│   ├── GearSystem.spec     # PyInstaller 配置
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端源码
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 公共组件
│   │   ├── api/            # API 封装
│   │   └── store/          # 状态管理
│   └── package.json
├── .github/
│   └── workflows/
│       └── build-desktop.yml  # GitHub Actions 自动构建
├── build.sh                # Linux 构建脚本
├── build_windows.bat       # Windows 构建脚本
└── README.md
```

## 快速开始

### 开发环境

#### 前置要求
- Python 3.9+
- Node.js 16+
- npm 或 yarn

#### 后端开发

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 文档将在 http://localhost:8000/docs 可用。

#### 前端开发

```bash
cd frontend
npm install
npm run dev
```

前端开发服务器将在 http://localhost:5173 启动。

### 数据文件

应用使用 CSV 格式存储皮带轮和皮带数据，文件位于应用运行目录的 `data/` 文件夹中：

- `pulleys.csv` - 皮带轮数据
- `belts.csv` - 皮带数据

首次运行时，如果数据文件不存在，应用会自动创建默认数据文件。
你可以使用 Excel 或任何文本编辑器直接修改这些 CSV 文件，支持 UTF-8、GBK、GB2312 等多种编码格式。

## 打包构建

### Linux 构建

```bash
chmod +x build.sh
./build.sh
```

### Windows 构建

```cmd
build_windows.bat
```

构建完成后，可执行文件位于 `backend/dist/` 目录。

### GitHub Actions 自动构建

项目配置了 GitHub Actions 工作流，推送标签时会自动触发多平台构建并发布 Release。

触发方式：
```bash
git tag v0.x.x
git push origin v0.x.x
```

工作流会自动构建 Windows 和 Linux 版本并上传到 Release。

## API 接口

### 数据管理

- `GET /api/pulleys` - 获取皮带轮列表
- `POST /api/pulleys` - 保存皮带轮数据
- `GET /api/belts` - 获取皮带列表
- `POST /api/belts` - 保存皮带数据
- `GET /api/data-info` - 查看数据目录和文件状态（调试用）

### 计算接口

- `POST /api/calculate` - 执行轮系计算

## License

MIT
