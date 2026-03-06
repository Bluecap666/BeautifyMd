"""
文件处理器模块
负责文件的读取、写入、分割和合并
"""
import os
from pathlib import Path
from typing import List, Tuple, Optional
from tqdm import tqdm


class FileHandler:
    """文件处理类"""
    
    def __init__(self, config):
        """
        初始化文件处理器
        
        Args:
            config: 配置对象
        """
        self.config = config
    
    def read_file(self, filepath: str) -> str:
        """
        读取文件内容
        
        Args:
            filepath: 文件路径
            
        Returns:
            文件内容字符串
            
        Raises:
            FileNotFoundError: 文件不存在
            UnicodeDecodeError: 编码错误
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在：{filepath}")
        
        # 尝试不同的编码读取
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"✓ 成功读取文件 ({encoding}): {path.name}")
                return content
            except UnicodeDecodeError:
                continue
        
        raise UnicodeDecodeError(f"无法使用支持的编码读取文件：{encodings}")
    
    def write_file(self, filepath: str, content: str, create_dir: bool = True):
        """
        写入文件内容
        
        Args:
            filepath: 文件路径
            content: 文件内容
            create_dir: 是否自动创建目录
        """
        path = Path(filepath)
        
        # 创建目录
        if create_dir and path.parent:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文件
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ 文件已保存：{path.name}")
    
    def get_file_size(self, filepath: str) -> int:
        """
        获取文件大小（字节）
        
        Args:
            filepath: 文件路径
            
        Returns:
            文件大小
        """
        return Path(filepath).stat().st_size
    
    def needs_splitting(self, filepath: str) -> bool:
        """
        判断文件是否需要分割
        
        Args:
            filepath: 文件路径
            
        Returns:
            是否需要分割
        """
        file_size = self.get_file_size(filepath)
        threshold = self.config.get('file_processing', 'split_threshold', default=50000)
        
        return file_size > threshold
    
    def split_file_by_chars(self, content: str, chunk_size: int = None, 
                           overlap: int = None) -> List[str]:
        """
        按字符数分割文件内容
        
        Args:
            content: 文件内容
            chunk_size: 每块大小（字符数）
            overlap: 重叠部分大小（字符数）
            
        Returns:
            分割后的内容块列表
        """
        if chunk_size is None:
            chunk_size = self.config.get('file_processing', 'chunk_size', default=5000)
        if overlap is None:
            overlap = self.config.get('file_processing', 'chunk_overlap', default=200)
        
        chunks = []
        start = 0
        total_length = len(content)
        
        with tqdm(total=total_length, desc="📝 分割文件", unit="char") as pbar:
            while start < total_length:
                end = start + chunk_size
                
                # 如果不是最后一块，尝试在段落处切断
                if end < total_length:
                    # 寻找最近的换行符
                    newline_pos = content.rfind('\n\n', start, end)
                    if newline_pos > start + chunk_size // 2:
                        end = newline_pos + 2  # 包含两个换行符
                
                chunk = content[start:end]
                chunks.append(chunk)
                
                pbar.update(end - start)
                
                # 移动起始位置，减去重叠部分
                start = end - overlap if end < total_length else total_length
        
        print(f"✓ 文件已分割为 {len(chunks)} 个块")
        return chunks
    
    def split_file_by_sections(self, content: str) -> List[str]:
        """
        按 Markdown 章节分割文件
        
        Args:
            content: 文件内容
            
        Returns:
            分割后的章节列表
        """
        sections = []
        current_section = []
        lines = content.split('\n')
        
        in_code_block = False
        
        for line in lines:
            # 检测代码块边界
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            
            # 检测标题（不在代码块内时）
            if not in_code_block and line.startswith('#'):
                # 保存之前的章节
                if current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
            
            current_section.append(line)
        
        # 添加最后一个章节
        if current_section:
            sections.append('\n'.join(current_section))
        
        print(f"✓ 文件已按章节分割为 {len(sections)} 个部分")
        return sections
    
    def merge_chunks(self, chunks: List[str], overlap: int = None) -> str:
        """
        合并分割的块
        
        Args:
            chunks: 内容块列表
            overlap: 重叠部分大小
            
        Returns:
            合并后的完整内容
        """
        if not chunks:
            return ""
        
        if len(chunks) == 1:
            return chunks[0]
        
        merged = [chunks[0]]
        
        for i in range(1, len(chunks)):
            chunk = chunks[i]
            prev_chunk = chunks[i - 1]
            
            # 移除重叠部分
            if overlap and len(prev_chunk) >= overlap:
                # 简单策略：直接跳过重叠部分
                # 更智能的策略可以比较文本相似度
                chunk = chunk[overlap:]
            
            merged.append(chunk)
        
        result = ''.join(merged)
        print(f"✓ 已合并 {len(chunks)} 个块")
        return result
    
    def get_output_path(self, input_path: str, output_dir: str = None, 
                       add_suffix: bool = True, suffix: str = '_beautified') -> str:
        """
        生成输出文件路径
        
        Args:
            input_path: 输入文件路径
            output_dir: 输出目录
            add_suffix: 是否添加后缀
            suffix: 文件名后缀
            
        Returns:
            输出文件路径
        """
        path = Path(input_path)
        
        # 确定输出目录
        if output_dir:
            output_path = Path(output_dir) / path.name
        else:
            output_path = path
        
        # 添加后缀
        if add_suffix and suffix:
            stem = path.stem
            output_path = path.parent / f"{stem}{suffix}{path.suffix}"
        
        return str(output_path)
    
    def backup_file(self, filepath: str, backup_suffix: str = '.bak'):
        """
        备份文件
        
        Args:
            filepath: 文件路径
            backup_suffix: 备份文件后缀
        """
        path = Path(filepath)
        backup_path = path.with_suffix(path.suffix + backup_suffix)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ 已备份文件：{backup_path.name}")
        except Exception as e:
            print(f"⚠️  备份失败：{e}")
    
    def process_large_file(self, filepath: str, beautify_func, 
                          progress_callback=None) -> str:
        """
        处理大文件（分割 - 美化 - 合并）
        
        Args:
            filepath: 文件路径
            beautify_func: 美化函数，接收 (content, chunk_index, total_chunks)
            progress_callback: 进度回调函数
            
        Returns:
            美化后的内容
        """
        # 读取文件
        content = self.read_file(filepath)
        
        # 分割文件
        chunks = self.split_file_by_chars(content)
        total_chunks = len(chunks)
        
        # 美化每个块
        beautified_chunks = []
        overlap = self.config.get('file_processing', 'chunk_overlap', default=200)
        
        with tqdm(total=total_chunks, desc="✨ 美化处理", unit="chunk") as pbar:
            for i, chunk in enumerate(chunks):
                if progress_callback:
                    progress_callback(i, total_chunks)
                
                # 调用美化函数
                beautified = beautify_func(chunk, i, total_chunks)
                beautified_chunks.append(beautified)
                
                pbar.update(1)
        
        # 合并结果
        result = self.merge_chunks(beautified_chunks, overlap)
        
        return result
    
    def find_markdown_files(self, directory: str, recursive: bool = True) -> List[str]:
        """
        查找目录中的 Markdown 文件
        
        Args:
            directory: 目录路径
            recursive: 是否递归搜索子目录
            
        Returns:
            Markdown 文件路径列表
        """
        path = Path(directory)
        
        if recursive:
            files = list(path.rglob('*.md'))
        else:
            files = list(path.glob('*.md'))
        
        # 排除输出目录的文件
        output_dir_name = self.config.get('output', 'output_dir', default='beautified')
        filtered_files = []
        
        for file in files:
            if output_dir_name not in file.parts:
                filtered_files.append(str(file))
        
        print(f"✓ 找到 {len(filtered_files)} 个 Markdown 文件")
        return sorted(filtered_files)
