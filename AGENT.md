# AI Agent 技术规范

本文档面向 AI Agent（如 Claude、GPT 等），提供生成 HTML 演示幻灯片的完整技术规范和最佳实践。

---

## 1. 格式规范

### 1.1 唯一硬性要求

HTML 文件中每一页幻灯片必须使用 `<div class="slide">` 包裹：

```html
<div class="slide">
    <!-- 页内容 -->
</div>
```

- `class` 必须以 `slide` 开头，可附加其他类名：`class="slide cover"`、`class="slide bg-dark"`
- 放映器通过正则 `<div\s+class="slide\b[^"]*"[^>]*>` 匹配，需处理嵌套 `</div>`
- `<head>` 中的 `<style>` 和 `<link>` 会被提取并注入放映器
- `<body>` 中的 `<script>` 会被提取并执行
- 支持 `.slidehtml`、`.html`、`.htm` 扩展名

### 1.2 完整文件结构

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="ratio" content="16:9">  <!-- 可选：页面比例，支持 16:9, 4:3, auto -->
    <title>演示标题</title>
    <!-- 可选：自定义样式 -->
    <style>
        .slide { /* 布局样式 */ }
        .slide.cover { /* 封面特有样式 */ }
    </style>
    <!-- 可选：外部资源 -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="slide cover">
        <h1>标题</h1>
    </div>
    <div class="slide">
        <h2>第二页</h2>
    </div>
    <!-- 可选：body 级脚本 -->
    <script src="script.js"></script>
</body>
</html>
```

---

## 2. 放映器行为

### 2.1 渲染流程

1. 读取 HTML 文件
2. 提取 `<head>` 中的 `<style>` / `<link rel="stylesheet">`
3. 提取 `<body>` 中所有 `<div class="slide...">...</div>`
4. 提取 `<meta name="ratio">` 设置页面比例（默认 16:9）
5. 设置 `<base href="file:///文件所在目录/">` 用于解析相对路径
6. 将用户样式注入 `<head>`，将 slide 元素注入 DOM
7. 幻灯片以 16:9 比例居中显示在视口中，通过 `display: none/block` 控制显隐

### 2.2 模板系统

放映器内置 6 套 CSS 模板。模板通过 `.presenter-tpl .slide` 选择器注入样式，仅覆盖视觉属性（颜色、背景、字体等）。

模板控制的属性：
- `background` — 背景色/渐变
- `color` — 文字颜色
- `font-family` — 字体
- `padding` — 使用 `vh` / `vw` 单位

放映器通过 `clamp()` 函数提供响应式字体大小，模板只需覆盖视觉样式（颜色、背景等）。

模板字体大小参考（clamp 值）：
- `h1`: `clamp(36px, 5vw, 80px)`
- `h2`: `clamp(28px, 3.8vw, 60px)`
- `h3`: `clamp(22px, 2.8vw, 44px)`
- `p/li`: `clamp(15px, 2vw, 30px)`

### 2.3 显隐机制

显隐通过两层控制：

1. **JS 内联样式**（最高优先级）：`element.style.display = 'none'` 隐藏，`element.style.display = ''` 移除内联让 CSS 接管
2. **CSS `.active` 类**：`.slide.active { display: block; }` 确保活动幻灯片显示

切换幻灯片时 JS 同时操作内联样式和 `.active` 类，确保模板切换后状态正确。

---

## 3. 生成指南

### 3.1 工作流程

当用户要求生成演示幻灯片时：

1. **询问用户**：
   - 演示主题和内容大纲
   - 选择方式：使用预设模板（推荐非技术用户）还是自定义设计版面
   - 如果选模板：询问偏好风格（简约白底/深色科技/渐变多彩/商务蓝/水墨风/Nord 冷调）
   - 如果选自定义：由 Agent 根据主题设计独特的视觉风格

2. **生成 HTML**：
   - 如果使用模板：HTML 只写结构和内容，不写颜色/背景/字体样式（模板会自动处理）
   - 如果自定义设计：在 `<style>` 中写完整的视觉设计

3. **保存文件**：使用 `.slidehtml` 扩展名

### 3.2 使用模板时的写法

当用户选择使用模板时，HTML 只需关注**内容结构和布局**：

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>演示标题</title>
    <style>
        /* 只写布局相关样式，不写颜色/背景/字体 */
        .slide {
            width: 100vw; height: 100vh;
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            padding: 8vh 10vw; box-sizing: border-box;
            text-align: center;
        }
        /* 两栏布局 */
        .two-col { flex-direction: row; gap: 5vw; }
        .col { flex: 1; text-align: left; }
        /* 数据卡片 */
        .stats { display: flex; gap: 4vw; margin-top: 3vh; }
        .stat-num { font-size: 4vw; font-weight: 700; }
    </style>
</head>
<body>
    <div class="slide"><h1>标题</h1><p>副标题</p></div>
    <div class="slide"><h2>目录</h2><ul><li>...</li></ul></div>
</body>
</html>
```

