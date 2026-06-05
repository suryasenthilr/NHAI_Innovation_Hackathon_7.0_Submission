import os
import re
import base64
import hashlib
import urllib.request
import markdown
import sys

def get_mermaid_svg(code):
    """
    Fetches the SVG representation of a Mermaid diagram from mermaid.ink.
    Caches the SVG locally based on the MD5 hash of the diagram code.
    """
    code_hash = hashlib.md5(code.encode('utf-8')).hexdigest()
    cache_dir = os.path.join('assets', 'docs-images', 'mermaid')
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f'{code_hash}.svg')
    
    # Check if cached locally
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading cache file {cache_path}: {e}")
            
    # Fetch from mermaid.ink
    graph_bytes = code.encode("utf-8")
    base64_bytes = base64.urlsafe_b64encode(graph_bytes)
    base64_string = base64_bytes.decode("ascii")
    
    url = f"https://mermaid.ink/svg/{base64_string}"
    print(f"Fetching Mermaid diagram from: {url}")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            svg_data = response.read()
            svg_text = svg_data.decode('utf-8')
            # Write to cache
            with open(cache_path, 'w', encoding='utf-8') as f:
                f.write(svg_text)
            return svg_text
    except Exception as e:
        print(f"Warning: Failed to fetch Mermaid SVG: {e}", file=sys.stderr)
        # Fallback to a clean inline SVG placeholder
        placeholder_svg = f"""<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#fff5f5" stroke="#f87171" stroke-width="2" rx="8"/>
            <text x="50%" y="45%" dominant-baseline="middle" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="16" fill="#b91c1c" font-weight="bold">⚠️ Offline Mermaid Diagram Placeholder</text>
            <text x="50%" y="60%" dominant-baseline="middle" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="12" fill="#7f1d1d">Diagram: {code_hash[:8]} | Please run compile script while online to render.</text>
        </svg>"""
        return placeholder_svg

def get_base64_image(img_path):
    """
    Reads a local image file and returns it as a base64 data URI.
    """
    original_path = img_path
    if img_path.startswith('./'):
        img_path = img_path[2:]
        
    if os.path.exists(img_path):
        try:
            with open(img_path, 'rb') as f:
                data = f.read()
            encoded = base64.b64encode(data).decode('utf-8')
            ext = os.path.splitext(img_path)[1].lower()
            mime = 'image/png' if ext == '.png' else ('image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/svg+xml')
            return f"data:{mime};base64,{encoded}"
        except Exception as e:
            print(f"Error encoding image {img_path}: {e}")
            return original_path
    else:
        print(f"Warning: Image file not found: {img_path}")
        return original_path

def fix_list_indentation(text):
    """
    Finds lines starting with 1 to 3 spaces that are NOT inside a fenced code block
    and indents them to exactly 4 spaces so that python-markdown compiles them correctly.
    """
    lines = text.split('\n')
    new_lines = []
    in_code_block = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
            
        if in_code_block:
            new_lines.append(line)
            continue
            
        if line.startswith(' ') and stripped:
            leading_spaces = len(line) - len(line.lstrip(' '))
            if 0 < leading_spaces < 4:
                line = ' ' * (4 - leading_spaces) + line
                
        new_lines.append(line)
        
    return '\n'.join(new_lines)

def make_github_links(html):
    # Regex to find code blocks containing file paths
    pattern = re.compile(
        r'<code>\s*(\.?/?src/[a-zA-Z0-9_\-/.]+'
        r'|\.?/?scripts/[a-zA-Z0-9_\-/.]+'
        r'|package\.json|eas\.json|app\.json|metro\.config\.js|tsconfig\.json'
        r'|README\.md|technical_documentation\.md|judges_presentation\.md)\s*</code>'
    )
    
    def repl(match):
        path = match.group(1).strip()
        clean_path = path
        if clean_path.startswith('./'):
            clean_path = clean_path[2:]
        if clean_path.startswith('/'):
            clean_path = clean_path[1:]
            
        url = f"https://github.com/suryasenthilr/NHAI_Innovation_Hackathon_7.0_Submission/blob/master/{clean_path}"
        return f'<a href="{url}" target="_blank" class="github-code-link"><code>{path}</code></a>'
        
    return pattern.sub(repl, html)

