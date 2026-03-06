"""
使用示例脚本
演示如何使用 MD BeautifyArts 的各种功能
"""
import os
from pathlib import Path

def print_example(num, title):
    """打印示例标题"""
    print(f"\n{'='*60}")
    print(f"示例 {num}: {title}")
    print(f"{'='*60}\n")

def main():
    """主函数"""
    print("=" * 60)
    print("MD BeautifyArts - 使用示例")
    print("=" * 60)
    
    # 示例 1: 基本用法
    print_example(1, "美化单个文件")
    print("命令：python main.py document.md")
    print("说明：使用默认配置美化单个 Markdown 文件")
    print()
    
    # 示例 2: 指定输出文件
    print_example(2, "指定输出文件路径")
    print("命令：python main.py input.md -o output/custom.md")
    print("说明：将美化后的文件保存到指定路径")
    print()
    
    # 示例 3: 批量处理
    print_example(3, "处理整个目录")
    print("命令：python main.py ./docs")
    print("说明：递归处理目录下所有 Markdown 文件")
    print("输出： beautified/ 子目录")
    print()
    
    # 示例 4: 使用不同风格
    print_example(4, "使用彩色风格")
    print("命令：python main.py readme.md --style colorful")
    print("说明：使用丰富多彩的 emoji 和装饰元素")
    print()
    
    print_example(5, "使用极简风格")
    print("命令：python main.py technical.md --style minimal")
    print("说明：适合技术文档，几乎不使用 emoji")
    print()
    
    print_example(6, "使用专业风格")
    print("命令：python main.py api.md --style professional")
    print("说明：正式专业的格式，注重规范性")
    print()
    
    # 示例 5: 自定义选项
    print_example(7, "不使用 emoji")
    print("命令：python main.py doc.md --no-emoji")
    print("说明：只进行格式化，不添加 emoji 表情")
    print()
    
    print_example(8, "不使用分割线")
    print("命令：python main.py doc.md --no-dividers")
    print("说明：不添加分割线，保持紧凑布局")
    print()
    
    # 示例 6: 快速模式
    print_example(9, "快速美化")
    print("命令：python main.py quick.md --quick --style default")
    print("说明：使用预设风格快速美化，忽略详细配置")
    print()
    
    # 示例 7: 仅验证修复
    print_example(10, "验证并修复格式")
    print("命令：python main.py draft.md --validate")
    print("说明：只检查和修复 Markdown 格式问题，不进行美化")
    print()
    
    # 示例 8: 自定义配置文件
    print_example(11, "使用自定义配置")
    print("命令：python main.py doc.md -c my_config.yaml")
    print("说明：使用指定的配置文件而非默认 config.yaml")
    print()
    
    # 编程接口示例
    print_example(12, "在代码中使用")
    code_example = '''
from config import get_config
from file_handler import FileHandler
from ai_beautifier import AIBeautifier

# 加载配置
config = get_config('config.yaml')

# 创建处理器
file_handler = FileHandler(config)
ai_beautifier = AIBeautifier(config)

# 读取文件
content = file_handler.read_file('document.md')

# 美化内容
options = {
    'add_emoji': True,
    'add_dividers': True,
}
beautified = ai_beautifier.beautify(content, options)

# 保存结果
file_handler.write_file('output.md', beautified)
'''
    print(code_example)
    
    # 配置文件示例
    print_example(13, "自定义配置项")
    config_example = '''
# config.yaml
beautify:
  add_emoji: true              # 添加 emoji
  add_dividers: true           # 添加分割线
  beautify_code_blocks: true   # 美化代码块
  optimize_headers: true       # 优化标题
  
file_processing:
  split_threshold: 50000       # 50KB 以上文件分割
  chunk_size: 5000             # 每块 5000 字符
  chunk_overlap: 200           # 重叠 200 字符

output:
  output_dir: "beautified"     # 输出目录
  add_suffix: true             # 添加后缀
  suffix: "_beautified"        # 后缀名
  keep_backup: false           # 不保留备份
'''
    print(config_example)
    
    # 环境变量示例
    print_example(14, "环境变量配置")
    env_example = '''
# .env 文件
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE_URL=https://api.openai.com/v1
DEFAULT_MODEL=gpt-3.5-turbo
REQUEST_TIMEOUT=120
MAX_RETRIES=3
'''
    print(env_example)
    
    # 大文件处理
    print_example(15, "大文件处理策略")
    print("当文件大小超过阈值时：")
    print("1. 📝 自动分割为多个块（默认 50KB）")
    print("2. ✨ 分别美化每个块")
    print("3. 🔗 智能合并所有块")
    print("4. ✅ 保持文档连贯性")
    print()
    print("命令：python main.py large_file.md")
    print("说明：系统会自动检测并采用分割 - 合并策略")
    print()
    
    # 批处理脚本示例
    print_example(16, "Windows 批处理脚本")
    bat_script = '''
@echo off
REM beautify_all.bat - 美化当前目录所有 MD 文件

echo 开始批量美化 Markdown 文件...

for %%f in (*.md) do (
    echo 处理：%%f
    python main.py "%%f"
)

echo 所有文件处理完成！
pause
'''
    print(bat_script)
    
    print_example(17, "Linux/Mac Shell 脚本")
    sh_script = '''#!/bin/bash
# beautify_all.sh - 美化当前目录所有 MD 文件

echo "开始批量美化 Markdown 文件..."

for file in *.md; do
    echo "处理：$file"
    python main.py "$file"
done

echo "所有文件处理完成！"
'''
    print(sh_script)
    
    # 提示
    print("\n" + "=" * 60)
    print("💡 使用提示:")
    print("=" * 60)
    print("1. 首次使用前请确保配置好 .env 文件中的 API 密钥")
    print("2. 建议先使用小文件测试效果")
    print("3. 大文件处理时间较长，请耐心等待")
    print("4. 可以使用 --quick 模式加快速度")
    print("5. 重要文件建议开启备份功能 (keep_backup: true)")
    print("6. 查看完整帮助：python main.py --help")
    print()


if __name__ == '__main__':
    main()
