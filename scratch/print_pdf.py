import subprocess
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_path = r"C:\bharatverify-antigravity\technical_documentation_print.html"
pdf_path = r"C:\bharatverify-antigravity\technical_documentation.pdf"

print("HTML file exists:", os.path.exists(html_path))

# Run Chrome
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    "--include-background",
    f"file:///{html_path}"
]

print("Running command:", " ".join(cmd))
result = subprocess.run(cmd, capture_output=True, text=True)

print("Exit code:", result.returncode)
print("Stdout:", result.stdout)
print("Stderr:", result.stderr)

print("PDF file exists after run:", os.path.exists(pdf_path))
