// 全局变量
let originalContent = '';
let beautifiedContent = '';
let currentMode = 'file';
let selectedFile = null;
let chatModel = '';
let chatHistory = [];

// 页面加载时获取可用模型列表
document.addEventListener('DOMContentLoaded', async () => {
    await loadModels();
    setupEventListeners();
});

// 加载可用模型
async function loadModels() {
    try {
        const response = await fetch('/api/models');
        const data = await response.json();
        
        if (data.success) {
            // 主模型选择器
            const select = document.getElementById('modelSelect');
            const info = document.getElementById('modelInfo');
            
            select.innerHTML = '';
            
            // 按提供商分组
            const providers = {};
            data.models.forEach(model => {
                if (!providers[model.provider]) {
                    providers[model.provider] = [];
                }
                providers[model.provider].push(model);
            });
            
            // 添加选项
            Object.keys(providers).forEach(provider => {
                const group = document.createElement('optgroup');
                group.label = provider;
                
                providers[provider].forEach(model => {
                    const option = document.createElement('option');
                    option.value = model.id;
                    option.textContent = model.name;
                    option.disabled = !model.available;
                    
                    if (model.id === data.default_model) {
                        option.selected = true;
                    }
                    
                    group.appendChild(option);
                });
                
                select.appendChild(group);
            });
            
            // 聊天模型选择器
            const chatSelect = document.getElementById('chatModel');
            chatSelect.innerHTML = '';
            
            Object.keys(providers).forEach(provider => {
                const group = document.createElement('optgroup');
                group.label = provider;
                
                providers[provider].forEach(model => {
                    const option = document.createElement('option');
                    option.value = model.id;
                    option.textContent = model.name;
                    option.disabled = !model.available;
                    group.appendChild(option);
                });
                
                chatSelect.appendChild(group);
            });
            
            // 设置默认聊天模型
            if (data.default_model) {
                chatModel = data.default_model;
                chatSelect.value = data.default_model;
            }
            
            // 更新模型信息
            updateModelInfo(select.value);
        }
    } catch (error) {
        console.error('加载模型列表失败:', error);
    }
}

// 更新模型信息显示
function updateModelInfo(modelId) {
    const info = document.getElementById('modelInfo');
    const models = {
        'gpt-3.5-turbo': 'OpenAI GPT-3.5 - 快速且经济',
        'gpt-4': 'OpenAI GPT-4 - 最强性能',
        'qwen-turbo': '通义千问 Turbo - 阿里云出品',
        'qwen-plus': '通义千问 Plus - 增强版',
        'ernie-bot': '文心一言 - 百度出品',
        'spark-v3.5': '讯飞星火 V3.5 - 科大讯飞',
        'chatglm_pro': 'ChatGLM Pro - 智谱 AI',
        'hunyuan-lite': '腾讯混元 Lite - 腾讯出品'
    };
    
    info.textContent = models[modelId] || '';
}

// 设置事件监听器
function setupEventListeners() {
    // 文件上传区域
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });
    
    // 拖拽上传
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFileSelect(e.dataTransfer.files[0]);
    });
    
    // 模型选择变化
    document.getElementById('modelSelect').addEventListener('change', (e) => {
        updateModelInfo(e.target.value);
    });
}

// 切换标签页
function switchTab(mode) {
    currentMode = mode;
    
    // 更新按钮状态
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // 显示对应的区域
    document.querySelectorAll('.upload-section').forEach(section => {
        section.classList.remove('active');
    });
    
    if (mode === 'file') {
        document.getElementById('fileUploadSection').classList.add('active');
    } else {
        document.getElementById('textInputSection').classList.add('active');
    }
}

// 处理文件选择
function handleFileSelect(file) {
    if (!file) return;
    
    if (!file.name.endsWith('.md')) {
        alert('请选择 Markdown (.md) 文件');
        return;
    }
    
    selectedFile = file;
    const fileInfo = document.getElementById('fileInfo');
    fileInfo.innerHTML = `
        <strong>✅ 已选择:</strong> ${file.name}<br>
        <strong>大小:</strong> ${(file.size / 1024).toFixed(2)} KB
    `;
    
    // 读取文件内容用于预览
    const reader = new FileReader();
    reader.onload = (e) => {
        originalContent = e.target.result;
    };
    reader.readAsText(file);
}

