# -*- coding: utf-8 -*-
"""
HTML Slide Presenter
Usage:
  Double-click .slidehtml file (run register_file_assoc.bat first)
  or: python player.py [file_path]
  or: run directly, then click "Open File"
"""

import sys
import os
import re
import json
import logging
import webview

# ==================== Logging ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('HTMLPresenter')

# ==================== Constants ====================
APP_TITLE = 'HTML Slide Presenter'
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
MIN_WIDTH = 960
MIN_HEIGHT = 600

# ==================== Template CSS ====================
TEMPLATES = {
    'none': {
        'name': 'Custom Styles',
        'css': ''
    },
    'white': {
        'name': 'Clean White',
        'css': r'''
/* Clean White Template */
.presenter-tpl .slide {
    background: #ffffff;
    color: #1a1a2e;
    font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
}
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    color: #1a1a2e;
    font-weight: 700;
    letter-spacing: -0.02em;
}
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    color: #444;
    line-height: 1.8;
}
.presenter-tpl .slide a { color: #2563eb; }
.presenter-tpl .slide code {
    background: #f1f5f9;
    color: #334155;
    padding: 0.15em 0.5em;
    border-radius: 4px;
    font-size: 0.9em;
}
.presenter-tpl .slide pre {
    background: #f8fafc;
    border-left: 3px solid #2563eb;
    border-radius: 8px;
    padding: 1.5em;
    text-align: left;
    overflow-x: auto;
}
.presenter-tpl .slide pre code {
    background: none;
    color: #334155;
    padding: 0;
}
.presenter-tpl .slide img {
    border-radius: 8px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
.presenter-tpl .slide blockquote {
    border-left: 3px solid #cbd5e1;
    color: #64748b;
    font-style: italic;
}
.presenter-tpl .slide table { border-collapse: collapse; }
.presenter-tpl .slide th {
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 600;
}
.presenter-tpl .slide td {
    border-bottom: 1px solid #e2e8f0;
}
'''
    },
    'dark': {
        'name': 'Dark Tech',
        'css': r'''
/* Dark Tech Template */
.presenter-tpl .slide {
    background: linear-gradient(160deg, #0a0a1a 0%, #12122a 40%, #0d1b2a 100%);
    color: #c8d6e5;
    font-family: "SF Mono", "Consolas", "Microsoft YaHei", "Courier New", monospace;
    position: relative;
}
.presenter-tpl .slide::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(circle at 20% 30%, rgba(0,210,255,0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(100,100,255,0.03) 0%, transparent 50%),
        radial-gradient(circle, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 24px 24px;
    pointer-events: none;
}
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    background: linear-gradient(135deg, #00d2ff 0%, #7b68ee 50%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    color: #94a3b8;
    line-height: 1.8;
}
.presenter-tpl .slide a {
    color: #38bdf8;
    text-decoration: underline;
    text-underline-offset: 2px;
}
.presenter-tpl .slide li::marker { color: #00d2ff; }
.presenter-tpl .slide code {
    background: rgba(0,210,255,0.08);
    color: #38bdf8;
    padding: 0.15em 0.5em;
    border-radius: 4px;
    font-size: 0.9em;
}
.presenter-tpl .slide pre {
    background: rgba(0,0,0,0.5);
    border: 1px solid rgba(0,210,255,0.12);
    border-left: 3px solid #00d2ff;
    border-radius: 8px;
    padding: 1.5em;
    text-align: left;
    overflow-x: auto;
}
.presenter-tpl .slide pre code {
    background: none;
    color: #e2e8f0;
    padding: 0;
}
.presenter-tpl .slide img {
    border-radius: 12px;
    box-shadow: 0 0 40px rgba(0,210,255,0.1), 0 8px 32px rgba(0,0,0,0.3);
}
.presenter-tpl .slide blockquote {
    border-left: 3px solid rgba(0,210,255,0.3);
    color: #64748b;
    font-style: italic;
}
.presenter-tpl .slide table { border-collapse: collapse; }
.presenter-tpl .slide th {
    background: rgba(0,210,255,0.08);
    color: #00d2ff;
    font-weight: 600;
}
.presenter-tpl .slide td {
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: #94a3b8;
}
'''
    },
    'gradient': {
        'name': 'Gradient',
        'css': r'''
/* Gradient Template - different gradient per page */
.presenter-tpl .slide {
    color: #ffffff;
    font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", sans-serif;
}
.presenter-tpl .slide:nth-child(6n+1) { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); }
.presenter-tpl .slide:nth-child(6n+2) { background: linear-gradient(135deg, #ec4899 0%, #f43f5e 50%, #fb7185 100%); }
.presenter-tpl .slide:nth-child(6n+3) { background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 50%, #22d3ee 100%); }
.presenter-tpl .slide:nth-child(6n+4) { background: linear-gradient(135deg, #10b981 0%, #34d399 50%, #6ee7b7 100%); }
.presenter-tpl .slide:nth-child(6n+5) { background: linear-gradient(135deg, #f59e0b 0%, #f97316 50%, #fb923c 100%); }
.presenter-tpl .slide:nth-child(6n+6) { background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 50%, #c4b5fd 100%); }
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    text-shadow: 0 2px 12px rgba(0,0,0,0.15);
    font-weight: 700;
}
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    color: rgba(255,255,255,0.92);
    line-height: 1.8;
}
.presenter-tpl .slide a {
    color: #fff;
    text-decoration: underline;
    text-underline-offset: 2px;
}
.presenter-tpl .slide code {
    background: rgba(0,0,0,0.2);
    color: rgba(255,255,255,0.95);
    padding: 0.15em 0.5em;
    border-radius: 4px;
    font-size: 0.9em;
}
.presenter-tpl .slide pre {
    background: rgba(0,0,0,0.3);
    border-left: 3px solid rgba(255,255,255,0.4);
    border-radius: 8px;
    padding: 1.5em;
    text-align: left;
    overflow-x: auto;
}
.presenter-tpl .slide pre code {
    background: none;
    color: #fff;
    padding: 0;
}
.presenter-tpl .slide img {
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
.presenter-tpl .slide blockquote {
    border-left: 3px solid rgba(255,255,255,0.4);
    color: rgba(255,255,255,0.75);
    font-style: italic;
}
.presenter-tpl .slide table { border-collapse: collapse; }
.presenter-tpl .slide th {
    background: rgba(0,0,0,0.15);
    font-weight: 600;
}
.presenter-tpl .slide td {
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
'''
    },
    'business': {
        'name': 'Business Blue',
        'css': r'''
/* Business Blue Template */
.presenter-tpl .slide {
    background: #f8fafc;
    color: #1e293b;
    font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", sans-serif;
    position: relative;
}
.presenter-tpl .slide::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #2563eb, #3b82f6, #60a5fa);
}
.presenter-tpl .slide::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: #e2e8f0;
}
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    color: #1e3a5f;
    font-weight: 700;
}
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    color: #475569;
    line-height: 1.8;
}
.presenter-tpl .slide a { color: #2563eb; }
.presenter-tpl .slide code {
    background: #eff6ff;
    color: #1d4ed8;
    padding: 0.15em 0.5em;
    border-radius: 4px;
    font-size: 0.9em;
}
.presenter-tpl .slide pre {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #2563eb;
    border-radius: 8px;
    padding: 1.5em;
    text-align: left;
    overflow-x: auto;
}
.presenter-tpl .slide pre code {
    background: none;
    color: #334155;
    padding: 0;
}
.presenter-tpl .slide img {
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}
.presenter-tpl .slide blockquote {
    border-left: 3px solid #93c5fd;
    color: #64748b;
    font-style: italic;
    background: #f0f9ff;
    padding: 0.5em 1em;
    border-radius: 0 8px 8px 0;
}
.presenter-tpl .slide table { border-collapse: collapse; }
.presenter-tpl .slide th {
    background: #1e3a5f;
    color: #fff;
    font-weight: 600;
}
.presenter-tpl .slide td {
    border-bottom: 1px solid #e2e8f0;
}
'''
    },
    'ink': {
        'name': 'Ink Style',
        'css': r'''
/* Ink Style Template */
.presenter-tpl .slide {
    background: #faf8f5;
    color: #2c2c2c;
    font-family: "KaiTi", "STKaiti", "Noto Serif SC", "Microsoft YaHei", serif;
    position: relative;
}
.presenter-tpl .slide::before {
    content: '';
    position: absolute;
    inset: 2.5vh 2.5vw;
    border: 1px solid rgba(0,0,0,0.06);
    pointer-events: none;
}
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    color: #1a1a1a;
    font-weight: 400;
    letter-spacing: 0.15em;
}
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    color: #555;
    line-height: 2;
    letter-spacing: 0.05em;
}
.presenter-tpl .slide a {
    color: #555;
    text-decoration: underline;
    text-underline-offset: 3px;
}
.presenter-tpl .slide code {
    background: rgba(0,0,0,0.04);
    color: #444;
    padding: 0.15em 0.5em;
    border-radius: 3px;
    font-size: 0.9em;
}
.presenter-tpl .slide pre {
    background: #fff;
    border-left: 2px solid #999;
    border-radius: 4px;
    padding: 1.5em;
    text-align: left;
    overflow-x: auto;
}
.presenter-tpl .slide pre code {
    background: none;
    color: #333;
    padding: 0;
}
.presenter-tpl .slide img {
    border-radius: 2px;
    filter: grayscale(15%) contrast(0.95);
}
.presenter-tpl .slide blockquote {
    border-left: 2px solid #bbb;
    color: #777;
    font-style: italic;
}
.presenter-tpl .slide table { border-collapse: collapse; }
.presenter-tpl .slide th {
    background: rgba(0,0,0,0.04);
    font-weight: 600;
    color: #333;
}
.presenter-tpl .slide td {
    border-bottom: 1px solid rgba(0,0,0,0.06);
}
'''
    },
    'nord': {
        'name': 'Nord Cool',
        'css': r'''
/* Nord Cool Template */
.presenter-tpl .slide {
    background: #2e3440;
    color: #d8dee9;
    font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", sans-serif;
}
.presenter-tpl .slide h1,
.presenter-tpl .slide h2,
.presenter-tpl .slide h3 {
    color: #88c0d0;
    font-weight: 700;
}
.presenter-tpl .slide p,
.presenter-tpl .slide li {
    color: #d8dee9;
    line-height: 1.8;
}
.presenter-tpl .slide a { color: #81a1c1; }
.presenter-tpl .slide code {
    background: rgba(136,192,208,0.1);
    color: #88c0d0;
    padding: 0.15em 0.5em;
    border-radius: 4px;
    font-size: 0.9em;
}
.presenter-tpl .slide pre {
    background: #3b4252;
    border-left: 3px solid #88c0d0;
    border-radius: 8px;
    padding: 1.5em;
    text-align: left;
    overflow-x: auto;
}
.presenter-tpl .slide pre code {
    background: none;
    color: #d8dee9;
    padding: 0;
}
.presenter-tpl .slide img {
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.presenter-tpl .slide blockquote {
    border-left: 3px solid #4c566a;
    color: #81a1c1;
    font-style: italic;
}
.presenter-tpl .slide table { border-collapse: collapse; }
.presenter-tpl .slide th {
    background: #3b4252;
    color: #88c0d0;
    font-weight: 600;
}
.presenter-tpl .slide td {
    border-bottom: 1px solid #4c566a;
}
'''
    }
}