def make_href_github_links(html):
    # Regex to find links to markdown files like href="./README.md"
    pattern = re.compile(r'href=["\']\./([a-zA-Z0-9_\-/.]+\.md)["\']')
    
    def repl(match):
        path = match.group(1)
        url = f"https://github.com/suryasenthilr/NHAI_Innovation_Hackathon_7.0_Submission/blob/master/{path}"
        return f'href="{url}" target="_blank"'
        
    return pattern.sub(repl, html)

def fix_markdown_spacing(text):
    """
    Ensures that headers, lists, and blockquotes have a blank line before them
    so that python-markdown compiles them correctly.
    """
    lines = text.split('\n')
    new_lines = []
    
    list_item_pattern = re.compile(r'^\s*(\d+\.|\*|\-)\s+')
    blockquote_pattern = re.compile(r'^\s*>\s*')
    header_pattern = re.compile(r'^\s*#+\s+')
    
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            new_lines.append(line)
            continue
            
        # Ensure lists have a blank line before them
        if list_item_pattern.match(line):
            if idx > 0:
                prev_line = lines[idx-1].strip()
                if prev_line and not list_item_pattern.match(lines[idx-1]) and not blockquote_pattern.match(lines[idx-1]):
                    new_lines.append('')
                    
        # Ensure headers have a blank line before them
        elif header_pattern.match(line):
            if idx > 0:
                prev_line = lines[idx-1].strip()
                if prev_line:
                    new_lines.append('')
                    
        # Ensure blockquotes have a blank line before them
        elif blockquote_pattern.match(line):
            if idx > 0:
                prev_line = lines[idx-1].strip()
                if prev_line and not blockquote_pattern.match(lines[idx-1]):
                    new_lines.append('')
                    
        new_lines.append(line)
        
    return '\n'.join(new_lines)

def preprocess_alerts(text):
    """
    Finds GitHub-style alert blocks:
    > [!IMPORTANT]
    > block content
    and pre-compiles their content using python-markdown, then wraps them in the alert div.
    This ensures that nested lists and formatting inside the alert block are preserved.
    """
    lines = text.split('\n')
    new_lines = []
    in_alert = False
    alert_type = ""
    alert_lines = []
    
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()
        
        # Check if alert starts
        if stripped.startswith('> [!'):
            # If we are already in an alert, close it first
            if in_alert:
                new_lines.append(render_alert_div(alert_type, alert_lines))
                
            in_alert = True
            alert_type = stripped[4:-1].lower()
            alert_lines = []
            idx += 1
            continue
            
        if in_alert:
            if stripped.startswith('>'):
                # Extract alert content (remove leading > and space)
                content = line.replace('>', '', 1)
                # If there's a space after >, remove it
                if content.startswith(' '):
                    content = content[1:]
                alert_lines.append(content)
                idx += 1
            else:
                # Alert block ends
                new_lines.append(render_alert_div(alert_type, alert_lines))
                in_alert = False
                new_lines.append(line)
                idx += 1
        else:
            new_lines.append(line)
            idx += 1
            
    if in_alert:
        new_lines.append(render_alert_div(alert_type, alert_lines))
        
    return '\n'.join(new_lines)

def render_alert_div(alert_type, alert_lines):
    alert_content = '\n'.join(alert_lines)
    alert_content = fix_markdown_spacing(alert_content)
    # We compile the alert content markdown to HTML separately!
    md = markdown.Markdown(extensions=['tables', 'fenced_code'])
    compiled_html = md.convert(alert_content)
    
    css_class = f"alert-{alert_type}"
    title = alert_type.upper()
    
    # Wrap in our alert structure
    return f'<div class="{css_class}"><strong>{title}</strong>: {compiled_html}</div>\n'

