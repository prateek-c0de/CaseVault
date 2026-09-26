import re

with open('app/static/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace root variables
new_root = ''':root {
    /* Backgrounds */
    --bg-base:        #F8FAFC;
    --bg-surface:     #FFFFFF;
    --bg-elevated:    #F8FAFC;
    --bg-hover:       #EFF6FF;

    /* Brand / Accent */
    --accent:         #2563EB;
    --accent-hover:   #1D4ED8;
    --accent-muted:   #EFF6FF;

    /* Semantic */
    --success:        #16A34A;
    --success-muted:  #F0FDF4;
    --danger:         #DC2626;
    --danger-muted:   #FEF2F2;
    --warning:        #D97706;
    --warning-muted:  #FFFBEB;
    --info:           #0284C7;
    --info-muted:     #F0F9FF;

    /* Text */
    --text-primary:   #0F172A;
    --text-secondary: #64748B;
    --text-muted:     #94A3B8;

    /* Borders */
    --border:         #E2E8F0;
    --border-subtle:  #F1F5F9;'''

content = re.sub(r':root\s*\{.*?(?=\/\*\s*Typography\s*\*\/)', new_root + '\n\n    ', content, flags=re.DOTALL)

with open('app/static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)
