import re

def fix_markdown_spacing(text):
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
            
        if list_item_pattern.match(line):
            if idx > 0:
                prev_line = lines[idx-1].strip()
                if prev_line and not list_item_pattern.match(lines[idx-1]) and not blockquote_pattern.match(lines[idx-1]):
                    new_lines.append('')
        elif header_pattern.match(line):
            if idx > 0:
                prev_line = lines[idx-1].strip()
                if prev_line:
                    new_lines.append('')
        elif blockquote_pattern.match(line):
            if idx > 0:
                prev_line = lines[idx-1].strip()
                if prev_line and not blockquote_pattern.match(lines[idx-1]):
                    new_lines.append('')
                    
        new_lines.append(line)
        
    return '\n'.join(new_lines)

def test():
    with open('technical_documentation.md', 'r', encoding='utf-8') as f:
        md_content = f.read()

    md_content = md_content.replace('Select {Blink, Smile, Yaw}', 'Select [Blink, Smile, Yaw]')
    
    # Step 1: Extract fenced code blocks
    lines = md_content.split('\n')
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
                leading_spaces = len(line) - len(line.lstrip(' '))
                code_indent = leading_spaces
                code_lines = []
                code_opening_line = line  # Save the opening line
                idx += 1
                continue
            else:
                in_fenced_code = False
                if code_indent > 0:
                    if new_lines and new_lines[-1].strip():
                        new_lines.append('')
                    for cl in code_lines:
                        cl_stripped = cl[code_indent:] if cl.startswith(' ' * code_indent) else cl.lstrip(' ')
                        new_lines.append('        ' + cl_stripped)
                    new_lines.append('')
                else:
                    new_lines.append(code_opening_line)  # Write opening line back
                    for cl in code_lines:
                        new_lines.append(cl)
                    new_lines.append(line)  # Write closing line back
                idx += 1
                continue
                
        if in_fenced_code:
            code_lines.append(line)
        else:
            new_lines.append(line)
        idx += 1
        
    text = '\n'.join(new_lines)
    text = fix_markdown_spacing(text)
    
    # Check if Diagram 6 now has the mermaid label
    lines_output = text.split('\n')
    for i, line in enumerate(lines_output):
        if "Diagram 6: UI Screen" in line:
            print("--- Found Diagram 6 in processed text (lines around it) ---")
            for j in range(max(0, i-5), min(len(lines_output), i+15)):
                print(f"{j}: {lines_output[j]}")
            break

if __name__ == "__main__":
    test()
