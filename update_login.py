import re

with open('app/templates/login.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove style block for btn-launch-red
html = re.sub(r'<style>.*?\.btn-launch-red.*?</style>', '', html, flags=re.DOTALL)

# Replace button class
html = re.sub(r'<button type="submit" class="btn-launch-red">.*?<span[^>]*>&#128640;</span> Sign In Securely.*?</button>', 
              '<button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem; padding: 0.8rem; font-weight: 600;">Sign In Securely</button>', 
              html, flags=re.DOTALL)

# Fix logo shadow in light theme
html = re.sub(r'box-shadow:\s*0 4px 24px rgba\(0,195,255,0\.3\);', 'box-shadow: 0 4px 12px rgba(0,0,0,0.1);', html)
# Fix subtitle color
html = re.sub(r'color:var\(--accent\);', 'color:var(--text-secondary);', html)

with open('app/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(html)
