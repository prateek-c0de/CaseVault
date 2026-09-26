import re

with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Card backgrounds and borders
css = re.sub(
    r'\.card\s*\{.*?\n\}',
    '''.card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
}''', css, flags=re.DOTALL
)

# Top header
css = re.sub(
    r'\.top-header\s*\{.*?\n\}',
    '''.top-header {
    height: var(--header-h);
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 2rem;
    position: sticky;
    top: 0;
    z-index: 100;
}''', css, flags=re.DOTALL
)

# Inputs/forms
css = re.sub(
    r'\.form-control\s*\{.*?\n\}',
    '''.form-control {
    width: 100%;
    padding: 0.6rem 0.8rem;
    background: var(--bg-surface);
    border: 1px solid #CBD5E1;
    border-radius: var(--radius-md);
    color: var(--text-primary);
    font-family: var(--font-body);
    font-size: 0.9rem;
    transition: border-color var(--transition), box-shadow var(--transition);
}''', css, flags=re.DOTALL
)

css = re.sub(
    r'\.form-control:focus\s*\{.*?\n\}',
    '''.form-control:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-muted);
}''', css, flags=re.DOTALL
)

css = re.sub(
    r'\.form-control::placeholder\s*\{.*?\n\}',
    '''.form-control::placeholder {
    color: var(--text-muted);
}''', css, flags=re.DOTALL
)

# Buttons
css = re.sub(
    r'\.btn-primary\s*\{.*?\n\}',
    '''.btn-primary {
    background: var(--accent);
    color: #FFFFFF;
    border: 1px solid var(--accent);
}
.btn-primary:hover {
    background: var(--accent-hover);
    border-color: var(--accent-hover);
}''', css, flags=re.DOTALL
)

css = re.sub(
    r'\.btn-secondary\s*\{.*?\n\}',
    '''.btn-secondary {
    background: var(--bg-surface);
    color: var(--text-secondary);
    border: 1px solid var(--border);
}
.btn-secondary:hover {
    background: var(--bg-base);
    color: var(--text-primary);
}''', css, flags=re.DOTALL
)

# Badges
css = re.sub(
    r'\.badge-success\s*\{.*?\}',
    '.badge-success { background: var(--success-bg); color: var(--success); border-color: rgba(22, 163, 74, 0.2); }', css, flags=re.DOTALL
)
css = re.sub(
    r'\.badge-danger\s*\{.*?\}',
    '.badge-danger { background: var(--danger-bg); color: var(--danger); border-color: rgba(220, 38, 38, 0.2); }', css, flags=re.DOTALL
)
css = re.sub(
    r'\.badge-warning\s*\{.*?\}',
    '.badge-warning { background: var(--warning-bg); color: var(--warning); border-color: rgba(217, 119, 6, 0.2); }', css, flags=re.DOTALL
)
css = re.sub(
    r'\.badge-info\s*\{.*?\}',
    '.badge-info { background: var(--info-bg); color: var(--info); border-color: rgba(2, 132, 199, 0.2); }', css, flags=re.DOTALL
)
css = re.sub(
    r'\.badge-neutral\s*\{.*?\}',
    '.badge-neutral { background: var(--bg-base); color: var(--text-secondary); border-color: var(--border); }', css, flags=re.DOTALL
)

# Clean up glass-cta and glass-search
css = re.sub(r'/\* -- Glassmorphism CTA Button \(Search\) ------------------- \*/.*', '', css, flags=re.DOTALL)

with open('app/static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
