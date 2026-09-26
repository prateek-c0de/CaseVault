import re

with open('app/templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement = '''            <div class="header-center" style="flex-grow: 1; max-width: 400px; margin: 0 2rem;">
                <style>
                    @keyframes borderBeamRotation {
                        0% { transform: translate(-50%, -50%) rotate(0deg); }
                        100% { transform: translate(-50%, -50%) rotate(360deg); }
                    }
                    .search-beam-wrapper {
                        position: relative; 
                        overflow: hidden; 
                        border-radius: 9999px; 
                        display: flex; 
                        width: 100%; 
                        box-shadow: 0 8px 40px rgba(129,140,248,0.2);
                        transition: all 0.3s ease;
                    }
                    .search-beam-wrapper:focus-within, .search-beam-wrapper:hover {
                        box-shadow: 0 0 40px 4px rgba(129,140,248,0.3);
                        transform: scale(1.02);
                    }
                    .search-btn-icon:hover {
                        color: rgba(129,140,248,1) !important;
                    }
                </style>
                <div class="search-beam-wrapper">
                    <div style="position: absolute; content: ' '; display: block; width: 200%; height: 200%; background: linear-gradient(90deg, transparent, rgba(129,140,248, 0.3), rgba(129,140,248, 0.9), rgba(129,140,248, 0.3), transparent); animation: borderBeamRotation 4s infinite linear; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 0;"></div>
                    <div style="position: relative; z-index: 1; margin: 1.5px; width: 100%; border-radius: 9999px; background: #FFFFFF; display: flex;">
                        <form action="{{ url_for('search.query') }}" method="GET" style="display: flex; width: 100%; margin: 0; padding: 0;">
                            <input type="text" name="q" placeholder="Search CaseVault..." style="flex-grow: 1; border: none; background: transparent; padding: 0.6rem 1.25rem; font-family: var(--font-body); font-size: 0.9rem; color: var(--text-primary); outline: none; border-radius: 9999px 0 0 9999px;">
                            <button type="submit" class="search-btn-icon" style="border: none; background: transparent; padding: 0 1.25rem; color: var(--text-secondary); cursor: pointer; border-radius: 0 9999px 9999px 0; transition: color 0.2s;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                            </button>
                        </form>
                    </div>
                </div>
            </div>'''

# Replace the current header-center div entirely.
html = re.sub(r'<div class="header-center"[^>]*>.*?</div>\s*<div class="header-right">', replacement + '\n              <div class="header-right">', html, flags=re.DOTALL)

with open('app/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(html)
