import re

with open('app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Tamper Alerts stat card styling
html = re.sub(
    r'<div class="stat-value" style="color: var\(--danger\);">\{\{ stats\.tamper_alerts_count \}\}</div>',
    '<div class="stat-value" {% if stats.tamper_alerts_count > 0 %}style="color: var(--danger);"{% else %}style="color: var(--success);"{% endif %}>{{ stats.tamper_alerts_count }}</div>',
    html
)

with open('app/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