# ==================== HTML/CSS/JS Template ====================
HTML_TEMPLATE = r'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
    height: 100%; width: 100%;
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    background: #0f0f1a; color: #fff;
    display: flex; flex-direction: column;
    overflow: hidden; user-select: none;
}

/* ---------- Toolbar ---------- */
.toolbar {
    height: 44px; flex-shrink: 0;
    background: #16162a;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    display: flex; align-items: center;
    padding: 0 14px; gap: 10px;
}
.toolbar .title {
    font-size: 13px; font-weight: 600;
    color: #a0a0b8;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    max-width: 280px;
    flex-shrink: 1;
}
.toolbar select {
    background: #1e1e38; color: #c0c0d8; border: 1px solid rgba(255,255,255,0.1);
    padding: 4px 8px; border-radius: 6px; cursor: pointer;
    font-size: 12px; font-family: inherit; outline: none;
    max-width: 180px;
}
.toolbar select:hover { border-color: rgba(255,255,255,0.2); }
.toolbar .sep {
    width: 1px; height: 20px;
    background: rgba(255,255,255,0.08);
    flex-shrink: 0;
}
.btn {
    background: #1e1e38; color: #c0c0d8; border: 1px solid rgba(255,255,255,0.08);
    padding: 5px 14px; border-radius: 6px; cursor: pointer;
    font-size: 12px; font-family: inherit;
    transition: all 0.15s;
    white-space: nowrap;
}
.btn:hover { background: #2a2a50; border-color: rgba(255,255,255,0.15); }
.btn:active { background: #18183a; }

/* ---------- Slide Viewport ---------- */
.slide-viewport {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0a0a14;
    overflow: hidden;
    position: relative;
}
.slide-container {
    position: relative;
    aspect-ratio: 16 / 9;
    width: 100%;
    height: 100%;
    max-width: calc((100vh - 88px) * 16 / 9);
    overflow: hidden;
}
/* Custom HTML mode: slides fill container, layout controlled by user CSS */
.slide-container .slide {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}
/* Display controlled by JS inline style + user/template CSS — viewer does not force display */
/* Template mode: flex centering so content is vertically/horizontally centered */
.presenter-tpl .slide.active {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 6vh 8vw;
    text-align: center;
}
/* Template mode: responsive font sizes via clamp() */
.presenter-tpl .slide h1 { font-size: clamp(36px, 5vw, 80px); }
.presenter-tpl .slide h2 { font-size: clamp(28px, 3.8vw, 60px); }
.presenter-tpl .slide h3 { font-size: clamp(22px, 2.8vw, 44px); }
.presenter-tpl .slide p,
.presenter-tpl .slide li { font-size: clamp(15px, 2vw, 30px); }
.presenter-tpl .slide ul, .presenter-tpl .slide ol {
    text-align: left;
    max-width: 85%;
}
.presenter-tpl .slide code { font-size: clamp(13px, 1.5vw, 24px); }
.presenter-tpl .slide pre code { font-size: clamp(12px, 1.3vw, 20px); }
.presenter-tpl .slide img {
    max-width: 80%;
    max-height: 55vh;
    object-fit: contain;
}
.presenter-tpl .slide blockquote {
    max-width: 80%;
    padding: 0.5em 1.2em;
}
.presenter-tpl .slide table {
    max-width: 90%;
}
.presenter-tpl .slide th,
.presenter-tpl .slide td {
    padding: 0.5em 1em;
}

/* ---------- Bottom Nav ---------- */
.nav-bar {
    height: 44px; flex-shrink: 0;
    background: #16162a;
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex; align-items: center; justify-content: center;
    gap: 10px; padding: 0 16px; position: relative;
}
.nav-btn {
    background: #1e1e38; color: #c0c0d8; border: 1px solid rgba(255,255,255,0.08);
    width: 30px; height: 30px; border-radius: 50%;
    font-size: 12px; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.15s;
}
.nav-btn:hover { background: #2a2a50; border-color: rgba(255,255,255,0.15); }
.nav-btn:active { background: #18183a; }
.slide-info {
    font-size: 12px; color: #666;
    min-width: 90px; text-align: center;
}
.nav-hint {
    font-size: 11px; color: #333;
    position: absolute; right: 14px;
}
/* Progress bar */
.progress-track {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: rgba(255,255,255,0.03);
}
.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    transition: width 0.3s ease;
    width: 0;
}
</style>
</head>
<body>

<div class="toolbar">
    <span class="title" id="titleText">HTML Slide Presenter</span>
    <div class="sep"></div>
    <select id="templateSelect" onchange="applyTemplate(this.value)">
        <option value="none">Custom Styles</option>
        <option value="white" selected>Clean White</option>
        <option value="dark">Dark Tech</option>
        <option value="gradient">Gradient</option>
        <option value="business">Business Blue</option>
        <option value="ink">Ink Style</option>
        <option value="nord">Nord Cool</option>
    </select>
    <button class="btn" onclick="openFile()">Open File</button>
</div>

<div class="slide-viewport">
    <div class="slide-container presenter-tpl" id="slideContainer"></div>
</div>

<div class="nav-bar">
    <div class="progress-track"><div class="progress-bar" id="progressBar"></div></div>
    <button class="nav-btn" onclick="prevSlide()" title="Previous">&#9664;</button>
    <span class="slide-info" id="slideInfo">0 / 0</span>
    <button class="nav-btn" onclick="nextSlide()" title="Next">&#9654;</button>
    <span class="nav-hint">&larr; &rarr; Flip &nbsp;|&nbsp; F11 Fullscreen</span>
</div>

<script>
// ==================== State ====================
let slides = [];
let currentIndex = 0;
let userStyleEls = [];
let userScriptEls = [];
let currentRatio = '16:9';

// ==================== Ratio System ====================
function applyRatio(ratio) {
    currentRatio = ratio;
    const container = document.getElementById('slideContainer');
    if (ratio === 'auto') {
        container.style.aspectRatio = '';
        container.style.maxWidth = '100%';
        container.style.maxHeight = '100%';
        container.style.width = '100%';
        container.style.height = '100%';
    } else {
        const [w, h] = ratio.split(':').map(Number);
        container.style.aspectRatio = w + ' / ' + h;
        container.style.width = '100%';
        container.style.height = '100%';
        container.style.maxWidth = 'calc((100vh - 88px) * ' + w + ' / ' + h + ')';
        container.style.maxHeight = '';
    }
}

// ==================== Template System ====================
function applyTemplate(tplKey) {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.get_template_css(tplKey).then(function(css) {
            injectTemplateCSS(css, tplKey);
        });
    }
}

function injectTemplateCSS(css, tplKey) {
    let oldTpl = document.getElementById('templateStyle');
    if (oldTpl) oldTpl.remove();

    const container = document.getElementById('slideContainer');
    if (tplKey === 'none') {
        container.classList.remove('presenter-tpl');
    } else {
        container.classList.add('presenter-tpl');
    }

    if (css) {
        const style = document.createElement('style');
        style.id = 'templateStyle';
        style.textContent = css;
        document.head.appendChild(style);
    }

    // Re-apply visibility
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

// ==================== Title Auto-fit ====================
function fitTitle() {
    const titleEl = document.getElementById('titleText');
    if (!titleEl) return;
    titleEl.style.fontSize = '';
    titleEl.style.maxWidth = '';
    requestAnimationFrame(() => {
        if (titleEl.scrollWidth > titleEl.clientWidth + 2) {
            let size = 13;
            titleEl.style.fontSize = size + 'px';
            while (titleEl.scrollWidth > titleEl.clientWidth + 2 && size > 10) {
                size -= 0.5;
                titleEl.style.fontSize = size + 'px';
            }
        }
    });
}

// ==================== Initialize ====================
function initSlides(data) {
    const container = document.getElementById('slideContainer');
    container.innerHTML = '';
    slides = [];

    // Remove old user styles/scripts
    userStyleEls.forEach(el => el.remove());
    userStyleEls = [];
    userScriptEls.forEach(el => el.remove());
    userScriptEls = [];

    // Set <base> for relative paths
    let baseEl = document.getElementById('userBase');
    if (baseEl) baseEl.remove();
    if (data.base_url) {
        baseEl = document.createElement('base');
        baseEl.id = 'userBase';
        baseEl.href = data.base_url;
        document.head.appendChild(baseEl);
        userStyleEls.push(baseEl);
    }

    // Inject user <head> styles
    if (data.head) {
        const tempHead = document.createElement('div');
        tempHead.innerHTML = data.head;
        tempHead.querySelectorAll('style, link[rel="stylesheet"]').forEach(el => {
            const clone = el.cloneNode(true);
            document.head.appendChild(clone);
            userStyleEls.push(clone);
        });
    }

    // Insert slides
    data.slides.forEach((html, i) => {
        const div = document.createElement('div');
        div.innerHTML = html;
        const slideEl = div.firstElementChild;
        if (slideEl) {
            if (i === 0) slideEl.classList.add('active');
            slideEl.style.display = (i === 0) ? '' : 'none';
            container.appendChild(slideEl);
            slides.push(slideEl);
        }
    });

    // Inject body-level <script>
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
    updateProgress();
    updateToolbar(data.title, data.total);

    // Apply ratio if specified
    if (data.ratio) {
        applyRatio(data.ratio);
    }

    // Auto-detect: if user HTML has its own styles, switch to custom mode
    const hasUserStyles = data.head && (
        data.head.includes('<style') || data.head.includes('stylesheet')
    );
    if (hasUserStyles) {
        document.getElementById('templateSelect').value = 'none';
        injectTemplateCSS('', 'none');
    }

    // Apply current template
    const tplKey = document.getElementById('templateSelect').value;
    if (tplKey !== 'none') {
        applyTemplate(tplKey);
    }

    fitTitle();
}

// ==================== Navigation ====================
function showSlide(index) {
    if (index < 0 || index >= slides.length) return;
    slides[currentIndex].classList.remove('active');
    slides[currentIndex].style.display = 'none';
    currentIndex = index;
    slides[currentIndex].classList.add('active');
    slides[currentIndex].style.display = '';
    updateInfo();
    updateProgress();
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

// ==================== Update Display ====================
function updateInfo() {
    document.getElementById('slideInfo').textContent =
        (slides.length ? currentIndex + 1 : 0) + ' / ' + slides.length;
}

function updateProgress() {
    const bar = document.getElementById('progressBar');
    if (slides.length <= 1) {
        bar.style.width = slides.length ? '100%' : '0';
    } else {
        bar.style.width = ((currentIndex / (slides.length - 1)) * 100) + '%';
    }
}

function updateToolbar(title, total) {
    document.getElementById('titleText').textContent = title;
    fitTitle();
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.set_window_title(title + ' - ' + total + ' slides');
    }
}

function syncIndex() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.update_index(currentIndex);
    }
}

// ==================== Open File ====================
function openFile() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.open_file_dialog().then(function(result) {
            if (result) initSlides(result);
        });
    }
}