// 开始美化
async function beautify() {
    const model = document.getElementById('modelSelect').value;
    const beautifyBtn = document.getElementById('beautifyBtn');
    
    // 验证输入
    if (currentMode === 'file' && !selectedFile) {
        alert('请先选择文件');
        return;
    }
    
    if (currentMode === 'text') {
        originalContent = document.getElementById('markdownInput').value;
        if (!originalContent.trim()) {
            alert('请输入 Markdown 内容');
            return;
        }
    }
    
    // 禁用按钮，显示进度
    beautifyBtn.disabled = true;
    document.getElementById('progressSection').style.display = 'block';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    
    try {
        let result;
        
        if (currentMode === 'file') {
            // 文件上传模式
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('model', model);
            
            const response = await fetch('/api/beautify', {
                method: 'POST',
                body: formData
            });
            
            result = await response.json();
            
            if (result.success) {
                // 下载美化后的文件以获取内容
                const downloadResponse = await fetch(result.download_url);
                beautifiedContent = await downloadResponse.text();
                showResult(result);
            } else {
                showError(result.error);
            }
        } else {
            // 文本输入模式
            const response = await fetch('/api/beautify-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: originalContent,
                    model: model
                })
            });
            
            result = await response.json();
            
            if (result.success) {
                beautifiedContent = result.content;
                showResult(result);
            } else {
                showError(result.error);
            }
        }
    } catch (error) {
        showError('网络错误：' + error.message);
    } finally {
        beautifyBtn.disabled = false;
        document.getElementById('progressSection').style.display = 'none';
    }
}

// 显示结果
function showResult(result) {
    document.getElementById('usedModel').textContent = result.model_used || '';
    document.getElementById('originalFile').textContent = result.original_filename || '文本输入';
    
    // 设置下载链接
    if (result.download_url) {
        document.getElementById('downloadLink').href = result.download_url;
    }
    
    // 渲染美化后的内容（Markdown 转 HTML）
    renderBeautifiedContent(beautifiedContent);
    
    // 显示预览内容
    showPreview('original');
    
    // 显示结果区域
    document.getElementById('resultSection').style.display = 'block';
    
    // 滚动到结果区域
    document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
}

