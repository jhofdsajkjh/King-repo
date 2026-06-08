---
name: officecli-installation
description: Install and configure OfficeCLI for AI Agent Office automation without Microsoft Office
trigger: User requests officecli installation or AI-powered Office automation setup
prioritize: When Office automation tasks are needed without installing Microsoft Office
---

# OfficeCLI 安装与使用指南

## 📦 简介
OfficeCLI 是 AI Agent 专用的 Office 自动化工具，单二进制文件（约 32MB），无需安装 Microsoft Office，支持 Word/Excel/PPT 文件的读取、编辑、生成操作。

- **GitHub**: [iOfficeAI/OfficeCLI](https://github.com/iOfficeAI/OfficeCLI) ⭐ 6322
- **最新版本**: v1.0.105 (2026-06-07)
- **特点**: 无需 Office 安装、跨平台、CLI 驱动

## 📥 安装步骤

### 方法 1：自动下载（推荐，需网络畅通）
```bash
# 进入 hermes venv bin 目录
cd /opt/hermes/.venv/bin

# 下载对应架构版本
wget https://github.com/iOfficeAI/OfficeCLI/releases/download/v1.0.105/officecli-linux-arm64 -O officecli

# 设置权限
chmod +x officecli
chown hermes:hermes officecli
```

### 方法 2：手动下载（网络受限时）
如果网络访问 GitHub 较慢，请在服务器上手动执行：
```bash
cd /opt/hermes/.venv/bin
wget https://github.com/iOfficeAI/OfficeCLI/releases/download/v1.0.105/officecli-linux-arm64 -O officecli
chmod +x officecli
chown hermes:hermes officecli
./officecli --version
```

## ✅ 验证安装
```bash
./officecli --version
./officecli --help
```

## 🔧 常用命令
```bash
# 读取 Word 文档
officecli read word -f document.docx

# 生成 Excel 报表
officecli generate excel -t template.xlsx -d data.json -o output.xlsx

# 转换 PPT 为 PDF
officecli convert ppt -f presentation.pptx -o output.pdf
```

## 🚨 注意事项
1. 系统架构：确认下载正确版本（ARM64 vs x64）
2. 权限：确保 officecli 文件有执行权限且属于 hermes 用户
3. 网络限制：GitHub 访问可能较慢，建议手动下载