def preprocess_markdown(text):
    """
    Extracts math blocks, mermaid blocks, and local images, replacing them
    with placeholders to prevent them from being mangled by the Markdown parser.
    Also converts indented fenced code blocks (inside lists) into indented code blocks.
    """
    # 0. Preprocess alerts first to avoid markdown blockquote mangling
    text = preprocess_alerts(text)
    
    # Fix Diagram 6 curly braces syntax errors
    text = text.replace('Select {Blink, Smile, Yaw}', 'Select [Blink, Smile, Yaw]')
    
    # 1. Extract Fenced Code Blocks (nested vs root level)
    lines = text.split('\n')
    new_lines = []
    
    in_fenced_code = False
    code_lines = []
    code_indent = 0
    code_opening_line = ""
    
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()
        
        if stripped.startswith('```'):
            if not in_fenced_code:
                in_fenced_code = True
                # Count leading spaces to see if it is inside a list
                leading_spaces = len(line) - len(line.lstrip(' '))
                code_indent = leading_spaces
                code_lines = []
                code_opening_line = line  # Save the opening line (e.g. ```mermaid)
                idx += 1
                continue
            else:
                in_fenced_code = False
                if code_indent > 0:
                    # Convert indented fenced code block to standard indented code block (8 spaces)
                    # This is recognized by python-markdown as nested inside list items
                    if new_lines and new_lines[-1].strip():
                        new_lines.append('')
                    
                    for cl in code_lines:
                        cl_stripped = cl[code_indent:] if cl.startswith(' ' * code_indent) else cl.lstrip(' ')
                        new_lines.append('        ' + cl_stripped)
                    
                    new_lines.append('')
                else:
                    # Root level code block: restore the exact opening and closing lines
                    new_lines.append(code_opening_line)
                    for cl in code_lines:
                        new_lines.append(cl)
                    new_lines.append(line)
                idx += 1
                continue
                
        if in_fenced_code:
            code_lines.append(line)
        else:
            new_lines.append(line)
        idx += 1
        
    text = '\n'.join(new_lines)
    
    # Fix 3-space list indentation to 4-space indentation for python-markdown
    text = fix_list_indentation(text)
    
    # Fix spacing around elements (lists, blockquotes)
    text = fix_markdown_spacing(text)
    
    # 2. Extract Mermaid Blocks (which are always root level now)
    mermaid_blocks = []
    def mermaid_repl(match):
        code = match.group(1).strip()
        placeholder = f"%%MERMAID_BLOCK_{len(mermaid_blocks)}%%"
        mermaid_blocks.append(code)
        return f"\n{placeholder}\n"
    
    text = re.sub(r'```mermaid\s*\n([\s\S]*?)\n```', mermaid_repl, text)
    
    # 3. Extract Display Math
    display_math = []
    def display_math_repl(match):
        indent = match.group(1) or ''
        math_content = match.group(2).strip()
        placeholder = f"%%DISPLAY_MATH_{len(display_math)}%%"
        display_math.append(math_content)
        return f"\n{indent}{placeholder}\n"
    
    text = re.sub(r'([ ]*)\$\$(.*?)\$\$', display_math_repl, text, flags=re.DOTALL)
    
    # 4. Extract Inline Math
    inline_math = []
    def inline_math_repl(match):
        math_content = match.group(1).strip()
        placeholder = f"%%INLINE_MATH_{len(inline_math)}%%"
        inline_math.append(math_content)
        return placeholder
    
    text = re.sub(r'(?<!\\)\$([^\$\n]+?)(?<!\\)\$', inline_math_repl, text)
    
    # 5. Resolve Local Images to Base64
    def md_img_repl(match):
        alt = match.group(1)
        path = match.group(2)
        base64_uri = get_base64_image(path)
        return f'![{alt}]({base64_uri})'
    
    text = re.sub(r'\!\[(.*?)\]\((.*?)\)', md_img_repl, text)
    
    def html_img_repl(match):
        attrs_before = match.group(1) or ''
        path = match.group(2)
        attrs_after = match.group(3) or ''
        base64_uri = get_base64_image(path)
        return f'<img {attrs_before}src="{base64_uri}"{attrs_after}>'
        
    text = re.sub(r'<img\s+([^>]*?)src=["\'](.*?)["\']([^>]*?)>', html_img_repl, text)

    return text, mermaid_blocks, display_math, inline_math

