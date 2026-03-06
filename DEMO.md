# 🎬 使用演示 - MD BeautifyArts

## 📝 实战演练

让我们通过实际例子来展示 MD BeautifyArts 的强大功能！

---

## 场景一：美化 README 文件

### 原始文件 (README_before.md)
```markdown
# 项目介绍

这是一个很好的 Python 项目。

## 功能
- 功能 1
- 功能 2
- 功能 3

## 安装
pip install myproject

## 使用
from myproject import main
main()

## 联系方式
email: test@example.com
```

### 运行命令
```bash
python main.py README_before.md --style colorful
```

### 美化后 (README_beautified.md)
```markdown
# 🚀 项目介绍

✨ 这是一个很好的 Python 项目。

---

## ✨ 功能

- ✅ 功能 1
- ✅ 功能 2
- ✅ 功能 3

---

## 📦 安装

运行以下命令进行安装：

```bash
pip install myproject
```

---

## 💡 使用

快速开始：

```python
from myproject import main
main()
```

---

## 📧 联系方式

**Email**: test@example.com
```

---

## 场景二：处理技术文档

### 原始文件 (api_docs.md)
```markdown
# API 文档

## 用户接口

### GET /users
获取所有用户

参数:
- limit: 数量限制
- offset: 偏移量

响应:
{
  "users": [],
  "total": 100
}

### POST /users
创建新用户

参数:
- name: 用户名
- email: 邮箱

错误码:
400 - 参数错误
409 - 用户已存在
```

### 运行命令
```bash
python main.py api_docs.md --style professional
```

### 美化后
```markdown
# 📋 API 文档

---

## 👥 用户接口

---

### 🔍 GET /users

**获取所有用户**

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `limit` | int | 数量限制 |
| `offset` | int | 偏移量 |

#### 响应

```json
{
  "users": [],
  "total": 100
}
```

---

### ➕ POST /users

**创建新用户**

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | str | 用户名 |
| `email` | str | 邮箱 |

#### ⚠️ 错误码

| 状态码 | 说明 |
|--------|------|
| `400` | 参数错误 |
| `409` | 用户已存在 |
```

---

## 场景三：教程文档美化

### 原始文件 (tutorial.md)
```markdown
# Python 入门教程

## 第一章：环境搭建

下载 Python
安装 Python
验证安装

## 第二章：基础语法

变量类型
循环语句
条件判断

## 第三章：函数

定义函数
调用函数
参数传递

## 总结

恭喜你完成了入门学习！
```

### 运行命令
```bash
python main.py tutorial.md --quick --style colorful
```

### 美化后
```markdown
# 🐍 Python 入门教程

---

## 📖 第一章：环境搭建

### 步骤

1. ✅ 下载 Python
2. ✅ 安装 Python
3. ✅ 验证安装

---

## 💻 第二章：基础语法

### 核心概念

- 🔹 变量类型
- 🔹 循环语句
- 🔹 条件判断

---

## ⚙️ 第三章：函数

### 学习内容

- 💡 定义函数
- 🚀 调用函数
- 📦 参数传递

---

## 🎉 总结

🎊 恭喜你完成了入门学习！

💪 继续加油，成为一名 Python 开发者！
```

---

## 场景四：批量处理整个项目文档

### 目录结构
```
docs/
├── introduction.md
├── installation.md
├── usage.md
├── api/
│   ├── users.md
│   └── products.md
└── faq.md
```

### 运行命令
```bash
python main.py ./docs --config config.yaml
```

### 输出结果
```
╔══════════════════════════════════════╗
║  MD BeautifyArts - AI Markdown       ║
╚══════════════════════════════════════╝

📁 搜索目录：./docs
✓ 找到 6 个文件

[1/6]
📄 处理文件：docs/introduction.md
✨ 美化完成！

[2/6]
📄 处理文件：docs/installation.md
✨ 美化完成！

[3/6]
📄 处理文件：docs/usage.md
✨ 美化完成！

[4/6]
📄 处理文件：docs/api/users.md
✨ 美化完成！

[5/6]
📄 处理文件：docs/api/products.md
✨ 美化完成！

[6/6]
📄 处理文件：docs/faq.md
✨ 美化完成！

==================================================
✨ 处理完成！
  成功：6 个文件
  失败：0 个文件
  输出目录：docs/beautified
==================================================
```

