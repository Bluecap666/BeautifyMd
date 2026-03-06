# 📁 项目结构说明

## 目录结构

```
BeautifyArts/
│
├── 📄 main.py                  # 主程序入口，命令行接口
├── ⚙️  config.py                # 配置管理模块
├── 🎨 beautify_rules.py         # 美化规则库 (emoji、分割线等)
├── 📂 file_handler.py           # 文件处理模块 (读写、分割、合并)
├── 🤖 ai_beautifier.py          # AI 美化引擎 (调用 API)
│
├── 📝 requirements.txt          # Python 依赖列表
├── 🔧 .env                      # 环境变量配置 (API 密钥)
├── 🔧 .env.example              # 环境变量示例
├── ⚙️  config.yaml               # 用户配置文件
├── ⚙️  config.example.yaml       # 配置文件示例
├── 🚫 .gitignore                # Git 忽略文件
│
├── 📖 README.md                 # 项目主文档
├── 🚀 QUICKSTART.md             # 快速开始指南
├── 💡 examples.py               # 使用示例脚本
│
└── 📝 test_document.md          # 测试文档
```

## 核心模块详解

### 🔹 main.py - 主控制器
**功能：**
- 解析命令行参数
- 协调各模块工作
- 处理整体流程
- 提供友好的用户界面

**关键函数：**
- `main()` - 程序入口
- `beautify_single_file()` - 单文件美化
- `beautify_directory()` - 目录批量美化

### 🔹 config.py - 配置管理
**功能：**
- 加载和管理配置文件
- 读取环境变量
- 提供配置验证
- 支持配置合并和覆盖

**关键类：**
- `Config` - 配置管理类
- `get_config()` - 获取全局配置实例

### 🔹 beautify_rules.py - 美化规则库
**功能：**
- 提供 emoji 映射表
- 定义分割线样式
- 字体格式模板
- 颜色和背景规则

**关键类：**
- `EmojiRules` - Emoji 规则
- `DividerRules` - 分割线规则
- `FontStyleRules` - 字体样式规则
- `ColorBackgroundRules` - 颜色背景规则
- `BeautifyPatterns` - 美化模式

### 🔹 file_handler.py - 文件处理器
**功能：**
- 文件读取和写入
- 文件大小检测
- 大文件分割
- 分块合并
- 批量文件查找

**关键类：**
- `FileHandler` - 文件处理类
- `split_file_by_chars()` - 按字符分割
- `split_file_by_sections()` - 按章节分割
- `merge_chunks()` - 合并分块

### 🔹 ai_beautifier.py - AI 美化引擎
**功能：**
- 调用 OpenAI API
- 构建美化提示词
- 批量处理文档块
- 格式验证和修复
- 多种美化风格

**关键类：**
- `AIBeautifier` - AI 美化器
- `beautify()` - 标准美化
- `quick_beautify()` - 快速美化
- `validate_and_fix()` - 验证修复

## 数据流图

```
用户输入
    ↓
main.py (解析参数)
    ↓
config.py (加载配置)
    ↓
file_handler.py (读取文件)
    ↓
判断文件大小
    ├─ 小文件 → ai_beautifier.py (直接美化)
    └─ 大文件 → 分割 → ai_beautifier.py (分块美化) → 合并
    ↓
file_handler.py (写入结果)
    ↓
输出美化后的文件
```

## 配置文件说明

### .env - 环境变量
```ini
OPENAI_API_KEY=你的 API 密钥
OPENAI_API_BASE_URL=API 地址
DEFAULT_MODEL=gpt-3.5-turbo
REQUEST_TIMEOUT=120
MAX_RETRIES=3
```

### config.yaml - 应用配置
```yaml
beautify:
  add_emoji: true
  add_dividers: true
  # ... 其他美化选项

file_processing:
  split_threshold: 50000
  chunk_size: 5000
  chunk_overlap: 200

output:
  output_dir: "beautified"
  add_suffix: true
  keep_backup: false
```

## 模块间关系

```
main.py
  ├── config.py (配置支持)
  ├── file_handler.py (文件操作)
  │     └── beautify_rules.py (规则支持)
  └── ai_beautifier.py (AI 美化)
        └── OpenAI API (外部服务)
```

## 技术栈

- **Python 3.7+** - 主要编程语言
- **openai** - AI API 客户端
- **PyYAML** - YAML 配置解析
- **python-dotenv** - 环境变量管理
- **tqdm** - 进度条显示
- **colorama** - 彩色终端输出

## 扩展开发

### 添加新的美化规则

在 `beautify_rules.py` 中添加：

```python
class NewRules:
    NEW_STYLES = {
        'style1': 'value1',
        'style2': 'value2',
    }
```

### 添加新的美化风格

在 `ai_beautifier.py` 的 `quick_beautify()` 方法中添加：

```python
style_prompts['new_style'] = "新风格的描述"
```

### 添加命令行参数

在 `main.py` 的 `main()` 函数中添加：

```python
parser.add_argument('--new-option', action='store_true')
```

## 性能优化建议

1. **大文件处理**: 调整 `chunk_size` 和 `chunk_overlap`
2. **批量处理**: 使用目录模式而非逐个处理
3. **快速模式**: 使用 `--quick` 参数加快速度
4. **并发处理**: 未来可考虑添加多线程支持

## 安全注意事项

1. **API 密钥**: 不要将 `.env` 提交到版本控制
2. **备份文件**: 重要文件开启备份功能
3. **网络请求**: 设置合理的超时时间
4. **错误处理**: 系统会自动重试失败请求

---

**通过理解项目结构，你可以更好地使用和扩展 MD BeautifyArts！** 🔧
