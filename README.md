<p align="center">
  <h1 align="center">HTML Slide Presenter</h1>
  <p align="center">用 HTML 做 PPT，自由设计，一键播放</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.7+-blue" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

---

## ✨ 这是什么

一个 **Windows 桌面应用**，能将 HTML 文件像 PPT 一样逐页播放。

你只需用 `<div class="slide">` 标记每一页，剩下的交给放映器。内置 5 套精美模板，不写样式也能一键美化。

## 🎯 核心特性

- **🎨 5 套预设模板** — 简约白底 / 深色科技 / 渐变多彩 / 商务蓝 / 水墨风，下拉菜单秒切
- **📐 文字自适应** — 使用 vw 单位，全屏/窗口化任意缩放，文字始终清晰
- **⌨️ 键盘翻页** — `← →` 翻页，`F11` 全屏，`Esc` 退出，无需鼠标
- **📂 双击即开** — 运行 `register_file_assoc.bat` 注册 `.slidehtml` 文件关联
- **🖼️ 图片支持** — 相对路径直接引用，自动解析
- **🔧 自由设计** — HTML/CSS/JS 任意发挥，不受模板限制

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install pywebview

# 2. 注册文件关联（右键管理员运行，可选）
register_file_assoc.bat

# 3. 打开示例
python player.py demo.slidehtml
```

## 🤖 用 AI 生成幻灯片

本项目包含一个 **AI Agent 技术规范** (`AGENT.md`)，你可以用 Claude、GPT 等 AI 工具直接生成 `.slidehtml` 文件。

**使用方法：**

1. 将 `AGENT.md` 的内容作为上下文提供给 AI Agent
2. 告诉 AI 你的演示主题和需求，例如：
   > "请根据 AGENT.md 的规范，生成一份关于「机器学习入门」的演示文稿，使用深色科技模板，约 10 页"

3. AI 会询问你的偏好（模板还是自定义设计、风格选择等），然后生成完整的 `.slidehtml` 文件
4. 将生成的文件保存，双击打开即可播放

**AGENT.md 中已包含：**
- 完整的 HTML 格式规范
- 5 套模板的适用场景对照表
- 文字自适应（vw 单位）规范
- 图片、代码块、动画的写法示例
- Agent 生成时的工作流程提示

你也可以直接复制以下提示词开始：

```
请阅读项目中的 AGENT.md 文件，理解 HTML Slide Presenter 的技术规范，
然后帮我生成一个演示文稿。
```

## 📝 幻灯片格式

**唯一规则：** 用 `<div class="slide">` 包裹每一页。

```html
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>我的演示</title></head>
<body>
  <div class="slide">
    <h1>第一页</h1>
    <p>内容自由发挥</p>
  </div>
  <div class="slide">
    <h2>第二页</h2>
    <ul><li>要点一</li><li>要点二</li></ul>
  </div>
</body>
</html>
```

不写样式直接在播放器里选模板即可。自己写了样式选"不使用模板"保留原样。

## ⌨️ 快捷键

| 按键 | 功能 |
|------|------|
| `→` `Space` `Enter` | 下一页 |
| `←` `Backspace` | 上一页 |
| `Home` / `End` | 第一页 / 最后一页 |
| `F11` | 全屏切换 |
| `Esc` | 退出全屏 |

## 📁 文件结构

```
HTMLSlidePresenter/
├── player.py                # 主程序
├── requirements.txt         # Python 依赖
├── register_file_assoc.bat  # 注册 .slidehtml 双击打开
├── unregister_file_assoc.bat# 取消文件关联
├── demo.slidehtml           # 示例幻灯片（11 页）
├── README.md                # 项目说明（中文）
├── README_EN.md             # English README
├── USER_GUIDE.md            # 用户使用指南
├── AGENT.md                 # AI Agent 技术规范
├── GITHUB_GUIDE.md          # GitHub 发布指南
└── LICENSE
```

## 📖 文档

| 文档 | 读者 | 内容 |
|------|------|------|
| `USER_GUIDE.md` | 普通用户 | 安装、使用、写幻灯片、常见问题 |
| `AGENT.md` | AI Agent | 完整技术规范、模板对照表、生成指南 |
| `GITHUB_GUIDE.md` | 开发者 | 如何发布到 GitHub、配置 Release |

## 🔧 系统要求

- **Windows 10/11**（Edge WebView2 运行时，Win10+ 自带）
- **Python 3.7+**
- `pip install pywebview`

## 📄 许可

MIT License — 详见 [LICENSE](LICENSE)
