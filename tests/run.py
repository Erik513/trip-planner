"""Runs tests/run.html in a headless Chromium (Playwright) and prints the result.

    python tests/run.py

Needs `pip install playwright` and `python -m playwright install chromium`. Nothing is shown on screen:
the repository is served on a free local port, the checks run in the background and the exit code is 0 only if all pass.
"""
import functools, http.server, pathlib, socketserver, sys, threading

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    handler = functools.partial(Quiet, directory=str(ROOT))
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as httpd:
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1000, "height": 800})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(f"http://127.0.0.1:{port}/tests/run.html")
            page.wait_for_function("document.title.startsWith('PASS') || document.title.startsWith('FAIL')", timeout=120000)
            summary = page.inner_text("#summary")
            lines = page.eval_on_selector_all("#out li", "els => els.map(e => e.innerText.replace(/\\n/g, ' | '))")
            browser.close()
        httpd.shutdown()
    print(summary)
    for line in lines:
        print(" ", line)
    if errors:
        print("page errors:", *errors, sep="\n  ")
    return 0 if summary.startswith("All") and not errors else 1


if __name__ == "__main__":
    sys.exit(main())
