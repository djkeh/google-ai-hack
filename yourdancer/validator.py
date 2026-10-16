from typing import Any, Dict, List

NPS_CAPS: Dict[str, float] = {
    "Easy": 2.0,
    "Normal": 4.0,
    "Hard": 7.0,
}

MIN_SAME_LANE_GAP_SEC = 0.080
HOLD_BUFFER_SEC = 0.050
MIN_BOUND_SEC = 0.50
MAX_BOUND_MARGIN_SEC = 0.30


def validate_difficulty_chart(
    difficulty: str,
    notes: List[Dict[str, Any]],
    duration: float,
) -> Dict[str, Any]:
    """
    Validates a single difficulty chart against all 4 YourDancer playability rules:
      - Rule 1: No same-lane notes within 80ms (t2 - t1 >= 0.080s)
      - Rule 2: Sliding 1.0s window Notes-Per-Second (NPS) <= cap (Easy<=2.0, Normal<=4.0, Hard<=7.0)
      - Rule 3: No overlapping hold notes on the same lane (hold.end_t + 0.05 <= next_note.t)
      - Rule 4: All notes within [0.5, duration - 0.3]
    """
    violations: List[Dict[str, Any]] = []
    sorted_notes = sorted(notes, key=lambda n: (float(n["t"]), int(n["lane"])))
    nps_cap = NPS_CAPS.get(difficulty, 4.0)
    max_bound = round(duration - MAX_BOUND_MARGIN_SEC, 3)

    # Group by lane for Rule 1 & Rule 3
    by_lane: Dict[int, List[Dict[str, Any]]] = {0: [], 1: [], 2: [], 3: []}
    for n in sorted_notes:
        lane = int(n["lane"])
        by_lane.setdefault(lane, []).append(n)

        # Rule 4: Bounds check [0.5, duration - 0.3]
        nt = float(n["t"])
        n_end = float(n.get("end_t", nt))
        if nt < MIN_BOUND_SEC - 1e-6 or n_end > max_bound + 1e-6:
            violations.append(
                {
                    "rule": "Rule 4 (Bounds [0.5s, duration-0.3s])",
                    "difficulty": difficulty,
                    "lane": lane,
                    "t": round(nt, 3),
                    "detail": (
                        f"Note '{n.get('label', 'note')}' at t={nt:.3f}s (end_t={n_end:.3f}s) "
                        f"falls outside safe window [{MIN_BOUND_SEC:.2f}s, {max_bound:.2f}s]."
                    ),
                }
            )

    # Rule 1 & Rule 3 per lane
    for lane, lane_notes in by_lane.items():
        for i in range(len(lane_notes) - 1):
            curr_n = lane_notes[i]
            next_n = lane_notes[i + 1]
            t1 = float(curr_n["t"])
            t2 = float(next_n["t"])
            gap = t2 - t1

            if gap < MIN_SAME_LANE_GAP_SEC - 1e-5:
                violations.append(
                    {
                        "rule": "Rule 1 (Min Same-Lane Gap >= 80ms)",
                        "difficulty": difficulty,
                        "lane": lane,
                        "t": round(t2, 3),
                        "detail": (
                            f"Lane {lane} double-tap collision: '{curr_n.get('label')}' (t={t1:.3f}s) "
                            f"and '{next_n.get('label')}' (t={t2:.3f}s) are only {gap * 1000.0:.1f}ms apart (< 80.0ms)."
                        ),
                    }
                )

            if curr_n.get("type") == "hold":
                hold_end = float(curr_n.get("end_t", t1))
                if hold_end + HOLD_BUFFER_SEC > t2 + 1e-5:
                    overlap_ms = (hold_end + HOLD_BUFFER_SEC - t2) * 1000.0
                    violations.append(
                        {
                            "rule": "Rule 3 (No Hold Overlap + 50ms Release Buffer)",
                            "difficulty": difficulty,
                            "lane": lane,
                            "t": round(t1, 3),
                            "detail": (
                                f"Lane {lane} hold note '{curr_n.get('label')}' (end_t={hold_end:.3f}s + 50ms buffer) "
                                f"overlaps next note '{next_n.get('label')}' at t={t2:.3f}s by {overlap_ms:.1f}ms."
                            ),
                        }
                    )

    # Rule 2: Sliding 1.0s window NPS cap
    peak_nps = 0.0
    reported_nps_windows = 0
    for i, n_start in enumerate(sorted_notes):
        w_start = float(n_start["t"])
        w_end = w_start + 1.0 - 1e-5
        count_in_1s = sum(1 for m in sorted_notes if w_start - 1e-6 <= float(m["t"]) <= w_end)
        if count_in_1s > peak_nps:
            peak_nps = float(count_in_1s)
        if count_in_1s > nps_cap and reported_nps_windows < 2:
            reported_nps_windows += 1
            violations.append(
                {
                    "rule": f"Rule 2 (NPS Cap <= {nps_cap:.1f} notes/s)",
                    "difficulty": difficulty,
                    "lane": int(n_start["lane"]),
                    "t": round(w_start, 3),
                    "detail": (
                        f"{difficulty} density burst in 1.0s window [{w_start:.2f}s, {w_start + 1.0:.2f}s]: "
                        f"{count_in_1s} notes/sec exceeds {difficulty} cap of {nps_cap:.1f} NPS."
                    ),
                }
            )

    return {
        "difficulty": difficulty,
        "passed": len(violations) == 0,
        "note_count": len(sorted_notes),
        "hold_count": sum(1 for n in sorted_notes if n.get("type") == "hold"),
        "peak_nps": round(peak_nps, 2),
        "nps_cap": nps_cap,
        "violation_count": len(violations),
        "violations": violations,
    }


def validate_all_charts(charts_by_diff: Dict[str, List[Dict[str, Any]]], duration: float) -> Dict[str, Any]:
    """Validates Easy, Normal, and Hard charts and returns an aggregate Signal 1 report."""
    per_diff: Dict[str, Any] = {}
    all_violations: List[Dict[str, Any]] = []

    for diff in ("Easy", "Normal", "Hard"):
        notes = charts_by_diff.get(diff, [])
        res = validate_difficulty_chart(diff, notes, duration)
        per_diff[diff] = res
        all_violations.extend(res["violations"])

    return {
        "passed": len(all_violations) == 0,
        "total_violations": len(all_violations),
        "difficulties": per_diff,
        "violations": all_violations,
    }
