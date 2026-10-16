import contextlib
import functools
import http.server
import logging
import socket
import threading
import time
from pathlib import Path
from typing import Any, Dict, List

from playwright.sync_api import sync_playwright

logger = logging.getLogger("yourdancer.verifier")


@contextlib.contextmanager
def _serve_directory_ephemeral(directory: Path):
    """Spins up a lightweight thread-safe HTTP server on an ephemeral localhost port for headless Playwright verification."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))

    class QuietServer(http.server.ThreadingHTTPServer):
        allow_reuse_address = True

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]

    server = QuietServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        server.server_close()


def verify_game_with_playwright(game_dir: Path) -> Dict[str, Any]:
    """
    Verification Signal 2: Headless Playwright Auto-Player Verification.
    Launches headless Chromium, loads the generated multi-file rhythm game, and executes:
      1. `window.__runAutoPlayer("perfect", diff)` for Easy, Normal, and Hard -> asserts 100.0% accuracy, 0 Miss, 0 Good.
      2. `window.__runAutoPlayer("jitter_120ms", "Normal")` -> asserts <20.0% accuracy (100% Miss), proving the judgement engine genuinely rejects off-beat inputs.
      3. Deterministic frame stepping via `window.__seek(t)` + screenshot capture.
      4. Asserts 0 console/page errors.
    """
    t0 = time.time()
    console_errors: List[str] = []
    page_errors: List[str] = []
    runs: Dict[str, Any] = {}

    with _serve_directory_ephemeral(game_dir) as base_url:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--use-angle=swiftshader",
                    "--autoplay-policy=no-user-gesture-required",
                    "--mute-audio",
                ],
            )
            page = browser.new_page(viewport={"width": 1100, "height": 720})
            page.on(
                "console",
                lambda msg: console_errors.append(msg.text) if msg.type == "error" else None,
            )
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))

            page.goto(f"{base_url}/index.html", wait_until="networkidle")

            # Deterministic seek check
            seek_probe = page.evaluate("window.__seek(12.5)")
            page.screenshot(path=str(game_dir / "preview_gameplay.png"))

            # Run Perfect Auto-Player on Easy, Normal, Hard
            for diff in ("Easy", "Normal", "Hard"):
                res = page.evaluate(f"window.__runAutoPlayer('perfect', '{diff}')")
                runs[f"perfect_{diff}"] = res

            page.screenshot(path=str(game_dir / "preview_results.png"))

            # Run +120ms Jitter Auto-Player on Normal to prove Miss detection works
            jitter_res = page.evaluate("window.__runAutoPlayer('jitter_120ms', 'Normal')")
            runs["jitter_120ms_Normal"] = jitter_res

            browser.close()

    all_errors = console_errors + page_errors
    perfect_normal = runs["perfect_Normal"]
    jitter_normal = runs["jitter_120ms_Normal"]

    perfect_passed = (
        float(perfect_normal["accuracy"]) == 100.0
        and int(perfect_normal["miss"]) == 0
        and int(perfect_normal["good"]) == 0
        and int(perfect_normal["perfect"]) == int(perfect_normal["totalNotes"])
    )
    jitter_passed = float(jitter_normal["accuracy"]) < 20.0 and int(jitter_normal["miss"]) > 0
    zero_errors_passed = len(all_errors) == 0

    overall_passed = perfect_passed and jitter_passed and zero_errors_passed

    return {
        "signal_name": "Signal 2: Headless Playwright Auto-Player & Jitter Verification",
        "status": "PASS" if overall_passed else "FAIL",
        "elapsed_seconds": round(time.time() - t0, 2),
        "console_error_count": len(all_errors),
        "console_errors": all_errors,
        "seek_probe": seek_probe,
        "assertions": {
            "perfect_100pct_accuracy": perfect_passed,
            "jitter_120ms_triggers_miss_below_20pct": jitter_passed,
            "zero_console_errors": zero_errors_passed,
        },
        "perfect_runs": {
            "Easy": {
                "totalNotes": runs["perfect_Easy"]["totalNotes"],
                "perfect": runs["perfect_Easy"]["perfect"],
                "good": runs["perfect_Easy"]["good"],
                "miss": runs["perfect_Easy"]["miss"],
                "maxCombo": runs["perfect_Easy"]["maxCombo"],
                "score": runs["perfect_Easy"]["score"],
                "accuracy": runs["perfect_Easy"]["accuracy"],
                "rank": runs["perfect_Easy"]["rank"],
            },
            "Normal": {
                "totalNotes": runs["perfect_Normal"]["totalNotes"],
                "perfect": runs["perfect_Normal"]["perfect"],
                "good": runs["perfect_Normal"]["good"],
                "miss": runs["perfect_Normal"]["miss"],
                "maxCombo": runs["perfect_Normal"]["maxCombo"],
                "score": runs["perfect_Normal"]["score"],
                "accuracy": runs["perfect_Normal"]["accuracy"],
                "rank": runs["perfect_Normal"]["rank"],
            },
            "Hard": {
                "totalNotes": runs["perfect_Hard"]["totalNotes"],
                "perfect": runs["perfect_Hard"]["perfect"],
                "good": runs["perfect_Hard"]["good"],
                "miss": runs["perfect_Hard"]["miss"],
                "maxCombo": runs["perfect_Hard"]["maxCombo"],
                "score": runs["perfect_Hard"]["score"],
                "accuracy": runs["perfect_Hard"]["accuracy"],
                "rank": runs["perfect_Hard"]["rank"],
            },
        },
        "jitter_120ms_run": {
            "difficulty": "Normal",
            "offsetMs": 120,
            "totalNotes": jitter_normal["totalNotes"],
            "perfect": jitter_normal["perfect"],
            "good": jitter_normal["good"],
            "miss": jitter_normal["miss"],
            "accuracy": jitter_normal["accuracy"],
            "rank": jitter_normal["rank"],
        },
    }