### 3.3 自定义设计时的写法

当用户要求自定义设计时，Agent 应根据主题创造独特的视觉风格：

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>演示标题</title>
    <style>
        /* 完整的自定义设计 */
        .slide {
            width: 100vw; height: 100vh;
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            padding: 8vh 10vw; box-sizing: border-box;
        }
        .cover {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #fff;
        }
        .cover h1 {
            font-size: 5vw;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        /* ... 更多自定义样式 */
    </style>
</head>
<body>
    <div class="slide cover"><h1>标题</h1></div>
</body>
</html>
```

### 3.4 文字缩放

所有文字大小必须使用 `vw` 单位，确保窗口缩放时文字自适应：

```css
h1 { font-size: 5vw; }
h2 { font-size: 3.5vw; }
p, li { font-size: 2vw; }
code { font-size: 1.8vw; }
```

### 3.5 图片处理

- 路径相对于 `.slidehtml` 文件位置
- 建议使用 `max-width` 和 `max-height` 限制大小
- 添加 `onerror` 处理图片缺失：`<img src="x.png" onerror="this.style.display='none'">`
- 推荐目录结构：
  ```
  我的演示/
  ├── 演示.slidehtml
  └── images/
      ├── 图1.png
      └── 图2.jpg
  ```

### 3.6 动画

CSS 入场动画建议：

```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
.slide.active h1, .slide.active h2 {
    animation: fadeInUp 0.6s ease-out both;
}
.slide.active li:nth-child(1) { animation-delay: 0.1s; }
.slide.active li:nth-child(2) { animation-delay: 0.2s; }
.slide.active li:nth-child(3) { animation-delay: 0.3s; }
```

### 3.7 外部资源

支持引入 CDN 资源：

```html
<!-- 代码高亮 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>

<!-- 图标 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

<!-- 字体 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&display=swap" rel="stylesheet">
```

---

## 4. 模板对照表

| 模板 ID | 名称 | 背景 | 字体 | 适合场景 |
|---------|------|------|------|---------|
| `none` | 自定义样式 | 文件自带 | 文件自带 | 自定义设计 |
| `white` | 简约白底 | #ffffff | Microsoft YaHei | 课堂、学术 |
| `dark` | 深色科技 | 深蓝渐变 | Consolas + YaHei | 技术分享 |
| `gradient` | 渐变多彩 | 每页不同渐变 | YaHei | 答辩、发布 |
| `business` | 商务蓝 | #f8fafc + 蓝色顶部条 | YaHei | 工作汇报 |
| `ink` | 水墨风 | #faf8f5 | KaiTi | 文化、文学 |
| `nord` | Nord 冷调 | #2e3440 | YaHei | 技术文档、北欧风 |

---

## 5. 注意事项

1. **不要覆盖 `display` 属性**：放映器用 `!important` 控制 `.slide` 的显隐，用户样式中的 `display` 不影响激活状态
2. **不要在 `.slide` 上设置 `position: fixed`**：会导致幻灯片脱离容器
3. **`<script>` 中不要覆盖 `document.onkeydown`**：会与翻页快捷键冲突，改用 `addEventListener`
4. **文件编码必须是 UTF-8**
5. **每个 `.slide` 建议设置 `width: 100%; height: 100%`**：确保铺满容器（不要用 100vw/100vh，因为幻灯片在 16:9 容器内居中显示）
6. **可以添加 `<meta name="ratio" content="16:9">`**：设置页面比例，支持 16:9、4:3、auto