def postprocess_html(html, mermaid_blocks, display_math, inline_math):
    """
    Restores the Mermaid and Math blocks, and formats Github blockquote alerts.
    """
    # 1. Parse Blockquotes to GitHub-Style Alerts
    def replace_blockquote(match):
        bq_content = match.group(1)
        # Check if it starts with [!TYPE]
        alert_match = re.match(r'^\s*<p>\s*\[\!(IMPORTANT|WARNING|CAUTION|NOTE|TIP)\]\s*(.*)$', bq_content, re.DOTALL)
        if alert_match:
            alert_type = alert_match.group(1).lower()
            rest_of_content = alert_match.group(2)
            css_class = f"alert-{alert_type}"
            title = alert_type.upper()
            return f'<div class="{css_class}"><strong>{title}</strong>: <p>{rest_of_content}</div>'
        return match.group(0)

    html = re.sub(r'<blockquote>([\s\S]*?)</blockquote>', replace_blockquote, html)

    # 2. Restore Mermaid Blocks as Base64 SVG images
    for idx, code in enumerate(mermaid_blocks):
        svg_text = get_mermaid_svg(code)
        svg_base64 = base64.b64encode(svg_text.encode('utf-8')).decode('utf-8')
        img_tag = f'<div class="mermaid-container"><img class="mermaid-svg" src="data:image/svg+xml;base64,{svg_base64}" alt="Mermaid Diagram"></div>'
        html = html.replace(f"%%MERMAID_BLOCK_{idx}%%", img_tag)
        
    # 3. Restore Display Math
    for idx, math in enumerate(display_math):
        math_tag = f"$${math}$$"
        html = html.replace(f"%%DISPLAY_MATH_{idx}%%", math_tag)
        
    # 4. Restore Inline Math
    for idx, math in enumerate(inline_math):
        math_tag = f"${math}$"
        html = html.replace(f"%%INLINE_MATH_{idx}%%", math_tag)
        
    # 5. Convert file paths in <code> blocks to GitHub links
    html = make_github_links(html)
    
    # 6. Convert relative links to markdown files to GitHub absolute links
    html = make_href_github_links(html)
    
    # 7. Tag Diagram headings with class="diagram-header"
    html = re.sub(r'<h3([^>]*)>(Diagram \d+[\s\S]*?)</h3>', r'<h3 class="diagram-header" \1>\2</h3>', html)
        
    return html

