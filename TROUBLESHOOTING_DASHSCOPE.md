# 🔧 通义千问配置问题解决指南

## ❌ 常见错误

### 错误现象
配置了通义千问 API 密钥但仍然报错。

---

## ✅ 解决步骤

### 步骤 1: 检查 .env 文件

打开项目根目录的 `.env` 文件，检查以下配置：

```ini
# ========== 错误的配置（使用占位符）==========
DASHSCOPE_API_KEY=your_dashscope_key_here  # ❌ 这是占位符！
DEFAULT_MODEL=gpt-3.5-turbo                # ❌ 默认还是 OpenAI

# ========== 正确的配置 ==========
DASHSCOPE_API_KEY=sk-your-real-api-key-here  # ✅ 填入真实密钥
DEFAULT_MODEL=qwen-turbo                     # ✅ 切换到通义千问
```

### 步骤 2: 获取真实的 API 密钥

1. **访问阿里云 DashScope 控制台**
   - 网址：https://dashscope.console.aliyun.com/
   
2. **登录/注册阿里云账号**

3. **开通 DashScope 服务**
   - 首次使用需要开通
   - 有免费额度

4. **创建 API Key**
   - 进入"API Key 管理"
   - 点击"创建新的 API Key"
   - 复制生成的密钥

5. **粘贴到 .env 文件**
   ```ini
   DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 步骤 3: 切换默认模型

在 `.env` 文件中修改：

```ini
# 将默认模型改为通义千问
DEFAULT_MODEL=qwen-turbo    # 或 qwen-plus, qwen-max
```

**可选的通义千问模型：**
- `qwen-turbo` - 快速版（推荐测试）
- `qwen-plus` - 增强版（推荐日常使用）
- `qwen-max` - 最强版（复杂任务）

### 步骤 4: 验证配置

运行测试脚本：

```bash
python test_config.py
```

**预期输出：**
```
============================================================
配置加载测试结果
============================================================

OpenAI API Key: ✗ 未配置
通义千问 API Key: ✓ 已配置      # ✅ 应该显示已配置
文心一言 API Key: ✗ 未配置
...

默认模型：qwen-turbo            # ✅ 应该显示 qwen-turbo

可用模型列表:
  gpt-3.5-turbo      - GPT-3.5 Turbo          [✗ 未配置]
  qwen-turbo         - 通义千问 Turbo          [✓ 可用]    # ✅ 应该显示可用
  qwen-plus          - 通义千问 Plus           [✓ 可用]
  ...
```

### 步骤 5: 测试使用

#### 方式一：命令行模式
```bash
# 使用默认模型（qwen-turbo）
python main.py test_document.md

# 或指定模型
python main.py test_document.md --model qwen-plus
```

#### 方式二：Web UI 模式
```bash
# 启动 Web 服务
python web_app.py

# 访问 http://localhost:5000
# 在下拉菜单中选择"通义千问 Turbo"或其他模型
```

---

## 🐛 其他可能的错误

### 错误 1: ModuleNotFoundError
```
No module named 'dashscope'
```

**解决：**
```bash
pip install dashscope
```

### 错误 2: Invalid API Key
```
Invalid API key provided
```

**原因：**
- API 密钥格式错误
- 密钥未正确复制
- 密钥已过期

**解决：**
1. 重新登录 DashScope 控制台
2. 重新创建 API Key
3. 确保完整复制（包含 `sk-` 前缀）

### 错误 3: Network Error
```
Network error, please check your connection
```

**原因：**
- 网络连接问题
- 需要代理

**解决：**
```bash
# 如果需要代理
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
```

### 错误 4: Model Not Found
```
Model qwen-turbo not found
```

**原因：**
- 模型名称拼写错误
- 该模型未开通

**解决：**
1. 检查模型名称是否正确
2. 在控制台确认已开通该模型

---

## 📝 完整的 .env 配置示例

```ini
# .env 文件完整配置

# OpenAI（如果不用可以注释掉）
# OPENAI_API_KEY=sk-...
# OPENAI_API_BASE_URL=https://api.openai.com/v1

# 通义千问（必须配置）
DASHSCOPE_API_KEY=sk-你的真实密钥

# 其他模型（不用的话可以注释掉）
# QIANFAN_AK=...
# QIANFAN_SK=...
# SPARK_API_KEY=...
# ZHIPU_API_KEY=...
# HUNYUAN_API_KEY=...

# 默认使用通义千问
DEFAULT_MODEL=qwen-turbo

# 其他配置
REQUEST_TIMEOUT=120
MAX_RETRIES=3
```

---

## 🎯 快速验证清单

使用前请确认：

- [ ] `.env` 文件存在
- [ ] `DASHSCOPE_API_KEY` 已填入真实密钥（不是占位符）
- [ ] `DEFAULT_MODEL` 设置为通义千问模型
- [ ] 运行 `python test_config.py` 显示"✓ 已配置"
- [ ] 通义千问模型显示"✓ 可用"

---

## 💡 使用建议

### 1. 先用免费额度测试
通义千问提供新用户免费额度，先测试效果。

### 2. 选择合适的模型
- 快速测试：`qwen-turbo`
- 日常使用：`qwen-plus`
- 高质量要求：`qwen-max`

### 3. 监控用量
定期查看 DashScope 控制台的用量统计。

### 4. 备份配置
```bash
cp .env .env.backup
```

---

## 🔗 相关链接

- [DashScope 控制台](https://dashscope.console.aliyun.com/)
- [通义千问文档](https://help.aliyun.com/zh/dashscope/)
- [API 参考](https://help.aliyun.com/zh/dashscope/developer-reference/api-reference)

---

## ❓ 仍然有问题？

1. **检查报错信息**
   - 仔细阅读完整的错误提示
   - 查看是哪一步出错

2. **查看日志**
   ```bash
   # 查看详细日志
   cat beautify.log
   ```

3. **重新配置**
   - 删除 `.env` 文件
   - 重新复制 `.env.example`
   - 重新填写配置

4. **联系支持**
   - 提交 Issue
   - 提供完整错误信息

---

**祝你使用顺利！** ✨
