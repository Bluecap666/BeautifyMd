"""
配置管理模块
负责加载和管理系统配置
"""
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, Optional


class Config:
    """配置管理类"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置
        
        Args:
            config_file: 配置文件路径，默认为 config.yaml
        """
        # 加载环境变量
        load_dotenv()
        
        # 默认配置
        self.default_config = {
            'beautify': {
                'add_emoji': True,
                'add_dividers': True,
                'beautify_code_blocks': True,
                'optimize_headers': True,
                'add_quote_styles': True,
                'beautify_lists': True,
                'beautify_tables': True,
                'add_emphasis': True,
            },
            'file_processing': {
                'split_threshold': 50000,  # 50KB
                'chunk_size': 5000,
                'chunk_overlap': 200,
            },
            'output': {
                'output_dir': 'beautified',
                'add_suffix': True,
                'suffix': '_beautified',
                'keep_backup': False,
            },
            'logging': {
                'level': 'INFO',
                'save_to_file': True,
                'log_file': 'beautify.log',
            }
        }
        
        # 加载配置文件
        if config_file is None:
            config_file = 'config.yaml'
        
        self.config_file = Path(config_file)
        self.config = self._load_config()
        
        # API 配置
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_base_url = os.getenv('OPENAI_API_BASE_URL', 'https://api.openai.com/v1')
        self.model = os.getenv('DEFAULT_MODEL', 'gpt-3.5-turbo')
        self.timeout = int(os.getenv('REQUEST_TIMEOUT', '120'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        
        # 国内大模型 API 密钥
        self.dashscope_api_key = os.getenv('DASHSCOPE_API_KEY')  # 通义千问
        self.qianfan_ak = os.getenv('QIANFAN_AK')  # 文心一言
        self.qianfan_sk = os.getenv('QIANFAN_SK')  # 文心一言
        self.spark_api_key = os.getenv('SPARK_API_KEY')  # 讯飞星火
        self.zhipu_api_key = os.getenv('ZHIPU_API_KEY')  # 智谱 AI
        self.hunyuan_api_key = os.getenv('HUNYUAN_API_KEY')  # 腾讯混元
        self.doubao_api_key = os.getenv('DOUBAO_API_KEY')  # 豆包大模型
        
        # 模型信息映射
        self.model_providers = {
            # OpenAI 系列
            'gpt-3.5-turbo': {'provider': 'OpenAI', 'name': 'GPT-3.5 Turbo'},
            'gpt-4': {'provider': 'OpenAI', 'name': 'GPT-4'},
            'gpt-4-turbo': {'provider': 'OpenAI', 'name': 'GPT-4 Turbo'},
            
            # 通义千问（阿里云）
            'qwen-turbo': {'provider': 'DashScope', 'name': '通义千问 Turbo'},
            'qwen-plus': {'provider': 'DashScope', 'name': '通义千问 Plus'},
            'qwen-max': {'provider': 'DashScope', 'name': '通义千问 Max'},
            
            # 文心一言（百度）
            'ernie-bot': {'provider': 'Qianfan', 'name': '文心一言'},
            'ernie-bot-turbo': {'provider': 'Qianfan', 'name': '文心一言 Turbo'},
            
            # 讯飞星火
            'spark-v3.5': {'provider': 'Spark', 'name': '讯飞星火 V3.5'},
            'spark-v3.0': {'provider': 'Spark', 'name': '讯飞星火 V3.0'},
            
            # 智谱 AI
            'chatglm_pro': {'provider': 'Zhipu', 'name': 'ChatGLM Pro'},
            'chatglm_std': {'provider': 'Zhipu', 'name': 'ChatGLM Std'},
            'chatglm_lite': {'provider': 'Zhipu', 'name': 'ChatGLM Lite'},
            
            # 腾讯混元
            'hunyuan-lite': {'provider': 'Hunyuan', 'name': '腾讯混元 Lite'},
            'hunyuan-standard': {'provider': 'Hunyuan', 'name': '腾讯混元 Standard'},
            
            # 豆包大模型（字节）
            'doubao-pro': {'provider': 'Doubao', 'name': '豆包大模型 Pro'},
            'doubao-lite': {'provider': 'Doubao', 'name': '豆包大模型 Lite'},
        }
        
        # 验证 API 密钥
        if not self.api_key:
            print("⚠️  警告：未找到 OPENAI_API_KEY，请确保 .env 文件已正确配置")
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        config = self.default_config.copy()
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        # 合并配置
                        self._merge_config(config, file_config)
                print(f"✓ 已加载配置文件：{self.config_file}")
            except Exception as e:
                print(f"⚠️  加载配置文件失败：{e}，使用默认配置")
        else:
            print(f"ℹ️  配置文件不存在：{self.config_file}，使用默认配置")
        
        return config
    
    def _merge_config(self, base: Dict, override: Dict):
        """
        递归合并配置字典
        
        Args:
            base: 基础配置
            override: 覆盖配置
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, *keys, default=None):
        """
        获取配置值
        
        Args:
            *keys: 配置键路径，如 ('beautify', 'add_emoji')
            default: 默认值
            
        Returns:
            配置值
        """
        result = self.config
        for key in keys:
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                return default
        return result
    
    def get_available_models(self) -> list:
        """
        获取可用的模型列表
        
        Returns:
            模型信息列表
        """
        available = []
        
        for model_id, info in self.model_providers.items():
            provider = info['provider']
            
            # 检查对应的 API 密钥是否存在
            has_key = False
            if provider == 'OpenAI' and self.api_key:
                has_key = True
            elif provider == 'DashScope' and self.dashscope_api_key:
                has_key = True
            elif provider == 'Qianfan' and self.qianfan_ak and self.qianfan_sk:
                has_key = True
            elif provider == 'Spark' and self.spark_api_key:
                has_key = True
            elif provider == 'Zhipu' and self.zhipu_api_key:
                has_key = True
            elif provider == 'Hunyuan' and self.hunyuan_api_key:
                has_key = True
            elif provider == 'Doubao' and self.doubao_api_key:
                has_key = True
            
            available.append({
                'id': model_id,
                'name': info['name'],
                'provider': provider,
                'available': has_key
            })
        
        return available
    
    def get_model_api_key(self, model: str) -> tuple:
        """
        根据模型获取对应的 API 密钥和基础 URL
        
        Args:
            model: 模型 ID
            
        Returns:
            (api_key, base_url) 元组
        """
        if model not in self.model_providers:
            return self.api_key, self.api_base_url
        
        provider = self.model_providers[model]['provider']
        
        if provider == 'OpenAI':
            return self.api_key, self.api_base_url
        elif provider == 'DashScope':
            return self.dashscope_api_key, 'https://dashscope.aliyuncs.com/api/v1'
        elif provider == 'Qianfan':
            return self.qianfan_ak, 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1'
        elif provider == 'Spark':
            return self.spark_api_key, 'https://spark-api-open.xf-yun.com/v1'
        elif provider == 'Zhipu':
            return self.zhipu_api_key, 'https://open.bigmodel.cn/api/paas/v4'
        elif provider == 'Hunyuan':
            return self.hunyuan_api_key, 'https://hunyuan.tencentcloudapi.com'
        elif provider == 'Doubao':
            return self.doubao_api_key, 'https://ark.cn-beijing.volces.com/api/v3'  # 豆包 API 地址
        
        return self.api_key, self.api_base_url
    
    def save_config(self, filepath: str):
        """
        保存配置到文件
        
        Args:
            filepath: 保存路径
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
        print(f"✓ 配置已保存到：{filepath}")


# 全局配置实例
_config: Optional[Config] = None


def get_config(config_file: Optional[str] = None) -> Config:
    """
    获取全局配置实例
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        配置实例
    """
    global _config
    if _config is None:
        _config = Config(config_file)
    return _config


def reload_config(config_file: Optional[str] = None) -> Config:
    """
    重新加载配置
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        新的配置实例
    """
    global _config
    _config = Config(config_file)
    return _config
