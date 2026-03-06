# 🤖 多模型支持指南

MD BeautifyArts v2.0 新增支持多种主流 AI 大模型，包括国内外的知名模型服务。

---

## 📋 支持的模型列表

### OpenAI 系列（国际）
| 模型 | 说明 | 特点 |
|------|------|------|
| `gpt-3.5-turbo` | GPT-3.5 Turbo | 快速、经济、性能好 |
| `gpt-4` | GPT-4 | 最强性能，适合复杂任务 |
| `gpt-4-turbo` | GPT-4 Turbo | GPT-4 的快速版本 |

**配置方式：**
```ini
# .env 文件
OPENAI_API_KEY=sk-你的密钥
OPENAI_API_BASE_URL=https://api.openai.com/v1
```

---

### 通义千问（阿里云）
| 模型 | 说明 | 特点 |
|------|------|------|
| `qwen-turbo` | 通义千问 Turbo | 速度快，成本低 |
| `qwen-plus` | 通义千问 Plus | 性能均衡 |
| `qwen-max` | 通义千问 Max | 最强性能 |

**配置方式：**
```ini
# .env 文件
DASHSCOPE_API_KEY=你的 DashScope 密钥
```

**获取密钥：**
1. 访问 [阿里云 DashScope](https://dashscope.aliyun.com/)
2. 注册/登录阿里云账号
3. 开通 DashScope 服务
4. 在控制台创建 API Key

---

### 文心一言（百度）
| 模型 | 说明 | 特点 |
|------|------|------|
| `ernie-bot` | 文心一言 | 标准版 |
| `ernie-bot-turbo` | 文心一言 Turbo | 快速版 |

**配置方式：**
```ini
# .env 文件
QIANFAN_AK=你的 Access Key
QIANFAN_SK=你的 Secret Key
```

**获取密钥：**
1. 访问 [百度智能云千帆](https://cloud.baidu.com/product/wenxinworkshop)
2. 注册/登录百度账号
3. 创建应用获取 AK/SK

---

### 讯飞星火（科大讯飞）
| 模型 | 说明 | 特点 |
|------|------|------|
| `spark-v3.5` | 讯飞星火 V3.5 | 最新版本 |
| `spark-v3.0` | 讯飞星火 V3.0 | 稳定版本 |

**配置方式：**
```ini
# .env 文件
SPARK_API_KEY=你的讯飞 API 密钥
```

**获取密钥：**
1. 访问 [讯飞开放平台](https://www.xfyun.cn/)
2. 注册/登录讯飞账号
3. 创建应用获取 API Key

---

### 智谱 AI（清华系）
| 模型 | 说明 | 特点 |
|------|------|------|
| `chatglm_pro` | ChatGLM Pro | 专业版 |
| `chatglm_std` | ChatGLM Std | 标准版 |
| `chatglm_lite` | ChatGLM Lite | 轻量版 |

**配置方式：**
```ini
# .env 文件
ZHIPU_API_KEY=你的智谱 API 密钥
```

**获取密钥：**
1. 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)
2. 注册/登录账号
3. 创建 API Key

---

### 腾讯混元（腾讯）
| 模型 | 说明 | 特点 |
|------|------|------|
| `hunyuan-lite` | 混元 Lite | 轻量版 |
| `hunyuan-standard` | 混元 Standard | 标准版 |

**配置方式：**
```ini
# .env 文件
HUNYUAN_API_KEY=你的腾讯 API 密钥
```

**获取密钥：**
1. 访问 [腾讯云混元](https://cloud.tencent.com/product/hunyuan)
2. 注册/登录腾讯账号
3. 开通服务并获取密钥

---

## ⚙️ 配置方法

### 方法一：编辑 .env 文件

1. 复制示例文件：
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

2. 编辑 `.env` 文件，填入你需要的模型密钥：
```ini
# 选择你要使用的模型并配置对应密钥

# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxx

# 或者使用国内模型
DASHSCOPE_API_KEY=xxxxx  # 通义千问
QIANFAN_AK=xxxxx         # 文心一言
QIANFAN_SK=xxxxx
SPARK_API_KEY=xxxxx      # 讯飞星火
ZHIPU_API_KEY=xxxxx      # 智谱 AI
HUNYUAN_API_KEY=xxxxx    # 腾讯混元

# 默认使用的模型
DEFAULT_MODEL=gpt-3.5-turbo
```

### 方法二：通过 Web UI 选择

启动 Web 服务后，可以在界面上直接选择要使用的模型。

---

## 🚀 使用方式

### 命令行模式

#### 使用不同模型
```bash
# 使用 GPT-3.5（默认）
python main.py document.md

# 使用通义千问
python main.py document.md -c config_qwen.yaml

# 使用文心一言
python main.py document.md -c config_ernie.yaml
```

#### 自定义配置文件
为不同模型创建独立的配置文件：

**config_qwen.yaml:**
```yaml
beautify:
  add_emoji: true
  add_dividers: true

file_processing:
  split_threshold: 50000
  chunk_size: 5000
```

然后在 `.env` 中配置对应的密钥，设置 `DEFAULT_MODEL=qwen-turbo`

### Web UI 模式

1. 启动 Web 服务：
```bash
python web_app.py
```

2. 访问 http://localhost:5000

3. 在界面上：
   - 从下拉菜单选择要使用的模型
   - 上传 Markdown 文件或输入文本
   - 点击"开始美化"按钮

---

## 💡 模型选择建议

### 按需求选择

**追求最佳效果：**
- ✅ GPT-4
- ✅ 通义千问 Max
- ✅ 文心一言

**追求性价比：**
- ✅ GPT-3.5 Turbo
- ✅ 通义千问 Turbo
- ✅ ChatGLM Lite

**支持中文场景：**
- ✅ 通义千问系列
- ✅ 文心一言系列
- ✅ 讯飞星火系列

**国内访问速度：**
- ✅ 通义千问（阿里云）
- ✅ 文心一言（百度）
- ✅ 讯飞星火（科大讯飞）

### 各模型对比

| 模型 | 速度 | 质量 | 成本 | 中文能力 |
|------|------|------|------|----------|
| GPT-3.5 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GPT-4 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 通义千问 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 文心一言 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 讯飞星火 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| ChatGLM | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 腾讯混元 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🔍 查看可用模型

### 命令行查看
```bash
python -c "from config import get_config; c = get_config(); models = c.get_available_models(); print('\n'.join([f\"{m['id']}: {m['name']} ({m['provider']}) - {'可用' if m['available'] else '未配置'}\" for m in models]))"
```

### Web UI 查看
启动 Web 服务后，在下拉菜单中会自动显示已配置可用的模型。

---

## ⚠️ 常见问题

### Q1: 如何切换模型？
**A:** 
- **命令行模式**: 修改 `.env` 中的 `DEFAULT_MODEL`
- **Web UI 模式**: 直接在界面下拉菜单选择

### Q2: 多个模型密钥都要配置吗？
**A:** 不需要。只配置你打算使用的模型密钥即可。

### Q3: 国内模型需要特殊配置吗？
**A:** 国内模型通常有各自的 API 地址，系统已自动配置，无需手动设置。

### Q4: 可以使用自己的代理吗？
**A:** 可以，配置环境变量：
```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
```

### Q5: 模型报错怎么办？
**A:** 
1. 检查 API 密钥是否正确
2. 确认账户余额充足
3. 查看网络是否通畅
4. 检查模型是否已开通

---

## 📊 计费说明

### OpenAI
- GPT-3.5 Turbo: $0.002 / 1K tokens
- GPT-4: $0.03 / 1K tokens (输入)

### 通义千问
- Qwen-Turbo: ¥0.008 / 1K tokens
- Qwen-Plus: ¥0.02 / 1K tokens

### 文心一言
- ERNIE-Bot: ¥0.012 / 1K tokens

### 其他模型
请参考各平台官方定价。

---

## 🎯 最佳实践

### 1. 先用小文件测试
```bash
# 用小文件测试效果
python main.py test.md
```

### 2. 批量处理前验证
确保模型配置正确后再批量处理。

### 3. 监控使用情况
定期查看各平台的用量统计。

### 4. 合理选择模型
根据文档重要性和预算选择合适的模型。

---

## 🔗 相关链接

- [OpenAI 平台](https://platform.openai.com/)
- [阿里云 DashScope](https://dashscope.aliyun.com/)
- [百度千帆大模型](https://cloud.baidu.com/product/wenxinworkshop)
- [讯飞开放平台](https://www.xfyun.cn/)
- [智谱 AI](https://open.bigmodel.cn/)
- [腾讯混元](https://cloud.tencent.com/product/hunyuan)

---

**祝你使用愉快！如有问题请查阅文档或提交 Issue。** ✨
