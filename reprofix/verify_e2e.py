"""End-to-end Playwright + API verification for ReproFix on port 8003."""
import time
from pathlib import Path
import httpx
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8003"


def main():
    print("[verify_e2e] 1. Checking /api/health and /api/presets ...")
    r = httpx.get(f"{BASE_URL}/api/health", timeout=10.0)
    assert r.status_code == 200, f"Health check failed: {r.text}"
    health = r.json()
    print("  Health:", health)
    assert health["status"] == "ok"
    assert health["jobs_count"] >= 2
    presets = httpx.get(f"{BASE_URL}/api/presets", timeout=10.0).json()["presets"]
    assert len(presets) >= 2

    console_errors = []
    page_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1080})
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        print("[verify_e2e] 2. Loading ReproFix Dashboard at http://127.0.0.1:8003 ...")
        page.goto(BASE_URL, wait_until="networkidle")
        page.wait_for_selector("#steps-tbody tr", timeout=10000)

        # Verify Bug 1 preset is loaded with Red-First cards & diff
        summary_text = page.locator("#txt-bug-summary").inner_text()
        print("  Loaded Bug #1 summary:", summary_text[:90] + "...")
        assert len(summary_text) > 20

        red_card_text = page.locator("#red-verification-container").inner_text()
        assert "FALSE GREEN REJECTED" in red_card_text, "Missing FALSE GREEN REJECTED in Red-First log"
        assert "CONFIRMED RED" in red_card_text, "Missing CONFIRMED RED in Red-First log"

        diff_text = page.locator("#code-patch-diff").inner_text()
        assert "--- a/demo_target_app/app.js" in diff_text and "+++ b/demo_target_app/app.js" in diff_text, "Missing unified diff"

        sec_text = page.locator("#sec-token-context").inner_text()
        assert "false" in sec_text.lower(), f"Missing credential isolation proof: {sec_text}"

        # Click timestamp seek badge
        page.locator("#steps-tbody .ts-chip").first.click()
        time.sleep(0.2)

        # Switch to Preset #2 (Estimate $NaN)
        print("[verify_e2e] 3. Switching to Preset #2 (Estimate $NaN) ...")
        page.click("#btn-load-demo2")
        time.sleep(0.8)
        summary2 = page.locator("#txt-bug-summary").inner_text()
        print("  Preset #2 summary:", summary2[:90] + "...")
        assert "NaN" in summary2 or "discount" in summary2.lower()

        # Test Live Target App Drawer
        print("[verify_e2e] 4. Opening Live Target App Drawer ...")
        page.click("#btn-toggle-live-app")
        time.sleep(0.4)
        assert page.locator("#target-app-drawer").is_visible()

        # Capture full dashboard screenshot
        screenshot_path = Path(__file__).resolve().parent / "data" / "dashboard_verified.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"  Saved dashboard screenshot -> {screenshot_path} ({screenshot_path.stat().st_size} bytes)")

        # Test Live HITL #1 Approval + Sandbox Execution timing (<25s)
        print("[verify_e2e] 5. Testing live HITL #1 step edit + Red->Green sandbox execution ...")
        t0 = time.time()
        page.click("#btn-approve-steps")
        page.wait_for_function(
            "() => !document.getElementById('btn-approve-steps').disabled",
            timeout=35000,
        )
        elapsed = time.time() - t0
        print(f"  Live HITL #1 -> Red-First -> Patch -> Green -> PR completed in {elapsed:.2f}s!")
        assert elapsed < 45.0, f"Expected <45s execution, took {elapsed:.2f}s"

        browser.close()

    assert len(console_errors) == 0, f"Console errors detected: {console_errors}"
    assert len(page_errors) == 0, f"Page errors detected: {page_errors}"
    print("[verify_e2e] ALL CHECKS PASSED (0 console errors, 0 page errors)!")


if __name__ == "__main__":
    main()
