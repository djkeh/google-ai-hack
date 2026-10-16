"""Existing Playwright regression test suite for TaskFlow Pro."""
import os
from playwright.sync_api import sync_playwright, expect

TARGET_URL = os.environ.get("TARGET_APP_URL", "http://127.0.0.1:4173")


def run_existing_suite(base_url: str = TARGET_URL) -> dict:
    """Runs the 3 existing regression tests against `base_url` and returns structured results."""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        # Test 1: Initial board render
        try:
            page.goto(base_url, wait_until="networkidle")
            expect(page.locator("#active-count")).to_have_text("3")
            expect(page.locator("#velocity-pts")).to_have_text("21")
            expect(page.locator(".task-card")).to_have_count(3)
            results.append({"name": "test_initial_board_renders", "status": "PASSED", "detail": "3 tasks, active-count=3, velocity=21"})
        except Exception as exc:
            results.append({"name": "test_initial_board_renders", "status": "FAILED", "detail": str(exc)})

        # Test 2: Adding a new task updates list and metrics
        try:
            page.goto(base_url, wait_until="networkidle")
            page.fill("#new-task-title", "Deploy canary build")
            page.fill("#new-task-pts", "5")
            page.click("#btn-add-task")
            expect(page.locator(".task-card")).to_have_count(4)
            expect(page.locator("#active-count")).to_have_text("4")
            expect(page.locator("#velocity-pts")).to_have_text("26")
            results.append({"name": "test_add_new_task_increments_counter", "status": "PASSED", "detail": "Added task -> 4 cards, active-count=4, velocity=26"})
        except Exception as exc:
            results.append({"name": "test_add_new_task_increments_counter", "status": "FAILED", "detail": str(exc)})

        # Test 3: Standard integer estimate calculation
        try:
            page.goto(base_url, wait_until="networkidle")
            page.fill("#est-hours", "10")
            page.fill("#est-rate", "100")
            page.fill("#est-discount", "0")
            page.click("#btn-calc-estimate")
            expect(page.locator("#estimate-total")).to_have_text("$1,000.00")
            results.append({"name": "test_estimate_without_discount", "status": "PASSED", "detail": "10h * $100 @ 0 discount -> $1,000.00"})
        except Exception as exc:
            results.append({"name": "test_estimate_without_discount", "status": "FAILED", "detail": str(exc)})

        browser.close()

    passed_all = all(r["status"] == "PASSED" for r in results)
    return {
        "passed": passed_all,
        "total": len(results),
        "passed_count": sum(1 for r in results if r["status"] == "PASSED"),
        "tests": results,
    }


def test_existing_regression_suite():
    res = run_existing_suite(TARGET_URL)
    assert res["passed"], f"Regression suite failed: {res}"


if __name__ == "__main__":
    summary = run_existing_suite(TARGET_URL)
    for t in summary["tests"]:
        print(f"[{t['status']}] {t['name']}: {t['detail']}")
    if not summary["passed"]:
        raise SystemExit(1)
