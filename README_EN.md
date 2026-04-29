<p align="center">
  <h1 align="center">HTML Slide Presenter</h1>
  <p align="center">Make PPTs with HTML — design freely, present with one click</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.7+-blue" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

> **Note:** The application UI is currently in Chinese. An English version is planned. Contributions welcome!

---

## What is this?

A **Windows desktop app** that plays HTML files as slides, just like PowerPoint.

Just mark each slide with `<div class="slide">` and the presenter handles the rest. Choose from 5 built-in templates to instantly polish your presentation — no CSS skills needed.

## Features

- **5 built-in templates** — Clean White / Dark Tech / Gradient / Business Blue / Ink Style
- **Responsive text** — Uses `vw` units, scales automatically with window size
- **Keyboard navigation** — `← →` to flip, `F11` for fullscreen
- **Double-click to open** — Run `register_file_assoc.bat` once, then open `.slidehtml` directly
- **Image support** — Relative paths resolved automatically
- **Full creative freedom** — Use any HTML/CSS/JS, not limited by templates

## Quick Start

```bash
# 1. Install dependency
pip install pywebview

# 2. Register file association (run as admin, optional)
register_file_assoc.bat

# 3. Open the demo
python player.py demo.slidehtml
```

## 🤖 Generate Slides with AI

This project includes an **AI Agent Technical Spec** (`AGENT.md`). You can use Claude, GPT, or other AI tools to generate `.slidehtml` presentation files directly.

**How to use:**

1. Provide the contents of `AGENT.md` as context to your AI Agent
2. Tell the AI what presentation you need, for example:
   > "Follow the spec in AGENT.md and generate a presentation about 'Introduction to Machine Learning' using the Dark Tech template, about 10 slides"

3. The AI will ask about your preferences (template vs custom design, style choice, etc.), then generate a complete `.slidehtml` file
4. Save the generated file and double-click to present

**AGENT.md includes:**
- Complete HTML format specification
- Template reference table with use cases
- Responsive text guidelines (vw units)
- Code blocks, images, animations examples
- Agent workflow prompts

Quick start prompt:

```
Read AGENT.md and understand the technical spec of HTML Slide Presenter,
then help me generate a presentation.
```

## Slide Format

**One rule:** wrap each page in `<div class="slide">`.

```html
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>My Presentation</title></head>
<body>
  <div class="slide">
    <h1>Slide 1</h1>
    <p>Content goes here</p>
  </div>
  <div class="slide">
    <h2>Slide 2</h2>
    <ul><li>Point one</li><li>Point two</li></ul>
  </div>
</body>
</html>
```

No styling needed — pick a template in the player. Write your own CSS and select "No Template" to use custom styles.

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `→` `Space` `Enter` | Next slide |
| `←` `Backspace` | Previous slide |
| `Home` / `End` | First / Last slide |
| `F11` | Toggle fullscreen |
| `Esc` | Exit fullscreen |

## Project Structure

```
HTMLSlidePresenter/
├── player.py                # Main application
├── requirements.txt         # Python dependencies
├── register_file_assoc.bat  # Register .slidehtml file association
├── unregister_file_assoc.bat# Unregister file association
├── demo.slidehtml           # Demo slides (11 slides)
├── README.md                # Chinese README
├── README_EN.md             # English README (this file)
├── USER_GUIDE.md            # User guide (Chinese)
├── AGENT.md                 # AI Agent technical spec
├── GITHUB_GUIDE.md          # GitHub publishing guide
└── LICENSE
```

## Documentation

| Doc | Audience | Language |
|-----|----------|----------|
| `USER_GUIDE.md` | End users | 中文 |
| `AGENT.md` | AI Agents | 中文 |
| `GITHUB_GUIDE.md` | Developers | 中文 |

## Requirements

- **Windows 10/11** (Edge WebView2 runtime, built into Win10+)
- **Python 3.7+**
- `pip install pywebview`

## License

MIT License — see [LICENSE](LICENSE)
