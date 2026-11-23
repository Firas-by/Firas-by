import subprocess, collections, os

script_dir = os.path.dirname(os.path.abspath(__file__))
ascii_path = os.path.join(script_dir, 'ascii-art.txt')

# 1. Load ascii-art.txt
with open(ascii_path, 'r', encoding='utf-8') as f:
    raw_lines = [line.rstrip('\r\n') for line in f]

cropped = [list(line[71:231]) for line in raw_lines[6:155]]
H = len(cropped)
W = len(cropped[0])

is_bg = [[False]*W for _ in range(H)]
q = collections.deque()
for r in range(H):
    for c in [0, W-1]:
        if cropped[r][c] == '@':
            q.append((r, c))
            is_bg[r][c] = True
for c in range(W):
    for r in [0, H-1]:
        if cropped[r][c] == '@' and not is_bg[r][c]:
            q.append((r, c))
            is_bg[r][c] = True

while q:
    r, c = q.popleft()
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < H and 0 <= nc < W and not is_bg[nr][nc] and cropped[nr][nc] == '@':
            is_bg[nr][nc] = True
            q.append((nr, nc))

# For Dark Mode:
# Background is space
dark_mat = [row[:] for row in cropped]
for r in range(H):
    for c in range(W):
        if is_bg[r][c]:
            dark_mat[r][c] = ' '

# Hair fill with % in dark mode
for r in range(45):
    non_spaces = [c for c in range(W) if dark_mat[r][c] != ' ']
    if len(non_spaces) >= 2:
        left, right = non_spaces[0], non_spaces[-1]
        for c in range(left, right):
            if dark_mat[r][c] == ' ':
                dark_mat[r][c] = '%'

dark_tspans = []
for r in range(H):
    y = 20 + r * 3.32
    row_str = ''.join(dark_mat[r])
    escaped = row_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    dark_tspans.append(f'<tspan x="25" y="{y:.2f}">{escaped}</tspan>')

dark_ascii_block = '\n'.join(dark_tspans)

# For Light Mode:
inv_map = {
    ' ': '@',
    '.': '%',
    ':': '#',
    '-': '*',
    '=': '=',
    '+': '+',
    '*': '-',
    '#': ':',
    '%': '.',
    '@': ' ',
}

light_mat = []
for r in range(H):
    row = []
    for c in range(W):
        if is_bg[r][c]:
            row.append(' ')
        else:
            row.append(inv_map.get(cropped[r][c], ' '))
    light_mat.append(row)

light_tspans = []
for r in range(H):
    y = 20 + r * 3.32
    row_str = ''.join(light_mat[r])
    escaped = row_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    light_tspans.append(f'<tspan x="25" y="{y:.2f}">{escaped}</tspan>')

light_ascii_block = '\n'.join(light_tspans)

