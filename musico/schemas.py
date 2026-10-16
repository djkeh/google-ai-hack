from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class OnsetPoint(BaseModel):
    t: float = Field(description="Onset timestamp in seconds")
    strength: float = Field(description="Normalized onset strength 0.0 to 1.0")


class CurvePoint(BaseModel):
    t: float
    value: float


class DetectedSection(BaseModel):
    index: int
    start: float
    end: float
    avg_energy: float
    avg_brightness: float
    suggested_role: str


class AudioFeatures(BaseModel):
    filename: str
    duration: float
    bpm: float
    beats: List[float]
    onsets: List[OnsetPoint]
    rms_curve: List[CurvePoint]
    spectral_centroid_curve: List[CurvePoint]
    sections_detected: List[DetectedSection]
    lyrics: Optional[str] = None


class CharacterSpec(BaseModel):
    name: str = Field(description="Character name, e.g. 'Aurelia the Sugar-Plum Sprite'")
    concept: str = Field(description="Visual concept & personality description")
    archetype: str = Field(description="'celestial_fairy' | 'cyber_dancer' | 'harmonic_spirit'")
    palette: List[str] = Field(description="4 to 5 hex colors ['#F9D5E5', '#6A4C93', ...]")
    style: str = Field(description="Art style direction for sprite and stage")
    accessories: List[str] = Field(default_factory=list, description="Signature props/details")


class SectionSpec(BaseModel):
    id: str = Field(description="Section identifier e.g. sec_1")
    name: str = Field(description="Musical section title e.g. 'Hushed Celesta Prelude'")
    start: float = Field(description="Start time in seconds")
    end: float = Field(description="End time in seconds")
    mood: str = Field(description="Emotional and rhythmic mood")
    energy: float = Field(description="Normalized energy level 0.0 to 1.0")
    motion_vocab: List[str] = Field(
        description="Allowed sprite poses from ['idle','bounce','step_left','step_right','arms_up','spin','jump','hold']"
    )
    background: str = Field(description="Background visual motif description")
    camera: str = Field(description="Camera behavior e.g. 'slow_drift', 'beat_pulse', 'dynamic_zoom'")
    particle_theme: str = Field(description="'stardust' | 'crystal_drops' | 'neon_grid' | 'aurora_sparks'")


class CueEvent(BaseModel):
    id: str = Field(description="Unique cue ID e.g. cue_01")
    raw_t: float = Field(description="Initial LLM-proposed timestamp before onset snapping")
    t: float = Field(description="Final librosa onset-snapped timestamp in seconds")
    snap_delta_ms: float = Field(default=0.0, description="(t - raw_t) * 1000 in milliseconds")
    action: str = Field(
        description="Pose/action triggered: 'jump' | 'spin' | 'arms_up' | 'step_left' | 'step_right' | 'bounce' | 'hold'"
    )
    intensity: float = Field(default=0.85, description="Visual intensity 0.1 to 1.0")
    trigger: str = Field(description="Musical signal trigger e.g. 'onset>0.85 (celesta high accent)'")
    why: str = Field(
        description="Directorial rationale explaining WHY this specific visual action happens at this exact musical moment"
    )


class ClimaxSpec(BaseModel):
    start: float = Field(description="Climax start time in seconds")
    end: float = Field(description="Climax end time in seconds")
    description: str = Field(description="Why this section is the musical climax and how visuals escalate")
    visual_boost: str = Field(description="Specific climax effects e.g. 'Golden stardust burst + 1.25x zoom + halo bloom'")


class VisualScore(BaseModel):
    title: str
    genre: str
    bpm: float
    duration: float
    director_summary: str
    character: CharacterSpec
    sections: List[SectionSpec]
    events: List[CueEvent]
    climax: ClimaxSpec


class ArgonCritiqueCheck(BaseModel):
    criterion: str
    passed: bool
    observation: str


class ArgonVisualCritique(BaseModel):
    passed: bool
    score: int = Field(description="0 to 100 directorial quality score")
    summary: str
    checks: List[ArgonCritiqueCheck]
    patch_instructions: str


class VerificationIteration(BaseModel):
    iteration: int
    status: str  # "FAIL" | "PASS"
    timestamp: str
    check_a_runtime: Dict[str, Any]
    check_b_timing_bounds: Dict[str, Any]
    check_c_argon_critique: Dict[str, Any]
    proxy_frames: List[str]
    failure_reasons: List[str] = Field(default_factory=list)
    patch_applied: Optional[str] = None
    patch_diff: Optional[str] = None


class JobRecord(BaseModel):
    job_id: str
    title: str
    track_id: str
    status: str  # "queued" | "analyzing" | "directing" | "generating_character" | "generating_scene" | "verifying" | "completed" | "failed"
    created_at: str
    updated_at: str
    prompt_override: Optional[str] = None
    model_used: str = "gemini-4-argon"
    companion_models: List[str] = Field(
        default_factory=lambda: ["gemini-nano-banana-2.1", "gemini-3.8-flash", "librosa-dsp"]
    )
    audio_url: str
    scene_url: str
    sprite_url: str
    sprite_raw_url: str
    features_summary: Dict[str, Any] = Field(default_factory=dict)
    score: Optional[VisualScore] = None
    verification_history: List[VerificationIteration] = Field(default_factory=list)
    final_verification: Optional[Dict[str, Any]] = None
    gcs_urls: Dict[str, str] = Field(default_factory=dict)
    firestore_synced: bool = False
    stage_logs: List[Dict[str, Any]] = Field(default_factory=list)
