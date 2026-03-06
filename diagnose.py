"""
Web UI 错误诊断工具
"""
import os
from pathlib import Path
from dotenv import load_dotenv

print("=" * 70)
print("MD BeautifyArts - Web UI 错误诊断工具")
print("=" * 70)

# 1. 检查 .env 文件
print("\n1️⃣  检查 .env 文件...")
env_file = Path('.env')
if env_file.exists():
    print(f"   ✓ .env 文件存在：{env_file.absolute()}")
    load_dotenv()
    
    # 检查各个 API 密钥
    print("\n2️⃣  检查 API 密钥配置:")
    api_keys = {
        'OpenAI': os.getenv('OPENAI_API_KEY'),
        '通义千问': os.getenv('DASHSCOPE_API_KEY'),
        '文心一言': os.getenv('QIANFAN_AK'),
        '讯飞星火': os.getenv('SPARK_API_KEY'),
        '智谱 AI': os.getenv('ZHIPU_API_KEY'),
        '腾讯混元': os.getenv('HUNYUAN_API_KEY'),
    }
    
    for provider, key in api_keys.items():
        if key and key != f'your_{provider.lower()}_key_here' and 'your_' not in key:
            print(f"   ✓ {provider}: 已配置 ({key[:10]}...)")
        else:
            print(f"   ✗ {provider}: 未配置或使用占位符")
else:
    print(f"   ❌ .env 文件不存在！请复制 .env.example 并改名")

# 3. 检查默认模型
print("\n3️⃣  检查默认模型:")
default_model = os.getenv('DEFAULT_MODEL', 'gpt-3.5-turbo')
print(f"   当前默认模型：{default_model}")

# 检查该模型的 API 密钥
model_providers = {
    'gpt-3.5-turbo': 'OpenAI',
    'gpt-4': 'OpenAI',
    'qwen-turbo': '通义千问',
    'qwen-plus': '通义千问',
    'qwen-max': '通义千问',
    'ernie-bot': '文心一言',
    'spark-v3.5': '讯飞星火',
    'chatglm_pro': '智谱 AI',
    'hunyuan-lite': '腾讯混元',
}

if default_model in model_providers:
    provider = model_providers[default_model]
    key = api_keys.get(provider)
    if key and 'your_' not in key:
        print(f"   ✓ 模型 {default_model} 的 API 密钥已配置")
    else:
        print(f"   ⚠️  警告：模型 {default_model} ({provider}) 的 API 密钥未配置！")
        print(f"      请在 .env 文件中配置 {provider} 的 API 密钥")

# 4. 检查上传目录
print("\n4️⃣  检查目录结构:")
directories = {
    'uploads': Path('uploads'),
    'outputs': Path('outputs'),
    'templates': Path('templates'),
    'static': Path('static'),
}

for name, path in directories.items():
    if path.exists():
        print(f"   ✓ {name}/ 目录存在")
    else:
        print(f"   ⚠️  {name}/ 目录不存在（会自动创建）")

# 5. 检查依赖
print("\n5️⃣  检查 Flask 依赖:")
try:
    import flask
    print(f"   ✓ Flask 已安装 (版本：{flask.__version__})")
except ImportError:
    print(f"   ❌ Flask 未安装！运行：pip install flask flask-cors")

try:
    import flask_cors
    print(f"   ✓ Flask-CORS 已安装")
except ImportError:
    print(f"   ❌ Flask-CORS 未安装！运行：pip install flask-cors")

# 6. 常见问题检查
print("\n6️⃣  常见问题检查:")

# 检查是否使用占位符
with open('.env', 'r', encoding='utf-8') as f:
    env_content = f.read()
    
placeholder_patterns = [
    'your_dashscope_key_here',
    'your_api_key_here',
    'your_qianfan_ak_here',
    'your_spark_key_here',
]

found_placeholders = []
for pattern in placeholder_patterns:
    if pattern in env_content:
        found_placeholders.append(pattern)

if found_placeholders:
    print(f"   ⚠️  发现占位符（需要替换为真实密钥）:")
    for ph in found_placeholders:
        print(f"      - {ph}")
else:
    print(f"   ✓ 未发现占位符")

# 总结
print("\n" + "=" * 70)
print("诊断完成！")
print("=" * 70)

if found_placeholders:
    print("\n❌ 发现问题：")
    print("   .env 文件中使用了占位符，需要替换为真实的 API 密钥")
    print("\n解决方法：")
    print("   1. 打开 .env 文件")
    print("   2. 将占位符替换为真实的 API 密钥")
    print("   3. 保存并重启 Web 服务")
elif not api_keys.get('通义千问'):
    print("\n⚠️  警告：通义千问 API 密钥未配置")
    print("\n如果要使用通义千问模型：")
    print("   1. 访问 https://dashscope.console.aliyun.com/")
    print("   2. 登录并创建 API Key")
    print("   3. 复制到 .env 文件的 DASHSCOPE_API_KEY 字段")
else:
    print("\n✅ 配置看起来正常！")
    print("\n如果仍然报错，请查看：")
    print("   1. Web 服务终端的详细错误信息")
    print("   2. 浏览器控制台的 JavaScript 错误")
    print("   3. 网络请求的具体响应内容")

print("\n建议的调试步骤：")
print("   1. 确保 .env 配置正确")
print("   2. 重启 Web 服务：python web_app.py")
print("   3. 查看终端输出的详细错误信息")
print("   4. 尝试上传小文件测试")
print("")
