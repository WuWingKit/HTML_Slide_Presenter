# GitHub 发布指南

## 1. 创建仓库

1. 打开 https://github.com/new
2. **Repository name** 填：`HTMLSlidePresenter`
3. **Description** 填：
   > 用 HTML 做 PPT 的 Windows 桌面放映器。内置 5 套模板，支持 AI 生成。Make PPTs with HTML — 5 built-in templates, AI-powered generation.
4. 选择 **Public**
5. 不要勾选 "Add a README file"
6. 点击 **Create repository**

## 2. 推送到 GitHub

```bash
git init
git add .
git commit -m "🎉 Initial commit"

git remote add origin https://github.com/你的用户名/HTMLSlidePresenter.git
git branch -M main
git push -u origin main
```

## 3. 仓库设置

### 3.1 添加 Topics
在仓库页面点击齿轮 → Topics：
```
html presentation slides powerpoint html-slides webview desktop-app windows python
```

### 3.2 About 描述
- **Description:** 用 HTML 做 PPT 的 Windows 桌面放映器 | Make PPTs with HTML
- **Topics:** 同上

## 4. 发布 Release

1. 点击 **Releases** → **Create a new release**
2. **Tag:** `v1.0.0`
3. **Title:** `v1.0.0 - 首次发布`
4. **Description:**

```markdown
## HTML Slide Presenter v1.0

用 HTML 做 PPT，自由设计，一键播放。

### 功能
- 5 套预设风格模板
- 文字自适应缩放
- 键盘翻页 / F11 全屏
- 双击 .slidehtml 文件直接打开
- 支持 AI (Claude/GPT) 通过 AGENT.md 规范生成幻灯片

### 安装
pip install pywebview

### 运行
python player.py demo.slidehtml
```

5. 点击 **Publish release**

## 5. 推荐简介

**中文：**
> HTML Slide Presenter — 用 HTML 做 PPT 的 Windows 桌面放映器。内置 5 套模板，支持 AI 生成，完全开源。

**English:**
> HTML Slide Presenter — A Windows desktop app that plays HTML files as PowerPoint slides. 5 templates, AI generation support, fully open-source.
