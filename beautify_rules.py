"""
美化规则库
提供 emoji、分割线、字体样式等美化元素
"""
from typing import Dict, List


class EmojiRules:
    """Emoji 映射规则"""
    
    # 文档结构相关 emoji
    STRUCTURE_EMOJIS = {
        'title': ['📋', '📝', '📄', '📚'],
        'section': ['🔹', '🔸', '▪️', '▫️'],
        'subsection': ['•', '◦', '▪️'],
        'conclusion': ['✅', '✔️', '💡', '🎯'],
        'summary': ['📊', '📈', '📉', '🔍'],
    }
    
    # 内容类型相关 emoji
    CONTENT_EMOJIS = {
        'note': ['💡', '📌', '📍', '🏷️'],
        'warning': ['⚠️', '❗', '🚨', '⛔'],
        'tip': ['💡', '✨', '🌟', '💫'],
        'important': ['❗', '‼️', '🔴', '📢'],
        'example': ['📖', '👁️', '🔍', '📝'],
        'code': ['💻', '🖥️', '⌨️', '🔧'],
        'link': ['🔗', '📎', '🖇️', '📑'],
        'image': ['🖼️', '📷', '🎨', '🖌️'],
        'table': ['📊', '📋', '📑', '🗂️'],
        'list': ['📝', '✅', '☑️', '📋'],
    }
    
    # 技术主题相关 emoji
    TECH_EMOJIS = {
        'python': ['🐍', '🐘', '🔵'],
        'javascript': ['🟨', '⚡', '📜'],
        'web': ['🌐', '🕸️', '📱'],
        'database': ['🗄️', '💾', '📀'],
        'api': ['🔌', '📡', '🔄'],
        'security': ['🔒', '🛡️', '🔐'],
        'cloud': ['☁️', '🌥️', '⛅'],
        'mobile': ['📱', '📲', '📳'],
        'ai': ['🤖', '🧠', '🤯'],
        'devops': ['🚀', '⚙️', '🔧'],
    }
    
    @classmethod
    def get_emoji(cls, category: str, index: int = 0) -> str:
        """
        获取指定类别的 emoji
        
        Args:
            category: 类别名称
            index: 选择该类别中的第几个 emoji
            
        Returns:
            emoji 字符
        """
        all_emojis = {**cls.STRUCTURE_EMOJIS, **cls.CONTENT_EMOJIS, **cls.TECH_EMOJIS}
        if category in all_emojis:
            emojis = all_emojis[category]
            return emojis[index % len(emojis)]
        return '✨'
    
    @classmethod
    def get_random_emoji(cls, category: str = None) -> str:
        """
        随机获取一个 emoji
        
        Args:
            category: 指定类别，None 则随机选择
            
        Returns:
            emoji 字符
        """
        import random
        
        if category and category in cls.STRUCTURE_EMOJIS:
            return random.choice(cls.STRUCTURE_EMOJIS[category])
        elif category and category in cls.CONTENT_EMOJIS:
            return random.choice(cls.CONTENT_EMOJIS[category])
        else:
            all_emojis = []
            for emojis in cls.STRUCTURE_EMOJIS.values():
                all_emojis.extend(emojis)
            for emojis in cls.CONTENT_EMOJIS.values():
                all_emojis.extend(emojis)
            return random.choice(all_emojis) if all_emojis else '✨'


