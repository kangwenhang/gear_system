gear_system/                # 项目根目录
│
├── frontend/               # ✅ 前端（Vue 3）
│   ├── public/
│   ├── src/
│   │   ├── api/            # 请求后端接口
│   │   │   └── gear.js
│   │   ├── views/          # 页面
│   │   │   ├── InputPage.vue
│   │   │   ├── ResultPage.vue
│   │   │   └── LayoutPage.vue
│   │   ├── components/     # 公共组件
│   │   ├── utils/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
├── backend/                # ✅ 后端（Python + venv）
│   ├── venv/               # Python 虚拟环境
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # 入口
│   │   ├── api/
│   │   │   └── calculate.py # 接口定义
│   │   ├── services/       # ✅ 公式 / 计算逻辑（核心）
│   │   │   ├── gear_base.py
│   │   │   ├── alignment.py
│   │   │   ├── vibration.py
│   │   │   ├── analysis.py
│   │   │   └── report.py
│   │   └── schemas/        # 输入输出数据结构
│   │       ├── input.py
│   │       └── output.py
│   ├── requirements.txt
│   └── README.md
│
└── docs/                  # 可选：说明文档