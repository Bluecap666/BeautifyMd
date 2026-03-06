# 🚀 快速开始指南

## 5 分钟上手 MD BeautifyArts

### 第一步：安装依赖 (1 分钟)

```bash
cd BeautifyArts
pip install -r requirements.txt
```

### 第二步：配置 API 密钥 (1 分钟)

1. 复制配置文件：
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的 API 密钥：
   ```ini
   OPENAI_API_KEY=sk-你的密钥
   OPENAI_API_BASE_URL=https://api.openai.com/v1
   ```

### 第三步：测试运行 (1 分钟)

使用内置的测试文档：

```bash
python main.py test_document.md
```

查看输出文件：
```bash
# Windows
notepad beautified\test_document_beautified.md

# Linux/Mac
cat beautified/test_document_beautified.md
```

### 第四步：美化你的文档 (2 分钟)

```bash
# 美化单个文件
python main.py README.md

# 美化整个目录
python main.py ./docs

# 使用彩色风格
python main.py guide.md --style colorful

# 不使用 emoji
python main.py doc.md --no-emoji
```

## 💡 常用命令速查

| 功能 | 命令 |
|------|------|
| 基本美化 | `python main.py file.md` |
| 指定输出 | `python main.py in.md -o out.md` |
| 彩色风格 | `python main.py file.md --style colorful` |
| 极简风格 | `python main.py file.md --style minimal` |
| 不要 emoji | `python main.py file.md --no-emoji` |
| 快速美化 | `python main.py file.md --quick` |
| 仅修复格式 | `python main.py file.md --validate` |
| 查看帮助 | `python main.py --help` |

## ⚙️ 配置说明

### 基础配置 (.env)

```ini
OPENAI_API_KEY=你的密钥
DEFAULT_MODEL=gpt-3.5-turbo
```

### 自定义行为 (config.yaml)

```yaml
beautify:
  add_emoji: true      # 添加 emoji
  add_dividers: true   # 添加分割线
  
output:
  output_dir: "beautified"  # 输出目录
```

## 🎨 美化风格

- **default** - 平衡美观和实用
- **minimal** - 极简，适合技术文档
- **colorful** - 丰富多彩，适合教程
- **professional** - 专业正式，适合 API 文档

## 📝 下一步

- 查看完整文档：`README.md`
- 查看更多示例：`examples.py`
- 自定义配置：`config.yaml`

## ❓ 遇到问题？

1. **API 密钥错误**: 检查 `.env` 文件是否正确配置
2. **依赖缺失**: 运行 `pip install -r requirements.txt`
3. **网络超时**: 增加 `REQUEST_TIMEOUT` 值

---

**开始美化你的文档吧！** ✨
