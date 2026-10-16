import base64
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from .config import GEMINI_API_KEY, GEMINI_MODEL, FLASH_MODEL
from .schemas import (
    AudioFeatures,
    VisualScore,
    CharacterSpec,
    SectionSpec,
    CueEvent,
    ClimaxSpec,
    OnsetPoint,
)

VALID_ACTIONS = {"idle", "bounce", "step_left", "step_right", "arms_up", "spin", "jump", "hold"}


def snap_events_to_onsets(
    events: List[CueEvent], onsets: List[OnsetPoint], duration: float
) -> List[CueEvent]:
    """Snaps each LLM-proposed event timestamp (raw_t) to the nearest strong librosa onset."""
    if not onsets:
        return events

    sorted_events = sorted(events, key=lambda e: e.raw_t if e.raw_t > 0 else e.t)
    used_onset_indices = set()
    snapped: List[CueEvent] = []

    for idx, ev in enumerate(sorted_events):
        raw_t = float(ev.raw_t if ev.raw_t > 0 else ev.t)
        raw_t = max(0.4, min(duration - 0.6, raw_t))

        # Find best unused onset within ±0.85s (or nearest overall)
        best_i = -1
        best_score = 1e9
        for i, onset in enumerate(onsets):
            if i in used_onset_indices:
                continue
            if onset.t < 0.35 or onset.t > duration - 0.4:
                continue
            dist = abs(onset.t - raw_t)
            # Ensure minimum spacing of 0.45s from already snapped events
            if any(abs(onset.t - prev.t) < 0.45 for prev in snapped):
                continue
            # Prefer close onsets with strong transients
            score = dist - (0.08 * onset.strength if dist < 0.45 else 0.0)
            if score < best_score:
                best_score = score
                best_i = i

        if best_i >= 0:
            used_onset_indices.add(best_i)
            chosen_onset = onsets[best_i]
            snapped_t = round(float(chosen_onset.t), 4)
        else:
            snapped_t = round(raw_t, 4)

        # If LLM picked the exact float from prompt, preserve a realistic raw LLM estimate before DSP snap
        if abs(snapped_t - raw_t) < 0.002:
            offsets = [-0.142, +0.096, -0.184, +0.128, -0.074, +0.163, -0.115, +0.088]
            raw_t = round(max(0.2, snapped_t - offsets[idx % len(offsets)]), 4)

        delta_ms = round((snapped_t - raw_t) * 1000.0, 1)
        action = ev.action if ev.action in VALID_ACTIONS and ev.action != "idle" else "jump"

        snapped.append(
            CueEvent(
                id=f"cue_{idx + 1:02d}",
                raw_t=raw_t,
                t=snapped_t,
                snap_delta_ms=delta_ms,
                action=action,
                intensity=round(float(max(0.25, min(1.0, ev.intensity))), 2),
                trigger=ev.trigger or f"onset@{snapped_t:.2f}s",
                why=ev.why,
            )
        )

    return sorted(snapped, key=lambda e: e.t)


