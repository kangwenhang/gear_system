#!/bin/bash

# gear_system Linux 启动脚本
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$BASE_DIR/backend"
FRONTEND_DIR="$BASE_DIR/frontend"
LOG_DIR="$BASE_DIR/logs"
PID_FILE="$BASE_DIR/.run_pids"
BACKEND_PORT=8000
FRONTEND_PORT=5173

# Python 虚拟环境路径
VENV_DIR="$BACKEND_DIR/venv"
PYTHON="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"

mkdir -p "$LOG_DIR"

# 检查并释放端口
free_port() {
    local port=$1
    local name=$2
    local pid=$(lsof -ti :$port 2>/dev/null || ss -tlnp 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d',' -f2 | cut -d'=' -f2 | head -1)
    if [ -n "$pid" ]; then
        echo -e "\033[33m$name port $port is occupied by PID $pid, killing...\033[0m"
        kill -9 $pid 2>/dev/null
        sleep 1
    fi
}

case "$1" in
    start)
        # 先释放端口
        free_port $BACKEND_PORT "Backend"
        free_port $FRONTEND_PORT "Frontend"

        # ===== 后端 =====
        echo -e "\033[36mChecking backend environment...\033[0m"
        cd "$BACKEND_DIR"

        # 1. 创建虚拟环境（如果不存在）
        if [ ! -d "$VENV_DIR" ]; then
            echo -e "\033[33mCreating Python virtual environment...\033[0m"
            python3 -m venv "$VENV_DIR"
            if [ $? -ne 0 ]; then
                echo -e "\033[31mFailed to create virtual environment!\033[0m"
                exit 1
            fi
        fi

        # 2. 确保虚拟环境可用
        if [ ! -f "$PYTHON" ]; then
            echo -e "\033[31mVirtual environment is broken. Please delete $VENV_DIR and retry.\033[0m"
            exit 1
        fi

        # 3. 安装 Python 依赖
        echo -e "\033[36mInstalling Python dependencies...\033[0m"
        "$PIP" install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo -e "\033[31mFailed to install Python dependencies!\033[0m"
            exit 1
        fi

        echo -e "\033[36mStarting backend...\033[0m"
        nohup "$PYTHON" -m uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload > "$LOG_DIR/backend.log" 2>&1 &
        BACKEND_PID=$!

        # ===== 前端 =====
        echo -e "\033[36mChecking frontend dependencies...\033[0m"
        cd "$FRONTEND_DIR"

        if [ ! -d "node_modules" ] || [ ! -f "node_modules/.bin/vite" ]; then
            echo -e "\033[33mDependencies not found, running npm install...\033[0m"
            npm install
            if [ $? -ne 0 ]; then
                echo -e "\033[31mnpm install failed!\033[0m"
                exit 1
            fi
        fi

        echo -e "\033[36mStarting frontend...\033[0m"
        nohup npx vite --host 0.0.0.0 --port $FRONTEND_PORT > "$LOG_DIR/frontend.log" 2>&1 &
        FRONTEND_PID=$!

        echo "$BACKEND_PID $FRONTEND_PID" > "$PID_FILE"
        echo -e "\033[32mDone!\033[0m"
        echo "Backend:  http://localhost:$BACKEND_PORT"
        echo "Frontend: http://localhost:$FRONTEND_PORT"
        echo "Logs:     $LOG_DIR"
        ;;
    stop)
        echo -e "\033[33mStopping...\033[0m"
        if [ -f "$PID_FILE" ]; then
            read BACKEND_PID FRONTEND_PID < "$PID_FILE"
            kill $BACKEND_PID 2>/dev/null
            kill $FRONTEND_PID 2>/dev/null
            rm -f "$PID_FILE"
        fi
        echo -e "\033[32mStopped.\033[0m"
        ;;
    status)
        if [ -f "$PID_FILE" ]; then
            read BACKEND_PID FRONTEND_PID < "$PID_FILE"
            if kill -0 $BACKEND_PID 2>/dev/null; then
                echo -e "\033[32mBackend running (PID: $BACKEND_PID)\033[0m"
            else
                echo -e "\033[31mBackend not running\033[0m"
            fi
            if kill -0 $FRONTEND_PID 2>/dev/null; then
                echo -e "\033[32mFrontend running (PID: $FRONTEND_PID)\033[0m"
            else
                echo -e "\033[31mFrontend not running\033[0m"
            fi
        else
            echo -e "\033[31mNo service record found\033[0m"
        fi
        ;;
    restart)
        echo -e "\033[33mRestarting...\033[0m"
        "$0" stop
        sleep 1
        "$0" start
        ;;
    *)
        echo "Usage: ./start.sh {start|stop|restart|status}"
        ;;
esac
