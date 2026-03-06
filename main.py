"""
MD BeautifyArts - AI 驱动的 Markdown 文档美化工具
主程序入口
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style

from config import get_config, Config
from file_handler import FileHandler
from ai_beautifier import AIBeautifier


# 初始化 colorama
init()


def print_banner():
    """打印欢迎横幅"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                                              ║
║     {Fore.YELLOW}MD BeautifyArts{Fore.CYAN} - AI Markdown Beautifier         ║
║                                              ║
║     ✨ 让 Markdown 文档更加美观和专业 ✨            ║
║                                              ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    
    MD BeautifyArts v1.0
    使用 AI 技术美化您的 Markdown 文档
    """
    print(banner)


def setup_logging(config: Config):
    """设置日志"""
    import logging
    
    log_level = config.get('logging', 'level', default='INFO')
    save_to_file = config.get('logging', 'save_to_file', default=True)
    log_file = config.get('logging', 'log_file', default='beautify.log')
    
    # 创建日志记录器
    logger = logging.getLogger('MDBeautify')
    logger.setLevel(getattr(logging, log_level))
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = '%(message)s'
    console_handler.setFormatter(logging.Formatter(console_format))
    logger.addHandler(console_handler)
    
    # 文件处理器
    if save_to_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        file_handler.setFormatter(logging.Formatter(file_format))
        logger.addHandler(file_handler)
    
    return logger


def beautify_single_file(filepath: str, output_path: str, config: Config, 
                        file_handler: FileHandler, ai_beautifier: AIBeautifier,
                        options: dict) -> bool:
    """
    美化单个文件
    
    Args:
        filepath: 输入文件路径
        output_path: 输出文件路径
        config: 配置对象
        file_handler: 文件处理器
        ai_beautifier: AI 美化器
        options: 美化选项
        
    Returns:
        是否成功
    """
    try:
        print(f"\n{Fore.BLUE}📄 处理文件：{filepath}{Style.RESET_ALL}")
        
        # 检查文件大小
        needs_split = file_handler.needs_splitting(filepath)
        
        if needs_split:
            print(f"{Fore.YELLOW}⚠️  文件较大，将采用分割 - 美化 - 合并策略{Style.RESET_ALL}")
            
            # 读取并处理大文件
            content = file_handler.read_file(filepath)
            
            def progress_callback(current, total):
                print(f"  进度：{current + 1}/{total} ({(current + 1) / total * 100:.1f}%)")
            
            # 使用分块美化
            chunks = file_handler.split_file_by_chars(content)
            beautified_chunks = ai_beautifier.beautify_batch(chunks, options)
            result = file_handler.merge_chunks(beautified_chunks)
            
        else:
            # 直接美化整个文件
            content = file_handler.read_file(filepath)
            result = ai_beautifier.beautify(content, options)
        
        # 写入结果
        file_handler.write_file(output_path, result)
        
        print(f"{Fore.GREEN}✅ 美化完成！{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ 处理失败：{e}{Style.RESET_ALL}")
        return False


def beautify_directory(directory: str, config: Config, 
                      file_handler: FileHandler, ai_beautifier: AIBeautifier,
                      options: dict):
    """
    美化目录中的所有 Markdown 文件
    
    Args:
        directory: 目录路径
        config: 配置对象
        file_handler: 文件处理器
        ai_beautifier: AI 美化器
        options: 美化选项
    """
    print(f"\n{Fore.BLUE}📁 搜索目录：{directory}{Style.RESET_ALL}")
    
    # 查找所有 Markdown 文件
    md_files = file_handler.find_markdown_files(directory, recursive=True)
    
    if not md_files:
        print(f"{Fore.YELLOW}⚠️  未找到 Markdown 文件{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}✓ 找到 {len(md_files)} 个文件{Style.RESET_ALL}")
    
    # 确定输出目录
    output_dir_name = config.get('output', 'output_dir', default='beautified')
    output_base = Path(directory) / output_dir_name
    
    # 处理每个文件
    success_count = 0
    fail_count = 0
    
    for i, filepath in enumerate(md_files, 1):
        print(f"\n{Fore.CYAN}[{i}/{len(md_files)}]{Style.RESET_ALL}")
        
        # 生成输出路径
        output_path = file_handler.get_output_path(
            filepath,
            output_dir=str(output_base),
            add_suffix=config.get('output', 'add_suffix', default=True),
            suffix=config.get('output', 'suffix', default='_beautified')
        )
        
        # 美化文件
        if beautify_single_file(filepath, output_path, config, file_handler, 
                               ai_beautifier, options):
            success_count += 1
        else:
            fail_count += 1
    
    # 打印统计
    print(f"\n{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✨ 处理完成！{Style.RESET_ALL}")
    print(f"  成功：{success_count} 个文件")
    print(f"  失败：{fail_count} 个文件")
    print(f"  输出目录：{output_base}")
    print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")


def main():
    """主函数"""
    print_banner()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='MD BeautifyArts - AI 驱动的 Markdown 文档美化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py document.md                    # 美化单个文件
  python main.py ./docs                         # 美化目录下所有 MD 文件
  python main.py document.md -o output.md       # 指定输出文件
  python main.py document.md --style colorful   # 使用彩色风格
  python main.py document.md --no-emoji         # 不添加 emoji
        """
    )
    
    parser.add_argument(
        'input',
        help='输入的 Markdown 文件或目录路径'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径（仅单文件模式有效）'
    )
    
    parser.add_argument(
        '-c', '--config',
        default='config.yaml',
        help='配置文件路径 (默认：config.yaml)'
    )
    
    parser.add_argument(
        '-s', '--style',
        choices=['default', 'minimal', 'colorful', 'professional'],
        default='default',
        help='美化风格 (默认：default)'
    )
    
    parser.add_argument(
        '--no-emoji',
        action='store_true',
        help='不添加 emoji'
    )
    
    parser.add_argument(
        '--no-dividers',
        action='store_true',
        help='不添加分割线'
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='快速美化模式（使用预设风格，忽略其他选项）'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='只验证和修复格式，不进行美化'
    )
    
    args = parser.parse_args()
    
    # 加载配置
    config = get_config(args.config)
    
    # 设置日志
    logger = setup_logging(config)
    
    # 验证 API 密钥
    if not config.api_key:
        print(f"{Fore.RED}❌ 错误：API 密钥未设置{Style.RESET_ALL}")
        print(f"请在 .env 文件中设置 OPENAI_API_KEY")
        sys.exit(1)
    
    # 创建处理器
    file_handler = FileHandler(config)
    ai_beautifier = AIBeautifier(config)
    
    # 构建美化选项
    options = {
        'add_emoji': not args.no_emoji and config.get('beautify', 'add_emoji', default=True),
        'add_dividers': not args.no_dividers and config.get('beautify', 'add_dividers', default=True),
        'beautify_code_blocks': config.get('beautify', 'beautify_code_blocks', default=True),
        'optimize_headers': config.get('beautify', 'optimize_headers', default=True),
        'add_quote_styles': config.get('beautify', 'add_quote_styles', default=True),
        'beautify_lists': config.get('beautify', 'beautify_lists', default=True),
        'beautify_tables': config.get('beautify', 'beautify_tables', default=True),
        'add_emphasis': config.get('beautify', 'add_emphasis', default=True),
    }
    
    # 处理输入
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"{Fore.RED}❌ 错误：路径不存在 - {args.input}{Style.RESET_ALL}")
        sys.exit(1)
    
    if input_path.is_file():
        # 单文件模式
        if not input_path.suffix.lower() == '.md':
            print(f"{Fore.YELLOW}⚠️  警告：文件可能不是 Markdown 格式{Style.RESET_ALL}")
        
        # 确定输出路径
        if args.output:
            output_path = args.output
        else:
            output_path = file_handler.get_output_path(
                str(input_path),
                output_dir=config.get('output', 'output_dir', default='beautified'),
                add_suffix=config.get('output', 'add_suffix', default=True),
                suffix=config.get('output', 'suffix', default='_beautified')
            )
        
        # 备份原始文件（如果需要）
        if config.get('output', 'keep_backup', default=False):
            file_handler.backup_file(str(input_path))
        
        # 美化文件
        if args.quick:
            # 快速美化模式
            print(f"{Fore.CYAN}⚡ 使用快速美化风格：{args.style}{Style.RESET_ALL}")
            content = file_handler.read_file(str(input_path))
            result = ai_beautifier.quick_beautify(content, args.style)
            file_handler.write_file(output_path, result)
        elif args.validate:
            # 仅验证修复模式
            print(f"{Fore.CYAN}🔧 验证并修复格式...{Style.RESET_ALL}")
            content = file_handler.read_file(str(input_path))
            result = ai_beautifier.validate_and_fix(content)
            file_handler.write_file(output_path, result)
        else:
            # 标准美化模式
            beautify_single_file(
                str(input_path), output_path, config,
                file_handler, ai_beautifier, options
            )
        
        print(f"\n{Fore.GREEN}✨ 完成！输出文件：{output_path}{Style.RESET_ALL}")
        
    elif input_path.is_dir():
        # 目录模式
        print(f"{Fore.CYAN}📂 开始处理目录...{Style.RESET_ALL}")
        beautify_directory(
            str(input_path), config,
            file_handler, ai_beautifier, options
        )
    else:
        print(f"{Fore.RED}❌ 错误：无效的路径类型{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()
