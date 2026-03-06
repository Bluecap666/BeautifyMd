# 🔧 安装和运行指南

## 📋 系统要求

### 最低要求
- **Python**: 3.7 或更高版本
- **内存**: 至少 512MB 可用内存
- **磁盘空间**: 至少 10MB 可用空间
- **网络**: 需要访问 AI API 服务

### 推荐配置
- **Python**: 3.9 或更高版本
- **内存**: 1GB 或更多
- **网络**: 稳定的互联网连接

---

## 🚀 快速安装（5 分钟）

### 步骤 1: 克隆或下载项目

```bash
# 如果使用 Git
git clone <repository-url>
cd BeautifyArts

# 或者直接解压下载的 ZIP 文件
cd BeautifyArts
```

### 步骤 2: 创建虚拟环境（推荐）

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 步骤 3: 安装依赖

```bash
pip install -r requirements.txt
```

**如果下载速度慢（中国用户）：**
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤 4: 配置 API 密钥

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件：
```ini
OPENAI_API_KEY=sk-你的 API 密钥
OPENAI_API_BASE_URL=https://api.openai.com/v1
DEFAULT_MODEL=gpt-3.5-turbo
```

### 步骤 5: 测试安装

```bash
python main.py --help
```

如果看到帮助信息，说明安装成功！✅

---

## 🎯 第一次运行

### 使用测试文档

```bash
# 运行测试
python main.py test_document.md

# 查看结果
# Windows
notepad beautified\test_document_beautified.md

# Linux/Mac
cat beautified/test_document_beautified.md
```

### 检查输出

美化后的文件应该在 `beautified/` 目录中。

---

## ⚙️ 详细配置

### 1. 环境变量配置 (.env)

```ini
# === 必需配置 ===
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# === 可选配置 ===
# API 基础 URL（默认：https://api.openai.com/v1）
OPENAI_API_BASE_URL=https://api.openai.com/v1

# 使用的模型（默认：gpt-3.5-turbo）
DEFAULT_MODEL=gpt-3.5-turbo

# 请求超时时间（秒，默认：120）
REQUEST_TIMEOUT=120

# 最大重试次数（默认：3）
MAX_RETRIES=3
```

### 2. 应用配置 (config.yaml)

```yaml
beautify:
  # 美化选项（true/false）
  add_emoji: true              # 添加 emoji
  add_dividers: true           # 添加分割线
  beautify_code_blocks: true   # 美化代码块
  optimize_headers: true       # 优化标题
  add_quote_styles: true       # 美化引用
  beautify_lists: true         # 美化列表
  beautify_tables: true        # 美化表格
  add_emphasis: true           # 添加强调

file_processing:
  # 文件处理选项
  split_threshold: 50000       # 文件大小阈值（字节）
  chunk_size: 5000             # 分割块大小（字符数）
  chunk_overlap: 200           # 重叠部分大小（字符数）

output:
  # 输出选项
  output_dir: "beautified"     # 输出目录名称
  add_suffix: true             # 添加文件名后缀
  suffix: "_beautified"        # 后缀内容
  keep_backup: false           # 保留原始备份

logging:
  # 日志选项
  level: "INFO"                # 日志级别
  save_to_file: true           # 保存到文件
  log_file: "beautify.log"     # 日志文件名
```

---

## 🔍 故障排除

### 问题 1: pip 安装失败

**错误信息：**
```
ERROR: Could not find a version that satisfies the requirement...
```

**解决方案：**
```bash
# 升级 pip
python -m pip install --upgrade pip

# 重新尝试安装
pip install -r requirements.txt
```

### 问题 2: API 密钥错误

**错误信息：**
```
❌ 错误：API 密钥未设置
```

**解决方案：**
1. 检查 `.env` 文件是否存在
2. 确认 `OPENAI_API_KEY` 已填写
3. 确保没有多余的空格或引号
4. 重启终端重新运行

### 问题 3: 网络连接超时

**错误信息：**
```
Request timeout
```

**解决方案：**
```ini
# 在 .env 文件中增加超时时间
REQUEST_TIMEOUT=300
```

**或者使用代理：**
```bash
export HTTP_PROXY=http://proxy-server:port
export HTTPS_PROXY=http://proxy-server:port
```

### 问题 4: 模块导入错误

**错误信息：**
```
ModuleNotFoundError: No module named 'openai'
```

