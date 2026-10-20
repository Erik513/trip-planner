"""Builds the standalone index.html from src/app.html (fonts and lz-string embedded, works offline).
Usage:  python3 build.py
"""
import base64, re, pathlib
root = pathlib.Path(__file__).parent
s = (root / "src/app.html").read_text(encoding="utf-8")

def face(family, file, weight):
    data = base64.b64encode((root / "vendor/fonts" / file).read_bytes()).decode()
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};font-display:swap;"
            f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")

faces = [face("Bricolage Grotesque", f"bricolage-grotesque-latin-{w}-normal.woff2", w) for w in (600, 800)]
faces += [face("Figtree", f"figtree-latin-{w}-normal.woff2", w) for w in (400, 500, 600, 700)]
faces += [face("JetBrains Mono", "jetbrains-mono-latin-500-normal.woff2", 500)]

# Remove the Google Fonts link, inline the fonts
s = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n?', "", s)
s = s.replace("<style>", "<style>\n" + "\n".join(faces) + "\n", 1)
# Replace lz-string from the CDN with the local copy
s = re.sub(r'<script src="https://cdnjs.cloudflare.com/ajax/libs/lz-string/[^"]+"></script>',
           lambda m: "<script>\n" + (root / "vendor/lz-string.min.js").read_text(encoding="utf-8") + "\n</script>", s)
# Remove the Claude-specific meta tag, move the title into <head>
s = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n?', "", s)
title = re.search(r"<title>.*?</title>", s).group(0)
s = s.replace(title + "\n", "", 1).replace(title, "", 1)

head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0f7c74">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Trip Planner">
{title}
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
"""
(root / "index.html").write_text(head + s + "\n</body>\n</html>\n", encoding="utf-8")
print("index.html built:", round((root / "index.html").stat().st_size / 1024), "KB")
