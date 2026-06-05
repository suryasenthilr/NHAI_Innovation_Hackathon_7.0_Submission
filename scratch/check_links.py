import re

print("Checking technical_documentation_print.html links:")
with open("technical_documentation_print.html", "r", encoding="utf-8") as f:
    content = f.read()

links = re.findall(r'href="([^"]+)"', content)
github_links = [l for l in links if "github" in l]
for l in github_links[:15]:
    print(" -", l)

print("\nChecking judges_presentation_print.html links:")
with open("judges_presentation_print.html", "r", encoding="utf-8") as f:
    content = f.read()

links = re.findall(r'href="([^"]+)"', content)
github_links = [l for l in links if "github" in l]
for l in github_links[:15]:
    print(" -", l)