// 渲染美化后的内容为 HTML
function renderBeautifiedContent(markdown) {
    const container = document.getElementById('beautifiedContent');
    const wechatContainer = document.getElementById('wechatContent');
    
    // 保存原始 Markdown
    beautifiedContent = markdown;
    
    // 简单的 Markdown 转 HTML（基础版本）
    let html = markdown
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*)\*/gim, '<em>$1</em>')
        .replace(/`([^`]+)`/gim, '<code>$1</code>')
        .replace(/```(\w*)\n([\s\S]*?)\n```/gim, '<pre><code class="language-$1">$2</code></pre>')
        .replace(/^\- (.*$)/gim, '<li>$1</li>')
        .replace(/^\d+\. (.*$)/gim, '<li>$1</li>')
        .replace(/\n/gim, '<br>');
    
    container.innerHTML = `<div class="markdown-preview">${html}</div>`;
    
    // 生成微信公众号格式
    generateWechatContent(markdown);
}

// 生成微信公众号格式
function generateWechatContent(markdown) {
    const wechatDiv = document.getElementById('wechatContent');
    
    // 先预处理 Markdown，移除多余的空行
    let processedMarkdown = markdown
        .replace(/\r\n/g, '\n')  // 统一换行符
        .replace(/\n{3,}/g, '\n\n');  // 将 3 个及以上换行减少为 2 个
    
    // 微信公众号专用样式
    let wechatHtml = `
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei UI', 'Microsoft YaHei', Arial, sans-serif; line-height: 1.75; color: #333; max-width: 100%;">
${processMarkdownForWechat(processedMarkdown)}
</div>`;
    
    wechatDiv.innerHTML = wechatHtml;
}

// 处理 Markdown 为微信公众号格式
function processMarkdownForWechat(markdown) {
    const lines = markdown.split('\n');
    let result = [];
    let inCodeBlock = false;
    let codeBlockContent = [];
    let codeBlockLang = '';
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        // 处理代码块开始
        if (line.startsWith('```')) {
            if (!inCodeBlock) {
                inCodeBlock = true;
                codeBlockLang = line.slice(3).trim();
                codeBlockContent = [];
            } else {
                inCodeBlock = false;
                result.push(`<section style="background: #2d3748; padding: 15px; border-radius: 8px; margin: 15px 0; overflow-x: auto;"><code style="color: #e2e8f0; font-family: Consolas, Monaco, monospace; font-size: 14px; line-height: 1.6;">${codeBlockContent.join('<br>')}</code></section>`);
            }
            continue;
        }
        
        if (inCodeBlock) {
            codeBlockContent.push(escapeHtml(line));
            continue;
        }
        
        // 跳过空行
        if (line.trim() === '') {
            continue;
        }
        
        // 一级标题
        if (line.match(/^# /)) {
            result.push(`<section style="margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px;"><h1 style="color: white; margin: 0; font-size: 24px;">${line.replace(/^# /, '')}</h1></section>`);
            continue;
        }
        
        // 二级标题
        if (line.match(/^## /)) {
            result.push(`<section style="margin: 25px 0 15px; padding-bottom: 10px; border-bottom: 3px solid #667eea;"><h2 style="color: #667eea; margin: 0; font-size: 20px;">${line.replace(/^## /, '')}</h2></section>`);
            continue;
        }
        
        // 三级标题
        if (line.match(/^### /)) {
            result.push(`<h3 style="color: #5a67d8; margin: 20px 0 10px; font-size: 18px;">${line.replace(/^### /, '')}</h3>`);
            continue;
        }
        
        // 无序列表
        if (line.match(/^[\-\*] /)) {
            result.push(`<section style="margin: 10px 0; padding-left: 20px; position: relative;"><span style="position: absolute; left: 0; color: #667eea;">●</span><span style="padding-left: 10px;">${formatInlineStyles(line.replace(/^[\-\*] /, ''))}</span></section>`);
            continue;
        }
        
        // 有序列表
        if (line.match(/^\d+\. /)) {
            const match = line.match(/^(\d+)\. /);
            const num = match ? match[1] : '';
            result.push(`<section style="margin: 10px 0; padding-left: 20px; position: relative;"><span style="position: absolute; left: 0; color: #667eea; font-weight: bold;">${num}.</span><span style="padding-left: 10px;">${formatInlineStyles(line.replace(/^\d+\. /, ''))}</span></section>`);
            continue;
        }
        
        // 引用
        if (line.match(/^> /)) {
            result.push(`<section style="margin: 15px 0; padding: 10px 15px; background: #f0f4ff; border-left: 4px solid #667eea; border-radius: 4px;">${formatInlineStyles(line.replace(/^> /, ''))}</section>`);
            continue;
        }
        
        // 分隔线
        if (line.match(/^[\-\*_]{3,}$/)) {
            result.push(`<hr style="border: none; height: 1px; background: linear-gradient(to right, transparent, #667eea, transparent); margin: 30px 0;">`);
            continue;
        }
        
        // 普通段落
        result.push(`<p style="margin: 15px 0; text-align: justify; line-height: 1.8;">${formatInlineStyles(line)}</p>`);
    }
    
    return result.join('');
}

// 格式化行内样式（粗体、斜体、代码）
function formatInlineStyles(text) {
    return text
        .replace(/\*\*(.+?)\*\*/g, '<strong style="color: #667eea;">$1</strong>')
        .replace(/\*(.+?)\*/g, '<em style="color: #764ba2;">$1</em>')
        .replace(/`(.+?)`/g, '<code style="background: #f7fafc; padding: 3px 8px; border-radius: 4px; color: #e53e3e; font-family: Consolas, Monaco, monospace;">$1</code>');
}

// HTML 转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 切换预览
function showPreview(type) {
    const preview = document.getElementById('previewContent');
    const beautifiedDiv = document.getElementById('beautifiedContent');
    const wechatDiv = document.getElementById('wechatContent');
    const tabs = document.querySelectorAll('.preview-tab');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    
    if (type === 'original') {
        preview.textContent = originalContent;
        preview.style.display = 'block';
        beautifiedDiv.style.display = 'none';
        wechatDiv.style.display = 'none';
        tabs[0].classList.add('active');
    } else if (type === 'beautified') {
        preview.style.display = 'none';
        beautifiedDiv.style.display = 'block';
        wechatDiv.style.display = 'none';
        tabs[1].classList.add('active');
    } else if (type === 'wechat') {
        preview.style.display = 'none';
        beautifiedDiv.style.display = 'none';
        wechatDiv.style.display = 'block';
        tabs[2].classList.add('active');
    }
}

// 复制内容
function copyContent() {
    if (beautifiedContent) {
        navigator.clipboard.writeText(beautifiedContent).then(() => {
            alert('✅ Markdown 内容已复制到剪贴板');
        }).catch(err => {
            alert('❌ 复制失败：' + err.message);
        });
    } else {
        alert('暂无可复制的内容');
    }
}

// 复制微信公众号格式内容
function copyWechatContent() {
    const wechatDiv = document.getElementById('wechatContent');
    
    if (wechatDiv && wechatDiv.innerHTML) {
        // 获取渲染后的 HTML 内容
        const htmlContent = wechatDiv.innerHTML;
        
        // 创建一个临时的可编辑区域
        const tempDiv = document.createElement('div');
        tempDiv.style.position = 'absolute';
        tempDiv.style.left = '-9999px';
        tempDiv.style.top = '0';
        tempDiv.style.width = '800px';  // 设置固定宽度，模拟公众号编辑器
        tempDiv.contentEditable = 'true';
        tempDiv.innerHTML = htmlContent;
        document.body.appendChild(tempDiv);
        
        // 选中内容
        const range = document.createRange();
        range.selectNodeContents(tempDiv);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        
        try {
            // 执行复制
            document.execCommand('copy');
            alert('✅ 微信公众号格式已复制！\n\n复制说明：\n1. 打开公众号后台编辑器\n2. 直接 Ctrl+V 粘贴\n3. 如格式有误，请尝试选择性粘贴');
        } catch (err) {
            alert('❌ 复制失败：' + err.message);
        }
        
        // 清理临时元素
        setTimeout(() => {
            document.body.removeChild(tempDiv);
            selection.removeAllRanges();
        }, 100);
    } else {
        alert('请先生成微信公众号格式内容');
    }
}

// 重置所有
function resetAll() {
    // 清空文件选择
    selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').innerHTML = '';
    
    // 清空文本输入
    document.getElementById('markdownInput').value = '';
    originalContent = '';
    beautifiedContent = '';
    
    // 隐藏结果和错误
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    
    // 重置按钮
    document.getElementById('beautifyBtn').disabled = false;
    
    // 切换到文件模式
    switchTab('file');
    
    // 滚动到顶部
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 重置错误
function resetError() {
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('beautifyBtn').disabled = false;
}

// 显示帮助
function showHelp() {
    document.getElementById('helpModal').style.display = 'flex';
}

// 显示关于
function showAbout() {
    document.getElementById('aboutModal').style.display = 'flex';
}

// 显示设置
function showSettings() {
    document.getElementById('settingsModal').style.display = 'flex';
}

// 关闭模态框
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// 保存 API 配置
async function saveApiConfig(event) {
    event.preventDefault();
    
    const config = {
        openai_key: document.getElementById('openai_key').value,
        dashscope_key: document.getElementById('dashscope_key').value,
        qianfan_ak: document.getElementById('qianfan_ak').value,
        qianfan_sk: document.getElementById('qianfan_sk').value,
        spark_key: document.getElementById('spark_key').value,
        zhipu_key: document.getElementById('zhipu_key').value,
        hunyuan_key: document.getElementById('hunyuan_key').value
    };
    
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ 配置已保存！当前会话有效。');
            closeModal('settingsModal');
            // 重新加载模型列表
            await loadModels();
        } else {
            alert('❌ 保存失败：' + result.error);
        }
    } catch (error) {
        alert('❌ 网络错误：' + error.message);
    }
}

