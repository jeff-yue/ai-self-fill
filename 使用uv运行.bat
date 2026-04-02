@echo off
chcp 65001 >nul
echo ============================================================
echo 自助提报自动化脚本 (uv环境)
echo ============================================================
echo.

echo 设置UTF-8编码环境...
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo 正在使用uv运行脚本...
echo.

uv run python run_with_config.py

echo.
echo ============================================================
echo 按任意键退出...
pause >nul