# Define Right Side Text for Dark Mode (x=380)
# Notice: Host dots adjusted from 29 to 19 to fit within 985px
dark_right_text = '''<text x="380" y="30" fill="#c9d1d9">
<tspan x="380" y="30">firas@sovereign</tspan> -———————————————————————————————————————————-—-
<tspan x="380" y="50" class="cc">. </tspan><tspan class="key">OS</tspan>:<tspan class="cc"> ........................ </tspan><tspan class="value">Windows 11, Linux (Ubuntu), Android</tspan>
<tspan x="380" y="70" class="cc">. </tspan><tspan class="key">Uptime</tspan>:<tspan class="cc" id="age_data_dots"> . </tspan><tspan class="value" id="age_data">24 years, 4 months, 21 days</tspan>
<tspan x="380" y="90" class="cc">. </tspan><tspan class="key">Host</tspan>:<tspan class="cc"> .................. </tspan><tspan class="value">ISET Sidi Bouzid (Licence Info)</tspan>
<tspan x="380" y="110" class="cc">. </tspan><tspan class="key">Kernel</tspan>:<tspan class="cc"> ...... </tspan><tspan class="value">Applied AI &amp; Quant Systems Developer</tspan>
<tspan x="380" y="130" class="cc">. </tspan><tspan class="key">IDE</tspan>:<tspan class="cc"> ........................ </tspan><tspan class="value">Antigravity, Cursor, VSCode, MT5</tspan>
<tspan x="380" y="150" class="cc">. </tspan>
<tspan x="380" y="170" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Programming</tspan>:<tspan class="cc"> ..... </tspan><tspan class="value">Python, TypeScript, JavaScript, MQL5</tspan>
<tspan x="380" y="190" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Web</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">React 19, Next.js, Node.js, FastAPI</tspan>
<tspan x="380" y="210" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Real</tspan>:<tspan class="cc"> ......................... </tspan><tspan class="value">Arabic, French, English</tspan>
<tspan x="380" y="230" class="cc">. </tspan>
<tspan x="380" y="250" class="cc">. </tspan><tspan class="key">Focus</tspan>.<tspan class="key">AI</tspan>:<tspan class="cc"> ........... </tspan><tspan class="value">Multi-Agent Swarms, MCP, Local RAG</tspan>
<tspan x="380" y="270" class="cc">. </tspan><tspan class="key">Focus</tspan>.<tspan class="key">Quant</tspan>:<tspan class="cc"> ........ </tspan><tspan class="value">ZeroMQ IPC (&lt;0.1ms), Risk Circuit Breaker</tspan>
<tspan x="380" y="290" class="cc">. </tspan><tspan class="key">Awards</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">1st Place National Hackathon (Atlal 3D)</tspan>
<tspan x="380" y="310">- Contact</tspan> -——————————————————————————————————————————————-—-
<tspan x="380" y="330" class="cc">. </tspan><tspan class="key">Email</tspan>.<tspan class="key">Personal</tspan>:<tspan class="cc"> ..................... </tspan><tspan class="value">firasbenyacoub@gmail.com</tspan>
<tspan x="380" y="350" class="cc">. </tspan><tspan class="key">Portfolio</tspan>:<tspan class="cc"> ...... </tspan><tspan class="value">firas-portfolio.firasby2002.workers.dev</tspan>
<tspan x="380" y="370" class="cc">. </tspan><tspan class="key">Custom Domain</tspan>:<tspan class="cc"> ................... </tspan><tspan class="value">firas.is-a.dev (Pending Merge)</tspan>
<tspan x="380" y="390" class="cc">. </tspan><tspan class="key">LinkedIn</tspan>:<tspan class="cc"> .................................. </tspan><tspan class="value">firas-ben-yacoub</tspan>
<tspan x="380" y="410" class="cc">. </tspan><tspan class="key">GitHub</tspan>:<tspan class="cc"> ......................................... </tspan><tspan class="value">Firas-by</tspan>
<tspan x="380" y="430" class="cc">. </tspan>
<tspan x="380" y="450">- GitHub Stats</tspan> -—————————————————————————————————————————-—-
<tspan x="380" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots"> ..... </tspan><tspan class="value" id="repo_data">8</tspan> {<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">8</tspan>} | <tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots"> ............ </tspan><tspan class="value" id="star_data">0</tspan>
<tspan x="380" y="490" class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc" id="commit_data_dots"> .................. </tspan><tspan class="value" id="commit_data">54</tspan> | <tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots"> ........ </tspan><tspan class="value" id="follower_data">0</tspan>
<tspan x="380" y="510" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc" id="loc_data_dots"> ... </tspan><tspan class="value" id="loc_data">28,450</tspan> ( <tspan class="addColor" id="loc_add">34,120</tspan><tspan class="addColor">++</tspan>, <tspan id="loc_del_dots"> . </tspan><tspan class="delColor" id="loc_del">5,670</tspan><tspan class="delColor">--</tspan> )
</text>'''

# Light Mode Right Side Text (x=380)
light_right_text = dark_right_text.replace('fill="#c9d1d9"', 'fill="#24292f"')

dark_svg = f'''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" viewBox="0 0 985 530" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
}}
.key {{fill: #ffa657;}}
.value {{fill: #a5d6ff;}}
.addColor {{fill: #3fb950;}}
.delColor {{fill: #f85149;}}
.cc {{fill: #616e7f;}}
text, tspan {{white-space: pre;}}
.ascii {{font-size: 3.3px; line-height: 3.32px; fill: #c9d1d9;}}
</style>
<rect width="985px" height="530px" fill="#161b22" rx="15"> </rect>
<text x="25" y="20" class="ascii">
{dark_ascii_block}
</text>
{dark_right_text}
</svg>'''

light_svg = f'''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" viewBox="0 0 985 530" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
}}
.key {{fill: #953800;}}
.value {{fill: #0a3069;}}
.addColor {{fill: #1a7f37;}}
.delColor {{fill: #cf222e;}}
.cc {{fill: #c2cfde;}}
text, tspan {{white-space: pre;}}
.ascii {{font-size: 3.3px; line-height: 3.32px; fill: #24292f;}}
</style>
<rect width="985px" height="530px" fill="#f6f8fa" stroke="#d0d7de" stroke-width="1" rx="15"> </rect>
<text x="25" y="20" class="ascii">
{light_ascii_block}
</text>
{light_right_text}
</svg>'''

dark_path = os.path.join(script_dir, 'dark_mode.svg')
light_path = os.path.join(script_dir, 'light_mode.svg')

with open(dark_path, 'w', encoding='utf-8') as f:
    f.write(dark_svg)

with open(light_path, 'w', encoding='utf-8') as f:
    f.write(light_svg)

print('Generated dark_mode.svg and light_mode.svg successfully.')

# Render screenshots if browser exists
browser_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if os.path.exists(browser_path):
    dark_shot = os.path.join(script_dir, 'final_dark_render.png')
    light_shot = os.path.join(script_dir, 'final_light_render.png')
    try:
        subprocess.run([browser_path, '--headless', f'--screenshot={dark_shot}', '--window-size=1050,600', f'file:///{dark_path.replace(os.sep, "/")}'], check=True)
        subprocess.run([browser_path, '--headless', f'--screenshot={light_shot}', '--window-size=1050,600', f'file:///{light_path.replace(os.sep, "/")}'], check=True)
        print('Rendered final_dark_render.png and final_light_render.png')
    except Exception as e:
        print(f'Notice: Browser render skipped ({e})')
