"""Baut aus src/app.html die eigenständige index.html (Schriften und lz-string eingebettet, läuft offline).
Aufruf:  python3 build.py
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

# Google-Fonts-Link entfernen, Schriften inline einsetzen
s = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n?', "", s)
s = s.replace("<style>", "<style>\n" + "\n".join(faces) + "\n", 1)
# lz-string vom CDN durch die lokale Kopie ersetzen
s = re.sub(r'<script src="https://cdnjs.cloudflare.com/ajax/libs/lz-string/[^"]+"></script>',
           lambda m: "<script>\n" + (root / "vendor/lz-string.min.js").read_text(encoding="utf-8") + "\n</script>", s)
# Claude-spezifisches Meta-Tag entfernen, Titel in den <head> verschieben
s = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n?', "", s)
title = re.search(r"<title>.*?</title>", s).group(0)
s = s.replace(title + "\n", "", 1).replace(title, "", 1)

head = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{title}
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
"""
(root / "index.html").write_text(head + s + "\n</body>\n</html>\n", encoding="utf-8")
print("index.html gebaut:", round((root / "index.html").stat().st_size / 1024), "KB")
