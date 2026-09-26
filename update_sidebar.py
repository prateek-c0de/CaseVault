import re

with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace dock-sidebar styles
css = re.sub(
    r'\.dock-sidebar\s*\{.*?\n\}',
    '''.dock-sidebar {
    width: 200px !important;
    background: #FFFFFF;
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    align-items: stretch;
    position: fixed;
    top: 0; bottom: 0; left: 0;
    z-index: 200;
    padding: 16px 10px;
    overflow-y: hidden;
}''', css, flags=re.DOTALL
)

# Replace dock-brand styles
css = re.sub(
    r'\.dock-brand\s*\{.*?\n\}',
    '''.dock-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    margin-bottom: 12px;
    border-radius: 12px;
    background: transparent;
    border: 1px solid transparent;
    flex-shrink: 0;
}''', css, flags=re.DOTALL
)

# Replace dock-separator
css = re.sub(
    r'\.dock-separator\s*\{.*?\n\}',
    '''.dock-separator {
    height: 1px;
    background: var(--border);
    margin: 6px 10px;
    flex-shrink: 0;
}''', css, flags=re.DOTALL
)

# Replace dock-item
css = re.sub(
    r'\.dock-item\s*\{.*?\n\}',
    '''.dock-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 10px;
    color: var(--text-secondary);
    background: transparent;
    border: 1px solid transparent;
    text-decoration: none;
    position: relative;
    cursor: pointer;
    transition: all 0.2s ease;
    transform-origin: center left;
}''', css, flags=re.DOTALL
)

# Replace dock-item hover
css = re.sub(
    r'\.dock-item:hover\s*\{.*?\}',
    '''.dock-item:hover {
    background: var(--bg-base);
    color: var(--accent);
    text-decoration: none;
}''', css, flags=re.DOTALL
)

# Replace dock-item active
css = re.sub(
    r'\.dock-item\.active\s*\{.*?\}',
    '''.dock-item.active {
    background: var(--accent-muted);
    color: var(--accent);
    font-weight: 500;
}''', css, flags=re.DOTALL
)

css = re.sub(r'\.dock-item\.active:hover\s*\{.*?\}', '', css, flags=re.DOTALL)
css = re.sub(r'\.dock-item svg\s*\{.*?\}', '.dock-item svg { flex-shrink: 0; }', css, flags=re.DOTALL)
css = re.sub(r'\.dock-item:hover svg\s*\{.*?\}', '', css, flags=re.DOTALL)

# Dock footer
css = re.sub(
    r'\.dock-footer\s*\{.*?\n\}',
    '''.dock-footer {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 6px;
    padding-top: 8px;
    border-top: 1px solid var(--border);
    flex-shrink: 0;
}''', css, flags=re.DOTALL
)

# Dock role badge
css = re.sub(
    r'\.dock-role-badge\s*\{.*?\n\}',
    '''.dock-role-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4px 8px;
    background: var(--bg-base);
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: var(--text-secondary);
    text-transform: uppercase;
    font-family: var(--font-ui);
}''', css, flags=re.DOTALL
)

with open('app/static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
