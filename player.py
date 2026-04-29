# -*- coding: utf-8 -*-
"""
HTML 演示放映器 (HTML Slide Presenter)
用法：
  双击 .slidehtml 文件（需先运行 register_file_assoc.bat）
  或：python player.py [文件路径]
  或：直接运行，然后点击"打开文件"选择
"""

import sys
import os
import re
import json
import logging
import webview

# ==================== 日志 ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('HTMLPresenter')

# ==================== 常量 ====================
APP_TITLE = 'HTML 演示放映器'
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
MIN_WIDTH = 960
MIN_HEIGHT = 600

# ==================== 预设模板 CSS ====================
TEMPLATES = {
    'none': {
        'name': '不使用模板（文件自带样式）',
        'css': ''
    },
    'white': {
        'name': '简约白底',
        'css': r'''
/* 简约白底模板 */
.presenter-tpl .slide {
    background: #ffffff !important;
    color: #2c3e50 !important;
    font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", sans-serif !important;
    padding: 8vh 10vw !important;
    width: 100vw !important;
    height: 100vh !important;
    text-align: center !important;
    box-sizing: border-box !important;
}
.presenter-tpl .slide.active {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
}
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    color: #2c3e50 !important;
    margin-bottom: 0.6em !important;
    font-weight: 700 !important;
}
.presenter-tpl .slide h1 { font-size: 5vw !important; }
.presenter-tpl .slide h2 { font-size: 3.5vw !important; }
.presenter-tpl .slide h3 { font-size: 2.8vw !important; }
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    font-size: 2vw !important;
    line-height: 1.8 !important;
    color: #555 !important;
}
.presenter-tpl .slide ul, .presenter-tpl .slide ol {
    text-align: left !important;
    max-width: 80% !important;
}
.presenter-tpl .slide code {
    background: #f0f0f0 !important;
    padding: 0.2em 0.6em !important;
    border-radius: 4px !important;
    font-size: 1.8vw !important;
}
.presenter-tpl .slide pre {
    background: #f8f8f8 !important;
    padding: 2vh 3vw !important;
    border-radius: 8px !important;
    border-left: 4px solid #3498db !important;
    text-align: left !important;
    max-width: 85% !important;
    overflow-x: auto !important;
}
.presenter-tpl .slide pre code {
    background: none !important;
    font-size: 1.6vw !important;
    line-height: 1.6 !important;
}
.presenter-tpl .slide img {
    max-width: 80% !important;
    max-height: 60vh !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
}
'''
    },
    'dark': {
        'name': '深色科技',
        'css': r'''
/* 深色科技模板 */
.presenter-tpl .slide {
    background: linear-gradient(135deg, #0c0c1d 0%, #1a1a3e 50%, #0c0c1d 100%) !important;
    color: #e0e0e0 !important;
    font-family: "Consolas", "Microsoft YaHei", "Courier New", monospace !important;
    padding: 8vh 10vw !important;
    width: 100vw !important;
    height: 100vh !important;
    text-align: center !important;
    box-sizing: border-box !important;
    position: relative !important;
}
.presenter-tpl .slide.active {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
}
.presenter-tpl .slide::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background-image: radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px) !important;
    background-size: 3vw 3vw !important;
    pointer-events: none !important;
}
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin-bottom: 0.6em !important;
    font-weight: 700 !important;
}
.presenter-tpl .slide h1 { font-size: 5vw !important; }
.presenter-tpl .slide h2 { font-size: 3.5vw !important; }
.presenter-tpl .slide h3 { font-size: 2.8vw !important; }
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    font-size: 2vw !important;
    line-height: 1.8 !important;
    color: #b0b0b0 !important;
}
.presenter-tpl .slide ul, .presenter-tpl .slide ol {
    text-align: left !important;
    max-width: 80% !important;
}
.presenter-tpl .slide li::marker { color: #00d2ff !important; }
.presenter-tpl .slide code {
    background: rgba(255,255,255,0.08) !important;
    padding: 0.2em 0.6em !important;
    border-radius: 4px !important;
    color: #4fc3f7 !important;
    font-size: 1.8vw !important;
}
.presenter-tpl .slide pre {
    background: rgba(0,0,0,0.4) !important;
    padding: 2vh 3vw !important;
    border-radius: 8px !important;
    border-left: 4px solid #00d2ff !important;
    text-align: left !important;
    max-width: 85% !important;
    overflow-x: auto !important;
}
.presenter-tpl .slide pre code {
    background: none !important;
    color: #e0e0e0 !important;
    font-size: 1.6vw !important;
    line-height: 1.6 !important;
}
.presenter-tpl .slide img {
    max-width: 80% !important;
    max-height: 60vh !important;
    border-radius: 12px !important;
    box-shadow: 0 0 30px rgba(0,210,255,0.2) !important;
}
'''
    },
    'gradient': {
        'name': '渐变多彩',
        'css': r'''
/* 渐变多彩模板 - 每页不同渐变 */
.presenter-tpl .slide {
    color: #fff !important;
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif !important;
    padding: 8vh 10vw !important;
    width: 100vw !important;
    height: 100vh !important;
    text-align: center !important;
    box-sizing: border-box !important;
}
.presenter-tpl .slide.active {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
}
.presenter-tpl .slide:nth-child(6n+1) { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; }
.presenter-tpl .slide:nth-child(6n+2) { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important; }
.presenter-tpl .slide:nth-child(6n+3) { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important; }
.presenter-tpl .slide:nth-child(6n+4) { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%) !important; }
.presenter-tpl .slide:nth-child(6n+5) { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%) !important; }
.presenter-tpl .slide:nth-child(6n+6) { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%) !important; }
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    text-shadow: 2px 2px 10px rgba(0,0,0,0.2) !important;
    margin-bottom: 0.6em !important;
    font-weight: 700 !important;
}
.presenter-tpl .slide h1 { font-size: 5vw !important; }
.presenter-tpl .slide h2 { font-size: 3.5vw !important; }
.presenter-tpl .slide h3 { font-size: 2.8vw !important; }
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    font-size: 2vw !important;
    line-height: 1.8 !important;
    opacity: 0.95 !important;
}
.presenter-tpl .slide ul, .presenter-tpl .slide ol {
    text-align: left !important;
    max-width: 80% !important;
}
.presenter-tpl .slide code {
    background: rgba(0,0,0,0.25) !important;
    padding: 0.2em 0.6em !important;
    border-radius: 4px !important;
    font-size: 1.8vw !important;
}
.presenter-tpl .slide pre {
    background: rgba(0,0,0,0.35) !important;
    padding: 2vh 3vw !important;
    border-radius: 8px !important;
    border-left: 4px solid rgba(255,255,255,0.4) !important;
    text-align: left !important;
    max-width: 85% !important;
    overflow-x: auto !important;
}
.presenter-tpl .slide pre code {
    background: none !important;
    color: #fff !important;
    font-size: 1.6vw !important;
    line-height: 1.6 !important;
}
.presenter-tpl .slide img {
    max-width: 80% !important;
    max-height: 60vh !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
}
'''
    },
    'business': {
        'name': '商务蓝',
        'css': r'''
/* 商务蓝模板 */
.presenter-tpl .slide {
    background: #f5f7fa !important;
    color: #2c3e50 !important;
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif !important;
    padding: 8vh 10vw !important;
    width: 100vw !important;
    height: 100vh !important;
    text-align: center !important;
    box-sizing: border-box !important;
    position: relative !important;
}
.presenter-tpl .slide.active {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
}
.presenter-tpl .slide::before {
    content: '' !important;
    position: absolute !important;
    top: 0; left: 0; right: 0 !important;
    height: 6px !important;
    background: linear-gradient(90deg, #2196F3, #1565C0) !important;
}
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    color: #1565C0 !important;
    margin-bottom: 0.6em !important;
    font-weight: 700 !important;
}
.presenter-tpl .slide h1 { font-size: 5vw !important; }
.presenter-tpl .slide h2 { font-size: 3.5vw !important; }
.presenter-tpl .slide h3 { font-size: 2.8vw !important; }
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    font-size: 2vw !important;
    line-height: 1.8 !important;
    color: #555 !important;
}
.presenter-tpl .slide ul, .presenter-tpl .slide ol {
    text-align: left !important;
    max-width: 80% !important;
}
.presenter-tpl .slide code {
    background: #e3f2fd !important;
    padding: 0.2em 0.6em !important;
    border-radius: 4px !important;
    color: #1565C0 !important;
    font-size: 1.8vw !important;
}
.presenter-tpl .slide pre {
    background: #fff !important;
    padding: 2vh 3vw !important;
    border-radius: 8px !important;
    border-left: 4px solid #2196F3 !important;
    text-align: left !important;
    max-width: 85% !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
}
.presenter-tpl .slide pre code {
    background: none !important;
    color: #333 !important;
    font-size: 1.6vw !important;
}
.presenter-tpl .slide img {
    max-width: 80% !important;
    max-height: 60vh !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}
'''
    },
    'ink': {
        'name': '水墨风',
        'css': r'''
/* 水墨风模板 */
.presenter-tpl .slide {
    background: #faf8f5 !important;
    color: #333 !important;
    font-family: "KaiTi", "STKaiti", "Microsoft YaHei", serif !important;
    padding: 8vh 10vw !important;
    width: 100vw !important;
    height: 100vh !important;
    text-align: center !important;
    box-sizing: border-box !important;
    position: relative !important;
}
.presenter-tpl .slide.active {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
}
.presenter-tpl .slide::before {
    content: '' !important;
    position: absolute !important;
    inset: 3vh 3vw !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    pointer-events: none !important;
}
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    color: #222 !important;
    margin-bottom: 0.6em !important;
    font-weight: 400 !important;
    letter-spacing: 0.1em !important;
}
.presenter-tpl .slide h1 { font-size: 5vw !important; }
.presenter-tpl .slide h2 { font-size: 3.5vw !important; }
.presenter-tpl .slide h3 { font-size: 2.8vw !important; }
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    font-size: 2vw !important;
    line-height: 2 !important;
    color: #555 !important;
}
.presenter-tpl .slide ul, .presenter-tpl .slide ol {
    text-align: left !important;
    max-width: 80% !important;
}
.presenter-tpl .slide code {
    background: rgba(0,0,0,0.06) !important;
    padding: 0.2em 0.6em !important;
    border-radius: 4px !important;
    font-size: 1.8vw !important;
    color: #333 !important;
}
.presenter-tpl .slide pre {
    background: #fff !important;
    padding: 2vh 3vw !important;
    border-radius: 8px !important;
    border-left: 4px solid #999 !important;
    text-align: left !important;
    max-width: 85% !important;
    overflow-x: auto !important;
}
.presenter-tpl .slide pre code {
    background: none !important;
    color: #333 !important;
    font-size: 1.6vw !important;
    line-height: 1.6 !important;
}
.presenter-tpl .slide img {
    max-width: 70% !important;
    max-height: 55vh !important;
    border-radius: 4px !important;
    filter: grayscale(20%) !important;
}
'''
    }
}


