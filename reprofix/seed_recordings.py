"""Generates 2 real screen recordings of bugs in TaskFlow Pro using Playwright + ffmpeg."""
import http.server
import os
import shutil
import socketserver
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
DEMO_APP_DIR = BASE_DIR / "demo_target_app"
RECORDINGS_DIR = BASE_DIR / "data" / "recordings"

CURSOR_INIT_SCRIPT = """
(() => {
  window.addEventListener('DOMContentLoaded', () => {
    const cursor = document.createElement('div');
    cursor.id = '__demo_cursor';
    cursor.style.cssText = `
      position: fixed;
      top: 60px;
      left: 60px;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: rgba(239, 68, 68, 0.85);
      border: 3px solid #ffffff;
      box-shadow: 0 0 14px rgba(239, 68, 68, 0.9);
      pointer-events: none;
      z-index: 999999;
      transform: translate(-50%, -50%);
      transition: top 0.35s cubic-bezier(0.22, 1, 0.36, 1), left 0.35s cubic-bezier(0.22, 1, 0.36, 1), transform 0.15s ease;
    `;
    document.body.appendChild(cursor);

    window.__moveCursorTo = (selector, showClick = false) => {
      const el = document.querySelector(selector);
      if (!el) return;
      const rect = el.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      cursor.style.left = cx + 'px';
      cursor.style.top = cy + 'px';
      if (showClick) {
        cursor.style.transform = 'translate(-50%, -50%) scale(1.6)';
        el.style.outline = '3px solid #f59e0b';
        setTimeout(() => {
          cursor.style.transform = 'translate(-50%, -50%) scale(1.0)';
        }, 220);
      }
    };
  });
})();
"""


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DEMO_APP_DIR), **kwargs)

    def log_message(self, format, *args):
        pass


def start_local_server():
    httpd = socketserver.TCPServer(("127.0.0.1", 0), QuietHandler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, f"http://127.0.0.1:{port}"


def convert_webm_to_mp4(webm_path: Path, mp4_path: Path):
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(webm_path),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-vf",
        "fps=24,scale=1280:720",
        "-movflags",
        "+faststart",
        str(mp4_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def record_bug1(playwright, base_url: str, out_dir: Path):
    """Records Bug 1: Deleting TASK-101 leaves Active Tasks (3) and Sprint Velocity (21) stale."""
    with tempfile.TemporaryDirectory() as tmpdir:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=tmpdir,
            record_video_size={"width": 1280, "height": 720},
        )
        context.add_init_script(CURSOR_INIT_SCRIPT)
        page = context.new_page()
        page.goto(base_url, wait_until="networkidle")
        time.sleep(1.2)

        # Hover over initial Active Tasks (3) to show starting state
        page.evaluate("window.__moveCursorTo('#active-count', false)")
        time.sleep(0.9)

        # Move to Delete Task button on TASK-101
        page.evaluate("window.__moveCursorTo('#delete-TASK-101', true)")
        time.sleep(0.7)
        page.click("#delete-TASK-101")
        time.sleep(1.0)

        # Move cursor up to #active-count (still showing 3!) and #velocity-pts (still showing 21!)
        page.evaluate("window.__moveCursorTo('#active-count', true)")
        time.sleep(1.2)
        page.evaluate("window.__moveCursorTo('#velocity-pts', true)")
        time.sleep(1.2)

        video_path = Path(page.video.path())
        context.close()
        browser.close()

        target_webm = out_dir / "bug1_counter_desync.webm"
        target_mp4 = out_dir / "bug1_counter_desync.mp4"
        shutil.copy2(video_path, target_webm)
        convert_webm_to_mp4(target_webm, target_mp4)
        print(f"[seed_recordings] Created {target_mp4} ({target_mp4.stat().st_size} bytes)")


def record_bug2(playwright, base_url: str, out_dir: Path):
    """Records Bug 2: Entering '15%' in Partner Discount renders '$NaN' and TypeError banner."""
    with tempfile.TemporaryDirectory() as tmpdir:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=tmpdir,
            record_video_size={"width": 1280, "height": 720},
        )
        context.add_init_script(CURSOR_INIT_SCRIPT)
        page = context.new_page()
        page.goto(base_url, wait_until="networkidle")
        time.sleep(1.0)

        # Focus Partner Discount field
        page.evaluate("window.__moveCursorTo('#est-discount', true)")
        time.sleep(0.6)
        page.click("#est-discount")
        page.fill("#est-discount", "")
        for ch in "15%":
            page.type("#est-discount", ch, delay=160)
        time.sleep(0.6)

        # Click Calculate Estimate
        page.evaluate("window.__moveCursorTo('#btn-calc-estimate', true)")
        time.sleep(0.6)
        page.click("#btn-calc-estimate")
        time.sleep(1.0)

        # Point cursor at the broken $NaN total & error banner
        page.evaluate("window.__moveCursorTo('#estimate-total', true)")
        time.sleep(1.5)

        video_path = Path(page.video.path())
        context.close()
        browser.close()

        target_webm = out_dir / "bug2_estimate_nan.webm"
        target_mp4 = out_dir / "bug2_estimate_nan.mp4"
        shutil.copy2(video_path, target_webm)
        convert_webm_to_mp4(target_webm, target_mp4)
        print(f"[seed_recordings] Created {target_mp4} ({target_mp4.stat().st_size} bytes)")


def main():
    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
    httpd, base_url = start_local_server()
    try:
        with sync_playwright() as p:
            record_bug1(p, base_url, RECORDINGS_DIR)
            record_bug2(p, base_url, RECORDINGS_DIR)
    finally:
        httpd.shutdown()


if __name__ == "__main__":
    main()