### 输出目录结构
```
docs/beautified/
├── introduction_beautified.md
├── installation_beautified.md
├── usage_beautified.md
├── api/
│   ├── users_beautified.md
│   └── products_beautified.md
└── faq_beautified.md
```

---

## 场景五：大文件处理（>100KB）

### 运行命令
```bash
python main.py large_document.md
```

### 终端输出
```
╔══════════════════════════════════════╗
║  MD BeautifyArts - AI Markdown       ║
╚══════════════════════════════════════╝

📄 处理文件：large_document.md
⚠️  文件较大，将采用分割 - 美化 - 合并策略

📝 分割文件: 100%|████████████| 50000/50000 [00:00<00:00]
✓ 文件已分割为 10 个块

✨ AI 美化中: 100%|██████████| 10/10 [00:45<00:00]
✓ 已合并 10 个块

✅ 美化完成！
✨ 完成！输出文件：beautified/large_document_beautified.md
```

---

## 场景六：仅修复格式问题

### 有问题的文件
```markdown
# 未闭合的标题

**未闭合的粗体

```python
def broken_code(  # 未闭合的代码块

- 不规范的列表
* 混用的列表符号

[无效链接](
```

### 运行命令
```bash
python main.py broken.md --validate
```

### 修复后
```markdown
# 闭合的标题

**闭合的粗体**

```python
def fixed_code():
    pass
```

- 规范的列表
- 混用的列表符号

[有效链接](https://example.com)
```

---

## 场景七：自定义配置美化

### 配置文件 (my_config.yaml)
```yaml
beautify:
  add_emoji: false          # 不使用 emoji
  add_dividers: true        # 使用分割线
  beautify_code_blocks: true
  optimize_headers: true
  
output:
  output_dir: "custom_output"
  add_suffix: true
  suffix: "_v2"
```

### 运行命令
```bash
python main.py document.md -c my_config.yaml
```

### 结果
```
✓ 已加载配置文件：my_config.yaml
📄 处理文件：document.md
✨ 美化完成！
✓ 文件已保存：custom_output/document_v2.md
```

---

## 场景八：对比不同风格

### 同一段落的不同风格

**原文：**
```markdown
注意事项
1. 第一点
2. 第二点
3. 第三点
```

**Default 风格:**
```markdown
## ⚠️ 注意事项

1. ✅ 第一点
2. ✅ 第二点
3. ✅ 第三点
```

**Minimal 风格:**
```markdown
## 注意事项

1. 第一点
2. 第二点
3. 第三点
```

**Colorful 风格:**
```markdown
## 🚨 注意事项

- 🔴 第一点
- 🟡 第二点
- 🟢 第三点
```

**Professional 风格:**
```markdown
## 📋 注意事项

> **重要提示：**
> 1. 第一点
> 2. 第二点
> 3. 第三点
```

---

## 🎯 最佳实践

### 1. 先测试后批量
```bash
# 先用小文件测试效果
python main.py sample.md --style colorful

# 确认效果后再批量处理
python main.py ./docs
```

### 2. 保留备份
```yaml
# config.yaml
output:
  keep_backup: true  # 开启备份
```

### 3. 分风格处理
```bash
# 技术文档用专业风格
python main.py api_docs.md --style professional

# 教程用彩色风格
python main.py tutorial.md --style colorful

# README 用默认风格
python main.py README.md
```

### 4. 检查日志
```bash
# 查看处理日志
cat beautify.log

# 或实时查看
tail -f beautify.log
```

---

## 🎨 创意用法

### 1. 制作精美的电子书
```bash
python main.py book_chapter1.md --style colorful
python main.py book_chapter2.md --style colorful
```

### 2. 优化项目文档
```bash
python main.py ./project/docs --style default
```

### 3. 准备演讲材料
```bash
python main.py presentation_notes.md --style colorful
```

### 4. 整理会议纪要
```bash
python main.py meeting_notes.md --style minimal
```

---

## 💡 小贴士

1. **API 费用控制**: 使用 `--quick` 模式减少 token 消耗
2. **网络不稳定**: 增加 `REQUEST_TIMEOUT` 值
3. **保持风格一致**: 同一项目使用相同配置
4. **版本控制**: 将美化后的文件提交到 Git
5. **自动化**: 编写脚本批量处理

---

**现在就开始美化你的文档吧！** ✨
