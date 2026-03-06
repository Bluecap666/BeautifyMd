# 🔧 Web UI 500 错误排查指南

## 📋 当前配置状态

✅ 已确认的配置：
- 通义千问 API 密钥：已配置 (`sk-e4f5487...`)
- 默认模型：`qwen-turbo`
- Flask 依赖：已安装
- 目录结构：完整

---

## 🔍 500 错误的可能原因

### 原因 1: API 密钥格式问题 ⭐⭐⭐⭐⭐
**最可能的原因！**

虽然 `.env` 中有密钥，但可能是：
1. **密钥已过期或无效**
2. **密钥没有开通服务**
3. **密钥余额不足**

**验证方法：**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('DASHSCOPE_API_KEY'))"
```

检查输出是否完整显示密钥。

---

### 原因 2: DashScope SDK 未安装 ⭐⭐⭐⭐

通义千问需要安装专门的 SDK：

**解决：**
```bash
pip install dashscope
```

---

### 原因 3: OpenAI 客户端初始化问题 ⭐⭐⭐

代码中使用 OpenAI 客户端兼容多种 API，但通义千问的 API 格式可能不兼容。

**查看 web_app.py 中的初始化代码。**

---

### 原因 4: 网络问题 ⭐⭐

无法访问阿里云 API。

**解决：**
```bash
# 如果需要代理
set HTTP_PROXY=http://your-proxy:port
set HTTPS_PROXY=http://your-proxy:port
```

---

## 🚑 立即诊断步骤

### 步骤 1: 查看详细错误信息

重启 Web 服务，然后再次上传文件：

```bash
python web_app.py
```

**终端会显示详细的错误堆栈！**

找到类似这样的输出：
```
❌ 美化失败:
  错误：具体的错误信息
  详情:
  Traceback (most recent call last):
    ...
```

**请把完整的错误信息复制给我！**

---

### 步骤 2: 测试 API 密钥有效性

创建测试脚本 `test_dashscope.py`:

```python
"""
测试通义千问 API
"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('DASHSCOPE_API_KEY')
print(f"API Key: {api_key}")
print(f"Key 长度：{len(api_key)}")
print(f"Key 前缀：{api_key[:10] if api_key else 'None'}")

# 尝试简单调用
try:
    import dashscope
    dashscope.api_key = api_key
    
    # 简单的测试调用
    response = dashscope.Generation.call(
        model='qwen-turbo',
        prompt='你好'
    )
    
    print(f"\n✅ API 调用成功!")
    print(f"响应：{response}")
    
except Exception as e:
    print(f"\n❌ API 调用失败:")
    print(f"错误：{e}")
    import traceback
    traceback.print_exc()
```

运行：
```bash
python test_dashscope.py
```

---

### 步骤 3: 检查 OpenAI 客户端兼容性

在 Python 中测试：

```python
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('DASHSCOPE_API_KEY')
base_url = 'https://dashscope.aliyuncs.com/api/v1'

print(f"尝试初始化 OpenAI 客户端...")
print(f"API Key: {api_key[:10]}...")
print(f"Base URL: {base_url}")

try:
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=120,
        max_retries=3,
    )
    
    print("✅ 客户端初始化成功")
    
    # 尝试简单调用
    response = client.chat.completions.create(
        model='qwen-turbo',
        messages=[{"role": "user", "content": "你好"}]
    )
    
    print(f"✅ API 调用成功: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ 失败：{e}")
    import traceback
    traceback.print_exc()
```

---

## 💡 常见错误及解决方案

### 错误 1: `No module named 'dashscope'`
```bash
pip install dashscope
```

### 错误 2: `Invalid API Key`
- 密钥格式不对
- 密钥已过期
- 密钥未开通服务

**解决：**
1. 重新登录 https://dashscope.console.aliyun.com/
2. 重新创建 API Key
3. 确保账户有余额或免费额度

### 错误 3: `Connection error`
网络连接问题。

**解决：**
检查是否需要代理，或者网络是否通畅。

### 错误 4: `Model not found`
模型名称错误或未开通。

**解决：**
在控制台确认已开通 `qwen-turbo` 模型。

---

## 🎯 快速修复方案

### 方案 A: 安装 DashScope SDK（推荐）

```bash
pip install dashscope
```

然后修改代码使用原生 SDK 而不是 OpenAI 兼容接口。

### 方案 B: 检查 API 格式

通义千问的 API 可能需要特殊的调用方式。

查看官方文档：
https://help.aliyun.com/zh/dashscope/developer-reference/quick-start

### 方案 C: 使用其他模型

如果通义千问有问题，可以临时切换到其他模型测试。

---

## 📝 获取详细错误的脚本

创建 `debug_web.py`:

```python
"""
调试 Web UI 错误
"""
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid

from config import get_config
from file_handler import FileHandler
from ai_beautifier import AIBeautifier

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('outputs')
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

config = get_config()
file_handler = FileHandler(config)

@app.route('/api/beautify', methods=['POST'])
def beautify():
    try:
        file = request.files['file']
        model = request.form.get('model', config.model)
        
        print(f"\n{'='*60}")
        print(f"收到请求:")
        print(f"  文件：{file.filename}")
        print(f"  模型：{model}")
        print(f"{'='*60}")
        
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]
        saved_filename = f"{unique_id}_{filename}"
        filepath = UPLOAD_FOLDER / saved_filename
        
        print(f"保存文件：{filepath}")
        file.save(str(filepath))
        
        content = file_handler.read_file(str(filepath))
        print(f"文件大小：{len(content)} 字符")
        
        # 关键步骤：创建 AI 美化器
        print(f"\n创建 AI 美化器...")
        print(f"  模型：{model}")
        
        api_key, base_url = config.get_model_api_key(model)
        print(f"  API Key: {api_key[:10] if api_key else 'None'}...")
        print(f"  Base URL: {base_url}")
        
        if not api_key:
            raise ValueError(f"模型 {model} 的 API 密钥未配置")
        
        ai_beautifier = AIBeautifier(config, model=model)
        print(f"✅ AI 美化器创建成功")
        
        # 调用美化
        print(f"\n开始美化...")
        beautified_content = ai_beautifier.beautify(content, {
            'add_emoji': True,
            'add_dividers': True,
        })
        print(f"✅ 美化成功")
        
        return jsonify({'success': True, 'message': '成功'})
        
    except Exception as e:
        print(f"\n❌ 失败:")
        print(f"  错误：{str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': str(e),
            'type': type(e).__name__
        }), 500

if __name__ == '__main__':
    print("\n调试服务器启动...")
    print("访问：http://localhost:5000")
    print("\n上传文件后查看详细输出\n")
    app.run(debug=True, port=5001)
```

运行：
```bash
python debug_web.py
```

然后在 http://localhost:5001 上传文件，查看详细的调试信息。

---

## 🆘 仍然无法解决？

请提供以下信息：

1. **完整的错误堆栈**（从终端复制）
2. 运行 `python diagnose.py` 的输出
3. 运行 `python test_dashscope.py` 的输出
4. 你使用的模型名称
5. API Key 的前 10 个字符

这样我可以更准确地帮你定位问题！

---

**下一步行动：**
1. 运行 `python web_app.py` 重新启动服务
2. 上传文件触发错误
3. **复制终端中的完整错误信息**
4. 把错误信息发给我

谢谢！🙏
