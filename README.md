# 🎨 MD BeautifyArts - AI 驱动的 Markdown 文档美化工具

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-3.0-red.svg)
![GitHub](https://img.shields.io/badge/GitHub-Repo-blue)
![Stars](https://img.shields.io/github/stars/Bluecap666/BeautifyMd?style=social)

一个强大的 AI 驱动工具，用于美化您的 Markdown 文档。自动添加 emoji、分割线、优化格式，让文档更加美观和专业！

**v3.0 新增功能：**
- 🌐 **Web UI 界面** - 无需命令行，在线美化
- 🤖 **19+ 模型支持** - OpenAI、通义千问、文心一言、豆包等
- 🎨 **富媒体样式** - 边框、背景、气泡、多彩文字
- 💬 **AI 聊天** - 多模型切换，智能对话
- 📱 **微信公众号** - 完美适配公众号编辑器
- 🔧 **在线配置** - 实时配置 API KEY

## ✨ 功能特性

### 🎯 核心功能
- **🤖 AI 智能美化** - 使用先进的 AI 模型自动美化文档
- **🌐 Web UI 界面** - 友好的网页界面，无需命令行经验
- **🔀 多模型支持** - 支持 OpenAI、通义千问、文心一言、讯飞星火等
- **📝 Emoji 增强** - 智能添加合适的 emoji 表情
- **📏 分割线优化** - 在适当位置添加美观的分割线
- **🎨 多样风格** - 支持多种美化风格（默认、极简、彩色、专业）
- **📊 大文件处理** - 自动分割大文件，美化后合并
- **🔄 批量处理** - 支持整个目录的批量处理
- **✅ 格式验证** - 验证并修复 Markdown 格式问题
- **💾 备份保护** - 可选的原始文件备份功能

### 🛠️ 美化元素
- ✅ Emoji 表情智能匹配
- ✅ 分割线样式多样化
- ✅ 标题层次优化
- ✅ 代码块格式化
- ✅ 列表样式统一
- ✅ 表格对齐美化
- ✅ 引用块装饰
- ✅ 强调效果增强

## 🚀 快速开始

### 方式一：Web UI（推荐新手）

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **配置 API 密钥**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件，填入至少一个模型的 API 密钥。

3. **启动 Web 服务**
```bash
python web_app.py
```

4. **访问界面**
打开浏览器访问：http://localhost:5000

详细文档：[WEB_UI_GUIDE.md](WEB_UI_GUIDE.md)

---

### 方式二：命令行模式

1. **安装依赖**

```bash
pip install -r requirements.txt
```

### 2️⃣ 配置 API 密钥

复制环境变量配置文件：

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：

```ini
# ========== OpenAI API 配置 ==========
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE_URL=https://api.openai.com/v1

# ========== 国内大模型配置 ==========

# 通义千问 (阿里云)
DASHSCOPE_API_KEY=your_dashscope_key_here

# 文心一言 (百度)
QIANFAN_AK=your_qianfan_ak_here
QIANFAN_SK=your_qianfan_sk_here

# 讯飞星火
SPARK_API_KEY=your_spark_key_here

# 智谱 AI
ZHIPU_API_KEY=your_zhipu_key_here

# 腾讯混元
HUNYUAN_API_KEY=your_hunyuan_key_here

# ========== 模型选择 ==========
DEFAULT_MODEL=gpt-3.5-turbo
```

**支持的模型：**
- OpenAI: gpt-3.5-turbo, gpt-4
- 通义千问：qwen-turbo, qwen-plus
- 文心一言：ernie-bot, ernie-bot-turbo
- 讯飞星火：spark-v3.5, spark-v3.0
- 智谱 AI: chatglm_pro, chatglm_std
- 腾讯混元：hunyuan-lite

详细配置文档：[MODELS_GUIDE.md](MODELS_GUIDE.md)

```bash
copy .env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：

```ini
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE_URL=https://api.openai.com/v1
DEFAULT_MODEL=gpt-3.5-turbo
```

### 3️⃣ 基本使用

#### 美化单个文件

```bash
python main.py document.md
```

#### 美化目录下所有文件

```bash
python main.py ./docs
```

#### 指定输出文件

```bash
python main.py input.md -o output.md
```

#### 使用不同风格

```bash
# 彩色风格
python main.py document.md --style colorful

# 极简风格
python main.py document.md --style minimal

# 专业风格
python main.py document.md --style professional
```

## 📖 详细用法

### 命令行参数

```
usage: main.py [-h] [-o OUTPUT] [-c CONFIG] [-s {default,minimal,colorful,professional}] 
               [--no-emoji] [--no-dividers] [--quick] [--validate]
               input

MD BeautifyArts - AI 驱动的 Markdown 文档美化工具

位置参数:
  input                 输入的 Markdown 文件或目录路径

可选参数:
  -h, --help            显示帮助信息
  -o OUTPUT, --output OUTPUT
                        输出文件路径（仅单文件模式有效）
  -c CONFIG, --config CONFIG
                        配置文件路径 (默认：config.yaml)
  -s STYLE, --style STYLE
                        美化风格 (default/minimal/colorful/professional)
  --no-emoji            不添加 emoji
  --no-dividers         不添加分割线
  --quick               快速美化模式
  --validate            只验证和修复格式，不进行美化
```

### 使用示例

#### 1. 标准美化

```bash
python main.py README.md
```

#### 2. 自定义配置

```bash
python main.py docs/ --config my_config.yaml
```

#### 3. 不使用 emoji

```bash
python main.py guide.md --no-emoji
```

#### 4. 快速彩色美化

```bash
python main.py tutorial.md --quick --style colorful
```

#### 5. 仅修复格式

```bash
python main.py draft.md --validate
```

## ⚙️ 配置说明

### 配置文件 (config.yaml)

```yaml
beautify:
  add_emoji: true           # 是否添加 emoji
  add_dividers: true        # 是否添加分割线
  beautify_code_blocks: true  # 是否美化代码块
  optimize_headers: true    # 是否优化标题
  add_quote_styles: true    # 是否美化引用
  beautify_lists: true      # 是否美化列表
  beautify_tables: true     # 是否美化表格
  add_emphasis: true        # 是否添加强调

file_processing:
  split_threshold: 50000    # 文件大小阈值（字节）
  chunk_size: 5000          # 分割块大小
  chunk_overlap: 200        # 分割块重叠

output:
  output_dir: "beautified"  # 输出目录
  add_suffix: true          # 是否添加后缀
  suffix: "_beautified"     # 文件名后缀
  keep_backup: false        # 是否保留备份

logging:
  level: "INFO"             # 日志级别
  save_to_file: true        # 是否保存日志
  log_file: "beautify.log"  # 日志文件名
```

### 环境变量 (.env)

```ini
# OpenAI API 配置
OPENAI_API_KEY=sk-...              # 你的 API 密钥
OPENAI_API_BASE_URL=https://api.openai.com/v1
DEFAULT_MODEL=gpt-3.5-turbo        # 使用的模型
REQUEST_TIMEOUT=120                # 请求超时（秒）
MAX_RETRIES=3                      # 最大重试次数
```

## 📁 项目结构

```
BeautifyArts/
├── main.py              # 主程序入口
├── config.py            # 配置管理模块
├── file_handler.py      # 文件处理模块
├── ai_beautifier.py     # AI 美化引擎
├── beautify_rules.py    # 美化规则库
├── requirements.txt     # Python 依赖
├── config.yaml          # 用户配置文件
├── .env                 # 环境变量配置
└── README.md            # 项目说明文档
```

## 🎨 美化风格说明

### Default (默认风格)
- 平衡美观和实用性
- 适度使用 emoji
- 清晰的层次结构
- 适合大多数文档

### Minimal (极简风格)
- 最少化的装饰
- 专注于内容本身
- 适合技术文档
- 几乎不使用 emoji

### Colorful (彩色风格)
- 丰富多彩的 emoji
- 活跃的视觉效果
- 适合教程和指南
- 增强可读性

### Professional (专业风格)
- 正式专业的格式
- 强调规范性
- 适合 API 文档
- 注重代码质量

## 🔧 高级功能

### 大文件处理

当文件超过 50KB 时，系统会自动：
1. 📝 将文件分割成合适大小的块
2. ✨ 分别美化每个块
3. 🔗 智能合并美化后的块
4. ✅ 保持文档连贯性

### 批量处理

处理整个目录：

```bash
python main.py ./my-docs
```

输出结构：
```
my-docs/
├── file1.md
├── file2.md
├── subdir/
│   └── file3.md
└── beautified/          # 美化后的文件
    ├── file1_beautified.md
    ├── file2_beautified.md
    └── subdir/
        └── file3_beautified.md
```

### 自定义美化规则

你可以在 `beautify_rules.py` 中自定义：
- Emoji 映射表
- 分割线样式
- 字体格式模板
- 颜色方案

## 📊 效果对比

### 美化前
```markdown
# 项目介绍
这是一个很好的项目。

## 功能
- 功能 1
- 功能 2
- 功能 3

## 安装
运行 pip install

## 使用
调用 main 函数
```

### 美化后
```markdown
# 📋 项目介绍

这是一个很好的项目。

---

## ✨ 功能

- ✅ 功能 1
- ✅ 功能 2
- ✅ 功能 3

---

## 📦 安装

运行以下命令：

```bash
pip install package-name
```

---

## 💡 使用

调用 `main()` 函数即可开始使用。
```

## ⚠️ 注意事项

1. **API 费用**: 使用 AI 服务会产生费用，请注意控制使用量
2. **网络要求**: 需要能够访问 API 服务
3. **文件大小**: 超大文件会自动分割处理
4. **编码支持**: 支持 UTF-8、GBK 等多种编码
5. **备份建议**: 建议开启备份功能以防意外

## 🐛 故障排除

### 问题 1: API 密钥错误
```
❌ 错误：API 密钥未设置
```
**解决**: 确保 `.env` 文件存在且正确配置了 `OPENAI_API_KEY`

### 问题 2: 依赖缺失
```
ModuleNotFoundError: No module named 'openai'
```
**解决**: 运行 `pip install -r requirements.txt`

### 问题 3: 文件编码错误
```
UnicodeDecodeError
```
**解决**: 系统会自动尝试多种编码，如仍失败请手动转换文件为 UTF-8

### 问题 4: 请求超时
```
Request timeout
```
**解决**: 增加 `.env` 中的 `REQUEST_TIMEOUT` 值

## 📝 更新日志

### v1.0.0
- ✨ 初始版本发布
- 🤖 AI 智能美化
- 📝 支持多种美化元素
- 🔄 大文件分割处理
- 📁 批量处理支持

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👥 联系方式

如有问题或建议，请提交 Issue。

---

<div align="center">

**Made with ❤️ by MD BeautifyArts Team**

⭐ 如果这个项目对你有帮助，请给个 Star！

</div>