// 聊天功能
function toggleChat() {
    const chatWindow = document.getElementById('chatWindow');
    const chatToggle = document.getElementById('chatToggle');
    
    if (chatWindow.style.display === 'none') {
        chatWindow.style.display = 'flex';
        chatToggle.textContent = '✖️ 关闭';
    } else {
        chatWindow.style.display = 'none';
        chatToggle.textContent = '💬 聊天';
    }
}

// 更新聊天模型
function updateChatModel() {
    chatModel = document.getElementById('chatModel').value;
    addSystemMessage(`已切换到模型：${chatModel}`);
}

// 发送消息
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    if (!chatModel) {
        alert('请先选择一个聊天模型');
        return;
    }
    
    // 添加用户消息
    addUserMessage(message);
    input.value = '';
    
    // 显示加载中
    const loadingId = addLoadingMessage();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                model: chatModel
            })
        });
        
        const result = await response.json();
        
        // 移除加载提示
        removeMessage(loadingId);
        
        if (result.success) {
            addAssistantMessage(result.response);
        } else {
            addSystemMessage(`❌ 错误：${result.error}`);
        }
    } catch (error) {
        removeMessage(loadingId);
        addSystemMessage(`❌ 网络错误：${error.message}`);
    }
}

// 处理按键
function handleChatKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// 添加消息到聊天
function addUserMessage(content) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.innerHTML = `<div class="message-content">${escapeHtml(content)}</div>`;
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
}

function addAssistantMessage(content) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    
    // 简单的格式化
    const formattedContent = content
        .replace(/\*\*(.*)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
    
    messageDiv.innerHTML = `<div class="message-content">${formattedContent}</div>`;
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
}

function addSystemMessage(content) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    messageDiv.innerHTML = `<div class="message-content">${content}</div>`;
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
}

function addLoadingMessage() {
    const id = 'loading-' + Date.now();
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant loading';
    messageDiv.id = id;
    messageDiv.innerHTML = `<div class="message-content">🤔 思考中...</div>`;
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
    return id;
}

function removeMessage(id) {
    const messageDiv = document.getElementById(id);
    if (messageDiv) {
        messageDiv.remove();
    }
}

function scrollToBottom() {
    const messagesDiv = document.getElementById('chatMessages');
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// HTML 转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 点击模态框外部关闭
window.onclick = function(event) {
    if (event.target.className === 'modal') {
        event.target.style.display = 'none';
    }
}
