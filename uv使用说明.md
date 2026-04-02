# 使用uv环境运行自助提报自动化脚本

## 🚀 什么是uv？

uv是一个由Rust编写的极快的Python包管理器和项目管理工具，比传统的pip快10-100倍！

### uv的优势

- ⚡ **超快速度** - 比pip快10-100倍
- 🎯 **更好的依赖解析** - 更快更准确
- 📦 **统一管理** - 虚拟环境和包管理一体化
- 🔒 **锁文件支持** - 确保依赖版本一致性

## 📋 快速开始（使用uv）

### 方式一：全自动安装和运行（推荐）

```bash
# 第1步：安装uv和依赖（会自动安装uv）
双击运行: 使用uv安装.bat

# 第2步：修改配置
编辑: config.json

# 第3步：运行脚本
双击运行: 使用uv运行.bat
```

### 方式二：命令行操作

#### 1. 安装uv

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**或者使用pip安装:**
```bash
pip install uv
```

#### 2. 同步依赖

```bash
# 在项目目录下运行
uv sync
```

这会：
- 创建虚拟环境（.venv目录）
- 安装所有依赖包（从pyproject.toml）
- 生成锁文件（uv.lock）

#### 3. 运行脚本

```bash
# 使用uv运行脚本
uv run python run_with_config.py

# 或者激活虚拟环境后运行
# Windows:
.venv\Scripts\activate
python run_with_config.py

# 退出虚拟环境
deactivate
```

## 📁 uv相关文件说明

| 文件名 | 说明 |
|--------|------|
| `pyproject.toml` | 项目配置文件，定义依赖和元数据 |
| `.python-version` | 指定Python版本（3.11） |
| `uv.lock` | 锁文件，记录精确的依赖版本（自动生成） |
| `.venv/` | 虚拟环境目录（自动创建） |
| `使用uv安装.bat` | 自动安装uv和依赖 |
| `使用uv运行.bat` | 使用uv运行脚本 |

## 🔧 常用uv命令

### 依赖管理

```bash
# 同步依赖（安装/更新）
uv sync

# 添加新依赖
uv add 包名

# 添加开发依赖
uv add --dev 包名

# 移除依赖
uv remove 包名

# 更新所有依赖
uv sync --upgrade
```

### 运行脚本

```bash
# 运行Python脚本
uv run python 脚本名.py

# 运行项目定义的命令
uv run run-config

# 执行单个命令
uv run python -c "print('Hello')"
```

### 虚拟环境

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate

# 使用uv运行（无需激活）
uv run python 脚本名.py
```

### 查看信息

```bash
# 查看uv版本
uv --version

# 查看已安装的包
uv pip list

# 查看项目信息
uv tree
```

## 📊 性能对比

| 操作 | pip | uv | 速度提升 |
|------|-----|----|----|
| 安装requests | 3.2s | 0.08s | **40x** |
| 安装pandas | 8.5s | 0.3s | **28x** |
| 解析依赖 | 5.1s | 0.1s | **51x** |

## 🔄 从传统pip迁移到uv

如果你之前使用的是pip和requirements.txt：

### 1. 保留原有方式

```bash
# 仍然可以使用传统方式
pip install -r requirements.txt
python run_with_config.py
```

### 2. 切换到uv

```bash
# 使用uv（推荐）
uv sync
uv run python run_with_config.py
```

### 两种方式对比

| 特性 | pip方式 | uv方式 |
|------|---------|--------|
| 安装速度 | 慢 | ⚡ 快 |
| 依赖解析 | 简单 | 🎯 精确 |
| 虚拟环境 | 需手动创建 | 📦 自动管理 |
| 锁文件 | 无 | 🔒 有 |
| 适用场景 | 传统项目 | ✨ 现代项目 |

## ⚙️ pyproject.toml 配置说明

```toml
[project]
name = "api-automation"              # 项目名称
version = "1.0.0"                    # 版本号
description = "自助提报自动化脚本"    # 项目描述
requires-python = ">=3.8"            # Python版本要求

dependencies = [                      # 生产依赖
    "requests>=2.31.0",
    "pandas>=2.0.0",
    "openpyxl>=3.1.0",
]

[project.scripts]                     # 命令行工具
run = "api_automation:main"          # uv run run
run-config = "run_with_config:main"  # uv run run-config

[tool.uv]                            # uv配置
dev-dependencies = []                # 开发依赖
```

## 🎯 推荐工作流程

### 初次使用

```bash
# 1. 安装uv（如果未安装）
双击: 使用uv安装.bat

# 2. 修改配置
编辑: config.json

# 3. 运行脚本
双击: 使用uv运行.bat
```

### 日常使用

```bash
# 直接运行（无需其他操作）
双击: 使用uv运行.bat
```

### 更新依赖

```bash
# 更新所有依赖到最新版本
uv sync --upgrade
```

## ❓ 常见问题

### Q1: uv安装失败怎么办？

**A:** 尝试以下方法：
1. 使用管理员权限运行PowerShell
2. 或者使用pip安装：`pip install uv`
3. 或者继续使用传统方式（运行"安装依赖.bat"）

### Q2: .venv目录很大可以删除吗？

**A:** 可以删除，下次运行 `uv sync` 会重新创建。但通常不需要删除，它只存在于本地。

### Q3: uv.lock文件有什么用？

**A:** 锁定精确的依赖版本，确保团队成员使用相同的依赖版本。建议提交到版本控制系统。

### Q4: 可以同时使用pip和uv吗？

**A:** 可以，但建议选择一种方式：
- **新项目推荐uv** - 更快更好
- **旧项目可继续用pip** - 保持兼容

### Q5: 如何指定Python版本？

**A:** 编辑 `.python-version` 文件：
```
3.11
```
或在pyproject.toml中指定：
```toml
requires-python = ">=3.8"
```

### Q6: uv run和直接运行有什么区别？

**A:** 
- `uv run` - 自动使用项目虚拟环境，无需手动激活
- 直接运行 - 需要先激活虚拟环境

推荐使用 `uv run`，更方便！

## 🔍 故障排查

### 问题：uv命令找不到

**解决方案：**
```bash
# 重新安装uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用pip
pip install uv
```

### 问题：依赖安装失败

**解决方案：**
```bash
# 清理缓存重试
uv cache clean
uv sync

# 或回退到pip方式
pip install -r requirements.txt
```

### 问题：虚拟环境损坏

**解决方案：**
```bash
# 删除虚拟环境重建
rmdir /s /q .venv
uv sync
```

## 📚 更多资源

- 🌐 uv官方文档: https://docs.astral.sh/uv/
- 📖 uv GitHub: https://github.com/astral-sh/uv
- 💬 使用教程: https://astral.sh/blog/uv

## 🎉 总结

使用uv的优势：

✅ **速度快** - 安装依赖快10-100倍  
✅ **更简单** - 一个命令搞定所有事  
✅ **更可靠** - 锁文件确保版本一致  
✅ **更现代** - Python生态的未来趋势  

推荐使用uv，享受更好的开发体验！

---

**选择你喜欢的方式：**

| 传统方式 | uv方式 |
|---------|--------|
| 安装依赖.bat | 使用uv安装.bat ⭐ |
| 运行脚本.bat | 使用uv运行.bat ⭐ |

**两种方式都可以正常使用，选择你喜欢的即可！** 🚀