**解决方案：**
```bash
# 确认在正确的环境中
which python  # Linux/Mac
where python  # Windows

# 重新安装依赖
pip install -r requirements.txt
```

### 问题 5: 文件编码错误

**错误信息：**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```

**解决方案：**
系统会自动尝试多种编码（UTF-8、GBK、GB2312 等）。如果仍然失败：

1. 手动转换文件为 UTF-8
2. 或使用文本编辑器另存为 UTF-8 编码

### 问题 6: 输出目录权限错误

**错误信息：**
```
PermissionError: [Errno 13] Permission denied
```

**解决方案：**
```bash
# Windows - 以管理员身份运行
# 右键点击终端 → 以管理员身份运行

# Linux/Mac - 检查权限
ls -la
chmod -R u+w .
```

---

## 🚀 性能优化

### 1. 加快处理速度

**使用更快的模型：**
```ini
# .env
DEFAULT_MODEL=gpt-4  # 质量更好但更贵
# 或
DEFAULT_MODEL=gpt-3.5-turbo  # 速度快，成本低
```

**减少美化元素：**
```yaml
# config.yaml
beautify:
  add_emoji: false
  add_dividers: false
```

### 2. 处理大文件

**调整分割参数：**
```yaml
file_processing:
  chunk_size: 10000      # 增大分块
  chunk_overlap: 100     # 减少重叠
```

### 3. 批量处理优化

**使用脚本批量处理：**

Windows (batch_process.bat):
```batch
@echo off
for %%f in (*.md) do (
    echo 处理：%%f
    python main.py "%%f" --quick
)
pause
```

Linux/Mac (batch_process.sh):
```bash
#!/bin/bash
for file in *.md; do
    echo "处理：$file"
    python main.py "$file" --quick
done
```

---

## 📊 验证安装

### 运行完整测试

```bash
# 1. 检查 Python 版本
python --version

# 2. 检查依赖
pip list | grep -E "openai|yaml|tqdm|colorama|dotenv"

# 3. 测试配置文件
python -c "from config import get_config; c = get_config(); print('✓ 配置加载成功')"

# 4. 测试文件处理
python -c "from file_handler import FileHandler; from config import get_config; h = FileHandler(get_config()); print('✓ 文件处理器正常')"

# 5. 测试 AI 引擎
python -c "from ai_beautifier import AIBeautifier; from config import get_config; a = AIBeautifier(get_config()); print('✓ AI 引擎正常')"

# 6. 完整流程测试
python main.py test_document.md
```

### 预期输出

```
╔══════════════════════════════════════════╗
║     MD BeautifyArts - AI Markdown        ║
╚══════════════════════════════════════════╝

✓ 已加载配置文件：config.yaml
📄 处理文件：test_document.md
✨ 美化完成！
✓ 文件已保存：test_document_beautified.md

✅ 所有测试通过！
```

---

## 🔄 更新和维护

### 更新依赖

```bash
# 更新所有包
pip install --upgrade -r requirements.txt
```

### 清理缓存

```bash
# 清理 Python 缓存
find . -type d -name "__pycache__" -exec rm -rf {} +

# 或手动删除
rm -rf __pycache__/
rm -rf *.pyc
```

### 查看日志

```bash
# 查看最新日志
tail -n 50 beautify.log

# 实时查看
tail -f beautify.log

# Windows
type beautify.log
```

---

## 🆘 获取帮助

### 命令行帮助

```bash
# 查看所有选项
python main.py --help

# 查看版本
python main.py --version
```

### 文档资源

- **README.md** - 完整使用文档
- **QUICKSTART.md** - 快速开始指南
- **DEMO.md** - 使用演示
- **PROJECT_STRUCTURE.md** - 项目结构说明

### 社区支持

- 提交 Issue
- 查看 FAQ
- 阅读 Wiki

---

## ✅ 安装检查清单

- [ ] Python 3.7+ 已安装
- [ ] 虚拟环境已创建并激活
- [ ] 依赖包已成功安装
- [ ] `.env` 文件已创建并配置 API 密钥
- [ ] `config.yaml` 文件存在
- [ ] 测试文件可以正常运行
- [ ] 能够访问 AI API 服务

如果以上都已完成，恭喜你！🎉 
**MD BeautifyArts 已经准备就绪！**

---

**开始美化你的 Markdown 文档吧！** ✨