class DividerRules:
    """分割线样式规则"""
    
    # 各种分割线样式
    DIVIDER_STYLES = {
        'simple': '---',
        'double': '===',
        'dashed': '- - -',
        'dotted': '. . .',
        'bold': '***',
        'arrow': '--->',
        'diamond': '<> <> <>',
        'star': '* * *',
        'wave': '~ ~ ~',
        'plus': '+ + +',
        'box': '─ ─ ─',
        'thick': '━━━',
        'mixed': '─ · ─',
        'elegant': '✦ ✦ ✦',
        'modern': '▬ ▬ ▬',
    }
    
    # 带描述的分割线
    DIVIDER_WITH_TEXT = [
        '---\n\n{text}\n\n---',
        '===\n\n◆ {text} ◆\n\n===',
        '***\n\n★ {text} ★\n\n***',
        '~ ~ ~\n\n◇ {text} ◇\n\n~ ~ ~',
    ]
    
    @classmethod
    def get_divider(cls, style: str = 'simple') -> str:
        """
        获取指定样式的分割线
        
        Args:
            style: 分割线样式名称
            
        Returns:
            分割线字符串
        """
        return cls.DIVIDER_STYLES.get(style, cls.DIVIDER_STYLES['simple'])
    
    @classmethod
    def get_all_dividers(cls) -> List[str]:
        """
        获取所有分割线样式
        
        Returns:
            分割线列表
        """
        return list(cls.DIVIDER_STYLES.values())
    
    @classmethod
    def create_section_divider(cls, title: str = None, style: str = 'simple') -> str:
        """
        创建带标题的分割线
        
        Args:
            title: 标题文本
            style: 分割线样式
            
        Returns:
            格式化后的分割线
        """
        divider = cls.get_divider(style)
        
        if title:
            return f"\n{divider}\n\n## {title}\n\n{divider}\n"
        else:
            return f"\n{divider}\n"


class FontStyleRules:
    """字体样式规则"""
    
    # Markdown 字体样式模板
    BOLD_TEMPLATES = ['**{}**', '__{}__']
    ITALIC_TEMPLATES = ['*{}*', '_{}_']
    BOLD_ITALIC_TEMPLATES = ['***{}***', '___{}___']
    STRIKETHROUGH_TEMPLATES = ['~~{}~~']
    HIGHLIGHT_TEMPLATES = ['=={}==']  # 部分 Markdown 支持
    
    # 代码样式
    INLINE_CODE_TEMPLATE = '`{}`'
    CODE_BLOCK_TEMPLATES = {
        'default': '```\n{}\n```',
        'with_lang': '```{}\n{}\n```',
    }
    
    # 引用样式
    QUOTE_TEMPLATES = [
        '> {}',
        '>> {}',
        '>>> {}',
        '> **Note:** {}',
        '> 💡 **Tip:** {}',
        '> ⚠️ **Warning:** {}',
    ]
    
    @classmethod
    def make_bold(cls, text: str) -> str:
        """加粗文本"""
        return f'**{text}**'
    
    @classmethod
    def make_italic(cls, text: str) -> str:
        """斜体文本"""
        return f'*{text}*'
    
    @classmethod
    def make_bold_italic(cls, text: str) -> str:
        """加粗斜体文本"""
        return f'***{text}***'
    
    @classmethod
    def make_strikethrough(cls, text: str) -> str:
        """删除线文本"""
        return f'~~{text}~~'
    
    @classmethod
    def make_code(cls, text: str, language: str = None) -> str:
        """
        代码格式化
        
        Args:
            text: 代码文本
            language: 编程语言
            
        Returns:
            格式化后的代码块
        """
        if language:
            return f'```{language}\n{text}\n```'
        else:
            return f'```\n{text}\n```'
    
    @classmethod
    def make_quote(cls, text: str, style: int = 0) -> str:
        """
        引用格式化
        
        Args:
            text: 引用文本
            style: 引用样式索引
            
        Returns:
            格式化后的引用
        """
        template = cls.QUOTE_TEMPLATES[style % len(cls.QUOTE_TEMPLATES)]
        return template.format(text)


