import markdown

def test():
    # Test case: Inline HTML pre/code block inside list item
    text_html = """1. **Item:**

    <pre><code class="language-bash">git clone https://github.com/...
cd NHAI_...
npm install</code></pre>

2. **Item 2:**"""

    print("--- HTML pre/code in list ---")
    print(markdown.markdown(text_html, extensions=['tables']))

if __name__ == "__main__":
    test()
