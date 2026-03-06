# 🌳 项目文件树

```
BeautifyArts/                              # 项目根目录
│
├── 📄 核心代码文件 (5 个)
│   ├── main.py                            # ⭐ 主程序入口 (~12KB)
│   │                                      #    - 命令行参数解析
│   │                                      #    - 单文件和批量处理
│   │                                      #    - 流程控制
│   │
│   ├── config.py                          # ⚙️ 配置管理 (~6KB)
│   │                                      #    - Config 类
│   │                                      #    - YAML 配置加载
│   │                                      #    - 环境变量读取
│   │                                      #    - 配置验证
│   │
│   ├── beautify_rules.py                  # 🎨 美化规则库 (~12KB)
│   │                                      #    - EmojiRules: emoji 映射
│   │                                      #    - DividerRules: 分割线样式
│   │                                      #    - FontStyleRules: 字体格式
│   │                                      #    - ColorBackgroundRules: 颜色
│   │                                      #    - BeautifyPatterns: 美化模式
│   │
│   ├── file_handler.py                    # 📂 文件处理器 (~11KB)
│   │                                      #    - 文件读写
│   │                                      #    - 大文件检测
│   │                                      #    - 智能分割
│   │                                      #    - 分块合并
│   │                                      #    - 批量查找
│   │
│   └── ai_beautifier.py                   # 🤖 AI 美化引擎 (~9KB)
│                                      #    - OpenAI API 集成
│                                      #    - 提示词构建
│                                      #    - 批量处理
│                                      #    - 快速美化模式
│                                      #    - 格式验证修复
│
├── 📝 配置文件 (6 个)
│   ├── requirements.txt                   # 📦 Python 依赖
│   │                                      #    openai, python-dotenv, 
│   │                                      #    tqdm, colorama, PyYAML
│   │
│   ├── .env                               # 🔐 环境变量（需配置）
│   │                                      #    OPENAI_API_KEY=...
│   │                                      #    DEFAULT_MODEL=gpt-3.5-turbo
│   │
│   ├── .env.example                       # 📋 环境变量示例
│   │
│   ├── config.yaml                        # ⚙️ 应用配置
│   │                                      #    beautify: {...}
│   │                                      #    file_processing: {...}
│   │                                      #    output: {...}
│   │
│   ├── config.example.yaml                # 📋 配置示例
│   │
│   └── .gitignore                         # 🚫 Git 忽略规则
│
├── 📖 文档文件 (4 个)
│   ├── README.md                          # 📘 主文档 (~8.4KB)
│   │                                      #    - 功能介绍
│   │                                      #    - 安装指南
│   │                                      #    - 详细用法
│   │                                      #    - 配置说明
│   │                                      #    - 故障排除
│   │
│   ├── QUICKSTART.md                      # 🚀 快速开始 (~2.5KB)
│   │                                      #    - 5 分钟上手
│   │                                      #    - 常用命令
│   │                                      #    - 基础配置
│   │
│   ├── PROJECT_STRUCTURE.md               # 🏗️ 结构说明 (~5.2KB)
│   │                                      #    - 模块详解
│   │                                      #    - 数据流图
│   │                                      #    - 扩展开发
│   │
│   └── SUMMARY.md                         # 📋 项目总结 (~7.7KB)
│                                          #    - 功能清单
│                                          #    - 技术亮点
│                                          #    - 使用统计
│
├── 💡 示例和测试 (2 个)
│   ├── examples.py                        # 💻 使用示例 (~6.1KB)
│   │                                      #    - 17 个使用场景
│   │                                      #    - 代码示例
│   │                                      #    - 脚本模板
│   │
│   └── test_document.md                   # 📝 测试文档
│                                          #    - 各种 MD 元素
│                                          #    - 测试用例
│
└── 📁 运行时生成的文件（不提交到 Git）
    ├── beautified/                        # 📤 输出目录
    │   └── *_beautified.md                #    美化后的文件
    │
    ├── *.log                              # 📊 日志文件
    │   └── beautify.log
    │
    └── *.bak                              # 💾 备份文件
        └── *.md.bak


📊 统计信息:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
核心代码：     5 个文件  ~49KB
配置文件：     6 个文件  ~3KB
文档：         4 个文件  ~24KB
示例：         2 个文件  ~6KB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总计：        17 个文件  ~82KB

代码行数估算:
- main.py:          ~340 行
- config.py:        ~195 行
- beautify_rules.py: ~390 行
- file_handler.py:  ~340 行
- ai_beautifier.py: ~300 行
- examples.py:      ~210 行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总计：          ~1775 行代码
```

---

## 🎯 快速导航

### 新手入门路径
```
1. README.md           → 了解项目
2. QUICKSTART.md       → 快速开始
3. test_document.md    → 测试运行
4. examples.py         → 深入学习
```

### 开发者路径
```
1. PROJECT_STRUCTURE.md → 理解架构
2. main.py             → 入口点
3. config.py + file_handler.py → 核心逻辑
4. ai_beautifier.py    → AI 集成
5. beautify_rules.py   → 规则系统
```

### 自定义路径
```
1. config.yaml         → 调整配置
2. beautify_rules.py   → 添加规则
3. .env                → 修改 API 设置
4. main.py             → 扩展功能
```

---

## 🔗 模块依赖关系

```
                    用户
                     ↓
                 main.py
                     ↓
         ┌───────────┼───────────┐
         ↓           ↓           ↓
    config.py  file_handler.py  ai_beautifier.py
         ↓           ↓               ↓
    .env 文件   beautify_rules.py  OpenAI API
         ↓           ↓
    config.yaml   规则数据
```

---

## 📦 数据流示例

### 单文件美化流程
```
document.md
    ↓ [读取]
file_handler.read_file()
    ↓ [内容]
ai_beautifier.beautify()
    ↓ [美化]
OpenAI API → 返回美化内容
    ↓ [写入]
beautified/document_beautified.md
```

### 大文件处理流程
```
large_file.md (>50KB)
    ↓ [检测需要分割]
file_handler.split_file_by_chars()
    ↓ [分块 1, 分块 2, ...]
for each chunk:
    ai_beautifier.beautify()
    ↓ [美化后的分块]
file_handler.merge_chunks()
    ↓ [合并]
beautified/large_file_beautified.md
```

---

**这就是完整的项目结构！每个模块都有其明确的职责，共同构成了这个强大的 Markdown 美化工具。** ✨
