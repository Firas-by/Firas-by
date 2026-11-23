import os
import re
import datetime
import urllib.request
import json
import xml.etree.ElementTree as ET

USER_NAME = os.environ.get('USER_NAME', 'Firas-by')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

# Default birthdate: July 5, 2002
BIRTHDAY = datetime.date(2002, 7, 5)

def calculate_uptime(birthday=BIRTHDAY):
    today = datetime.date.today()
    years = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    prev_bday_year = today.year if (today.month, today.day) >= (birthday.month, birthday.day) else today.year - 1
    last_bday = datetime.date(prev_bday_year, birthday.month, birthday.day)
    diff_days = (today - last_bday).days
    months = diff_days // 30
    days = diff_days % 30
    
    y_str = f"{years} year" + ("s" if years != 1 else "")
    m_str = f"{months} month" + ("s" if months != 1 else "")
    d_str = f"{days} day" + ("s" if days != 1 else "")
    return f"{y_str}, {m_str}, {d_str}"

def fetch_github_stats():
    stats = {
        'repos': 8,
        'contrib': 8,
        'stars': 0,
        'commits': 54,
        'followers': 0,
        'loc': 28450,
        'loc_add': 34120,
        'loc_del': 5670
    }
    
    headers = {'User-Agent': 'Firas-Profile-Updater'}
    if ACCESS_TOKEN:
        headers['Authorization'] = f'token {ACCESS_TOKEN}'
        
    try:
        # Fetch user details
        url = f"https://api.github.com/users/{USER_NAME}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            stats['repos'] = data.get('public_repos', stats['repos'])
            stats['followers'] = data.get('followers', stats['followers'])
            
        # Fetch repos for stars
        url_repos = f"https://api.github.com/users/{USER_NAME}/repos?per_page=100"
        req_repos = urllib.request.Request(url_repos, headers=headers)
        with urllib.request.urlopen(req_repos, timeout=10) as resp:
            repos = json.loads(resp.read().decode('utf-8'))
            stats['stars'] = sum(r.get('stargazers_count', 0) for r in repos)
            stats['contrib'] = max(stats['repos'], len(repos))
    except Exception as e:
        print(f"Notice: Using cached stats ({e})")
        
    return stats

def update_svg(filename, age_str, stats):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    tree = ET.parse(filename)
    root = tree.getroot()

    def set_elem(elem_id, text):
        for el in root.iter():
            if el.attrib.get('id') == elem_id:
                el.text = str(text)
                return el
        return None

    def justify(elem_id, value, total_length=0):
        if isinstance(value, int):
            formatted_val = f"{value:,}"
        else:
            formatted_val = str(value)
        set_elem(elem_id, formatted_val)
        
        if total_length > 0:
            diff = max(1, total_length - len(formatted_val))
            if diff <= 2:
                dots = ' . '
            else:
                dots = ' ' + ('.' * diff) + ' '
            set_elem(f"{elem_id}_dots", dots)

    # 1. Uptime - 29 total length ensures at least a couple dots
    justify('age_data', age_str, 29)

    # 2. GitHub Stats
    justify('repo_data', stats['repos'], 6)
    set_elem('contrib_data', str(stats['contrib']))
    justify('star_data', stats['stars'], 13)
    justify('commit_data', stats['commits'], 20)
    justify('follower_data', stats['followers'], 9)
    justify('loc_data', stats['loc'], 9)
    set_elem('loc_add', f"{stats['loc_add']:,}")
    justify('loc_del', stats['loc_del'], 6)

    # Ensure no element text is None or empty to prevent self-closing tags
    for el in root.iter():
        if el.text is None or el.text == '':
            el.text = ' '

    # Save SVG
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    
    # Post-process to guarantee absolutely zero self-closing tspan tags
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    # Replace any <tspan ... /> with <tspan ...> </tspan>
    content = re.sub(r'<tspan([^>]*)\s*/>', r'<tspan\1> </tspan>', content)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {filename} successfully.")

if __name__ == '__main__':
    uptime = calculate_uptime()
    print("Calculated Uptime:", uptime)
    stats = fetch_github_stats()
    print("GitHub Stats:", stats)
    update_svg('F:/Firas-by/dark_mode.svg', uptime, stats)
    update_svg('F:/Firas-by/light_mode.svg', uptime, stats)
