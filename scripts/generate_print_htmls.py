import os

def generate_spec_html():
    md_path = 'technical_documentation.md'
    html_path = 'technical_documentation_print.html'
    
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        return
        
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    # Escape javascript template literals backticks
    escaped_md = md_content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BharatVerify - Technical Specification (Print Ready)</title>
<!-- Marked.js for markdown parsing -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
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
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<!-- Mermaid.js for rendering diagrams -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
    mermaid.initialize({{ 
        startOnLoad: false, 
        theme: 'default',
        securityLevel: 'loose',
        flowchart: {{ useMaxWidth: false, htmlLabels: true }}
    }});
</script>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        max-width: 900px;
        margin: 40px auto;
        padding: 0 30px;
        color: #24292e;
        background-color: #ffffff;
    }}
    h1, h2, h3, h4, h5, h6 {{
        margin-top: 28px;
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
    p {{ margin-top: 0; margin-bottom: 16px; }}
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
        padding: 16px;
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
        padding: 8px 13px;
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
        background-color: #f6f8fa;
    }}
    blockquote {{
        padding: 0 1.5em;
        color: #6a737d;
        border-left: 0.3em solid #dfe2e5;
        margin: 0 0 20px 0;
        font-style: italic;
    }}
    img {{
        max-width: 80%;
        height: auto;
        display: block;
        margin: 25px auto;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
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
    .mermaid {{
        background: #ffffff;
        display: flex;
        justify-content: center;
        margin: 25px 0;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #eaecef;
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
        pre, table, .alert-note, .alert-important, .alert-tip, .mermaid {{
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
<div id="content">Loading technical specification...</div>

<!-- RAW MARKDOWN DATA -->
<script type="text/markdown" id="markdown-src">
{escaped_md}
</script>

<script>
    // Global error handler to print diagnostic panels inside the browser
    window.addEventListener('error', function(e) {{
        document.getElementById('content').innerHTML = 
            '<div style="color:red;padding:20px;border:2px solid red;background:#fff5f5;border-radius:8px;font-family:sans-serif;">' +
            '<h3>⚠️ JavaScript Compilation Error</h3>' +
            '<strong>Error Message:</strong> ' + e.message + '<br>' +
            '<strong>Filename:</strong> ' + e.filename + '<br>' +
            '<strong>Line:</strong> ' + e.lineno + ':' + e.colno + '<br>' +
            '<strong>Stack Trace:</strong> <pre style="background:#fdf0f0;padding:10px;border:1px solid #f5c2c2;">' + (e.error ? e.error.stack : '') + '</pre>' +
            '</div>';
    }});

    document.addEventListener('DOMContentLoaded', async () => {{
        // Parse markdown
        let mdText = document.getElementById('markdown-src').textContent;
        
        // Resolve escapes
        mdText = mdText.replace(/\\\\\\\\/g, '\\\\').replace(/\\\\\\`/g, '`').replace(/\\\\\\$/g, '$');
        
        // --- BULLETPROOF PREPROCESSOR ---
        
        // 1. Extract mermaid blocks
        const mermaidBlocks = [];
        mdText = mdText.replace(/```mermaid\s*\n([\s\S]*?)\n```/g, function(match, code) {{
            const placeholder = `%%MERMAID_BLOCK_${{mermaidBlocks.length}}%%`;
            mermaidBlocks.push(code.trim());
            return '\\n' + placeholder + '\\n';
        }});

        // 2. Extract display math blocks ($$...$$)
        const displayMathBlocks = [];
        mdText = mdText.replace(/\$\$\s*\n([\s\S]*?)\n\$\$/g, function(match, math) {{
            const placeholder = `%%DISPLAY_MATH_${{displayMathBlocks.length}}%%`;
            displayMathBlocks.push(math.trim());
            return '\\n' + placeholder + '\\n';
        }});
        mdText = mdText.replace(/\$\$([\s\S]*?)\$\$/g, function(match, math) {{
            const placeholder = `%%DISPLAY_MATH_${{displayMathBlocks.length}}%%`;
            displayMathBlocks.push(math.trim());
            return '\\n' + placeholder + '\\n';
        }});

        // 3. Extract inline math blocks ($...$)
        const inlineMathBlocks = [];
        mdText = mdText.replace(/\$([^\$\s](?:[^\$]*?[^\$\s])?)\$/g, function(match, math) {{
            const placeholder = `%%INLINE_MATH_${{inlineMathBlocks.length}}%%`;
            inlineMathBlocks.push(math.trim());
            return placeholder;
        }});
        
        // Preprocess Github alerts
        const lines = mdText.split('\\n');
        let inAlert = false;
        let alertType = "";
        let alertLines = [];
        let processedLines = [];
        
        for (let line of lines) {{
            let trimmed = line.trim();
            if (trimmed.startsWith('> [!')) {{
                inAlert = true;
                alertType = trimmed.substring(4, trimmed.length - 1).toLowerCase();
                alertLines = [];
                continue;
            }}
            
            if (inAlert) {{
                if (trimmed.startsWith('>')) {{
                    let content = line.substring(line.indexOf('>') + 1).trim();
                    alertLines.push(content);
                }} else {{
                    let cssClass = "alert-" + alertType;
                    let title = alertType.toUpperCase();
                    let contentHtml = alertLines.join('<br>');
                    processedLines.push(`<div class="${{cssClass}}"><strong>${{title}}</strong>: ${{contentHtml}}</div>\\n`);
                    inAlert = false;
                    processedLines.push(line);
                }}
            }} else {{
                processedLines.push(line);
            }}
        }}
        
        if (inAlert) {{
            let cssClass = "alert-" + alertType;
            let title = alertType.toUpperCase();
            let contentHtml = alertLines.join('<br>');
            processedLines.push(`<div class="${{cssClass}}"><strong>${{title}}</strong>: ${{contentHtml}}</div>\\n`);
        }}
        
        // Parse the preprocessed markdown using marked
        let parsedHtml = marked.parse(processedLines.join('\\n'));
        
        // --- RESTORE EXTRACTED BLOCKS ---
        
        // 4. Restore mermaid blocks
        mermaidBlocks.forEach((code, index) => {{
            parsedHtml = parsedHtml.replace(`%%MERMAID_BLOCK_${{index}}%%`, `<div class="mermaid">${{code}}</div>`);
        }});

        // 5. Restore display math
        displayMathBlocks.forEach((math, index) => {{
            parsedHtml = parsedHtml.replace(`%%DISPLAY_MATH_${{index}}%%`, `$$\\n${{math}}\\n$$`);
        }});

        // 6. Restore inline math
        inlineMathBlocks.forEach((math, index) => {{
            parsedHtml = parsedHtml.replace(`%%INLINE_MATH_${{index}}%%`, `$${{math}}$`);
        }});
        
        document.getElementById('content').innerHTML = parsedHtml;

        // Render Mermaid Diagrams
        try {{
            await mermaid.run();
        }} catch (e) {{
            console.error("Mermaid rendering failed:", e);
        }}
        
        // Render LaTeX equations
        try {{
            if (window.MathJax) {{
                MathJax.typesetPromise();
            }}
        }} catch (e) {{
            console.error("MathJax rendering failed:", e);
        }}
    }});
</script>
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Successfully generated: {html_path}")

def generate_slides_html():
    md_path = 'judges_presentation.md'
    html_path = 'judges_presentation_print.html'
    
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        return
        
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        
    # Escape javascript template literals backticks
    escaped_md = md_content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BharatVerify - Slides Presentation (Print Ready)</title>
<!-- Marked.js for markdown parsing -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
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
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<!-- Mermaid.js for rendering diagrams -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
    mermaid.initialize({{ 
        startOnLoad: false, 
        theme: 'dark',
        securityLevel: 'loose',
        flowchart: {{ useMaxWidth: false, htmlLabels: true }}
    }});
</script>
<style>
    body {{
        background-color: #0d1117;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #c9d1d9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .slide {{
        background-color: #0d1117;
        color: #c9d1d9;
        width: 297mm; /* A4 Landscape width */
        height: 210mm; /* A4 Landscape height */
        padding: 40px 60px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        border-bottom: 2px dashed #30363d;
        page-break-after: always;
        overflow: hidden;
    }}
    h1, h2, h3 {{
        color: #f0f6fc;
        margin-top: 0;
    }}
    h1 {{ font-size: 2.2em; border-bottom: 2px solid #30363d; padding-bottom: 10px; margin-bottom: 15px; }}
    h2 {{ font-size: 1.8em; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 12px; }}
    h3 {{ font-size: 1.6em; margin-bottom: 10px; }}
    h4 {{ font-size: 1.3em; color: #ff8c00; margin-top: 0; margin-bottom: 15px; }}
    p {{ font-size: 1.15em; line-height: 1.5; }}
    ul {{ font-size: 1.15em; line-height: 1.5; margin-top: 5px; }}
    code {{
        font-family: monospace;
        background-color: rgba(110,118,129,0.4);
        padding: 0.2em 0.4em;
        border-radius: 4px;
        font-size: 85%;
        color: #ff7b72;
    }}
    pre {{
        background-color: #161b22;
        padding: 12px;
        border-radius: 8px;
        overflow: auto;
        border: 1px solid #30363d;
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
        font-size: 0.85em;
    }}
    table th, table td {{
        padding: 6px 10px;
        border: 1px solid #30363d;
    }}
    table th {{
        background-color: #161b22;
        color: #f0f6fc;
    }}
    table tr:nth-child(2n) {{
        background-color: #161b22;
    }}
    img {{
        max-height: 42%;
        max-width: 85%;
        display: block;
        margin: 10px auto;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    }}
    .alert-note, .alert-important, .alert-tip {{
        padding: 10px 15px;
        margin-bottom: 12px;
        border-left: 5px solid;
        border-radius: 4px;
        font-size: 1.0em;
    }}
    .alert-note {{
        background-color: #1f2a3c;
        border-color: #1f6feb;
        color: #c9d1d9;
    }}
    .alert-important {{
        background-color: #3c1f24;
        border-color: #f85149;
        color: #c9d1d9;
    }}
    .alert-tip {{
        background-color: #1f3c24;
        border-color: #3fb950;
        color: #c9d1d9;
    }}
    .mermaid {{
        background: #161b22;
        display: flex;
        justify-content: center;
        margin: 10px 0;
        padding: 8px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }}
    @media print {{
        body {{
            background-color: #0d1117;
        }}
        .slide {{
            border-bottom: none;
            width: 100%;
            height: 100vh;
            page-break-after: always;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
    }}
</style>
</head>
<body>
<div id="content">Loading presentation slides...</div>

<!-- RAW MARKDOWN DATA -->
<script type="text/markdown" id="markdown-src">
{escaped_md}
</script>

<script>
    // Global error handler to print diagnostic panels inside the browser
    window.addEventListener('error', function(e) {{
        document.getElementById('content').innerHTML = 
            '<div style="color:red;padding:20px;border:2px solid red;background:#fff5f5;border-radius:8px;font-family:sans-serif;">' +
            '<h3>⚠️ JavaScript Compilation Error</h3>' +
            '<strong>Error Message:</strong> ' + e.message + '<br>' +
            '<strong>Filename:</strong> ' + e.filename + '<br>' +
            '<strong>Line:</strong> ' + e.lineno + ':' + e.colno + '<br>' +
            '<strong>Stack Trace:</strong> <pre style="background:#fdf0f0;padding:10px;border:1px solid #f5c2c2;">' + (e.error ? e.error.stack : '') + '</pre>' +
            '</div>';
    }});

    document.addEventListener('DOMContentLoaded', async () => {{
        // Parse markdown
        let mdText = document.getElementById('markdown-src').textContent;
        
        // Resolve escapes
        mdText = mdText.replace(/\\\\\\\\/g, '\\\\').replace(/\\\\\\`/g, '`').replace(/\\\\\\$/g, '$');
        
        // --- BULLETPROOF PREPROCESSOR ---
        
        // 1. Extract mermaid blocks
        const mermaidBlocks = [];
        mdText = mdText.replace(/```mermaid\s*\n([\s\S]*?)\n```/g, function(match, code) {{
            const placeholder = `%%MERMAID_BLOCK_${{mermaidBlocks.length}}%%`;
            mermaidBlocks.push(code.trim());
            return '\\n' + placeholder + '\\n';
        }});

        // 2. Extract display math blocks ($$...$$)
        const displayMathBlocks = [];
        mdText = mdText.replace(/\$\$\s*\n([\s\S]*?)\n\$\$/g, function(match, math) {{
            const placeholder = `%%DISPLAY_MATH_${{displayMathBlocks.length}}%%`;
            displayMathBlocks.push(math.trim());
            return '\\n' + placeholder + '\\n';
        }});
        mdText = mdText.replace(/\$\$([\s\S]*?)\$\$/g, function(match, math) {{
            const placeholder = `%%DISPLAY_MATH_${{displayMathBlocks.length}}%%`;
            displayMathBlocks.push(math.trim());
            return '\\n' + placeholder + '\\n';
        }});

        // 3. Extract inline math blocks ($...$)
        const inlineMathBlocks = [];
        mdText = mdText.replace(/\$([^\$\s](?:[^\$]*?[^\$\s])?)\$/g, function(match, math) {{
            const placeholder = `%%INLINE_MATH_${{inlineMathBlocks.length}}%%`;
            inlineMathBlocks.push(math.trim());
            return placeholder;
        }});
        
        // Split markdown by slide separator (---)
        const rawSlides = mdText.split(/\\n---\\n/);
        const container = document.getElementById('content');
        container.innerHTML = '';
        
        for (let rawSlide of rawSlides) {{
            let trimmed = rawSlide.trim();
            if (!trimmed) continue;
            
            // Preprocess Github alerts inside slide
            const lines = trimmed.split('\\n');
            let inAlert = false;
            let alertType = "";
            let alertLines = [];
            let processedLines = [];
            
            for (let line of lines) {{
                let lineTrimmed = line.trim();
                if (lineTrimmed.startsWith('> [!')) {{
                    inAlert = true;
                    alertType = lineTrimmed.substring(4, lineTrimmed.length - 1).toLowerCase();
                    alertLines = [];
                    continue;
                }}
                
                if (inAlert) {{
                    if (lineTrimmed.startsWith('>')) {{
                        let content = line.substring(line.indexOf('>') + 1).trim();
                        alertLines.push(content);
                    }} else {{
                        let cssClass = "alert-" + alertType;
                        let title = alertType.toUpperCase();
                        let contentHtml = alertLines.join('<br>');
                        processedLines.push(`<div class="${{cssClass}}"><strong>${{title}}</strong>: ${{contentHtml}}</div>\\n`);
                        inAlert = false;
                        processedLines.push(line);
                    }}
                }} else {{
                    processedLines.push(line);
                }}
            }}
            
            if (inAlert) {{
                let cssClass = "alert-" + alertType;
                let title = alertType.toUpperCase();
                let contentHtml = alertLines.join('<br>');
                processedLines.push(`<div class="${{cssClass}}"><strong>${{title}}</strong>: ${{contentHtml}}</div>\\n`);
            }}
            
            // Parse preprocessed slide markdown
            let parsedSlideHtml = marked.parse(processedLines.join('\\n'));
            
            // --- RESTORE EXTRACTED BLOCKS ---
            
            // 4. Restore mermaid blocks
            mermaidBlocks.forEach((code, index) => {{
                parsedSlideHtml = parsedSlideHtml.replace(`%%MERMAID_BLOCK_${{index}}%%`, `<div class="mermaid">${{code}}</div>`);
            }});

            // 5. Restore display math
            displayMathBlocks.forEach((math, index) => {{
                parsedSlideHtml = parsedSlideHtml.replace(`%%DISPLAY_MATH_${{index}}%%`, `$$\\n${{math}}\\n$$`);
            }});

            // 6. Restore inline math
            inlineMathBlocks.forEach((math, index) => {{
                parsedSlideHtml = parsedSlideHtml.replace(`%%INLINE_MATH_${{index}}%%`, `$${{math}}$`);
            }});
            
            const slideDiv = document.createElement('div');
            slideDiv.className = 'slide';
            slideDiv.innerHTML = parsedSlideHtml;
            container.appendChild(slideDiv);
        }}

        // Render Mermaid Diagrams
        try {{
            await mermaid.run();
        }} catch (e) {{
            console.error("Mermaid rendering failed:", e);
        }}
        
        // Render LaTeX equations
        try {{
            if (window.MathJax) {{
                MathJax.typesetPromise();
            }}
        }} catch (e) {{
            console.error("MathJax rendering failed:", e);
        }}
    }});
</script>
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Successfully generated: {html_path}")

if __name__ == '__main__':
    generate_spec_html()
    generate_slides_html()