# ==================== HTML/CSS/JS 模板 ====================
HTML_TEMPLATE = r'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
    height: 100%; width: 100%;
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    background: #1a1a2e; color: #fff;
    display: flex; flex-direction: column;
    overflow: hidden; user-select: none;
}

/* ---------- 工具栏 ---------- */
.toolbar {
    height: 48px; flex-shrink: 0;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    display: flex; align-items: center;
    padding: 0 16px; gap: 12px;
}
.toolbar .title {
    font-size: 14px; font-weight: 600;
    color: #e0e0e0;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.toolbar select {
    background: #0f3460; color: #e0e0e0; border: 1px solid rgba(255,255,255,0.15);
    padding: 5px 10px; border-radius: 6px; cursor: pointer;
    font-size: 12px; font-family: inherit; outline: none;
    max-width: 200px;
}
.toolbar select:hover { border-color: rgba(255,255,255,0.3); }
.btn {
    background: #0f3460; color: #e0e0e0; border: none;
    padding: 6px 16px; border-radius: 6px; cursor: pointer;
    font-size: 12px; font-family: inherit;
    transition: background 0.2s;
    white-space: nowrap;
}
.btn:hover { background: #1a5276; }
.btn:active { background: #0a2d4e; }

/* ---------- 幻灯片区域 ---------- */
.slide-container {
    flex: 1; position: relative;
    background: #111; overflow: hidden;
}
/* 显隐由 JS 通过 element.style.display + .active 类控制 */
/* 无模板时，.active 默认 display: flex 确保布局正确 */
.slide-container .slide.active { display: flex; }

/* ---------- 底部导航 ---------- */
.nav-bar {
    height: 44px; flex-shrink: 0;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-top: 1px solid rgba(255,255,255,0.08);
    display: flex; align-items: center; justify-content: center;
    gap: 12px; padding: 0 20px; position: relative;
}
.nav-btn {
    background: #0f3460; color: #e0e0e0; border: none;
    width: 32px; height: 32px; border-radius: 50%;
    font-size: 14px; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: background 0.2s;
}
.nav-btn:hover { background: #1a5276; }
.nav-btn:active { background: #0a2d4e; }
.slide-info {
    font-size: 13px; color: #bdc3c7;
    min-width: 100px; text-align: center;
}
.nav-hint {
    font-size: 11px; color: #444;
    position: absolute; right: 16px;
}
</style>
</head>
<body>

<div class="toolbar">
    <span class="title">HTML 演示放映器</span>
    <select id="templateSelect" onchange="applyTemplate(this.value)">
        <option value="none">不使用模板</option>
        <option value="white" selected>简约白底</option>
        <option value="dark">深色科技</option>
        <option value="gradient">渐变多彩</option>
        <option value="business">商务蓝</option>
        <option value="ink">水墨风</option>
    </select>
    <button class="btn" onclick="openFile()">打开文件</button>
</div>

<div class="slide-container presenter-tpl" id="slideContainer"></div>

<div class="nav-bar">
    <button class="nav-btn" onclick="prevSlide()" title="上一页">&#9664;</button>
    <span class="slide-info" id="slideInfo">第 0 / 0 页</span>
    <button class="nav-btn" onclick="nextSlide()" title="下一页">&#9654;</button>
    <span class="nav-hint">&larr; &rarr; 翻页 &nbsp;|&nbsp; F11 全屏</span>
</div>

<script>
// ==================== 状态 ====================
let slides = [];
let currentIndex = 0;
let userStyleEls = [];
let userScriptEls = [];

// ==================== 模板系统 ====================
function applyTemplate(tplKey) {
    const container = document.getElementById('slideContainer');
    // 通过 Python API 获取模板 CSS
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.get_template_css(tplKey).then(function(css) {
            injectTemplateCSS(css, tplKey);
        });
    }
}

function injectTemplateCSS(css, tplKey) {
    // 移除旧模板样式
    let oldTpl = document.getElementById('templateStyle');
    if (oldTpl) oldTpl.remove();

    // 添加/移除 presenter-tpl 类
    const container = document.getElementById('slideContainer');
    if (tplKey === 'none') {
        container.classList.remove('presenter-tpl');
    } else {
        container.classList.add('presenter-tpl');
    }

    // 注入新模板 CSS
    if (css) {
        const style = document.createElement('style');
        style.id = 'templateStyle';
        style.textContent = css;
        document.head.appendChild(style);
    }

    // 重新应用显隐状态（内联样式确保不被模板覆盖）
    slides.forEach((el, i) => {
        if (i === currentIndex) {
            el.classList.add('active');
            el.style.display = '';
        } else {
            el.classList.remove('active');
            el.style.display = 'none';
        }
    });
}

// ==================== 初始化 ====================
function initSlides(data) {
    const container = document.getElementById('slideContainer');
    container.innerHTML = '';
    slides = [];

    // 移除旧的用户样式/脚本
    userStyleEls.forEach(el => el.remove());
    userStyleEls = [];
    userScriptEls.forEach(el => el.remove());
    userScriptEls = [];

    // 设置 <base> 让外部资源的相对路径正确解析
    let baseEl = document.getElementById('userBase');
    if (baseEl) baseEl.remove();
    if (data.base_url) {
        baseEl = document.createElement('base');
        baseEl.id = 'userBase';
        baseEl.href = data.base_url;
        document.head.appendChild(baseEl);
        userStyleEls.push(baseEl);
    }

    // 注入用户的 <head> 样式（style/link）
    if (data.head) {
        const tempHead = document.createElement('div');
        tempHead.innerHTML = data.head;
        tempHead.querySelectorAll('style, link[rel="stylesheet"]').forEach(el => {
            const clone = el.cloneNode(true);
            document.head.appendChild(clone);
            userStyleEls.push(clone);
        });
    }

    // 直接插入用户原始的 <div class="slide ..."> 元素
    data.slides.forEach((html, i) => {
        const div = document.createElement('div');
        div.innerHTML = html;
        const slideEl = div.firstElementChild;
        if (slideEl) {
            // 用内联 style.display + .active 类控制显隐
            if (i === 0) slideEl.classList.add('active');
            slideEl.style.display = (i === 0) ? '' : 'none';
            container.appendChild(slideEl);
            slides.push(slideEl);
        }
    });

    // 注入 body 级 <script>
    if (data.scripts) {
        data.scripts.forEach(scriptHtml => {
            const temp = document.createElement('div');
            temp.innerHTML = scriptHtml;
            const scriptEl = temp.querySelector('script');
            if (scriptEl) {
                const newScript = document.createElement('script');
                if (scriptEl.src) newScript.src = scriptEl.src;
                else newScript.textContent = scriptEl.textContent;
                document.body.appendChild(newScript);
                userScriptEls.push(newScript);
            }
        });
    }

    currentIndex = 0;
    updateInfo();
    updateToolbar(data.title, data.total);

    // 应用当前选择的模板
    const tplKey = document.getElementById('templateSelect').value;
    if (tplKey !== 'none') {
        applyTemplate(tplKey);
    }
}

// ==================== 导航 ====================
function showSlide(index) {
    if (index < 0 || index >= slides.length) return;
    slides[currentIndex].classList.remove('active');
    slides[currentIndex].style.display = 'none';
    currentIndex = index;
    slides[currentIndex].classList.add('active');
    slides[currentIndex].style.display = '';
    updateInfo();
    syncIndex();
}

function nextSlide() { showSlide(currentIndex + 1); }
function prevSlide() { showSlide(currentIndex - 1); }
function firstSlide() { showSlide(0); }
function lastSlide() { showSlide(slides.length - 1); }

function jumpTo(pageNum) {
    const idx = pageNum - 1;
    if (idx >= 0 && idx < slides.length) showSlide(idx);
}

// ==================== 更新显示 ====================
function updateInfo() {
    document.getElementById('slideInfo').textContent =
        '第 ' + (slides.length ? currentIndex + 1 : 0) + ' / ' + slides.length + ' 页';
}

function updateToolbar(title, total) {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.set_window_title(title + ' - ' + total + ' 页');
    }
}

function syncIndex() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.update_index(currentIndex);
    }
}

