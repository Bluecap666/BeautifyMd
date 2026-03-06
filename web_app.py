"""
Web UI 后端 - Flask 应用
提供 Markdown 文档美化的 Web 界面
"""
import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid
from datetime import datetime

from config import get_config
from file_handler import FileHandler
from ai_beautifier import AIBeautifier


# 初始化 Flask 应用
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大 16MB
CORS(app)  # 允许跨域请求

# 配置上传文件夹
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('outputs')
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['OUTPUT_FOLDER'] = str(OUTPUT_FOLDER)

# 初始化配置和处理器
config = get_config()
file_handler = FileHandler(config)


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/models', methods=['GET'])
def get_models():
    """获取可用的模型列表"""
    try:
        models = config.get_available_models()
        return jsonify({
            'success': True,
            'models': models,
            'default_model': config.model
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config', methods=['POST'])
def update_config():
    """更新 API 配置"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': '无效数据'}), 400
        
        # 更新环境变量（临时生效，仅当前会话）
        if 'openai_key' in data and data['openai_key']:
            os.environ['OPENAI_API_KEY'] = data['openai_key']
        
        if 'dashscope_key' in data and data['dashscope_key']:
            os.environ['DASHSCOPE_API_KEY'] = data['dashscope_key']
        
        if 'qianfan_ak' in data and data['qianfan_ak']:
            os.environ['QIANFAN_AK'] = data['qianfan_ak']
        
        if 'qianfan_sk' in data and data['qianfan_sk']:
            os.environ['QIANFAN_SK'] = data['qianfan_sk']
        
        if 'spark_key' in data and data['spark_key']:
            os.environ['SPARK_API_KEY'] = data['spark_key']
        
        if 'zhipu_key' in data and data['zhipu_key']:
            os.environ['ZHIPU_API_KEY'] = data['zhipu_key']
        
        if 'hunyuan_key' in data and data['hunyuan_key']:
            os.environ['HUNYUAN_API_KEY'] = data['hunyuan_key']
        
        # 重新加载配置
        global config, file_handler, ai_beautifier
        from config import reload_config
        config = reload_config()
        file_handler = FileHandler(config)
        
        print("✅ API 配置已更新")
        
        return jsonify({
            'success': True,
            'message': '配置已保存，当前会话有效'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/beautify', methods=['POST'])
def beautify():
    """美化 Markdown 文档"""
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '未找到上传文件'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '未选择文件'
            }), 400
        
        # 获取模型参数
        model = request.form.get('model', config.model)
        style = request.form.get('style', 'default')
        
        print(f"\n收到美化请求:")
        print(f"  文件：{file.filename}")
        print(f"  模型：{model}")
        print(f"  风格：{style}")
        
        # 验证文件类型
        if not file.filename.lower().endswith('.md'):
            return jsonify({
                'success': False,
                'error': '只支持 Markdown (.md) 文件'
            }), 400
        
        # 保存上传的文件
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]
        saved_filename = f"{unique_id}_{filename}"
        filepath = UPLOAD_FOLDER / saved_filename
        file.save(str(filepath))
        
        print(f"  文件已保存：{filepath}")
        
        # 读取文件内容
        content = file_handler.read_file(str(filepath))
        print(f"  文件大小：{len(content)} 字符")
        
        # 检查模型的 API 密钥
        api_key, base_url = config.get_model_api_key(model)
        if not api_key:
            error_msg = f"模型 {model} 的 API 密钥未配置。请在 .env 文件中配置对应的密钥。"
            print(f"❌ 错误：{error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        print(f"  使用 API: {base_url}")
        
        # 创建 AI 美化器（使用指定模型）
        print(f"  正在初始化 AI 美化器...")
        ai_beautifier = AIBeautifier(config, model=model)
        
        # 美化内容
        options = {
            'add_emoji': True,
            'add_dividers': True,
            'beautify_code_blocks': True,
            'optimize_headers': True,
        }
        
        print(f"  正在调用 AI 进行美化...")
        beautified_content = ai_beautifier.beautify(content, options)
        print(f"  ✓ 美化完成")
        
        # 保存美化后的文件
        output_filename = f"beautified_{saved_filename}"
        output_path = OUTPUT_FOLDER / output_filename
        file_handler.write_file(str(output_path), beautified_content)
        
        # 返回结果
        return jsonify({
            'success': True,
            'message': '美化成功',
            'original_filename': filename,
            'output_filename': output_filename,
            'download_url': f'/api/download/{output_filename}',
            'model_used': model,
            'style_used': style
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n❌ 美化失败:")
        print(f"  错误：{str(e)}")
        print(f"  详情:\n{error_details}")
        
        return jsonify({
            'success': False,
            'error': f'处理失败：{str(e)}',
            'details': error_details if app.debug else None
        }), 500


@app.route('/api/beautify-text', methods=['POST'])
def beautify_text():
    """美化文本内容（直接输入 Markdown 文本）"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': '未提供内容'
            }), 400
        
        content = data['content']
        model = data.get('model', config.model)
        style = data.get('style', 'default')
        
        # 创建 AI 美化器
        ai_beautifier = AIBeautifier(config, model=model)
        
        # 美化内容
        options = {
            'add_emoji': True,
            'add_dividers': True,
            'beautify_code_blocks': True,
            'optimize_headers': True,
        }
        
        beautified_content = ai_beautifier.beautify(content, options)
        
        return jsonify({
            'success': True,
            'message': '美化成功',
            'content': beautified_content,
            'model_used': model,
            'style_used': style
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'处理失败：{str(e)}'
        }), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download(filename):
    """下载美化后的文件"""
    try:
        filepath = OUTPUT_FOLDER / filename
        
        if not filepath.exists():
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404
        
        return send_file(
            str(filepath),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'下载失败：{str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天功能"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': '消息不能为空'
            }), 400
        
        message = data['message']
        model = data.get('model', config.model)
        system_prompt = data.get('system_prompt', '')
        
        # 获取当前日期，让 AI 知道今天是什么时候
        from datetime import datetime
        current_date = datetime.now().strftime('%Y年%m月%d日 %A')
        
        print(f"\n收到聊天请求:")
        print(f"  模型：{model}")
        print(f"  消息：{message[:50]}...")
        print(f"  当前日期：{current_date}")
        
        # 检查 API 密钥
        api_key, base_url = config.get_model_api_key(model)
        if not api_key:
            error_msg = f'模型 {model} 的 API 密钥未配置。请在 .env 文件中配置对应的密钥。'
            print(f"❌ 错误：{error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        # 创建 AI 实例
        ai = AIBeautifier(config, model=model)
        
        # 构建更智能的系统提示词（包含当前日期）
        enhanced_system_prompt = f"""你是一个有帮助的 AI 助手。
今天是{current_date}。
请用中文友好地回答用户的问题。
{system_prompt}"""
        
        # 根据模型类型分别处理
        if model.startswith('qwen-'):
            # DashScope SDK 聊天模式
            import dashscope
            from dashscope import Generation
            
            print(f"  使用 DashScope SDK 聊天模式...")
            
            messages = [
                {"role": "system", "content": enhanced_system_prompt},
                {"role": "user", "content": message}
            ]
            
            response = Generation.call(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
            )
            
            # 解析响应
            if hasattr(response, 'output') and hasattr(response.output, 'text'):
                result = response.output.text.strip()
            elif hasattr(response, 'text'):
                result = response.text.strip()
            else:
                result = str(response).strip()
                
        else:
            # OpenAI 兼容接口
            print(f"  使用 OpenAI 兼容接口聊天模式...")
            
            response = ai.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": enhanced_system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=2048,
            )
            
            result = response.choices[0].message.content.strip()
        
        print(f"  回复：{result[:100]}...")
        
        return jsonify({
            'success': True,
            'message': message,
            'response': result,
            'model': model,
            'date': current_date
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n❌ 聊天失败:")
        print(f"  错误：{str(e)}")
        print(f"  详情:\n{error_details}")
        
        return jsonify({
            'success': False,
            'error': str(e),
            'details': error_details if app.debug else None
        }), 500


@app.errorhandler(413)
def too_large(e):
    """文件过大错误"""
    return jsonify({
        'success': False,
        'error': '文件过大，最大支持 16MB'
    }), 413


@app.errorhandler(500)
def server_error(e):
    """服务器错误"""
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════╗
║                                                      ║
║     MD BeautifyArts - Web UI Server                  ║
║                                                      ║
║     🚀 服务已启动                                    ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
    
    访问地址：http://localhost:5000
    API 文档：http://localhost:5000/api/health
    
    按 Ctrl+C 停止服务
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
