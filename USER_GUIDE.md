# 使用指南

## 这个软件是干什么的？

简单说：**用 HTML 文件做演示文稿（PPT）**。

你用 HTML 写内容，放映器帮你一页一页地播放。不用装 PowerPoint，不用学 LaTeX Beamer，写几行 HTML 就能上台演示。

## 安装

1. 确保你的电脑装了 Python（在命令行输入 `python --version` 能看到版本号就行）
2. 打开命令行，进入这个文件夹，运行：
   ```
   pip install pywebview
   ```
3. （可选）右键 `register_file_assoc.bat` → 以管理员身份运行，这样以后双击 `.slidehtml` 文件就能直接打开

## 怎么用

### 打开放映器

- **方式一：** 直接双击 `demo.slidehtml`（需要先注册文件关联）
- **方式二：** 命令行运行 `python player.py`
- **方式三：** 命令行运行 `python player.py 你的文件.slidehtml`

### 操作方式

| 操作 | 说明 |
|------|------|
| `→` 或 `Space` | 下一页 |
| `←` | 上一页 |
| `F11` | 全屏 / 退出全屏 |
| `Esc` | 退出全屏 |
| 点击下拉菜单 | 切换风格模板 |
| 点击"打开文件" | 选择其他 HTML 文件 |

## 怎么写幻灯片

### 最简单的写法

新建一个文本文件，把后缀改成 `.slidehtml`，写入以下内容：

```html
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>我的演示</title></head>
<body>
    <div class="slide">
        <h1>大家好</h1>
        <p>这是我的演示文稿</p>
    </div>
    <div class="slide">
        <h2>第二页</h2>
        <p>这是第二页的内容</p>
    </div>
</body>
</html>
```

**规则只有一条：每一页用 `<div class="slide">...</div>` 包起来。**

保存后双击打开（或用命令行运行），放映器会自动显示。不写任何样式也没关系，在放映器里选择一个模板就会自动美化。

### 添加图片

把图片放在和 `.slidehtml` 文件同一个文件夹里（建议建一个 `images/` 文件夹），然后这样写：

```html
<div class="slide">
    <h2>效果图</h2>
    <img src="images/效果图.png">
</div>
```

路径是相对于 `.slidehtml` 文件的位置。

### 添加代码

```html
<div class="slide">
    <h2>代码示例</h2>
    <pre><code>def hello():
    print("Hello, World!")</code></pre>
</div>
```

### 两栏布局

```html
<div class="slide" style="display:flex; flex-direction:row; gap:5vw; align-items:center;">
    <div style="flex:1; text-align:left;">
        <h2>左侧标题</h2>
        <p>左侧内容</p>
    </div>
    <div style="flex:1;">
        <img src="images/diagram.png" style="max-width:100%;">
    </div>
</div>
```

### 每页不同背景（不用模板时）

```html
<style>
    .slide { display:flex; justify-content:center; align-items:center;
             width:100vw; height:100vh; }
    .bg1 { background: linear-gradient(135deg, #667eea, #764ba2); color:#fff; }
    .bg2 { background: #fff; color: #333; }
</style>
<body>
    <div class="slide bg1"><h1>渐变背景页</h1></div>
    <div class="slide bg2"><h1>白色背景页</h1></div>
</body>
```

## 模板系统

放映器内置了 6 套风格模板，打开文件后在顶部下拉菜单中选择即可：

| 模板 | 适合场景 |
|------|---------|
| 简约白底 | 课堂汇报、学术答辩 |
| 深色科技 | 技术分享、编程演示 |
| 渐变多彩 | 毕业答辩、产品发布 |
| 商务蓝 | 工作汇报、商务演示 |
| 水墨风 | 文化类、文学类主题 |
| Nord 冷调 | 技术文档、北欧风格 |

**模板会自动覆盖幻灯片的颜色、字体、文字大小**，让未写样式的 HTML 也能呈现专业效果。如果你自己写了样式，选择"自定义样式"即可保留原样。

幻灯片会以 16:9 比例居中显示，底部有进度条指示当前页码。

## 常见问题

**Q: 打开后是空白？**
检查文件编码是否为 UTF-8，检查 `<div class="slide">` 拼写是否正确。

**Q: 图片不显示？**
确认图片路径正确，路径是相对于 `.slidehtml` 文件的。用 `onerror` 可以避免图片缺失时报错：`<img src="xxx.png" onerror="this.style.display='none'">`

**Q: 文字太大/太小？**
模板使用 `clamp()` 单位自动缩放（最小值到最大值范围内）。如果觉得不合适，可以在文件里自己写样式覆盖。

**Q: 想用自己设计的样式，不要模板？**
在下拉菜单选"自定义样式"，或者在文件的 `<style>` 里写好自己的样式（放映器会自动检测并切换）。

**Q: 幻灯片不居中？**
幻灯片默认以 16:9 比例居中显示。如果你的 HTML 写了 `width: 100vw; height: 100vh`，建议改为 `width: 100%; height: 100%`。

**Q: 怎么在演示中播放视频？**
```html
<div class="slide">
    <video src="video.mp4" controls style="max-width:80%;"></video>
</div>
```
