import re

with open('app/templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove warp.js script tag
html = re.sub(r'<script src="\{\{\s*url_for\(\'static\',\s*filename=\'js/warp\.js\'\)\s*\}\}"></script>', '', html)

# Replace the search beam wrapper with a clean search bar
search_replacement = '''            <div class="header-center" style="flex-grow: 1; max-width: 400px; margin: 0 2rem;">
                <form action="{{ url_for('search.query') }}" method="GET" style="display: flex; width: 100%;">
                    <input type="text" name="q" placeholder="Search CaseVault..." class="form-control" style="border-radius: 4px 0 0 4px; border-right: none; background: #F8FAFC;">
                    <button type="submit" class="btn btn-secondary" style="border-radius: 0 4px 4px 0; background: #F8FAFC;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    </button>
                </form>
            </div>'''

html = re.sub(r'<div class="header-center"[^>]*>.*?</div>\s*<div class="header-right">', search_replacement + '\n            <div class="header-right">', html, flags=re.DOTALL)

with open('app/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(html)