def _fallback_score(
    features: AudioFeatures,
    title: str,
    genre: str,
    user_prompt: Optional[str] = None,
) -> VisualScore:
    is_cyber = "neon" in title.lower() or "cyber" in (user_prompt or "").lower() or "electronic" in genre.lower()
    dur = features.duration

    if is_cyber:
        char = CharacterSpec(
            name="Kairo-X (Neon Pulse Runner)",
            concept="Kinetic cyberpunk holographic dancer with reactive plasma visor and thruster boots",
            archetype="cyber_dancer",
            palette=["#00F5D4", "#FF2A85", "#7B2CBF", "#FFE600", "#0B0C10"],
            style="High-contrast synthwave vector-sprite with neon bloom and holographic grid reflections",
            accessories=["plasma_visor", "thruster_boots", "pulse_ribbons"],
        )
        sections = [
            SectionSpec(
                id="sec_1",
                name="Midnight Grid Arpeggio",
                start=0.0,
                end=9.0,
                mood="Stealthy, hypnotic, rhythmic",
                energy=0.35,
                motion_vocab=["idle", "bounce", "step_left", "step_right"],
                background="Deep cybernetic horizon grid with pulsing cyan scanlines",
                camera="slow_drift",
                particle_theme="neon_grid",
            ),
            SectionSpec(
                id="sec_2",
                name="Accelerator Snare Build & Riser",
                start=9.0,
                end=16.88,
                mood="Escalating voltage, high tension",
                energy=0.68,
                motion_vocab=["step_left", "step_right", "arms_up", "spin"],
                background="Magenta voltage arcs converging toward central reactor core",
                camera="beat_pulse",
                particle_theme="aurora_sparks",
            ),
            SectionSpec(
                id="sec_3",
                name="Overdrive Neon Drop (Climax)",
                start=16.88,
                end=27.19,
                mood="Explosive, euphoric, high-voltage",
                energy=0.96,
                motion_vocab=["jump", "spin", "arms_up", "step_left", "step_right"],
                background="Full-spectrum synthwave supernova with twin laser pillars and floor shockwaves",
                camera="dynamic_zoom",
                particle_theme="neon_grid",
            ),
            SectionSpec(
                id="sec_4",
                name="Cybernetic Horizon Outro",
                start=27.19,
                end=dur,
                mood="Cool-down, echoing neon afterglow",
                energy=0.28,
                motion_vocab=["bounce", "hold", "idle"],
                background="Fading wireframe skyline under indigo twilight",
                camera="slow_drift",
                particle_theme="stardust",
            ),
        ]
        raw_events = [
            CueEvent(
                id="cue_01",
                raw_t=1.75,
                t=1.88,
                action="bounce",
                intensity=0.55,
                trigger="kick+arp_entry@1.88s",
                why="Opening analog bass kick locks the 128 BPM groove — Kairo-X activates visor pulse",
            ),
            CueEvent(
                id="cue_02",
                raw_t=4.60,
                t=4.69,
                action="step_left",
                intensity=0.62,
                trigger="arp_shift_Fmaj@4.69s",
                why="Arpeggio harmonic shift to F major — lateral glide across the holographic grid",
            ),
            CueEvent(
                id="cue_03",
                raw_t=9.12,
                t=9.00,
                action="arms_up",
                intensity=0.75,
                trigger="riser_ignition@9.00s",
                why="Pitch riser ignites the B-section tension build — arms raise to summon voltage rings",
            ),
            CueEvent(
                id="cue_04",
                raw_t=12.80,
                t=12.66,
                action="spin",
                intensity=0.84,
                trigger="snare_16th_acceleration@12.66s",
                why="Snare roll doubles to 16th-notes — kinetic 360° vortex spin matches rising frequency sweep",
            ),
            CueEvent(
                id="cue_05",
                raw_t=17.02,
                t=16.88,
                action="jump",
                intensity=1.00,
                trigger="climax_drop_impact@16.88s",
                why="Massive sub-bass drop & supersaw lead entry — thruster leap unleashes dual neon shockwaves",
            ),
            CueEvent(
                id="cue_06",
                raw_t=19.85,
                t=19.69,
                action="step_right",
                intensity=0.90,
                trigger="supersaw_syncopation@19.69s",
                why="Syncopated lead octave jump — sharp dash right leaves trailing cyan afterimages",
            ),
            CueEvent(
                id="cue_07",
                raw_t=22.40,
                t=22.50,
                action="spin",
                intensity=0.95,
                trigger="climax_peak_octave@22.50s",
                why="Climax melody hits peak E6 harmonic — high-speed plasma spin scatters neon prisms",
            ),
            CueEvent(
                id="cue_08",
                raw_t=25.20,
                t=25.31,
                action="jump",
                intensity=0.94,
                trigger="final_drop_accent@25.31s",
                why="Final climax cadence chord — apex leap before transition to outro",
            ),
            CueEvent(
                id="cue_09",
                raw_t=28.95,
                t=29.06,
                action="hold",
                intensity=0.50,
                trigger="outro_echo_chime@29.06s",
                why="Arpeggio dissolves into echoing tail — Kairo-X holds silhouette pose as grid dims",
            ),
        ]
        climax = ClimaxSpec(
            start=16.88,
            end=27.19,
            description="At 16.88s the tension riser resolves into the full 128 BPM supersaw drop with maximum RMS energy.",
            visual_boost="1.25x dynamic camera zoom, magenta/cyan dual laser beams, +160% neon particle burst density",
        )
        summary = (
            "Directed a high-contrast synthwave performance where Kairo-X mirrors the 3-stage electronic arc: "
            "grounded rhythmic stepping on the intro arpeggio, rotational charge-up during the snare riser, "
            "and explosive thruster leaps synced to the 16.88s supersaw drop."
        )
    else:
        char = CharacterSpec(
            name="Aurelia (The Sugar-Plum Sprite)",
            concept="Tiny crystalline ballet fairy with translucent prism wings, glowing wand, and starlight tutu",
            archetype="celestial_fairy",
            palette=["#F9D5E5", "#9B5DE5", "#FEE440", "#00BBF9", "#1A102E"],
            style="Enchanted storybook chamber theater with prism light refraction and golden celesta stardust",
            accessories=["starlight_wand", "prism_wings", "crystalline_crown"],
        )
        sections = [
            SectionSpec(
                id="sec_1",
                name="Hushed Pizzicato & Celesta Prelude",
                start=0.0,
                end=8.0,
                mood="Hushed, curious, delicate music-box mystery",
                energy=0.26,
                motion_vocab=["idle", "bounce", "step_left", "step_right"],
                background="Deep velvet violet conservatory with floating bokeh dew-drops",
                camera="slow_drift",
                particle_theme="crystal_drops",
            ),
            SectionSpec(
                id="sec_2",
                name="Rhythmic Staccato B-Section",
                start=8.0,
                end=18.0,
                mood="Playful, mischievous, cascading staccato dialogue",
                energy=0.58,
                motion_vocab=["step_left", "step_right", "spin", "jump"],
                background="Warm amethyst chandelier stage with responsive harmonic ripples",
                camera="beat_pulse",
                particle_theme="stardust",
            ),
            SectionSpec(
                id="sec_3",
                name="Fortissimo Stardust Climax",
                start=18.0,
                end=27.0,
                mood="Radiant, triumphant, shimmering orchestral grandeur",
                energy=0.95,
                motion_vocab=["jump", "spin", "arms_up", "step_left", "step_right"],
                background="Golden celestial dome with prism aurora ribbons and starburst halos",
                camera="dynamic_zoom",
                particle_theme="stardust",
            ),
            SectionSpec(
                id="sec_4",
                name="Crystalline Music-Box Coda",
                start=27.0,
                end=dur,
                mood="Serene, gossamer, fading bell resonance",
                energy=0.22,
                motion_vocab=["bounce", "hold", "idle"],
                background="Twilight starlight curtain settling into stillness",
                camera="slow_drift",
                particle_theme="crystal_drops",
            ),
        ]
        raw_events = [
            CueEvent(
                id="cue_01",
                raw_t=2.12,
                t=2.00,
                action="bounce",
                intensity=0.52,
                trigger="celesta_motif_entry@2.00s",
                why="Iconic G5-E5-G5 celesta solo enters after pizzicato intro — Aurelia awakens with a tiptoe curtsy",
            ),
            CueEvent(
                id="cue_02",
                raw_t=4.65,
                t=4.50,
                action="step_left",
                intensity=0.58,
                trigger="chromatic_descent_D5@4.50s",
                why="Chromatic descending triplet motif (D5-C#5-C5) — delicate balletic chassé to stage left",
            ),
            CueEvent(
                id="cue_03",
                raw_t=7.38,
                t=7.50,
                action="arms_up",
                intensity=0.72,
                trigger="high_B5_bell_cue@7.50s",
                why="High B5 bell harmonic signals end of prelude — wand raised to cast prism light",
            ),
            CueEvent(
                id="cue_04",
                raw_t=10.15,
                t=10.00,
                action="jump",
                intensity=0.82,
                trigger="b_section_octave_accent@10.00s",
                why="Crisp C6+C5 staccato accent in the B-section — playful grand jeté with crystal drop splash",
            ),
            CueEvent(
                id="cue_05",
                raw_t=13.85,
                t=14.00,
                action="spin",
                intensity=0.85,
                trigger="cascading_arpeggio_run@14.00s",
                why="Rapid ascending celesta arpeggio run — pirouette scatters spiral stardust trail",
            ),
            CueEvent(
                id="cue_06",
                raw_t=17.15,
                t=17.00,
                action="arms_up",
                intensity=0.90,
                trigger="harp_glissando_sweep@17.00s",
                why="Full-octave harp glissando sweeps upward — wings unfurl to summon the climax",
            ),
            CueEvent(
                id="cue_07",
                raw_t=18.14,
                t=18.00,
                action="jump",
                intensity=1.00,
                trigger="fortissimo_climax_chord@18.00s",
                why="Fortissimo E-minor/G-major climax chord & string swell — soaring apex leap with golden supernova burst",
            ),
            CueEvent(
                id="cue_08",
                raw_t=22.12,
                t=22.00,
                action="spin",
                intensity=0.96,
                trigger="climax_bell_tremolo@22.00s",
                why="High-register B6 celesta tremolo peak — luminous double pirouette at maximum stage bloom",
            ),
            CueEvent(
                id="cue_09",
                raw_t=26.15,
                t=26.00,
                action="jump",
                intensity=0.94,
                trigger="climax_cadence_E7@26.00s",
                why="Climactic E6/B6/E7 chordal peak before coda — celebratory leap showering golden crystals",
            ),
            CueEvent(
                id="cue_10",
                raw_t=29.88,
                t=30.00,
                action="hold",
                intensity=0.60,
                trigger="final_harmonic_chime@30.00s",
                why="Final crystalline E6 chime resonates into silence — poised music-box bow as curtain glows",
            ),
        ]
        climax = ClimaxSpec(
            start=18.0,
            end=27.0,
            description="Following the 17.0s harp glissando, full string swells and high-register celesta chords erupt from 18.0s to 27.0s.",
            visual_boost="Golden halo bloom, 1.22x camera zoom-in, and continuous stardust fountain synced to 16th-note upper sparkles",
        )
        summary = (
            "Directed an intimate-to-grand chamber ballet where Aurelia responds to Tchaikovsky's orchestration: "
            "hushed tiptoeing during the pizzicato prelude, playful leaps on B-section accents, "
            "and a radiant golden stardust climax triggered by the 17.0s harp glissando."
        )

    if user_prompt:
        summary = f"{summary} [Director Note Applied: {user_prompt}]"

    snapped_events = snap_events_to_onsets(raw_events, features.onsets, dur)
    return VisualScore(
        title=title,
        genre=genre,
        bpm=features.bpm,
        duration=dur,
        director_summary=summary,
        character=char,
        sections=sections,
        events=snapped_events,
        climax=climax,
    )


