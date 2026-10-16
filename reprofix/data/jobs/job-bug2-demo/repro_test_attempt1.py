"""Attempt 1 (Naive Reproduction Test) — checks superficial DOM state."""
import os
from playwright.sync_api import sync_playwright, expect

TARGET_URL = os.environ.get("TARGET_APP_URL", "http://127.0.0.1:4173")

def run_repro():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(TARGET_URL, wait_until="networkidle")
        page.fill('#est-discount', '15%')
        page.click('#btn-calc-estimate')
        # Weak assertion: only checks that #estimate-total element is visible, missing '$NaN' text check!
        expect(page.locator('#estimate-total')).to_be_visible()
        browser.close()

if __name__ == "__main__":
    run_repro()
