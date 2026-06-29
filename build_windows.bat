@echo off
chcp 65001 >nul
echo ====================================
echo   Gear System - Windows 打包脚本
echo ====================================
echo.

echo [1/4] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

echo.
echo [2/4] 安装依赖...
cd /d "%~dp0backend"
pip install -r requirements.txt
pip install pywebview pyinstaller
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

echo.
echo [3/4] 构建前端...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install
)
call npm run build
if errorlevel 1 (
    echo 错误: 前端构建失败
    pause
    exit /b 1
)

echo 复制前端构建产物到后端目录...
if exist "%~dp0backend\frontend_dist" (
    rmdir /s /q "%~dp0backend\frontend_dist"
)
xcopy /e /i /y "%~dp0frontend\dist" "%~dp0backend\frontend_dist" >nul

echo.
echo [4/4] 打包 exe...
cd /d "%~dp0backend"
pyinstaller --clean GearSystem.spec
if errorlevel 1 (
    echo 错误: 打包失败
    pause
    exit /b 1
)

echo.
echo ====================================
echo   打包完成!
echo   输出目录: backend\dist\GearSystem.exe
echo ====================================
pause
