"""
AI 美化引擎模块
负责调用 AI API 进行文档美化
"""
import json
from typing import Optional, Dict, Any
from openai import OpenAI
from tqdm import tqdm
import time


class AIBeautifier:
    """AI 美化器类"""
    
    def __init__(self, config, model: str = None):
        """
        初始化 AI 美化器
        
        Args:
            config: 配置对象
            model: 指定使用的模型，None 则使用默认配置
        """
        self.config = config
        self.model = model if model else config.model
        self.max_retries = config.max_retries
        
        # 根据模型获取对应的 API 密钥和 URL
        api_key, base_url = config.get_model_api_key(self.model)
        
        # 初始化 OpenAI 客户端（兼容多种 API）
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=config.timeout,
            max_retries=config.max_retries,
        )
    
    def beautify(self, content: str, options: Optional[Dict] = None) -> str:
        """
        美化 Markdown 文档
        
        Args:
            content: 原始内容
            options: 美化选项
            
        Returns:
            美化后的内容
        """
        if options is None:
            options = {}
        
        # 构建提示词
        prompt = self._build_beautify_prompt(content, options)
        
        # 调用 AI
        response = self._call_ai(prompt)
        
        return response
    
    def _build_beautify_prompt(self, content: str, options: Dict) -> str:
        """
        构建美化提示词
        
        Args:
            content: 原始内容
            options: 美化选项
            
        Returns:
            完整的提示词
        """
        # 基础指令 - 强调完整美化和智能优化
        system_instruction = """你是一个专业的 Markdown 文档美化专家和內容优化顾问。
你的任务是将提供的 Markdown 文档进行美化和优化，使其更加美观、易读和专业，特别适配微信公众号格式。

⚠️ 重要要求：
1. 必须美化整篇文档的每一个部分，不能遗漏任何内容
2. 从第一个字符到最后一个字符都要进行美化
3. 确保文档的完整性，不要删除或跳过任何段落
4. 如果文档很长，请耐心处理每一部分内容
5. 美化后的内容需要适配微信公众号的显示特性

🎯 智能优化职责：
1. **格式检查**：检查文档结构是否合理，必要时进行调整
2. **内容补充**：在适当位置添加过渡句、总结或说明性文字
3. **逻辑优化**：如果内容逻辑不连贯，可以添加衔接内容
4. **示例补充**：在需要的地方可以添加适当的示例或说明
5. **重点标注**：对重要内容添加粗体、斜体等强调标记
6. **结构完善**：如果章节划分不合理，可以适当调整

📋 微信公众号格式要求：
1. **标题**：在文档最开始添加一个吸引人的标题（如：《文章主题：关键技术全解析》）
2. **技术概览列表**：紧随标题之后，使用列表形式展示文章中实际提及的核心技术关键词及简短解释
3. **内容区域**：对每个问题或段落使用淡色背景或边框进行包装
4. **分割线**：使用多样形状和颜色的分割线分隔不同内容块
5. **尾语**：在文档末尾添加总结性尾语或相关引导内容

⚠️ 技术概览关键要求：
- 严格基于原文内容提取技术点，不得凭空创造
- 只能使用文章中明确提及的技术术语、框架、工具或概念
- 若文章中未提及特定技术，则不应出现在概览中
- 对于每个技术点，仅提供文章中相关的简短解释

技术概览列表格式（基于原文内容）：
### 🔍 核心技术概览
- **[原文中提及的技术A]**：[根据原文提供的简短解释]
- **[原文中提及的技术B]**：[根据原文提供的简短解释]  
- **[原文中提及的技术C]**：[根据原文提供的简短解释]

🎨 微信样式美化规则：
1. **内容区域背景/边框**：
   - 使用 HTML/CSS 样式模拟淡色背景块（如使用灰色阴影块）
   - 或使用 Markdown 的引用格式 `>` 来创建视觉上的分隔
   - 也可使用特殊的符号或 emoji 作为内容区域的边框装饰

2. **分割线多样性**：
   - 使用不同颜色或形状的分割线，如：
     ***
     * * *
     ---
     *** 
     或使用重复符号：★★★★★★，✿✿✿✿✿，◇◇◇◇◇
   
3. **视觉层次**：
   - 一级标题使用 H1 或 H2 标签
   - 二级标题使用 H3 或 H4 标签
   - 重要内容使用粗体或高亮标记

📏 间距一致性要求：
1. 确保各章节之间、问题与问题之间有统一的间距
2. 每个独立问题或段落之间只保留一个空行（即一个换行符）
3. 避免出现连续多个空行的情况，保持文档紧凑整洁
4. 对于列表、代码块、引用等特殊格式，保持与其前后内容的间距一致
5. 在处理换行时，确保不会产生多余的空行，维持整体视觉平衡

美化规则：
1. 添加合适的 emoji 表情来增强视觉效果和表达力
2. 在适当位置添加分割线来区分不同章节
3. 优化标题格式，确保层次清晰
4. 美化代码块，添加语言标识
5. 优化列表格式，使用统一的样式
6. 美化表格，确保对齐整齐
7. 添加强调效果（粗体、斜体等）突出重点内容
8. 优化引用块格式
9. 保持原文核心内容不变，可以进行视觉美化和适度的内容优化
10. 确保美化后的文档仍然保持良好的可读性和专业性

请返回美化后的完整 Markdown 内容，不需要额外说明。"""
        
        # 自定义选项
        custom_options = []
        
        if options.get('add_emoji', True):
            custom_options.append("✓ 添加 emoji 表情")
        if options.get('add_dividers', True):
            custom_options.append("✓ 添加分割线")
        if options.get('beautify_code_blocks', True):
            custom_options.append("✓ 美化代码块")
        if options.get('optimize_headers', True):
            custom_options.append("✓ 优化标题")
        if options.get('add_quote_styles', True):
            custom_options.append("✓ 美化引用")
        if options.get('beautify_lists', True):
            custom_options.append("✓ 美化列表")
        if options.get('beautify_tables', True):
            custom_options.append("✓ 美化表格")
        if options.get('add_emphasis', True):
            custom_options.append("✓ 添加强调")
        
        if custom_options:
            system_instruction += "\n\n本次美化的具体要求：\n" + "\n".join(custom_options)
        
        # 处理大文件的分块提示
        chunk_info = options.get('chunk_info', '')
        if chunk_info:
            system_instruction += f"\n\n注意：这是文档的第 {options.get('chunk_index', 1)} 部分（共 {options.get('total_chunks', 1)} 部分）"
            system_instruction += "\n请保持文档的连贯性，特别是开头和结尾部分。"
        
        # 针对长文档的特殊提示
        if len(content) > 10000:  # 超过 10000 字符
            system_instruction += "\n\n📝 这是一篇长文档，请务必：\n"
            system_instruction += "1. 从头到尾完整美化每一个段落\n"
            system_instruction += "2. 不要因为文档长度而跳过部分内容\n"
            system_instruction += "3. 保持美化风格的一致性\n"
            system_instruction += "4. 确保输出完整的美化后文档\n"
        
        # 完整提示词
        full_prompt = f"""{system_instruction}

---
待美化的 Markdown 内容：

{content}

---
请返回美化后的完整内容（从第一个字符到最后一个字符都要美化）："""
        
        return full_prompt
    
    def _call_ai(self, prompt: str, retry_count: int = 0) -> str:
        """
        调用 AI API
        
        Args:
            prompt: 提示词
            retry_count: 重试次数
            
        Returns:
            AI 响应内容
        """
        try:
            # 检查是否使用 DashScope（通义千问）
            if self.model.startswith('qwen-'):
                # 使用 DashScope SDK
                import dashscope
                from http import HTTPStatus
                
                print(f"  使用 DashScope SDK 调用 {self.model}...")
                
                # 设置API密钥
                dashscope.api_key = self.config.dashscope_api_key
                
                response = dashscope.Generation.call(
                    model=self.model,
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=4096,
                    top_p=0.8
                )
                
                # 增强的响应解析
                result = ""
                
                # 检查响应状态
                if hasattr(response, 'status_code'):
                    if response.status_code != HTTPStatus.OK:
                        raise Exception(f"API 请求失败：HTTP {response.status_code}, Message: {getattr(response, 'message', 'Unknown error')}")
                
                # 尝试多种方式获取文本
                if hasattr(response, 'output') and hasattr(response.output, 'text'):
                    result = response.output.text.strip()
                elif hasattr(response, 'output') and isinstance(response.output, dict):
                    result = response.output.get('text', '').strip()
                elif hasattr(response, 'text'):
                    result = response.text.strip()
                else:
                    # 如果是字符串，直接使用
                    result = str(response).strip()
                
                # 验证结果
                if not result or len(result) < 10:
                    raise Exception(f"AI 返回内容为空或过短：{result[:50] if result else 'None'}")
                
                # 检查是否包含 Markdown 特征
                if not any(marker in result for marker in ['#', '\n', '**', '-']):
                    print(f"⚠️  警告：返回内容可能不是有效的 Markdown")
                    print(f"前 100 个字符：{result[:100]}")
                
                return result
            else:
                # 使用 OpenAI 兼容接口
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "你是一个专业的 Markdown 文档美化专家。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4096,
                )
                
                result = response.choices[0].message.content.strip()
                
                # 验证结果
                if not result or len(result) < 10:
                    raise Exception(f"AI 返回内容为空或过短")
                
                return result
            
        except Exception as e:
            if retry_count < self.max_retries:
                wait_time = (retry_count + 1) * 2
                print(f"\n⚠️  请求失败：{e}")
                print(f"🔄 {wait_time}秒后重试... (第{retry_count + 1}/{self.max_retries}次)")
                import time
                time.sleep(wait_time)
                return self._call_ai(prompt, retry_count + 1)
            else:
                raise Exception(f"AI 请求失败，已达到最大重试次数：{e}")
    
    def get_available_models(self) -> list:
        """
        获取可用的模型列表
        
        Returns:
            模型信息列表
        """
        return self.config.get_available_models()
    
    def switch_model(self, model: str) -> bool:
        """
        切换使用的模型
        
        Args:
            model: 新的模型 ID
            
        Returns:
            是否成功切换
        """
        try:
            api_key, base_url = self.config.get_model_api_key(model)
            if not api_key:
                print(f"❌ 模型 {model} 的 API 密钥未配置")
                return False
            
            self.model = model
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url,
                timeout=self.config.timeout,
                max_retries=self.config.max_retries,
            )
            print(f"✅ 已切换到模型：{model}")
            return True
        except Exception as e:
            print(f"❌ 切换模型失败：{e}")
            return False
    
    def beautify_batch(self, contents: list, options: Optional[Dict] = None) -> list:
        """
        批量美化文档块
        
        Args:
            contents: 内容块列表
            options: 美化选项
            
        Returns:
            美化后的内容列表
        """
        if options is None:
            options = {}
        
        results = []
        total = len(contents)
        
        with tqdm(total=total, desc="✨ AI 美化中", unit="chunk") as pbar:
            for i, content in enumerate(contents):
                try:
                    # 添加分块信息
                    chunk_options = options.copy()
                    chunk_options['chunk_info'] = 'true'
                    chunk_options['chunk_index'] = i + 1
                    chunk_options['total_chunks'] = total
                    
                    beautified = self.beautify(content, chunk_options)
                    results.append(beautified)
                    
                except Exception as e:
                    print(f"\n❌ 美化第 {i+1} 个块失败：{e}")
                    # 保留原始内容
                    results.append(content)
                
                pbar.update(1)
        
        return results
    
    def quick_beautify(self, content: str, style: str = 'default') -> str:
        """
        快速美化（使用预设风格）
        
        Args:
            content: 原始内容
            style: 美化风格 ('default', 'minimal', 'colorful', 'professional')
            
        Returns:
            美化后的内容
        """
        style_prompts = {
            'default': "使用标准的美化风格，平衡美观和实用性",
            'minimal': "使用极简风格，只添加必要的格式化，少用 emoji",
            'colorful': "使用丰富多彩的风格，多使用 emoji 和装饰元素",
            'professional': "使用专业风格，适合技术文档，重点在格式规范",
        }
        
        style_instruction = style_prompts.get(style, style_prompts['default'])
        
        prompt = f"""你是一个 Markdown 文档美化专家。
{style_instruction}

美化要求：
- 保持原文结构和内容
- 提升视觉美观度
- 增强可读性
- 适当使用 emoji 和格式化

请美化以下内容：

{content}

美化后的结果："""
        
        return self._call_ai(prompt)
    
    def validate_and_fix(self, content: str) -> str:
        """
        验证并修复 Markdown 格式
        
        Args:
            content: 需要验证的内容
            
        Returns:
            修复后的内容
        """
        prompt = f"""你是一个 Markdown 格式检查专家。

请检查以下 Markdown 内容的格式问题并修复：
1. 检查标题层级是否正确
2. 检查代码块是否完整（开始和结束的 ```）
3. 检查列表格式是否统一
4. 检查链接和图片格式是否正确
5. 检查表格是否对齐
6. 检查是否有未闭合的标记（如 **, *, ` 等）

如果有问题，请修复并返回完整的正确内容。
如果没有问题，保持原样返回。

内容：

{content}

修复后的结果："""
        
        return self._call_ai(prompt)
    
    def add_table_of_contents(self, content: str) -> str:
        """
        为文档添加目录
        
        Args:
            content: Markdown 内容
            
        Returns:
            带目录的内容
        """
        prompt = f"""你是一个 Markdown 文档编辑专家。

请为以下 Markdown 文档生成一个目录（Table of Contents），放在文档开头。

要求：
1. 提取所有标题（# 到 ######）
2. 生成带链接的目录项
3. 保持正确的缩进层次
4. 在目录后添加分隔线
5. 然后接上原文档内容

文档内容：

{content[:500]}... (内容过长，仅显示前 500 字符)

请返回带目录的完整文档："""
        
        return self._call_ai(prompt)
