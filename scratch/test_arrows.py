import base64
import urllib.request
import sys

def try_mermaid(code, description):
    graph_bytes = code.encode("utf-8")
    base64_bytes = base64.urlsafe_b64encode(graph_bytes)
    base64_string = base64_bytes.decode("ascii")
    url = f"https://mermaid.ink/svg/{base64_string}"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            svg_data = r.read()
            print(f"SUCCESS {description}: ({len(svg_data)} bytes)")
            return True
    except Exception as e:
        print(f"FAILED {description}: ({e})")
        return False

def test():
    # Test 1: Using -> in unquoted label (like in Diagram 6)
    code_fail = """stateDiagram-v2
    StateA --> StateB: Reconnect Online -> AWS POST trigger"""
    try_mermaid(code_fail, "Test 1: Unquoted label containing ->")

    # Test 2: Using -> in quoted label
    code_quoted = """stateDiagram-v2
    StateA --> StateB: "Reconnect Online -> AWS POST trigger\""""
    try_mermaid(code_quoted, "Test 2: Quoted label containing ->")

    # Test 3: Replacing -> with unicode arrow →
    code_unicode = """stateDiagram-v2
    StateA --> StateB: Reconnect Online → AWS POST trigger"""
    try_mermaid(code_unicode, "Test 3: Unicode arrow in label")

if __name__ == "__main__":
    test()
