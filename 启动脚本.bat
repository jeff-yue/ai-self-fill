@echo off
chcp 65001 >nul
title 自助提报自动化脚本 - 启动器

:menu
cls
echo ============================================================
echo           自助提报自动化脚本 - 启动器
echo ============================================================
echo.
echo 请选择操作：
echo.
echo   [1] 运行脚本 ⚡
echo   [2] 安装/更新依赖
echo   [3] 测试环境
echo   [4] 查看帮助文档
echo   [0] 退出
echo.
echo ============================================================
set /p choice=请输入选项 [0-4]: 

if "%choice%"=="1" goto run_uv
if "%choice%"=="2" goto install_uv
if "%choice%"=="3" goto test
if "%choice%"=="4" goto help
if "%choice%"=="0" goto end
goto menu

:run_uv
cls
echo ============================================================
echo 运行脚本
echo ============================================================
echo.
echo 设置UTF-8编码环境...
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
echo.
uv run python run_with_config.py
echo.
echo ============================================================
pause
goto menu

:install_uv
cls
echo ============================================================
echo 安装/更新依赖
echo ============================================================
echo.

echo 设置UTF-8编码环境...
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
echo.

uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo uv未安装，正在安装...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
)

echo.
echo 正在同步依赖...
uv sync
echo.
echo ============================================================
echo 安装完成！
echo ============================================================
pause
goto menu

:test
cls
echo ============================================================
echo 测试环境
echo ============================================================
echo.
python test_import.py
echo.
echo ============================================================
pause
goto menu

:help
cls
echo ============================================================
echo 帮助文档
echo ============================================================
echo.
echo 可用文档：
echo   - 从这里开始.txt       新手入门指南
echo   - 快速开始.txt         快速使用教程
echo   - uv使用说明.md        uv环境详细说明
echo   - 使用说明.md          完整使用文档
echo   - README.md            技术文档
echo   - 文件清单.txt         完整文件说明
echo.
echo 推荐阅读顺序：
echo   1. 从这里开始.txt
echo   2. 快速开始.txt
echo   3. uv使用说明.md 或 使用说明.md
echo.
echo ============================================================
pause
goto menu

:end
cls
echo.
echo 感谢使用！再见 👋
echo.
timeout /t 2 >nul
exit