// ==================== 打开文件 ====================
function openFile() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.open_file_dialog().then(function(result) {
            if (result) initSlides(result);
        });
    }
}

// ==================== 键盘 ====================
document.addEventListener('keydown', function(e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' ||
        e.target.tagName === 'SELECT') return;

    switch(e.key) {
        case 'ArrowRight': case ' ': case 'PageDown': case 'Enter':
            e.preventDefault(); nextSlide(); break;
        case 'ArrowLeft': case 'Backspace': case 'PageUp':
            e.preventDefault(); prevSlide(); break;
        case 'Home': e.preventDefault(); firstSlide(); break;
        case 'End': e.preventDefault(); lastSlide(); break;
        case 'Escape':
            if (window.pywebview && window.pywebview.api)
                window.pywebview.api.exit_fullscreen();
            break;
        case 'F11':
            e.preventDefault();
            if (window.pywebview && window.pywebview.api)
                window.pywebview.api.toggle_fullscreen();
            break;
    }
});

// ==================== pywebview 就绪 ====================
function onReady() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.on_ready();
    }
}

if (window.pywebview) {
    window.addEventListener('pywebviewready', onReady);
} else {
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            if (window.pywebview) onReady();
        }, 200);
    });
}
</script>
</body>
</html>'''


# ==================== Python API ====================
class PresentationAPI:

    def __init__(self):
        self.window = None
        self.current_file = None
        self.pending_file = None
        self.current_index = 0

    def set_window(self, window):
        self.window = window

    # ---------- JS 可调用的方法 ----------

    def on_ready(self):
        if self.pending_file:
            path = self.pending_file
            self.pending_file = None
            result = self.load_file(path)
            if result:
                self.window.evaluate_js(f'initSlides({json.dumps(result)})')

    def open_file_dialog(self):
        file_types = ('演示文件 (*.slidehtml;*.html;*.htm)', '所有文件 (*.*)')
        result = self.window.create_file_dialog(
            webview.OPEN_DIALOG,
            file_types=file_types
        )
        if not result:
            return None
        path = result[0] if isinstance(result, (list, tuple)) else str(result)
        return self.load_file(path)

    def get_template_css(self, tpl_key):
        """返回指定模板的 CSS"""
        tpl = TEMPLATES.get(tpl_key, TEMPLATES['none'])
        return tpl['css']

    @staticmethod
    def _find_slide_content(html, start):
        depth = 0
        i = start
        tag_re = re.compile(r'<(/?)div\b', re.IGNORECASE)
        while i < len(html):
            m = tag_re.search(html, i)
            if not m:
                break
            if m.group(1) == '/':
                depth -= 1
                if depth == 0:
                    return html[start:m.start()]
            else:
                depth += 1
            i = m.end()
        return html[start:]

    def load_file(self, path):
        try:
            path = os.path.abspath(path)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f'读取文件失败: {e}')
            return None

        self.current_file = path
        self.current_index = 0

        # 提取 <head>
        head_match = re.search(r'<head[^>]*>(.*?)</head>', content, re.DOTALL | re.IGNORECASE)
        head_html = head_match.group(1).strip() if head_match else ''

        # 提取 <body>
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        body_html = body_match.group(1) if body_match else content

        # 提取 <div class="slide..."> 块
        slides = []
        for m in re.finditer(
            r'<div\s+class=["\']slide\b[^"\']*["\'][^>]*>',
            body_html, re.DOTALL | re.IGNORECASE
        ):
            inner = self._find_slide_content(body_html, m.end())
            full_tag = body_html[m.start():m.end()]
            slides.append(full_tag + inner + '</div>')

        if not slides:
            logger.warning('未找到 class="slide" 的元素，将整个页面作为一页显示')
            slides = [body_html]

        # 提取 body 内的 <script>
        body_scripts = re.findall(r'<script\b[^>]*>.*?</script>', body_html, re.DOTALL | re.IGNORECASE)

        # 提取标题
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else os.path.splitext(os.path.basename(path))[0]

        total = len(slides)
        logger.info(f'已加载: {os.path.basename(path)} ({total} 页)')

        return {
            'title': title,
            'slides': slides,
            'total': total,
            'head': head_html,
            'scripts': body_scripts,
            'base_url': 'file:///' + os.path.dirname(path).replace('\\', '/') + '/'
        }

    def update_index(self, index):
        self.current_index = index

    def set_window_title(self, title):
        if self.window:
            self.window.set_title(f'{APP_TITLE} - {title}')

    def toggle_fullscreen(self):
        if self.window:
            self.window.toggle_fullscreen()

    def exit_fullscreen(self):
        if self.window and self.window.fullscreen:
            self.window.toggle_fullscreen()


# ==================== 主程序 ====================
def main():
    file_path = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isfile(arg):
            file_path = os.path.abspath(arg)
            logger.info(f'命令行文件: {file_path}')

    api = PresentationAPI()
    api.pending_file = file_path

    window = webview.create_window(
        title=APP_TITLE,
        html=HTML_TEMPLATE,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        min_size=(MIN_WIDTH, MIN_HEIGHT),
        js_api=api
    )
    api.set_window(window)

    logger.info('放映器启动')
    webview.start(debug=False)


if __name__ == '__main__':
    main()