// ==================== Keyboard ====================
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

// ==================== pywebview Ready ====================
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

    # ---------- JS-callable methods ----------

    def on_ready(self):
        if self.pending_file:
            path = self.pending_file
            self.pending_file = None
            result = self.load_file(path)
            if result:
                self.window.evaluate_js(f'initSlides({json.dumps(result)})')

    def open_file_dialog(self):
        file_types = ('Presentation files (*.slidehtml;*.html;*.htm)', 'All files (*.*)')
        result = self.window.create_file_dialog(
            webview.OPEN_DIALOG,
            file_types=file_types
        )
        if not result:
            return None
        path = result[0] if isinstance(result, (list, tuple)) else str(result)
        return self.load_file(path)

    def get_template_css(self, tpl_key):
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
            logger.error(f'Failed to read file: {e}')
            return None

        self.current_file = path
        self.current_index = 0

        # Extract <head>
        head_match = re.search(r'<head[^>]*>(.*?)</head>', content, re.DOTALL | re.IGNORECASE)
        head_html = head_match.group(1).strip() if head_match else ''

        # Extract <body>
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        body_html = body_match.group(1) if body_match else content

        # Extract ratio from meta tag
        ratio = None
        ratio_match = re.search(
            r'<meta\s+name=["\']ratio["\']\s+content=["\']([^"\']+)["\']',
            content, re.IGNORECASE
        )
        if ratio_match:
            ratio = ratio_match.group(1).strip()

        # Extract <div class="slide..."> blocks
        slides = []
        for m in re.finditer(
            r'<div\s+class=["\']slide\b[^"\']*["\'][^>]*>',
            body_html, re.DOTALL | re.IGNORECASE
        ):
            inner = self._find_slide_content(body_html, m.end())
            full_tag = body_html[m.start():m.end()]
            slides.append(full_tag + inner + '</div>')

        if not slides:
            logger.warning('No slide elements found, showing entire body as one page')
            slides = [body_html]

        # Extract body <script> tags
        body_scripts = re.findall(r'<script\b[^>]*>.*?</script>', body_html, re.DOTALL | re.IGNORECASE)

        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else os.path.splitext(os.path.basename(path))[0]

        total = len(slides)
        logger.info(f'Loaded: {os.path.basename(path)} ({total} slides)')

        return {
            'title': title,
            'slides': slides,
            'total': total,
            'head': head_html,
            'scripts': body_scripts,
            'base_url': 'file:///' + os.path.dirname(path).replace('\\', '/') + '/',
            'ratio': ratio
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


# ==================== Main ====================
def main():
    file_path = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isfile(arg):
            file_path = os.path.abspath(arg)
            logger.info(f'Command line file: {file_path}')

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

    logger.info('Presenter started')
    webview.start(debug=False)


if __name__ == '__main__':
    main()