class ColorBackgroundRules:
    """颜色和背景规则"""
    
    # HTML 颜色代码 (用于支持的 Markdown 渲染器)
    COLORS = {
        'red': '#FF6B6B',
        'green': '#4ECDC4',
        'blue': '#45B7D1',
        'yellow': '#FFE66D',
        'purple': '#A64AC9',
        'orange': '#F5A623',
        'pink': '#FF85A2',
        'teal': '#008080',
        'navy': '#001F3F',
        'maroon': '#85144B',
    }
    
    # 背景色方案
    BG_COLORS = {
        'light': '#F8F9FA',
        'medium': '#E9ECEF',
        'dark': '#343A40',
        'warm': '#FFF3CD',
        'cool': '#D1ECF1',
        'success': '#D4EDDA',
        'danger': '#F8D7DA',
        'info': '#D6D8DB',
    }
    
    # HTML 注释标记 (用于添加元数据)
    COMMENT_TEMPLATES = [
        '<!-- {} -->',
        '<!--- {} --->',
        '{/* {} */}',
    ]
    
    @classmethod
    def get_color(cls, color_name: str) -> str:
        """获取颜色代码"""
        return cls.COLORS.get(color_name, '#000000')
    
    @classmethod
    def get_bg_color(cls, bg_name: str) -> str:
        """获取背景色代码"""
        return cls.BG_COLORS.get(bg_name, '#FFFFFF')
    
    @classmethod
    def create_colored_text(cls, text: str, color: str) -> str:
        """
        创建彩色文本 (HTML 格式，适用于支持的渲染器)
        
        Args:
            text: 文本内容
            color: 颜色名称或代码
            
        Returns:
            HTML 格式的彩色文本
        """
        color_code = cls.COLORS.get(color, color)
        return f'<span style="color: {color_code}">{text}</span>'
    
    @classmethod
    def create_comment(cls, text: str, style: int = 0) -> str:
        """
        创建 HTML 注释
        
        Args:
            text: 注释内容
            style: 注释样式索引
            
        Returns:
            HTML 注释
        """
        template = cls.COMMENT_TEMPLATES[style % len(cls.COMMENT_TEMPLATES)]
        return template.format(text)


class BeautifyPatterns:
    """常用美化模式"""
    
    # 标题美化模式
    TITLE_PATTERNS = {
        'emoji_prefix': '{emoji} {title}',
        'emoji_suffix': '{title} {emoji}',
        'with_border': '# {title}\n{border}',
        'centered': '## {title}',
    }
    
    # 列表美化模式
    LIST_PATTERNS = {
        'checkbox': '- [ ] {item}',
        'checked': '- [x] {item}',
        'priority': '- [{priority}] {item}',
        'numbered': '{num}. {item}',
    }
    
    # 链接美化模式
    LINK_PATTERNS = {
        'with_emoji': '[{emoji} {text}]({url})',
        'with_title': '[{text}]({url} "{title}")',
        'button': '[👉 {text}]({url})',
    }
    
    @classmethod
    def beautify_title(cls, title: str, pattern: str = 'emoji_prefix') -> str:
        """美化标题"""
        from random import choice
        
        if pattern == 'emoji_prefix':
            emoji = EmojiRules.get_random_emoji('title')
            return cls.TITLE_PATTERNS[pattern].format(emoji=emoji, title=title)
        elif pattern == 'with_border':
            border = DividerRules.get_divider('thick') * (len(title) // 3 + 1)
            return cls.TITLE_PATTERNS[pattern].format(title=title, border=border)
        else:
            return cls.TITLE_PATTERNS.get(pattern, '{title}').format(title=title)
    
    @classmethod
    def beautify_list_item(cls, item: str, pattern: str = 'checkbox', **kwargs) -> str:
        """美化列表项"""
        if pattern == 'priority':
            priority = kwargs.get('priority', '!')
            return cls.LIST_PATTERNS[pattern].format(priority=priority, item=item)
        elif pattern == 'numbered':
            num = kwargs.get('num', '1')
            return cls.LIST_PATTERNS[pattern].format(num=num, item=item)
        else:
            return cls.LIST_PATTERNS.get(pattern, '- {item}').format(item=item)
    
    @classmethod
    def beautify_link(cls, text: str, url: str, pattern: str = 'with_emoji', **kwargs) -> str:
        """美化链接"""
        from random import choice
        
        if pattern == 'with_emoji':
            emoji = choice(['🔗', '📎', '🖇️', '👉'])
            return cls.LINK_PATTERNS[pattern].format(emoji=emoji, text=text, url=url)
        elif pattern == 'with_title':
            title = kwargs.get('title', '')
            return cls.LINK_PATTERNS[pattern].format(text=text, url=url, title=title)
        else:
            return cls.LINK_PATTERNS.get(pattern, '[{text}]({url})').format(text=text, url=url)
