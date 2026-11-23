import os
import datetime
from PIL import Image, ImageEnhance

# Approximate birthdate for Uptime calculation (2002)
BIRTHDAY = datetime.date(2002, 1, 1)

def calculate_uptime():
    today = datetime.date.today()
    years = today.year - BIRTHDAY.year
    months = today.month - BIRTHDAY.month
    days = today.day - BIRTHDAY.day
    if days < 0:
        months -= 1
        days += 30
    if months < 0:
        years -= 1
        months += 12
    return f"{years}y, {months}m, {days}d (PFE Capstone)"

def generate_ascii_art(image_path, width=38, height=25):
    if not os.path.exists(image_path):
        return []
    
    img = Image.open(image_path)
    w, h = img.size
    face = img.crop((int(w * 0.12), int(h * 0.05), int(w * 0.88), int(h * 0.75)))
    face = face.convert('L')
    face = ImageEnhance.Contrast(face).enhance(2.0)
    face = face.resize((width, height), Image.Resampling.LANCZOS)
    
    chars = '   ..::--==++**##%%@@'
    pixels = list(face.getdata())
    lines = []
    for row in range(height):
        line = ''
        for col in range(width):
            pixel = pixels[row * width + col]
            char_idx = int((pixel / 255) * (len(chars) - 1))
            line += chars[char_idx]
        lines.append(line)
    return lines

def escape_xml(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def build_svg(ascii_lines, theme='dark'):
    is_dark = theme == 'dark'
    bg_color = "#161b22" if is_dark else "#f6f8fa"
    card_border = "#30363d" if is_dark else "#d0d7de"
    text_color = "#c9d1d9" if is_dark else "#24292f"
    key_color = "#ffa657" if is_dark else "#953800"
    val_color = "#79c0ff" if is_dark else "#0969da"
    dot_color = "#484f58" if is_dark else "#8c959f"
    add_color = "#3fb950" if is_dark else "#1a7f37"
    del_color = "#f85149" if is_dark else "#cf222e"
    header_color = "#58a6ff" if is_dark else "#0969da"
    
    uptime_str = calculate_uptime()
    
    svg = []
    svg.append(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" width="985px" height="540px" font-size="14px">
<style>
  .ascii {{ fill: {text_color}; white-space: pre; font-size: 13px; }}
  .key {{ fill: {key_color}; font-weight: bold; }}
  .val {{ fill: {val_color}; }}
  .dot {{ fill: {dot_color}; }}
  .head {{ fill: {header_color}; font-weight: bold; }}
  .add {{ fill: {add_color}; }}
  .del {{ fill: {del_color}; }}
  text, tspan {{ white-space: pre; }}
</style>
<rect width="985px" height="540px" fill="{bg_color}" stroke="{card_border}" stroke-width="1" rx="14"/>
''')
    
    svg.append(f'<text x="25" y="36" class="ascii">')
    y_pos = 36
    for line in ascii_lines:
        svg.append(f'<tspan x="25" y="{y_pos}">{escape_xml(line)}</tspan>')
        y_pos += 19
    svg.append('</text>')
    
    rx = 390
    y = 36
    dy = 19
    
    def row(key, val, dots_len=18):
        nonlocal y
        dots = '.' * max(2, dots_len - len(key))
        res = f'<tspan x="{rx}" y="{y}"><tspan class="dot">. </tspan><tspan class="key">{escape_xml(key)}</tspan><tspan class="dot"> {dots} </tspan><tspan class="val">{escape_xml(val)}</tspan></tspan>'
        y += dy
        return res
    
    def section(title):
        nonlocal y
        line_fill = '─' * max(2, 45 - len(title))
        res = f'<tspan x="{rx}" y="{y}" class="head">{escape_xml(title)} <tspan class="dot">{line_fill}</tspan></tspan>'
        y += dy
        return res
    
    def space():
        nonlocal y
        res = f'<tspan x="{rx}" y="{y}" class="dot">. </tspan>'
        y += dy
        return res

    svg.append(f'<text x="{rx}" y="36" fill="{text_color}">')
    svg.append(f'<tspan x="{rx}" y="{y}" class="head">firas@sovereign <tspan class="dot">───────────────────────────────────</tspan></tspan>')
    y += dy
    svg.append(row("OS", "Windows 11, Linux (Ubuntu), Android"))
    svg.append(row("Uptime", uptime_str))
    svg.append(row("Host", "ISET Sidi Bouzid · Licence Informatique"))
    svg.append(row("Kernel", "Applied AI & Automation Developer"))
    svg.append(row("IDE", "Antigravity, Cursor, VSCode, MetaEditor 5"))
    svg.append(space())
    svg.append(row("Languages.Code", "Python, TypeScript, JavaScript, MQL5, SQL"))
    svg.append(row("Languages.Web", "React 19, Next.js, Tailwind, WebGL Shaders"))
    svg.append(row("Languages.Real", "Arabic (Native), French (Bilingual), English"))
    svg.append(space())
    svg.append(row("Focus.AI", "Model Context Protocol (MCP), Evals, RAG"))
    svg.append(row("Focus.Quant", "ZeroMQ TCP IPC (<0.1ms), Risk Watchdogs"))
    svg.append(row("Awards", "1st Place National Hackathon (Atlal 3D)"))
    svg.append(space())
    svg.append(section("- Contact Channels"))
    svg.append(row("Email", "firasbenyacoub@gmail.com"))
    svg.append(row("Portfolio", "firas-portfolio.firasby2002.workers.dev"))
    svg.append(row("Custom Domain", "firas.is-a.dev (Pending Merge)"))
    svg.append(row("LinkedIn", "linkedin.com/in/firas-ben-yacoub"))
    svg.append(row("GitHub", "github.com/Firas-by"))
    svg.append(space())
    svg.append(section("- Verified Deliverables"))
    svg.append(row("Traidify-Sovereign", "Dual-Process Python/MQL5 Gold Risk Engine"))
    svg.append(row("TuniBill", "Tunisian Elfatoora XML/C14N Compliance Engine"))
    svg.append(row("Atlal-Heritage", "Flutter Impeller 3D Monument Viewer + RAG"))
    svg.append('</text>')
    svg.append('</svg>')
    
    return '\n'.join(svg)

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, 'firas.jpg')
    ascii_art = generate_ascii_art(img_path, width=38, height=25)
    
    dark_svg = build_svg(ascii_art, theme='dark')
    light_svg = build_svg(ascii_art, theme='light')
    
    with open(os.path.join(script_dir, 'dark_mode.svg'), 'w', encoding='utf-8') as f:
        f.write(dark_svg)
    with open(os.path.join(script_dir, 'light_mode.svg'), 'w', encoding='utf-8') as f:
        f.write(light_svg)
    print("Profile SVGs updated successfully!")
