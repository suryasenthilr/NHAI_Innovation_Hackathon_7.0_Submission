import os
import re
import markdown

md_path = 'technical_documentation.md'
html_path = 'technical_documentation.html'

if not os.path.exists(md_path):
    print(f"Error: {md_path} not found.")
    exit(1)

with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pre-process custom alert blocks to render as beautiful HTML alerts
def replace_alerts(text):
    # Match blockquotes starting with alerts
    # Matches pattern: > [!ALERT_TYPE]
    #                 > line 1
    #                 > line 2
    pattern = r'(?:^|\n)(?>\s*\[\!(IMPORTANT|WARNING|CAUTION|NOTE|TIP)\]\s*\n)((?>\s*.*(?:\n|$))*)'
    
    # Simple regex based replacements for GH alerts
    # We can search line by line and replace blockquote alerts
    lines = text.split('\n')
    in_alert = False
    alert_type = ""
    alert_lines = []
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Check if alert starts
        if stripped.startswith('> [!'):
            in_alert = True
            alert_type = stripped[4:-1].lower()
            alert_lines = []
            i += 1
            continue
            
        if in_alert:
            if stripped.startswith('>'):
                # Strip the leading > and space
                alert_content = line.replace('>', '', 1).strip()
                alert_lines.append(alert_content)
                i += 1
            else:
                # Alert block ends
                # render alert div
                css_class = f"alert-{alert_type}"
                title = alert_type.upper()
                content_html = "<br>".join(alert_lines)
                alert_div = f'<div class="{css_class}"><strong>{title}</strong>: {content_html}</div>\n'
                new_lines.append(alert_div)
                in_alert = False
        else:
            new_lines.append(line)
            i += 1
            
    # Handle end of file alert block
    if in_alert:
        css_class = f"alert-{alert_type}"
        title = alert_type.upper()
        content_html = "<br>".join(alert_lines)
        alert_div = f'<div class="{css_class}"><strong>{title}</strong>: {content_html}</div>\n'
        new_lines.append(alert_div)
        
    return '\n'.join(new_lines)

processed_content = replace_alerts(content)

# Convert math formulas (LaTex) to a web-safe format using MathJax
# We don't want python-markdown to mess up math equations containing underscores or asterisks, so we escape them or let MathJax process them.
# Standard markdown conversion
html_body = markdown.markdown(processed_content, extensions=['tables', 'fenced_code', 'toc'])

# Wrap in a premium HTML template with CSS styling and MathJax for LaTeX math rendering
full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BharatVerify - Deep Engineering & Mathematical Specification</title>
<!-- MathJax for rendering LaTeX formulas -->
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.7;
    max-width: 960px;
    margin: 40px auto;
    padding: 0 30px;
    color: #24292e;
    background-color: #ffffff;
}}
h1, h2, h3, h4, h5, h6 {{
    margin-top: 32px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.3;
    color: #1b1f23;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.3em;
}}
h1 {{ font-size: 2.25em; border-bottom: 2px solid #eaecef; }}
h2 {{ font-size: 1.6em; }}
h3 {{ font-size: 1.3em; }}
p {{
    margin-top: 0;
    margin-bottom: 16px;
}}
code {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    background-color: rgba(27,31,35,0.05);
    padding: 0.2em 0.4em;
    border-radius: 4px;
    font-size: 85%;
    color: #c7254e;
}}
pre {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    background-color: #f6f8fa;
    padding: 20px;
    border-radius: 8px;
    overflow: auto;
    font-size: 90%;
    line-height: 1.45;
    border: 1px solid #eaecef;
}}
pre code {{
    background-color: transparent;
    padding: 0;
    border-radius: 0;
    color: #24292e;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin-top: 10px;
    margin-bottom: 24px;
}}
table th, table td {{
    padding: 10px 15px;
    border: 1px solid #dfe2e5;
}}
table th {{
    background-color: #f6f8fa;
    font-weight: 600;
}}
table tr {{
    background-color: #fff;
    border-top: 1px solid #c6cbd1;
}}
table tr:nth-child(2n) {{
    background-color: #f8f9fa;
}}
blockquote {{
    padding: 0 1.5em;
    color: #6a737d;
    border-left: 0.3em solid #dfe2e5;
    margin: 0 0 20px 0;
    font-style: italic;
}}
img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 30px auto;
    border-radius: 8px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}}
.alert-note, .alert-important, .alert-tip {{
    padding: 16px 20px;
    margin-bottom: 24px;
    border-left: 6px solid;
    border-radius: 6px;
    font-size: 95%;
}}
.alert-note {{
    background-color: #f1f8ff;
    border-color: #0366d6;
    color: #24292e;
}}
.alert-important {{
    background-color: #fff5f5;
    border-color: #d73a49;
    color: #24292e;
}}
.alert-tip {{
    background-color: #f0fff4;
    border-color: #28a745;
    color: #24292e;
}}
hr {{
    height: 0.25em;
    padding: 0;
    margin: 40px 0;
    background-color: #e1e4e8;
    border: 0;
}}
.toc {{
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #e9ecef;
    margin-bottom: 30px;
}}
.toc ul {{
    padding-left: 20px;
    margin: 0;
}}
@media print {{
    body {{
        max-width: 100%;
        margin: 20px;
        color: #000;
        background-color: #fff;
    }}
    pre, table, .alert-note, .alert-important, .alert-tip {{
        page-break-inside: avoid;
    }}
    a {{
        text-decoration: none;
        color: #000;
    }}
}}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Successfully converted technical_documentation.md to technical_documentation.html")
print(f"Output saved at: {os.path.abspath(html_path)}")