def compile_spec():
    md_path = 'technical_documentation.md'
    html_path = 'technical_documentation_print.html'
    
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        return
        
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    print(f"Compiling {md_path}...")
    
    # Preprocess
    text, mermaid_blocks, display_math, inline_math = preprocess_markdown(md_content)
    
    # Render Markdown to HTML body
    md = markdown.Markdown(extensions=['tables', 'toc', 'fenced_code'])
    html_body = md.convert(text)
    toc_html = md.toc
    
    # Postprocess
    html_body = postprocess_html(html_body, mermaid_blocks, display_math, inline_math)
    
    # Recommendation bar (User requested specific preference text and direct links)
    header_html = """
    <div class="screen-only-header">
        <div class="header-notice">
            <strong>⚠️ Important Notice (GitHub Preference)</strong>: For the best reading and evaluation experience, <strong>we highly prefer and recommend that you read these documents directly on GitHub</strong> (or download the compiled PDF versions). The GitHub repository natively renders all interactive zoomable diagrams, full vector schemas, code block formatting, and dark mode controls.
        </div>
        <div class="header-links">
            <a href="https://github.com/suryasenthilr/NHAI_Innovation_Hackathon_7.0_Submission" target="_blank">📂 View Full Repository on GitHub</a>
            <a href="https://github.com/suryasenthilr/NHAI_Innovation_Hackathon_7.0_Submission/blob/master/README.md" target="_blank">📄 Read README.md on GitHub</a>
            <a href="https://github.com/suryasenthilr/NHAI_Innovation_Hackathon_7.0_Submission/blob/master/technical_documentation.md" target="_blank">📘 Read Technical Specification on GitHub</a>
            <a href="https://github.com/suryasenthilr/NHAI_Innovation_Hackathon_7.0_Submission/blob/master/judges_presentation.md" target="_blank">🏆 Read Pitch Slide Deck on GitHub</a>
        </div>
    </div>
    """
    
    # HTML Template
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BharatVerify - Technical Specification</title>
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
<!-- MathJax for rendering LaTeX math formulas -->
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  }},
  options: {{
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
    :root {{
        --primary: #0284c7;
        --text-color: #334155;
        --heading-color: #0f172a;
        --bg-color: #ffffff;
        --sidebar-bg: #f8fafc;
        --border-color: #e2e8f0;
    }}
    
    body {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        line-height: 1.7;
        color: var(--text-color);
        background-color: var(--bg-color);
        margin: 0;
        padding: 0;
    }}
    
    a {{
        color: #0284c7;
        text-decoration: underline;
    }}
    
    a:hover {{
        color: #0369a1;
    }}
    
    .container {{
        display: flex;
        min-height: 100vh;
    }}
    
    .sidebar {{
        width: 280px;
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
        padding: 30px 20px;
        box-sizing: border-box;
        position: sticky;
        top: 0;
        height: 100vh;
        overflow-y: auto;
    }}
    
    .sidebar-title {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.1em;
        font-weight: 700;
        color: var(--heading-color);
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--border-color);
    }}
    
    .sidebar ul {{
        list-style-type: none;
        padding-left: 0;
        margin: 0;
    }}
    
    .sidebar li {{
        margin-bottom: 8px;
    }}
    
    .sidebar a {{
        color: #64748b;
        text-decoration: none;
        font-size: 0.92em;
        font-weight: 500;
        display: block;
        padding: 6px 10px;
        border-radius: 6px;
        transition: all 0.2s ease;
    }}
    
    .sidebar a:hover {{
        color: var(--primary);
        background-color: #f1f5f9;
        padding-left: 14px;
    }}
    
    .sidebar li li {{
        padding-left: 15px;
        font-size: 0.95em;
    }}
    
    .main-content {{
        flex: 1;
        max-width: 900px;
        padding: 50px 60px;
        box-sizing: border-box;
    }}
    
    /* Recommendation Bar Styles */
    .screen-only-header {{
        background-color: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 30px;
        font-size: 0.95em;
        color: #0369a1;
        font-family: 'Inter', sans-serif;
    }}
    .header-notice {{
        margin-bottom: 12px;
        line-height: 1.5;
    }}
    .header-links {{
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
    }}
    .header-links a {{
        color: #0284c7;
        text-decoration: none;
        font-weight: 600;
        border-bottom: 1px dashed #0284c7;
        padding-bottom: 2px;
        transition: all 0.15s ease;
    }}
    .header-links a:hover {{
        color: #0369a1;
        border-bottom-style: solid;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Outfit', sans-serif;
        color: var(--heading-color);
        margin-top: 36px;
        margin-bottom: 16px;
        font-weight: 600;
        line-height: 1.3;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 0.3em;
    }}
    
    h1 {{ font-size: 2.2em; border-bottom: 2px solid var(--border-color); margin-top: 20px; }}
    h2 {{ font-size: 1.6em; }}
    h3 {{ font-size: 1.3em; border-bottom: none; padding-bottom: 0; }}
    h4 {{ font-size: 1.15em; border-bottom: none; padding-bottom: 0; color: #0f172a; }}
    
    p {{ margin-top: 0; margin-bottom: 18px; }}
    
    ul, ol {{ margin-top: 0; margin-bottom: 18px; padding-left: 24px; }}
    li {{ margin-bottom: 6px; }}
    
    code {{
        font-family: 'Fira Code', monospace;
        background-color: #f1f5f9;
        padding: 0.2em 0.4em;
        border-radius: 4px;
        font-size: 85%;
        color: #e11d48;
        font-weight: 500;
    }}
    
    pre {{
        font-family: 'Fira Code', monospace;
        background-color: #0f172a;
        color: #f8fafc;
        padding: 18px;
        border-radius: 8px;
        overflow: auto;
        font-size: 90%;
        line-height: 1.5;
        border: 1px solid #1e293b;
        margin: 20px 0;
    }}
    
    pre code {{
        background-color: transparent;
        padding: 0;
        border-radius: 0;
        color: #f8fafc;
    }}
    
    table {{
        border-collapse: collapse;
        width: 100%;
        margin-top: 15px;
        margin-bottom: 26px;
        font-size: 0.95em;
    }}
    
    table th, table td {{
        padding: 10px 14px;
        border: 1px solid var(--border-color);
        text-align: left;
    }}
    
    table th {{
        background-color: #f8fafc;
        font-weight: 600;
        color: var(--heading-color);
    }}
    
    table tr {{
        background-color: #fff;
    }}
    
    table tr:nth-child(2n) {{
        background-color: #f8fafc;
    }}
    
    blockquote {{
        padding: 10px 20px;
        color: #475569;
        border-left: 4px solid #cbd5e1;
        margin: 0 0 20px 0;
        background-color: #f8fafc;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
    }}
    
    img {{
        max-width: 100%;
        height: auto;
        display: block;
        margin: 30px auto;
        border-radius: 8px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    }}
    
    .mermaid-container {{
        background: #ffffff;
        display: flex;
        justify-content: center;
        margin: 30px 0;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }}
    
    .mermaid-svg {{
        max-width: 100%;
        height: auto;
    }}
    
    .alert-note, .alert-important, .alert-tip, .alert-warning, .alert-caution {{
        padding: 16px 20px;
        margin-bottom: 24px;
        border-left: 6px solid;
        border-radius: 8px;
        font-size: 95%;
    }}
    
    .alert-note {{
        background-color: #f0f9ff;
        border-color: #0284c7;
        color: #0369a1;
    }}
    
    .alert-important, .alert-caution {{
        background-color: #fef2f2;
        border-color: #ef4444;
        color: #991b1b;
    }}
    
    .alert-warning {{
        background-color: #fffbeb;
        border-color: #f59e0b;
        color: #92400e;
    }}
    
    .alert-tip {{
        background-color: #f0fdf4;
        border-color: #22c55e;
        color: #166534;
    }}
    
    .alert-note p, .alert-important p, .alert-tip p, .alert-warning p, .alert-caution p {{
        margin: 4px 0 0 0;
    }}

    hr {{
        height: 2px;
        background-color: var(--border-color);
        border: none;
        margin: 40px 0;
    }}
    
    @media (max-width: 768px) {{
        .container {{
            flex-direction: column;
        }}
        .sidebar {{
            width: 100%;
            height: auto;
            position: relative;
            border-right: none;
            border-bottom: 1px solid var(--border-color);
            padding: 20px;
        }}
        .main-content {{
            padding: 30px 20px;
        }}
    }}
    
    @media print {{
        .sidebar, .screen-only-header {{
            display: none !important;
        }}
        .main-content {{
            padding: 0;
            max-width: 100%;
        }}
        body {{
            color: #000;
            background-color: #fff;
        }}
        pre, table, .alert-note, .alert-important, .alert-tip, .alert-warning, .alert-caution, .mermaid-container {{
            page-break-inside: avoid;
        }}
        h2 {{
            page-break-before: always;
        }}
        h1 + h2 {{
            page-break-before: avoid;
        }}
        h1, h2, h3 {{
            page-break-after: avoid;
        }}
        .diagram-header {{
            page-break-before: always;
        }}
        a {{
            text-decoration: underline;
            color: #0284c7 !important;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        .mermaid-svg {{
            max-height: 180mm;
            width: auto;
        }}
    }}
</style>
</head>
<body>
<div class="container">
    <aside class="sidebar">
        <div class="sidebar-title">Sections</div>
        {toc_html}
    </aside>
    <main class="main-content">
        {header_html}
        {html_body}
    </main>
</div>
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    print(f"Successfully generated static HTML at: {html_path}")

def compile_slides():
    md_path = 'judges_presentation.md'
    html_path = 'judges_presentation_print.html'
    
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        return
        
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    print(f"Compiling {md_path}...")
    
    # Preprocess
    text, mermaid_blocks, display_math, inline_math = preprocess_markdown(md_content)
    
    # Split by slide separator (---)
    raw_slides = re.split(r'\n\s*---\s*\n', text)
    
    slides_html_list = []
    
    for idx, raw_slide in enumerate(raw_slides):
        trimmed = raw_slide.strip()
        if not trimmed:
            continue
            
        # Compile slide markdown to HTML
        slide_body = markdown.markdown(trimmed, extensions=['tables', 'fenced_code'])
        
        # Postprocess alerts and restore code/math
        slide_body = postprocess_html(slide_body, mermaid_blocks, display_math, inline_math)
        
        # Determine slide class
        slide_class = "slide title-slide" if idx == 0 else "slide"
        
        # Wrap slide
        slide_div = f'<div class="{slide_class}">{slide_body}</div>'
        slides_html_list.append(slide_div)
        
    slides_content = "\n".join(slides_html_list)
    
    # Recommendation bar
    header_html = """
    <div class="screen-only-header">
        <div class="header-notice">
            <strong>⚠️ Important Notice (GitHub Preference)</strong>: For the best reading and evaluation experience, <strong>we highly prefer and recommend that you read these documents directly on GitHub</strong> (or download the compiled PDF versions). The GitHub repository natively renders all interactive zoomable diagrams, full vector schemas, code block formatting, and dark mode controls.
        </div>
        <div class="header-links">
            <a href="https://github.com/suryasenthilr/NHAI_Innovation_Hackathon_7.0_Submission" target="_blank">📂 View Full Repository on GitHub</a>
            <a href="https://github.com/suryasenthilr/NHAI_Innovation_Hackathon_7.0_Submission/blob/master/README.md" target="_blank">📄 Read README.md on GitHub</a>
            <a href="https://github.com/suryasenthilr/NHAI_Innovation_Hackathon_7.0_Submission/blob/master/technical_documentation.md" target="_blank">📘 Read Technical Specification on GitHub</a>
            <a href="https://github.com/suryasenthilr/NHAI_Innovation_Hackathon_7.0_Submission/blob/master/judges_presentation.md" target="_blank">🏆 Read Pitch Slide Deck on GitHub</a>
        </div>
    </div>
    """
    
    # HTML Template
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BharatVerify - Judges Presentation</title>
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
<!-- MathJax for rendering LaTeX math formulas -->
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  }},
  options: {{
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
    body {{
        background-color: #090d16;
        color: #e1e7f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        margin: 0;
        padding: 40px 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-sizing: border-box;
    }}
    
    a {{
        color: #58a6ff;
        text-decoration: underline;
    }}
    
    a:hover {{
        color: #79c0ff;
    }}
    
    .slide-container {{
        display: flex;
        flex-direction: column;
        gap: 40px;
        width: 100%;
        max-width: 1000px;
        align-items: center;
    }}
    
    /* Recommendation Bar Styles */
    .screen-only-header {{
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 10px;
        font-size: 0.9em;
        color: #8892b0;
        width: 100%;
        box-sizing: border-box;
    }}
    .header-notice {{
        margin-bottom: 12px;
        line-height: 1.5;
    }}
    .header-notice strong {{
        color: #ffffff;
    }}
    .header-links {{
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
    }}
    .header-links a {{
        color: #58a6ff;
        text-decoration: none;
        font-weight: 600;
        border-bottom: 1px dashed #58a6ff;
        padding-bottom: 2px;
        transition: all 0.15s ease;
    }}
    .header-links a:hover {{
        color: #79c0ff;
        border-bottom-style: solid;
    }}
    
    .slide {{
        background-color: #0d1117;
        color: #c9d1d9;
        border-radius: 12px;
        border: 1px solid #30363d;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        width: 100%;
        aspect-ratio: 297 / 210; /* A4 Landscape Ratio */
        box-sizing: border-box;
        padding: 25px 45px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
        page-break-after: always;
        page-break-inside: avoid;
    }}
    
    /* Title Slide Specifics */
    .title-slide {{
        text-align: center;
        align-items: center;
        background: radial-gradient(circle at center, #161b22 0%, #0d1117 100%);
    }}
    
    .title-slide h1 {{
        font-size: 2.3em;
        background: linear-gradient(135deg, #00d2d3, #00a8ff, #a55eea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: none;
        padding-bottom: 0;
        margin-bottom: 25px;
    }}
    
    .title-slide h2 {{
        font-size: 1.4em;
        color: #8892b0;
        font-weight: 500;
        border-bottom: none;
        margin-bottom: 30px;
    }}
    
    .title-slide h3 {{
        font-size: 1.1em;
        color: #00d2d3;
        font-weight: 600;
    }}
    
    /* Header Styles */
    h1, h2, h3, h4 {{
        font-family: 'Outfit', sans-serif;
        color: #f0f6fc;
        margin-top: 0;
        margin-bottom: 12px;
        font-weight: 600;
    }}
    
    h1 {{ font-size: 1.7em; border-bottom: 2px solid #30363d; padding-bottom: 6px; margin-bottom: 12px; }}
    h2 {{ font-size: 1.35em; border-bottom: 1px solid #30363d; padding-bottom: 4px; margin-bottom: 10px; }}
    h3 {{ font-size: 1.15em; color: #ff9f43; margin-bottom: 8px; }}
    h4 {{ font-size: 1.05em; color: #00d2d3; margin-top: 6px; margin-bottom: 8px; }}
    
    p, li {{
        font-size: 0.95em;
        line-height: 1.45;
        color: #8892b0;
    }}
    
    p {{ margin-top: 0; margin-bottom: 8px; }}
    ul {{ margin-top: 0; margin-bottom: 8px; padding-left: 20px; }}
    li {{ margin-bottom: 4px; color: #c9d1d9; }}
    li strong {{ color: #ffffff; }}
    
    code {{
        font-family: 'Fira Code', monospace;
        background-color: rgba(110,118,129,0.3);
        padding: 0.2em 0.4em;
        border-radius: 4px;
        font-size: 85%;
        color: #ff7b72;
    }}
    
    pre {{
        background-color: #161b22;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #30363d;
        overflow: auto;
        margin: 10px 0;
    }}
    
    pre code {{
        color: #c9d1d9;
        background-color: transparent;
        font-size: 85%;
    }}
    
    table {{
        border-collapse: collapse;
        width: 100%;
        margin-top: 10px;
        margin-bottom: 15px;
        font-size: 0.78em; /* Compact table for slides */
    }}
    
    table th, table td {{
        padding: 6px 8px;
        border: 1px solid #30363d;
    }}
    
    table th {{
        background-color: #161b22;
        color: #ffffff;
        font-weight: 600;
    }}
    
    table tr {{
        background-color: #0d1117;
    }}
    
    table tr:nth-child(2n) {{
        background-color: #161b22;
    }}
    
    img {{
        max-height: 110mm;
        max-width: 90%;
        display: block;
        margin: 8px auto;
        border-radius: 8px;
        box-shadow: 0 5px 25px rgba(0,0,0,0.4);
    }}
    
    .alert-note, .alert-important, .alert-tip, .alert-warning, .alert-caution {{
        padding: 10px 15px;
        margin-bottom: 12px;
        border-left: 5px solid;
        border-radius: 6px;
        font-size: 90%;
    }}
    
    .alert-note {{
        background-color: #1f2a3c;
        border-color: #1f6feb;
        color: #58a6ff;
    }}
    
    .alert-important, .alert-caution {{
        background-color: #3c1f24;
        border-color: #f85149;
        color: #ff7b72;
    }}
    
    .alert-warning {{
        background-color: #342a18;
        border-color: #d29922;
        color: #d29922;
    }}
    
    .alert-tip {{
        background-color: #1f3c24;
        border-color: #3fb950;
        color: #56d364;
    }}
    
    .alert-note p, .alert-important p, .alert-tip p, .alert-warning p, .alert-caution p {{
        margin: 2px 0 0 0;
    }}
    
    .mermaid-container {{
        background: #161b22;
        display: flex;
        justify-content: center;
        margin: 10px 0;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }}
    
    .mermaid-svg {{
        max-width: 100%;
        max-height: 100px;
    }}

    @media (max-width: 768px) {{
        .slide {{
            aspect-ratio: auto;
            min-height: auto;
            padding: 30px 20px;
        }}
        body {{
            padding: 10px;
        }}
    }}
    
    @page {{
        size: A4 landscape;
        margin: 0;
    }}
    
    @media print {{
        body {{
            padding: 0;
            background-color: #0d1117;
        }}
        .screen-only-header {{
            display: none !important;
        }}
        .slide-container {{
            gap: 0;
            max-width: 100%;
        }}
        .slide {{
            width: 297mm;
            height: 210mm;
            border-radius: 0;
            border: none;
            box-shadow: none;
            margin: 0;
            padding: 25px 45px;
            page-break-after: always;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        table {{
            font-size: 0.72em;
        }}
        a {{
            text-decoration: underline;
            color: #58a6ff !important;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        .mermaid-svg {{
            max-height: 120mm;
            width: auto;
        }}
    }}
</style>
</head>
<body>
<div class="slide-container">
    {header_html}
    {slides_content}
</div>
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    print(f"Successfully generated static slides HTML at: {html_path}")

if __name__ == '__main__':
    compile_spec()
    compile_slides()