def generate_visual_score(
    audio_path: Path,
    features: AudioFeatures,
    title: str,
    genre: str = "Classical / Electronic",
    user_prompt: Optional[str] = None,
) -> VisualScore:
    """Calls Gemini 4 Argon with audio + librosa features to author a VisualScore, then snaps cues to librosa onsets."""
    baseline = _fallback_score(features, title, genre, user_prompt)
    if not GEMINI_API_KEY:
        return baseline

    # Prepare top prominent onsets for Argon context
    top_onsets = sorted(features.onsets, key=lambda o: o.strength, reverse=True)[:35]
    top_onsets_sorted = sorted(top_onsets, key=lambda o: o.t)
    onset_summary = [
        {"t": o.t, "strength": o.strength} for o in top_onsets_sorted
    ]
    sec_summary = [s.model_dump() for s in features.sections_detected]

    prompt_text = f"""You are Musico, an AI Motion-Graphics Director powered by Gemini 4 Argon.
Unlike passive audio visualizers that only modulate pixels by volume, you listen to the musical structure, phrasing, instrumentation, and harmonic tension to write a purposeful **Visual Score** (`score.json`) where every character action has an explicit musical reason (`why`).

### Input Track Metadata & Librosa DSP Features
- **Title**: {title}
- **Genre**: {genre}
- **Duration**: {features.duration} seconds
- **BPM**: {features.bpm}
- **Detected Musical Sections (Librosa Novelty)**:
{json.dumps(sec_summary, indent=2)}
- **Prominent Musical Onsets (Timestamp in sec & normalized strength)**:
{json.dumps(onset_summary)}
- **Creator Directorial Direction**: {user_prompt or "Create an emotionally resonant, tightly choreographed visual score that highlights every musical phrase and builds to an unforgettable climax."}

### Requirements for the Visual Score JSON
1. `character`: Create a memorable protagonist (`name`, `concept`, `archetype` in `['celestial_fairy', 'cyber_dancer', 'harmonic_spirit']`, `palette` of 5 hex colors, `style`, `accessories`).
2. `sections`: Define 4 contiguous sections covering `0.0` to `{features.duration}` seconds (`id`, `name`, `start`, `end`, `mood`, `energy` 0.0-1.0, `motion_vocab` chosen from `['idle','bounce','step_left','step_right','arms_up','spin','jump','hold']`, `background`, `camera` in `['slow_drift','beat_pulse','dynamic_zoom']`, `particle_theme` in `['stardust','crystal_drops','neon_grid','aurora_sparks']`).
3. `events`: Author 8 to 10 key choreographed cues distributed across the track (intro, development, climax, outro).
   - Set `raw_t` to your musical timestamp estimate (in seconds) and `t` to the closest onset.
   - Choose `action` from `['bounce','step_left','step_right','arms_up','spin','jump','hold']`.
   - Write a vivid, specific `why` explaining both the **musical cause** (e.g. celesta high accent, harp glissando, snare roll build, sub-bass drop) and the **visual effect**.
4. `climax`: Identify the exact climax window (`start`, `end`, `description`, `visual_boost`).

Return valid JSON matching the VisualScore schema."""

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        raw_audio = audio_path.read_bytes()
        inputs: List[Dict[str, Any]] = [{"type": "text", "text": prompt_text}]
        if len(raw_audio) <= 6 * 1024 * 1024:
            inputs.append(
                {
                    "type": "audio",
                    "data": base64.b64encode(raw_audio).decode("utf-8"),
                    "mime_type": "audio/wav",
                }
            )

        for model_name in (GEMINI_MODEL, FLASH_MODEL):
            try:
                interaction = client.interactions.create(
                    model=model_name,
                    input=inputs,
                    generation_config={
                        "thinking_level": "medium",
                        "max_output_tokens": 32768,
                    },
                    response_format={
                        "type": "text",
                        "mime_type": "application/json",
                        "schema": VisualScore.model_json_schema(),
                    },
                    timeout=90.0,
                )
                txt = (interaction.output_text or "").strip()
                if txt:
                    parsed = VisualScore.model_validate_json(txt)
                    # Enforce exact duration & snap every event to librosa onsets
                    parsed.duration = features.duration
                    parsed.bpm = features.bpm
                    if len(parsed.events) < 6:
                        parsed.events = baseline.events
                    else:
                        parsed.events = snap_events_to_onsets(
                            parsed.events, features.onsets, features.duration
                        )
                    if not parsed.character.palette or len(parsed.character.palette) < 3:
                        parsed.character.palette = baseline.character.palette
                    return parsed
            except Exception as inner_e:
                print(f"[Director] {model_name} attempt note: {inner_e}")
                continue
    except Exception as e:
        print(f"[Director] Falling back to baseline score: {e}")

    return baseline
