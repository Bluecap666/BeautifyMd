#  Change Log

All notable changes to **MD BeautifyArts** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [v3.0.0] - 2026-03-08

### ✨ Added
- 🚀 **Multi-model support** for 19+ mainstream AI models (OpenAI, Qwen, ERNIE Bot, Spark, ChatGLM, HunYuan, Doubao)
- 🎨 **AI-powered Markdown beautification** with emojis, dividers, borders, backgrounds, bubbles, colorful texts and card layouts
- 💬 **AI chat functionality** with multi-model switching
- 🖥️ **Web UI interface** supporting file upload and text input modes
- 📱 **WeChat Official Accounts format** perfect adaptation
- ⚙️ **Real-time API KEY configuration**
- 🔗 **Online configuration API KEY** feature
- 📁 **Diagnostic tool** (`diagnose.py`) for troubleshooting
- 📄 **Comprehensive documentation** (21+ documents covering all use cases)

### 🔧 Changed
- 🔄 **Enhanced copy logic** for WeChat official accounts format to prevent content overlap
- 🔄 **Improved AI role definition** to actively check document format issues, supplement content, and optimize structure
- 🔄 **Expanded AI permissions** to allow moderate content optimization while maintaining core content
- 🔄 **Added current date injection** to system prompt for better context awareness
- 🔄 **Refined styling** for preview containers with fixed height and scrollable content
- 🔄 **Optimized file handling** for large files with automatic splitting, processing, and merging

### 🐛 Fixed
- 🛠️ **WeChat format copying overlap issue** - Fixed content overlapping when pasted to editor
- 🛠️ **Chat network access problems** - Implemented proper SDK calls for different model types
- 🛠️ **Long document display issues** - Added fixed height containers with independent scrolling
- 🛠️ **DashScope SDK integration** - Corrected message format and API calls for Qwen models
- 🛠️ **UI responsiveness** - Improved preview area layout for better user experience

### 📚 Documentation
- 📖 **V3 Update Guide** (`V3_UPDATE_GUIDE.md`) - Complete guide for new features
- 📖 **Features Documentation** (`FEATURES_v2.1.md`) - Detailed feature explanations
- 📖 **Quick Start Guide** (`QUICKSTART.md`) - Step-by-step setup instructions
- 📖 **Model Usage Guide** (`MODELS_GUIDE.md`) - Instructions for different AI models
- 📖 **Web UI Guide** (`WEB_UI_GUIDE.md`) - Interface usage instructions
- 📖 **Troubleshooting Guide** (`TROUBLESHOOTING_DASHSCOPE.md`) - Problem resolution steps
- 📖 **Network Explanation** (`CHAT_NETWORK_EXPLANATION.md`) - Details on AI's network limitations

---

## [v2.1.3] - 2026-02-28

### 🐛 Fixed
- 🔧 **WeChat Official Account copy overlap** - Optimized copy logic to prevent content overlapping
- 🐛 **Content duplication** when pasted to editor

### ✨ Added
- 📋 **AI autonomous beautification and content supplementation** - Enhanced AI to proactively check document formats and supplement content
- 📄 **Chat network explanation documentation** - Detailed explanation of AI's inability to access the internet

---

## [v2.1.1] - 2026-01-27

### ✨ Added
- 📱 **WeChat Official Account format support** - Professional styling generation for public account posts
- ♶ **Fixed height containers** - Scrollable areas for better UX with long documents
- 📋 **Copy functionality** for WeChat format

### 🔧 Fixed
- 🐛 **Chat network access** - Fixed DashScope SDK calls and message formatting
- 🐛 **Scrolling issues** - Long documents no longer cause infinite page extension

---

## [v2.0.0] - 2025-xx-xx

### ✨ Added
- 🖥️ **Web UI interface** - Graphical interface with drag-and-drop support
- 🤖 **Multi-model support** - Support for various AI models
- 💬 **AI chat window** - Real-time conversation with AI
- ⚙️ **API KEY configuration** - Online configuration in UI

---

## [v1.0.0] - 2025-xx-xx

### ✨ Added
- 🛠️ **Command-line tool** - Basic Markdown beautification
- 🎨 **Basic beautification features** - Initial set of Markdown enhancements

---