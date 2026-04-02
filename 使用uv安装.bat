@echo off
chcp 65001 >nul
echo ============================================================
echo 使用uv安装依赖包
echo ============================================================
echo.

echo 检查uv是否已安装...
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo uv未安装，正在安装uv...
    echo.
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    if %errorlevel% neq 0 (
        echo.
        echo uv安装失败！请手动安装uv或使用传统方式安装依赖。
        echo 手动安装命令: pip install uv
        echo.
        pause
        exit /b 1
    )
)

echo.
echo uv已安装，版本信息：
uv --version
echo.

echo 设置UTF-8编码环境（解决中文路径问题）...
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
echo.

echo 正在使用uv同步依赖...
uv sync

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo 依赖安装完成！
    echo ============================================================
    echo.
    echo 虚拟环境已创建在: .venv 目录
    echo.
) else (
    echo.
    echo ============================================================
    echo 依赖安装失败！
    echo ============================================================
    echo.
)

echo 按任意键退出...
pause >nul
