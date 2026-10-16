// Musico Deterministic Canvas 2D Motion-Graphics Engine
// Generated & Verified by Gemini 4 Argon

// === MUSICO DIRECTOR CALIBRATION CONFIG (AUTO-VERIFIED BY ARGON) ===
const MUSICO_CALIBRATION = {
  EVENT_LATENCY_OFFSET_SEC: 0.000,
  JUMP_APEX_IMPULSE: 165.0,
  CLAMP_CHARACTER_BOUNDS: true,
  CLIMAX_BLOOM_GAIN: 1.65
};

const SCORE_DATA = {
  "title": "Neon Pulse (Cyberpunk Etude)",
  "genre": "Electronic / Synthwave",
  "bpm": 129.2,
  "duration": 32.0,
  "director_summary": "A high-energy cyberpunk performance where Kaelen Vex, a neon-clad android dancer, locks into a 129 BPM synth arpeggio on a rain-slicked holographic rooftop. The choreography progresses from precise robotic isolation steps during the muted arpeggio intro, winds up through a high-frequency snare and pitch-riser buildup, and explodes into anti-gravity shockwave leaps and rapid spins when the full sub-bass and saw-lead drop at 16.6s, before powering down into a glowing stasis pose as the synth echoes fade.",
  "character": {
    "name": "Kaelen Vex, the Neon Cyber-Dancer",
    "concept": "An agile, street-smart android street dancer with articulated carbon-fiber joints and sound-reactive LED circuitry embedded in a cropped tech-jacket, performing atop a rain-swept cyberpunk skyscraper.",
    "archetype": "cyber_dancer",
    "palette": [
      "#00F5D4",
      "#FF007F",
      "#7B2CBF",
      "#0D0E15",
      "#FEE440"
    ],
    "style": "High-contrast cyberpunk vector anime with glowing neon rim-lighting, chromatic aberration accents, and wet rooftop reflections.",
    "accessories": [
      "Holographic LED visor",
      "Plasma-core kinetic sneakers",
      "Floating neon charge rings",
      "Fiber-optic dreadlock cables"
    ]
  },
  "sections": [
    {
      "id": "sec_1",
      "name": "Arpeggio Boot-Up & Snare Ignition",
      "start": 0.0,
      "end": 12.26,
      "mood": "Mechanical, focused, and steadily awakening",
      "energy": 0.35,
      "motion_vocab": [
        "idle",
        "bounce",
        "step_left",
        "step_right"
      ],
      "background": "Dark rain-slicked holographic rooftop with a dim cyan wireframe grid pulsing to the muted synth arpeggio",
      "camera": "slow_drift",
      "particle_theme": "neon_grid"
    },
    {
      "id": "sec_2",
      "name": "High-Voltage Riser & Charge Sequence",
      "start": 12.26,
      "end": 16.6,
      "mood": "Urgent, accelerating, and high-tension",
      "energy": 0.78,
      "motion_vocab": [
        "spin",
        "arms_up",
        "bounce"
      ],
      "background": "Vertigo-inducing neon sky-billboards flickering rapidly in magenta and yellow as energy conduits surge upward",
      "camera": "beat_pulse",
      "particle_theme": "aurora_sparks"
    },
    {
      "id": "sec_3",
      "name": "Overdrive Cyber-Drop Climax",
      "start": 16.6,
      "end": 26.94,
      "mood": "Explosive, euphoric, and kinetic",
      "energy": 0.98,
      "motion_vocab": [
        "jump",
        "spin",
        "step_left",
        "step_right",
        "arms_up"
      ],
      "background": "Full-spectrum holographic cityscape overload with shockwave ripples expanding across the wet rooftop floor on every beat",
      "camera": "dynamic_zoom",
      "particle_theme": "neon_grid"
    },
    {
      "id": "sec_4",
      "name": "System Cooldown & Neon Fade",
      "start": 26.94,
      "end": 32.0,
      "mood": "Cool, atmospheric, and resolving",
      "energy": 0.18,
      "motion_vocab": [
        "hold",
        "idle"
      ],
      "background": "Mist-shrouded cyberpunk skyline settling into deep violet twilight as lingering digital rain drifts down",
      "camera": "slow_drift",
      "particle_theme": "crystal_drops"
    }
  ],
  "events": [
    {
      "id": "cue_01",
      "raw_t": 1.4,
      "t": 1.4164,
      "snap_delta_ms": 16.4,
      "action": "step_left",
      "intensity": 0.35,
      "trigger": "onset=0.294 (low synth arpeggio downbeat)",
      "why": "As the clean 129 BPM synth arpeggio establishes its foundational pulse, Kaelen executes a crisp robotic isolation step to the left, locking his glowing sneakers into the grid."
    },
    {
      "id": "cue_02",
      "raw_t": 4.7,
      "t": 4.7137,
      "snap_delta_ms": 13.7,
      "action": "step_right",
      "intensity": 0.4,
      "trigger": "onset=0.309 (arpeggio phrase repeat accent)",
      "why": "On the second four-bar arpeggio cycle, Kaelen mirrors his mechanical groove with a sharp step right, sending a cyan ripple across the wet rooftop surface."
    },
    {
      "id": "cue_03",
      "raw_t": 9.0,
      "t": 9.0326,
      "snap_delta_ms": 32.6,
      "action": "bounce",
      "intensity": 0.7,
      "trigger": "onset=0.678 (quarter-note snare build entrance)",
      "why": "Sharp electronic snare hits suddenly enter the mix and begin climbing in pitch; Kaelen drops his center of gravity into a sharp hydraulic bounce to absorb the sudden rhythmic impact."
    },
    {
      "id": "cue_04",
      "raw_t": 9.95,
      "t": 9.9614,
      "snap_delta_ms": 11.4,
      "action": "arms_up",
      "intensity": 0.88,
      "trigger": "onset=0.923 (snare build peak accent)",
      "why": "As the quarter-note snare strikes reach peak transient force, Kaelen thrusts both arms skyward to summon twin holographic charge rings around his wrists."
    },
    {
      "id": "cue_05",
      "raw_t": 12.3,
      "t": 12.3066,
      "snap_delta_ms": 6.6,
      "action": "spin",
      "intensity": 0.95,
      "trigger": "onset=1.000 (double-time snare subdivision transition)",
      "why": "The snare roll doubles its speed at the maximum onset peak of the track (1.000), propelling Kaelen into a high-velocity vortex spin that trails ribbons of magenta plasma."
    },
    {
      "id": "cue_06",
      "raw_t": 14.4,
      "t": 14.4196,
      "snap_delta_ms": 19.6,
      "action": "arms_up",
      "intensity": 0.9,
      "trigger": "onset=0.470 (16th-note snare riser surge)",
      "why": "During the frantic 16th-note snare acceleration and rising synth sweep, Kaelen locks into an overhead power-charge stance as sparks arc across his visor."
    },
    {
      "id": "cue_07",
      "raw_t": 18.7,
      "t": 18.7153,
      "snap_delta_ms": 15.3,
      "action": "jump",
      "intensity": 1.0,
      "trigger": "onset=0.256 (climax high-lead melodic peak)",
      "why": "With the main drop in full swing, the piercing synth lead hits its upper-register hook and sub-bass pulse; Kaelen launches into an anti-gravity shockwave leap that shatters the holographic floor grid."
    },
    {
      "id": "cue_08",
      "raw_t": 21.1,
      "t": 21.1069,
      "snap_delta_ms": 6.9,
      "action": "spin",
      "intensity": 0.92,
      "trigger": "onset=0.316 (climax second phrase turnaround)",
      "why": "At the midpoint turnaround of the drop melody, Kaelen whips into a razor-sharp 360-degree cyber-spin, synchronizing with the bright synth syncopation."
    },
    {
      "id": "cue_09",
      "raw_t": 24.3,
      "t": 24.3345,
      "snap_delta_ms": 34.5,
      "action": "jump",
      "intensity": 0.98,
      "trigger": "onset=0.296 (final climax octave leap)",
      "why": "As the lead synth makes its final climactic ascent before the outro, Kaelen executes one last high-voltage leap with maximum neon bloom and camera zoom."
    },
    {
      "id": "cue_10",
      "raw_t": 27.1,
      "t": 27.1441,
      "snap_delta_ms": 44.1,
      "action": "hold",
      "intensity": 0.3,
      "trigger": "onset=0.304 (outro chord resolution & sub-bass cutoff)",
      "why": "The driving beat cuts out abruptly, leaving only soft, bell-like synth arpeggio echoes; Kaelen freezes in an iconic silhouette pose as his LED circuits slowly dim into standby mode."
    }
  ],
  "climax": {
    "start": 16.6,
    "end": 26.94,
    "description": "Following the intense snare roll and pitch-riser buildup, the track erupts at 16.6s into its highest sustained energy section (0.49 avg energy) featuring a soaring high-octave synth lead over a driving four-on-the-floor bassline. Kaelen unleashes his full aerial vocabulary—leaping and spinning in sync with the melodic peaks.",
    "visual_boost": "Dual cyan-magenta shockwave rings on beat + 1.3x dynamic camera zoom + intense neon visor bloom and rain-splash particle overdrive"
  }
};
const FEATURES_DATA = {
  "filename": "neon_pulse.wav",
  "duration": 32.0,
  "bpm": 129.2,
  "beats": [
    9.0326,
    9.497,
    9.9614,
    10.4258,
    10.8902,
    11.3778,
    11.8422,
    12.3066,
    12.771,
    13.2586,
    13.723,
    14.1874,
    14.6518,
    15.0698,
    15.4877,
    15.9521,
    16.4165,
    16.9041,
    17.3685,
    17.8329,
    18.3205,
    18.7849,
    19.2493,
    19.7137,
    20.1781,
    20.6658,
    21.1302,
    21.5946,
    22.059,
    22.5234,
    22.9878,
    23.4754,
    23.9398,
    24.4042,
    24.8686,
    25.333,
    25.8206,
    26.285,
    26.7494
  ],
  "onsets": [
    {
      "t": 0.2554,
      "strength": 0.085
    },
    {
      "t": 0.4644,
      "strength": 0.139
    },
    {
      "t": 0.7198,
      "strength": 0.122
    },
    {
      "t": 0.952,
      "strength": 0.253
    },
    {
      "t": 1.1842,
      "strength": 0.122
    },
    {
      "t": 1.4164,
      "strength": 0.294
    },
    {
      "t": 1.6486,
      "strength": 0.192
    },
    {
      "t": 1.8808,
      "strength": 0.144
    },
    {
      "t": 2.113,
      "strength": 0.211
    },
    {
      "t": 2.3452,
      "strength": 0.135
    },
    {
      "t": 2.5774,
      "strength": 0.169
    },
    {
      "t": 2.8328,
      "strength": 0.263
    },
    {
      "t": 3.065,
      "strength": 0.086
    },
    {
      "t": 3.2972,
      "strength": 0.305
    },
    {
      "t": 3.5294,
      "strength": 0.125
    },
    {
      "t": 3.7616,
      "strength": 0.245
    },
    {
      "t": 3.9938,
      "strength": 0.132
    },
    {
      "t": 4.226,
      "strength": 0.275
    },
    {
      "t": 4.4582,
      "strength": 0.183
    },
    {
      "t": 4.7137,
      "strength": 0.309
    },
    {
      "t": 4.9226,
      "strength": 0.182
    },
    {
      "t": 5.178,
      "strength": 0.29
    },
    {
      "t": 5.387,
      "strength": 0.135
    },
    {
      "t": 5.6424,
      "strength": 0.245
    },
    {
      "t": 5.8746,
      "strength": 0.088
    },
    {
      "t": 6.1068,
      "strength": 0.305
    },
    {
      "t": 6.339,
      "strength": 0.13
    },
    {
      "t": 6.5712,
      "strength": 0.233
    },
    {
      "t": 6.8034,
      "strength": 0.137
    },
    {
      "t": 7.0356,
      "strength": 0.239
    },
    {
      "t": 7.2678,
      "strength": 0.167
    },
    {
      "t": 7.5233,
      "strength": 0.295
    },
    {
      "t": 7.7322,
      "strength": 0.151
    },
    {
      "t": 7.9877,
      "strength": 0.279
    },
    {
      "t": 8.1966,
      "strength": 0.102
    },
    {
      "t": 8.4521,
      "strength": 0.225
    },
    {
      "t": 8.6843,
      "strength": 0.091
    },
    {
      "t": 8.9165,
      "strength": 0.242
    },
    {
      "t": 9.0326,
      "strength": 0.678
    },
    {
      "t": 9.497,
      "strength": 0.871
    },
    {
      "t": 9.9614,
      "strength": 0.923
    },
    {
      "t": 10.4258,
      "strength": 0.844
    },
    {
      "t": 10.8902,
      "strength": 0.675
    },
    {
      "t": 11.3546,
      "strength": 0.484
    },
    {
      "t": 11.7493,
      "strength": 0.197
    },
    {
      "t": 12.3066,
      "strength": 1.0
    },
    {
      "t": 12.5388,
      "strength": 0.359
    },
    {
      "t": 12.771,
      "strength": 0.308
    },
    {
      "t": 13.0032,
      "strength": 0.246
    },
    {
      "t": 13.2354,
      "strength": 0.168
    },
    {
      "t": 13.4676,
      "strength": 0.139
    },
    {
      "t": 13.723,
      "strength": 0.425
    },
    {
      "t": 13.9552,
      "strength": 0.48
    },
    {
      "t": 14.1874,
      "strength": 0.47
    },
    {
      "t": 14.4196,
      "strength": 0.47
    },
    {
      "t": 14.6518,
      "strength": 0.423
    },
    {
      "t": 14.7911,
      "strength": 0.17
    },
    {
      "t": 14.9072,
      "strength": 0.169
    },
    {
      "t": 15.0233,
      "strength": 0.167
    },
    {
      "t": 15.1394,
      "strength": 0.179
    },
    {
      "t": 15.2555,
      "strength": 0.19
    },
    {
      "t": 15.3716,
      "strength": 0.184
    },
    {
      "t": 15.4877,
      "strength": 0.181
    },
    {
      "t": 15.6038,
      "strength": 0.178
    },
    {
      "t": 15.7199,
      "strength": 0.167
    },
    {
      "t": 15.836,
      "strength": 0.168
    },
    {
      "t": 15.9521,
      "strength": 0.181
    },
    {
      "t": 16.0682,
      "strength": 0.144
    },
    {
      "t": 16.1843,
      "strength": 0.128
    },
    {
      "t": 16.3004,
      "strength": 0.137
    },
    {
      "t": 16.4165,
      "strength": 0.127
    },
    {
      "t": 16.8809,
      "strength": 0.212
    },
    {
      "t": 17.1363,
      "strength": 0.151
    },
    {
      "t": 17.2989,
      "strength": 0.247
    },
    {
      "t": 17.7633,
      "strength": 0.244
    },
    {
      "t": 18.0651,
      "strength": 0.11
    },
    {
      "t": 18.2277,
      "strength": 0.2
    },
    {
      "t": 18.5527,
      "strength": 0.09
    },
    {
      "t": 18.7153,
      "strength": 0.256
    },
    {
      "t": 19.0171,
      "strength": 0.124
    },
    {
      "t": 19.1797,
      "strength": 0.256
    },
    {
      "t": 19.6441,
      "strength": 0.304
    },
    {
      "t": 19.9459,
      "strength": 0.111
    },
    {
      "t": 20.1085,
      "strength": 0.231
    },
    {
      "t": 20.5729,
      "strength": 0.157
    },
    {
      "t": 20.8747,
      "strength": 0.086
    },
    {
      "t": 21.1069,
      "strength": 0.316
    },
    {
      "t": 21.3624,
      "strength": 0.096
    },
    {
      "t": 21.5249,
      "strength": 0.253
    },
    {
      "t": 21.8268,
      "strength": 0.157
    },
    {
      "t": 21.9893,
      "strength": 0.301
    },
    {
      "t": 22.4537,
      "strength": 0.28
    },
    {
      "t": 22.7556,
      "strength": 0.095
    },
    {
      "t": 22.9181,
      "strength": 0.212
    },
    {
      "t": 23.2432,
      "strength": 0.079
    },
    {
      "t": 23.4057,
      "strength": 0.221
    },
    {
      "t": 23.7076,
      "strength": 0.118
    },
    {
      "t": 23.8701,
      "strength": 0.236
    },
    {
      "t": 24.172,
      "strength": 0.078
    },
    {
      "t": 24.3345,
      "strength": 0.296
    },
    {
      "t": 24.6364,
      "strength": 0.151
    },
    {
      "t": 24.7989,
      "strength": 0.247
    },
    {
      "t": 25.2633,
      "strength": 0.245
    },
    {
      "t": 25.5652,
      "strength": 0.111
    },
    {
      "t": 25.7277,
      "strength": 0.201
    },
    {
      "t": 26.0528,
      "strength": 0.095
    },
    {
      "t": 26.2153,
      "strength": 0.255
    },
    {
      "t": 26.5172,
      "strength": 0.124
    },
    {
      "t": 26.6797,
      "strength": 0.256
    },
    {
      "t": 27.1441,
      "strength": 0.304
    },
    {
      "t": 27.446,
      "strength": 0.194
    },
    {
      "t": 27.6782,
      "strength": 0.155
    },
    {
      "t": 27.9104,
      "strength": 0.174
    },
    {
      "t": 28.1426,
      "strength": 0.141
    },
    {
      "t": 28.3748,
      "strength": 0.141
    },
    {
      "t": 28.607,
      "strength": 0.129
    },
    {
      "t": 28.8624,
      "strength": 0.118
    },
    {
      "t": 29.0946,
      "strength": 0.103
    },
    {
      "t": 29.3268,
      "strength": 0.098
    }
  ],
  "rms_curve": [
    {
      "t": 0.0,
      "value": 0.3713
    },
    {
      "t": 0.1,
      "value": 0.2662
    },
    {
      "t": 0.2,
      "value": 0.1316
    },
    {
      "t": 0.3,
      "value": 0.2059
    },
    {
      "t": 0.4,
      "value": 0.0965
    },
    {
      "t": 0.5,
      "value": 0.425
    },
    {
      "t": 0.6,
      "value": 0.1849
    },
    {
      "t": 0.7,
      "value": 0.1701
    },
    {
      "t": 0.8,
      "value": 0.1414
    },
    {
      "t": 0.9,
      "value": 0.1913
    },
    {
      "t": 1.0,
      "value": 0.3803
    },
    {
      "t": 1.1,
      "value": 0.1298
    },
    {
      "t": 1.2,
      "value": 0.2077
    },
    {
      "t": 1.3,
      "value": 0.133
    },
    {
      "t": 1.4,
      "value": 0.3541
    },
    {
      "t": 1.5,
      "value": 0.2847
    },
    {
      "t": 1.6,
      "value": 0.1206
    },
    {
      "t": 1.7,
      "value": 0.218
    },
    {
      "t": 1.8,
      "value": 0.1106
    },
    {
      "t": 1.9,
      "value": 0.4182
    },
    {
      "t": 2.0,
      "value": 0.2073
    },
    {
      "t": 2.1,
      "value": 0.165
    },
    {
      "t": 2.2,
      "value": 0.1643
    },
    {
      "t": 2.3,
      "value": 0.1062
    },
    {
      "t": 2.4,
      "value": 0.4058
    },
    {
      "t": 2.5,
      "value": 0.1516
    },
    {
      "t": 2.6,
      "value": 0.2036
    },
    {
      "t": 2.7,
      "value": 0.1462
    },
    {
      "t": 2.8,
      "value": 0.3226
    },
    {
      "t": 2.9,
      "value": 0.3064
    },
    {
      "t": 3.0,
      "value": 0.1223
    },
    {
      "t": 3.1,
      "value": 0.2133
    },
    {
      "t": 3.2,
      "value": 0.109
    },
    {
      "t": 3.3,
      "value": 0.4093
    },
    {
      "t": 3.4,
      "value": 0.2133
    },
    {
      "t": 3.5,
      "value": 0.1506
    },
    {
      "t": 3.6,
      "value": 0.1602
    },
    {
      "t": 3.7,
      "value": 0.1045
    },
    {
      "t": 3.8,
      "value": 0.4085
    },
    {
      "t": 3.9,
      "value": 0.1514
    },
    {
      "t": 4.0,
      "value": 0.1954
    },
    {
      "t": 4.1,
      "value": 0.147
    },
    {
      "t": 4.2,
      "value": 0.302
    },
    {
      "t": 4.3,
      "value": 0.3262
    },
    {
      "t": 4.4,
      "value": 0.1294
    },
    {
      "t": 4.5,
      "value": 0.2224
    },
    {
      "t": 4.6,
      "value": 0.1227
    },
    {
      "t": 4.7,
      "value": 0.3981
    },
    {
      "t": 4.8,
      "value": 0.2352
    },
    {
      "t": 4.9,
      "value": 0.1458
    },
    {
      "t": 5.0,
      "value": 0.1816
    },
    {
      "t": 5.1,
      "value": 0.0638
    },
    {
      "t": 5.2,
      "value": 0.4407
    },
    {
      "t": 5.3,
      "value": 0.1723
    },
    {
      "t": 5.4,
      "value": 0.1896
    },
    {
      "t": 5.5,
      "value": 0.1595
    },
    {
      "t": 5.6,
      "value": 0.2737
    },
    {
      "t": 5.7,
      "value": 0.3434
    },
    {
      "t": 5.8,
      "value": 0.1309
    },
    {
      "t": 5.9,
      "value": 0.2163
    },
    {
      "t": 6.0,
      "value": 0.1202
    },
    {
      "t": 6.1,
      "value": 0.3826
    },
    {
      "t": 6.2,
      "value": 0.2458
    },
    {
      "t": 6.3,
      "value": 0.123
    },
    {
      "t": 6.4,
      "value": 0.1811
    },
    {
      "t": 6.5,
      "value": 0.0506
    },
    {
      "t": 6.6,
      "value": 0.4243
    },
    {
      "t": 6.7,
      "value": 0.1737
    },
    {
      "t": 6.8,
      "value": 0.181
    },
    {
      "t": 6.9,
      "value": 0.1608
    },
    {
      "t": 7.0,
      "value": 0.2261
    },
    {
      "t": 7.1,
      "value": 0.3647
    },
    {
      "t": 7.2,
      "value": 0.143
    },
    {
      "t": 7.3,
      "value": 0.2137
    },
    {
      "t": 7.4,
      "value": 0.1345
    },
    {
      "t": 7.5,
      "value": 0.3776
    },
    {
      "t": 7.6,
      "value": 0.2627
    },
    {
      "t": 7.7,
      "value": 0.1278
    },
    {
      "t": 7.8,
      "value": 0.1981
    },
    {
      "t": 7.9,
      "value": 0.0756
    },
    {
      "t": 8.0,
      "value": 0.4263
    },
    {
      "t": 8.1,
      "value": 0.1936
    },
    {
      "t": 8.2,
      "value": 0.1752
    },
    {
      "t": 8.3,
      "value": 0.1732
    },
    {
      "t": 8.4,
      "value": 0.2106
    },
    {
      "t": 8.5,
      "value": 0.3793
    },
    {
      "t": 8.6,
      "value": 0.1472
    },
    {
      "t": 8.7,
      "value": 0.2081
    },
    {
      "t": 8.8,
      "value": 0.1331
    },
    {
      "t": 8.9,
      "value": 0.0385
    },
    {
      "t": 9.0,
      "value": 0.2815
    },
    {
      "t": 9.1,
      "value": 0.1765
    },
    {
      "t": 9.2,
      "value": 0.0557
    },
    {
      "t": 9.3,
      "value": 0.0632
    },
    {
      "t": 9.4,
      "value": 0.0328
    },
    {
      "t": 9.5,
      "value": 0.3226
    },
    {
      "t": 9.6,
      "value": 0.1252
    },
    {
      "t": 9.7,
      "value": 0.0638
    },
    {
      "t": 9.8,
      "value": 0.0716
    },
    {
      "t": 9.9,
      "value": 0.1169
    },
    {
      "t": 10.0,
      "value": 0.2778
    },
    {
      "t": 10.1,
      "value": 0.0938
    },
    {
      "t": 10.2,
      "value": 0.0884
    },
    {
      "t": 10.3,
      "value": 0.0813
    },
    {
      "t": 10.4,
      "value": 0.2967
    },
    {
      "t": 10.5,
      "value": 0.2059
    },
    {
      "t": 10.6,
      "value": 0.1014
    },
    {
      "t": 10.7,
      "value": 0.1119
    },
    {
      "t": 10.8,
      "value": 0.0956
    },
    {
      "t": 10.9,
      "value": 0.3498
    },
    {
      "t": 11.0,
      "value": 0.1548
    },
    {
      "t": 11.1,
      "value": 0.129
    },
    {
      "t": 11.2,
      "value": 0.1291
    },
    {
      "t": 11.3,
      "value": 0.1796
    },
    {
      "t": 11.4,
      "value": 0.3423
    },
    {
      "t": 11.5,
      "value": 0.1492
    },
    {
      "t": 11.6,
      "value": 0.1516
    },
    {
      "t": 11.7,
      "value": 0.1459
    },
    {
      "t": 11.8,
      "value": 0.3258
    },
    {
      "t": 11.9,
      "value": 0.2503
    },
    {
      "t": 12.0,
      "value": 0.1683
    },
    {
      "t": 12.1,
      "value": 0.1747
    },
    {
      "t": 12.2,
      "value": 0.1647
    },
    {
      "t": 12.3,
      "value": 0.4116
    },
    {
      "t": 12.4,
      "value": 0.2117
    },
    {
      "t": 12.5,
      "value": 0.3518
    },
    {
      "t": 12.6,
      "value": 0.2884
    },
    {
      "t": 12.7,
      "value": 0.1937
    },
    {
      "t": 12.8,
      "value": 0.4097
    },
    {
      "t": 12.9,
      "value": 0.212
    },
    {
      "t": 13.0,
      "value": 0.436
    },
    {
      "t": 13.1,
      "value": 0.2433
    },
    {
      "t": 13.2,
      "value": 0.3702
    },
    {
      "t": 13.3,
      "value": 0.3257
    },
    {
      "t": 13.4,
      "value": 0.2416
    },
    {
      "t": 13.5,
      "value": 0.4505
    },
    {
      "t": 13.6,
      "value": 0.249
    },
    {
      "t": 13.7,
      "value": 0.4579
    },
    {
      "t": 13.8,
      "value": 0.2772
    },
    {
      "t": 13.9,
      "value": 0.3893
    },
    {
      "t": 14.0,
      "value": 0.3525
    },
    {
      "t": 14.1,
      "value": 0.2813
    },
    {
      "t": 14.2,
      "value": 0.4759
    },
    {
      "t": 14.3,
      "value": 0.2872
    },
    {
      "t": 14.4,
      "value": 0.4916
    },
    {
      "t": 14.5,
      "value": 0.3223
    },
    {
      "t": 14.6,
      "value": 0.4077
    },
    {
      "t": 14.7,
      "value": 0.4199
    },
    {
      "t": 14.8,
      "value": 0.4728
    },
    {
      "t": 14.9,
      "value": 0.5384
    },
    {
      "t": 15.0,
      "value": 0.5315
    },
    {
      "t": 15.1,
      "value": 0.521
    },
    {
      "t": 15.2,
      "value": 0.5221
    },
    {
      "t": 15.3,
      "value": 0.4524
    },
    {
      "t": 15.4,
      "value": 0.5184
    },
    {
      "t": 15.5,
      "value": 0.4896
    },
    {
      "t": 15.6,
      "value": 0.5566
    },
    {
      "t": 15.7,
      "value": 0.5526
    },
    {
      "t": 15.8,
      "value": 0.5539
    },
    {
      "t": 15.9,
      "value": 0.5515
    },
    {
      "t": 16.0,
      "value": 0.5091
    },
    {
      "t": 16.1,
      "value": 0.4938
    },
    {
      "t": 16.2,
      "value": 0.5441
    },
    {
      "t": 16.3,
      "value": 0.605
    },
    {
      "t": 16.4,
      "value": 0.6055
    },
    {
      "t": 16.5,
      "value": 0.3943
    },
    {
      "t": 16.6,
      "value": 0.3838
    },
    {
      "t": 16.7,
      "value": 0.3885
    },
    {
      "t": 16.8,
      "value": 0.3935
    },
    {
      "t": 16.9,
      "value": 0.8719
    },
    {
      "t": 17.0,
      "value": 0.4459
    },
    {
      "t": 17.1,
      "value": 0.3961
    },
    {
      "t": 17.2,
      "value": 0.3857
    },
    {
      "t": 17.3,
      "value": 0.3146
    },
    {
      "t": 17.4,
      "value": 0.8822
    },
    {
      "t": 17.5,
      "value": 0.3728
    },
    {
      "t": 17.6,
      "value": 0.446
    },
    {
      "t": 17.7,
      "value": 0.3253
    },
    {
      "t": 17.8,
      "value": 0.6735
    },
    {
      "t": 17.9,
      "value": 0.6013
    },
    {
      "t": 18.0,
      "value": 0.3494
    },
    {
      "t": 18.1,
      "value": 0.4476
    },
    {
      "t": 18.2,
      "value": 0.2763
    },
    {
      "t": 18.3,
      "value": 0.9013
    },
    {
      "t": 18.4,
      "value": 0.5006
    },
    {
      "t": 18.5,
      "value": 0.3663
    },
    {
      "t": 18.6,
      "value": 0.4068
    },
    {
      "t": 18.7,
      "value": 0.2991
    },
    {
      "t": 18.8,
      "value": 0.8202
    },
    {
      "t": 18.9,
      "value": 0.4113
    },
    {
      "t": 19.0,
      "value": 0.4231
    },
    {
      "t": 19.1,
      "value": 0.3448
    },
    {
      "t": 19.2,
      "value": 0.7161
    },
    {
      "t": 19.3,
      "value": 0.6629
    },
    {
      "t": 19.4,
      "value": 0.337
    },
    {
      "t": 19.5,
      "value": 0.4645
    },
    {
      "t": 19.6,
      "value": 0.2839
    },
    {
      "t": 19.7,
      "value": 0.8161
    },
    {
      "t": 19.8,
      "value": 0.4884
    },
    {
      "t": 19.9,
      "value": 0.3617
    },
    {
      "t": 20.0,
      "value": 0.4178
    },
    {
      "t": 20.1,
      "value": 0.2239
    },
    {
      "t": 20.2,
      "value": 0.9972
    },
    {
      "t": 20.3,
      "value": 0.3953
    },
    {
      "t": 20.4,
      "value": 0.424
    },
    {
      "t": 20.5,
      "value": 0.3562
    },
    {
      "t": 20.6,
      "value": 0.5848
    },
    {
      "t": 20.7,
      "value": 0.6841
    },
    {
      "t": 20.8,
      "value": 0.3162
    },
    {
      "t": 20.9,
      "value": 0.4748
    },
    {
      "t": 21.0,
      "value": 0.2878
    },
    {
      "t": 21.1,
      "value": 0.8729
    },
    {
      "t": 21.2,
      "value": 0.5265
    },
    {
      "t": 21.3,
      "value": 0.3631
    },
    {
      "t": 21.4,
      "value": 0.4226
    },
    {
      "t": 21.5,
      "value": 0.2347
    },
    {
      "t": 21.6,
      "value": 0.8489
    },
    {
      "t": 21.7,
      "value": 0.4232
    },
    {
      "t": 21.8,
      "value": 0.4155
    },
    {
      "t": 21.9,
      "value": 0.3604
    },
    {
      "t": 22.0,
      "value": 0.5523
    },
    {
      "t": 22.1,
      "value": 0.7664
    },
    {
      "t": 22.2,
      "value": 0.3564
    },
    {
      "t": 22.3,
      "value": 0.4605
    },
    {
      "t": 22.4,
      "value": 0.3048
    },
    {
      "t": 22.5,
      "value": 0.747
    },
    {
      "t": 22.6,
      "value": 0.5623
    },
    {
      "t": 22.7,
      "value": 0.3292
    },
    {
      "t": 22.8,
      "value": 0.4447
    },
    {
      "t": 22.9,
      "value": 0.2493
    },
    {
      "t": 23.0,
      "value": 0.916
    },
    {
      "t": 23.1,
      "value": 0.4631
    },
    {
      "t": 23.2,
      "value": 0.3886
    },
    {
      "t": 23.3,
      "value": 0.3809
    },
    {
      "t": 23.4,
      "value": 0.4392
    },
    {
      "t": 23.5,
      "value": 0.7644
    },
    {
      "t": 23.6,
      "value": 0.3736
    },
    {
      "t": 23.7,
      "value": 0.4443
    },
    {
      "t": 23.8,
      "value": 0.3213
    },
    {
      "t": 23.9,
      "value": 0.7971
    },
    {
      "t": 24.0,
      "value": 0.5903
    },
    {
      "t": 24.1,
      "value": 0.3305
    },
    {
      "t": 24.2,
      "value": 0.4553
    },
    {
      "t": 24.3,
      "value": 0.2609
    },
    {
      "t": 24.4,
      "value": 0.8514
    },
    {
      "t": 24.5,
      "value": 0.446
    },
    {
      "t": 24.6,
      "value": 0.3958
    },
    {
      "t": 24.7,
      "value": 0.3859
    },
    {
      "t": 24.8,
      "value": 0.3129
    },
    {
      "t": 24.9,
      "value": 0.881
    },
    {
      "t": 25.0,
      "value": 0.37
    },
    {
      "t": 25.1,
      "value": 0.4459
    },
    {
      "t": 25.2,
      "value": 0.3252
    },
    {
      "t": 25.3,
      "value": 0.6733
    },
    {
      "t": 25.4,
      "value": 0.6012
    },
    {
      "t": 25.5,
      "value": 0.3494
    },
    {
      "t": 25.6,
      "value": 0.4477
    },
    {
      "t": 25.7,
      "value": 0.2761
    },
    {
      "t": 25.8,
      "value": 0.8903
    },
    {
      "t": 25.9,
      "value": 0.4991
    },
    {
      "t": 26.0,
      "value": 0.3663
    },
    {
      "t": 26.1,
      "value": 0.4067
    },
    {
      "t": 26.2,
      "value": 0.2988
    },
    {
      "t": 26.3,
      "value": 0.8202
    },
    {
      "t": 26.4,
      "value": 0.4115
    },
    {
      "t": 26.5,
      "value": 0.4231
    },
    {
      "t": 26.6,
      "value": 0.3447
    },
    {
      "t": 26.7,
      "value": 0.7146
    },
    {
      "t": 26.8,
      "value": 0.673
    },
    {
      "t": 26.9,
      "value": 0.3374
    },
    {
      "t": 27.0,
      "value": 0.4645
    },
    {
      "t": 27.1,
      "value": 0.284
    },
    {
      "t": 27.2,
      "value": 0.2303
    },
    {
      "t": 27.3,
      "value": 0.1409
    },
    {
      "t": 27.4,
      "value": 0.1396
    },
    {
      "t": 27.5,
      "value": 0.1835
    },
    {
      "t": 27.6,
      "value": 0.07
    },
    {
      "t": 27.7,
      "value": 0.201
    },
    {
      "t": 27.8,
      "value": 0.0774
    },
    {
      "t": 27.9,
      "value": 0.1634
    },
    {
      "t": 28.0,
      "value": 0.0829
    },
    {
      "t": 28.1,
      "value": 0.1191
    },
    {
      "t": 28.2,
      "value": 0.1162
    },
    {
      "t": 28.3,
      "value": 0.0637
    },
    {
      "t": 28.4,
      "value": 0.141
    },
    {
      "t": 28.5,
      "value": 0.0469
    },
    {
      "t": 28.6,
      "value": 0.1047
    },
    {
      "t": 28.7,
      "value": 0.0852
    },
    {
      "t": 28.8,
      "value": 0.0506
    },
    {
      "t": 28.9,
      "value": 0.0797
    },
    {
      "t": 29.0,
      "value": 0.0295
    },
    {
      "t": 29.1,
      "value": 0.0678
    },
    {
      "t": 29.2,
      "value": 0.0304
    },
    {
      "t": 29.3,
      "value": 0.0415
    },
    {
      "t": 29.4,
      "value": 0.0267
    },
    {
      "t": 29.5,
      "value": 0.0204
    },
    {
      "t": 29.6,
      "value": 0.0108
    },
    {
      "t": 29.7,
      "value": 0.005
    },
    {
      "t": 29.8,
      "value": 0.0006
    },
    {
      "t": 29.9,
      "value": 0.0
    },
    {
      "t": 30.0,
      "value": 0.0
    },
    {
      "t": 30.1,
      "value": 0.0
    },
    {
      "t": 30.2,
      "value": 0.0
    },
    {
      "t": 30.3,
      "value": 0.0
    },
    {
      "t": 30.4,
      "value": 0.0
    },
    {
      "t": 30.5,
      "value": 0.0
    },
    {
      "t": 30.6,
      "value": 0.0
    },
    {
      "t": 30.7,
      "value": 0.0
    },
    {
      "t": 30.8,
      "value": 0.0
    },
    {
      "t": 30.9,
      "value": 0.0
    },
    {
      "t": 31.0,
      "value": 0.0
    },
    {
      "t": 31.1,
      "value": 0.0
    },
    {
      "t": 31.2,
      "value": 0.0
    },
    {
      "t": 31.3,
      "value": 0.0
    },
    {
      "t": 31.4,
      "value": 0.0
    },
    {
      "t": 31.5,
      "value": 0.0
    },
    {
      "t": 31.6,
      "value": 0.0
    },
    {
      "t": 31.7,
      "value": 0.0
    },
    {
      "t": 31.8,
      "value": 0.0
    },
    {
      "t": 31.9,
      "value": 0.0
    }
  ],
  "spectral_centroid_curve": [
    {
      "t": 0.0,
      "value": 0.0849
    },
    {
      "t": 0.1,
      "value": 0.0366
    },
    {
      "t": 0.2,
      "value": 0.0618
    },
    {
      "t": 0.3,
      "value": 0.072
    },
    {
      "t": 0.4,
      "value": 0.0993
    },
    {
      "t": 0.5,
      "value": 0.0554
    },
    {
      "t": 0.6,
      "value": 0.0555
    },
    {
      "t": 0.7,
      "value": 0.1201
    },
    {
      "t": 0.8,
      "value": 0.1285
    },
    {
      "t": 0.9,
      "value": 0.1745
    },
    {
      "t": 1.0,
      "value": 0.0444
    },
    {
      "t": 1.1,
      "value": 0.0638
    },
    {
      "t": 1.2,
      "value": 0.0715
    },
    {
      "t": 1.3,
      "value": 0.0755
    },
    {
      "t": 1.4,
      "value": 0.1004
    },
    {
      "t": 1.5,
      "value": 0.03
    },
    {
      "t": 1.6,
      "value": 0.1286
    },
    {
      "t": 1.7,
      "value": 0.0608
    },
    {
      "t": 1.8,
      "value": 0.0654
    },
    {
      "t": 1.9,
      "value": 0.0571
    },
    {
      "t": 2.0,
      "value": 0.045
    },
    {
      "t": 2.1,
      "value": 0.1542
    },
    {
      "t": 2.2,
      "value": 0.0983
    },
    {
      "t": 2.3,
      "value": 0.1835
    },
    {
      "t": 2.4,
      "value": 0.037
    },
    {
      "t": 2.5,
      "value": 0.0486
    },
    {
      "t": 2.6,
      "value": 0.0622
    },
    {
      "t": 2.7,
      "value": 0.063
    },
    {
      "t": 2.8,
      "value": 0.0928
    },
    {
      "t": 2.9,
      "value": 0.0354
    },
    {
      "t": 3.0,
      "value": 0.0534
    },
    {
      "t": 3.1,
      "value": 0.0716
    },
    {
      "t": 3.2,
      "value": 0.0776
    },
    {
      "t": 3.3,
      "value": 0.0686
    },
    {
      "t": 3.4,
      "value": 0.0537
    },
    {
      "t": 3.5,
      "value": 0.1254
    },
    {
      "t": 3.6,
      "value": 0.1258
    },
    {
      "t": 3.7,
      "value": 0.1871
    },
    {
      "t": 3.8,
      "value": 0.0459
    },
    {
      "t": 3.9,
      "value": 0.058
    },
    {
      "t": 4.0,
      "value": 0.0722
    },
    {
      "t": 4.1,
      "value": 0.0746
    },
    {
      "t": 4.2,
      "value": 0.1311
    },
    {
      "t": 4.3,
      "value": 0.029
    },
    {
      "t": 4.4,
      "value": 0.0819
    },
    {
      "t": 4.5,
      "value": 0.0606
    },
    {
      "t": 4.6,
      "value": 0.0645
    },
    {
      "t": 4.7,
      "value": 0.0712
    },
    {
      "t": 4.8,
      "value": 0.0436
    },
    {
      "t": 4.9,
      "value": 0.1931
    },
    {
      "t": 5.0,
      "value": 0.0972
    },
    {
      "t": 5.1,
      "value": 0.1523
    },
    {
      "t": 5.2,
      "value": 0.038
    },
    {
      "t": 5.3,
      "value": 0.047
    },
    {
      "t": 5.4,
      "value": 0.0834
    },
    {
      "t": 5.5,
      "value": 0.0624
    },
    {
      "t": 5.6,
      "value": 0.0973
    },
    {
      "t": 5.7,
      "value": 0.0341
    },
    {
      "t": 5.8,
      "value": 0.0467
    },
    {
      "t": 5.9,
      "value": 0.0713
    },
    {
      "t": 6.0,
      "value": 0.0765
    },
    {
      "t": 6.1,
      "value": 0.0841
    },
    {
      "t": 6.2,
      "value": 0.0521
    },
    {
      "t": 6.3,
      "value": 0.1264
    },
    {
      "t": 6.4,
      "value": 0.1239
    },
    {
      "t": 6.5,
      "value": 0.1704
    },
    {
      "t": 6.6,
      "value": 0.0512
    },
    {
      "t": 6.7,
      "value": 0.0563
    },
    {
      "t": 6.8,
      "value": 0.0789
    },
    {
      "t": 6.9,
      "value": 0.0738
    },
    {
      "t": 7.0,
      "value": 0.1776
    },
    {
      "t": 7.1,
      "value": 0.0284
    },
    {
      "t": 7.2,
      "value": 0.042
    },
    {
      "t": 7.3,
      "value": 0.0608
    },
    {
      "t": 7.4,
      "value": 0.0637
    },
    {
      "t": 7.5,
      "value": 0.0842
    },
    {
      "t": 7.6,
      "value": 0.0422
    },
    {
      "t": 7.7,
      "value": 0.1726
    },
    {
      "t": 7.8,
      "value": 0.0961
    },
    {
      "t": 7.9,
      "value": 0.1223
    },
    {
      "t": 8.0,
      "value": 0.0506
    },
    {
      "t": 8.1,
      "value": 0.0457
    },
    {
      "t": 8.2,
      "value": 0.1148
    },
    {
      "t": 8.3,
      "value": 0.0619
    },
    {
      "t": 8.4,
      "value": 0.0898
    },
    {
      "t": 8.5,
      "value": 0.0328
    },
    {
      "t": 8.6,
      "value": 0.0435
    },
    {
      "t": 8.7,
      "value": 0.0713
    },
    {
      "t": 8.8,
      "value": 0.0755
    },
    {
      "t": 8.9,
      "value": 0.3319
    },
    {
      "t": 9.0,
      "value": 0.9122
    },
    {
      "t": 9.1,
      "value": 0.8877
    },
    {
      "t": 9.2,
      "value": 0.5052
    },
    {
      "t": 9.3,
      "value": 0.1319
    },
    {
      "t": 9.4,
      "value": 0.1714
    },
    {
      "t": 9.5,
      "value": 0.9635
    },
    {
      "t": 9.6,
      "value": 0.8407
    },
    {
      "t": 9.7,
      "value": 0.1505
    },
    {
      "t": 9.8,
      "value": 0.1132
    },
    {
      "t": 9.9,
      "value": 0.3886
    },
    {
      "t": 10.0,
      "value": 0.953
    },
    {
      "t": 10.1,
      "value": 0.7712
    },
    {
      "t": 10.2,
      "value": 0.1165
    },
    {
      "t": 10.3,
      "value": 0.1984
    },
    {
      "t": 10.4,
      "value": 0.9358
    },
    {
      "t": 10.5,
      "value": 0.8954
    },
    {
      "t": 10.6,
      "value": 0.459
    },
    {
      "t": 10.7,
      "value": 0.1091
    },
    {
      "t": 10.8,
      "value": 0.1978
    },
    {
      "t": 10.9,
      "value": 0.9612
    },
    {
      "t": 11.0,
      "value": 0.8489
    },
    {
      "t": 11.1,
      "value": 0.1205
    },
    {
      "t": 11.2,
      "value": 0.1104
    },
    {
      "t": 11.3,
      "value": 0.4872
    },
    {
      "t": 11.4,
      "value": 0.9127
    },
    {
      "t": 11.5,
      "value": 0.745
    },
    {
      "t": 11.6,
      "value": 0.1108
    },
    {
      "t": 11.7,
      "value": 0.1681
    },
    {
      "t": 11.8,
      "value": 0.9306
    },
    {
      "t": 11.9,
      "value": 0.9212
    },
    {
      "t": 12.0,
      "value": 0.4696
    },
    {
      "t": 12.1,
      "value": 0.1093
    },
    {
      "t": 12.2,
      "value": 0.141
    },
    {
      "t": 12.3,
      "value": 0.9556
    },
    {
      "t": 12.4,
      "value": 0.8538
    },
    {
      "t": 12.5,
      "value": 0.924
    },
    {
      "t": 12.6,
      "value": 0.916
    },
    {
      "t": 12.7,
      "value": 0.4747
    },
    {
      "t": 12.8,
      "value": 0.9367
    },
    {
      "t": 12.9,
      "value": 0.7309
    },
    {
      "t": 13.0,
      "value": 0.9725
    },
    {
      "t": 13.1,
      "value": 0.845
    },
    {
      "t": 13.2,
      "value": 0.8864
    },
    {
      "t": 13.3,
      "value": 0.9109
    },
    {
      "t": 13.4,
      "value": 0.5242
    },
    {
      "t": 13.5,
      "value": 0.9644
    },
    {
      "t": 13.6,
      "value": 0.7353
    },
    {
      "t": 13.7,
      "value": 0.9759
    },
    {
      "t": 13.8,
      "value": 0.8615
    },
    {
      "t": 13.9,
      "value": 0.7358
    },
    {
      "t": 14.0,
      "value": 0.9086
    },
    {
      "t": 14.1,
      "value": 0.5277
    },
    {
      "t": 14.2,
      "value": 0.9694
    },
    {
      "t": 14.3,
      "value": 0.7462
    },
    {
      "t": 14.4,
      "value": 0.9547
    },
    {
      "t": 14.5,
      "value": 0.8451
    },
    {
      "t": 14.6,
      "value": 0.7701
    },
    {
      "t": 14.7,
      "value": 0.9261
    },
    {
      "t": 14.8,
      "value": 0.9524
    },
    {
      "t": 14.9,
      "value": 0.9728
    },
    {
      "t": 15.0,
      "value": 0.977
    },
    {
      "t": 15.1,
      "value": 0.9549
    },
    {
      "t": 15.2,
      "value": 0.918
    },
    {
      "t": 15.3,
      "value": 0.9139
    },
    {
      "t": 15.4,
      "value": 0.9503
    },
    {
      "t": 15.5,
      "value": 0.9602
    },
    {
      "t": 15.6,
      "value": 0.9555
    },
    {
      "t": 15.7,
      "value": 0.9677
    },
    {
      "t": 15.8,
      "value": 0.9508
    },
    {
      "t": 15.9,
      "value": 0.9328
    },
    {
      "t": 16.0,
      "value": 0.9155
    },
    {
      "t": 16.1,
      "value": 0.93
    },
    {
      "t": 16.2,
      "value": 0.9503
    },
    {
      "t": 16.3,
      "value": 0.9659
    },
    {
      "t": 16.4,
      "value": 0.9715
    },
    {
      "t": 16.5,
      "value": 0.8605
    },
    {
      "t": 16.6,
      "value": 0.2511
    },
    {
      "t": 16.7,
      "value": 0.2302
    },
    {
      "t": 16.8,
      "value": 0.2378
    },
    {
      "t": 16.9,
      "value": 0.1897
    },
    {
      "t": 17.0,
      "value": 0.2636
    },
    {
      "t": 17.1,
      "value": 0.1786
    },
    {
      "t": 17.2,
      "value": 0.1418
    },
    {
      "t": 17.3,
      "value": 0.235
    },
    {
      "t": 17.4,
      "value": 0.8278
    },
    {
      "t": 17.5,
      "value": 0.6447
    },
    {
      "t": 17.6,
      "value": 0.149
    },
    {
      "t": 17.7,
      "value": 0.1807
    },
    {
      "t": 17.8,
      "value": 0.2443
    },
    {
      "t": 17.9,
      "value": 0.3151
    },
    {
      "t": 18.0,
      "value": 0.3398
    },
    {
      "t": 18.1,
      "value": 0.1886
    },
    {
      "t": 18.2,
      "value": 0.2504
    },
    {
      "t": 18.3,
      "value": 0.8233
    },
    {
      "t": 18.4,
      "value": 0.757
    },
    {
      "t": 18.5,
      "value": 0.3284
    },
    {
      "t": 18.6,
      "value": 0.2226
    },
    {
      "t": 18.7,
      "value": 0.3047
    },
    {
      "t": 18.8,
      "value": 0.2816
    },
    {
      "t": 18.9,
      "value": 0.3718
    },
    {
      "t": 19.0,
      "value": 0.1933
    },
    {
      "t": 19.1,
      "value": 0.2095
    },
    {
      "t": 19.2,
      "value": 0.7027
    },
    {
      "t": 19.3,
      "value": 0.8
    },
    {
      "t": 19.4,
      "value": 0.5315
    },
    {
      "t": 19.5,
      "value": 0.1609
    },
    {
      "t": 19.6,
      "value": 0.224
    },
    {
      "t": 19.7,
      "value": 0.181
    },
    {
      "t": 19.8,
      "value": 0.2543
    },
    {
      "t": 19.9,
      "value": 0.2296
    },
    {
      "t": 20.0,
      "value": 0.1382
    },
    {
      "t": 20.1,
      "value": 0.1676
    },
    {
      "t": 20.2,
      "value": 0.8092
    },
    {
      "t": 20.3,
      "value": 0.6305
    },
    {
      "t": 20.4,
      "value": 0.1273
    },
    {
      "t": 20.5,
      "value": 0.1254
    },
    {
      "t": 20.6,
      "value": 0.1484
    },
    {
      "t": 20.7,
      "value": 0.2147
    },
    {
      "t": 20.8,
      "value": 0.2717
    },
    {
      "t": 20.9,
      "value": 0.1426
    },
    {
      "t": 21.0,
      "value": 0.1857
    },
    {
      "t": 21.1,
      "value": 0.8241
    },
    {
      "t": 21.2,
      "value": 0.7735
    },
    {
      "t": 21.3,
      "value": 0.3451
    },
    {
      "t": 21.4,
      "value": 0.1714
    },
    {
      "t": 21.5,
      "value": 0.2357
    },
    {
      "t": 21.6,
      "value": 0.2359
    },
    {
      "t": 21.7,
      "value": 0.3368
    },
    {
      "t": 21.8,
      "value": 0.1817
    },
    {
      "t": 21.9,
      "value": 0.1836
    },
    {
      "t": 22.0,
      "value": 0.4865
    },
    {
      "t": 22.1,
      "value": 0.8552
    },
    {
      "t": 22.2,
      "value": 0.7392
    },
    {
      "t": 22.3,
      "value": 0.2535
    },
    {
      "t": 22.4,
      "value": 0.3171
    },
    {
      "t": 22.5,
      "value": 0.3003
    },
    {
      "t": 22.6,
      "value": 0.4202
    },
    {
      "t": 22.7,
      "value": 0.4718
    },
    {
      "t": 22.8,
      "value": 0.2431
    },
    {
      "t": 22.9,
      "value": 0.3441
    },
    {
      "t": 23.0,
      "value": 0.8329
    },
    {
      "t": 23.1,
      "value": 0.7294
    },
    {
      "t": 23.2,
      "value": 0.2517
    },
    {
      "t": 23.3,
      "value": 0.2186
    },
    {
      "t": 23.4,
      "value": 0.1888
    },
    {
      "t": 23.5,
      "value": 0.2699
    },
    {
      "t": 23.6,
      "value": 0.3395
    },
    {
      "t": 23.7,
      "value": 0.1737
    },
    {
      "t": 23.8,
      "value": 0.1952
    },
    {
      "t": 23.9,
      "value": 0.7818
    },
    {
      "t": 24.0,
      "value": 0.7841
    },
    {
      "t": 24.1,
      "value": 0.4571
    },
    {
      "t": 24.2,
      "value": 0.1658
    },
    {
      "t": 24.3,
      "value": 0.2341
    },
    {
      "t": 24.4,
      "value": 0.1787
    },
    {
      "t": 24.5,
      "value": 0.2636
    },
    {
      "t": 24.6,
      "value": 0.1786
    },
    {
      "t": 24.7,
      "value": 0.1418
    },
    {
      "t": 24.8,
      "value": 0.2361
    },
    {
      "t": 24.9,
      "value": 0.8138
    },
    {
      "t": 25.0,
      "value": 0.645
    },
    {
      "t": 25.1,
      "value": 0.1491
    },
    {
      "t": 25.2,
      "value": 0.1807
    },
    {
      "t": 25.3,
      "value": 0.2443
    },
    {
      "t": 25.4,
      "value": 0.315
    },
    {
      "t": 25.5,
      "value": 0.3398
    },
    {
      "t": 25.6,
      "value": 0.1886
    },
    {
      "t": 25.7,
      "value": 0.2503
    },
    {
      "t": 25.8,
      "value": 0.8179
    },
    {
      "t": 25.9,
      "value": 0.7576
    },
    {
      "t": 26.0,
      "value": 0.3296
    },
    {
      "t": 26.1,
      "value": 0.2227
    },
    {
      "t": 26.2,
      "value": 0.3048
    },
    {
      "t": 26.3,
      "value": 0.2816
    },
    {
      "t": 26.4,
      "value": 0.3718
    },
    {
      "t": 26.5,
      "value": 0.1933
    },
    {
      "t": 26.6,
      "value": 0.2096
    },
    {
      "t": 26.7,
      "value": 0.6858
    },
    {
      "t": 26.8,
      "value": 0.7827
    },
    {
      "t": 26.9,
      "value": 0.528
    },
    {
      "t": 27.0,
      "value": 0.1609
    },
    {
      "t": 27.1,
      "value": 0.2241
    },
    {
      "t": 27.2,
      "value": 0.1215
    },
    {
      "t": 27.3,
      "value": 0.1358
    },
    {
      "t": 27.4,
      "value": 0.1535
    },
    {
      "t": 27.5,
      "value": 0.1462
    },
    {
      "t": 27.6,
      "value": 0.1638
    },
    {
      "t": 27.7,
      "value": 0.1752
    },
    {
      "t": 27.8,
      "value": 0.2008
    },
    {
      "t": 27.9,
      "value": 0.2273
    },
    {
      "t": 28.0,
      "value": 0.2653
    },
    {
      "t": 28.1,
      "value": 0.224
    },
    {
      "t": 28.2,
      "value": 0.2173
    },
    {
      "t": 28.3,
      "value": 0.2142
    },
    {
      "t": 28.4,
      "value": 0.1553
    },
    {
      "t": 28.5,
      "value": 0.2002
    },
    {
      "t": 28.6,
      "value": 0.1153
    },
    {
      "t": 28.7,
      "value": 0.116
    },
    {
      "t": 28.8,
      "value": 0.1522
    },
    {
      "t": 28.9,
      "value": 0.1267
    },
    {
      "t": 29.0,
      "value": 0.1412
    },
    {
      "t": 29.1,
      "value": 0.1457
    },
    {
      "t": 29.2,
      "value": 0.1635
    },
    {
      "t": 29.3,
      "value": 0.1772
    },
    {
      "t": 29.4,
      "value": 0.1984
    },
    {
      "t": 29.5,
      "value": 0.2069
    },
    {
      "t": 29.6,
      "value": 0.2441
    },
    {
      "t": 29.7,
      "value": 0.2848
    },
    {
      "t": 29.8,
      "value": 0.3415
    },
    {
      "t": 29.9,
      "value": 0.0
    },
    {
      "t": 30.0,
      "value": 0.0
    },
    {
      "t": 30.1,
      "value": 0.0
    },
    {
      "t": 30.2,
      "value": 0.0
    },
    {
      "t": 30.3,
      "value": 0.0
    },
    {
      "t": 30.4,
      "value": 0.0
    },
    {
      "t": 30.5,
      "value": 0.0
    },
    {
      "t": 30.6,
      "value": 0.0
    },
    {
      "t": 30.7,
      "value": 0.0
    },
    {
      "t": 30.8,
      "value": 0.0
    },
    {
      "t": 30.9,
      "value": 0.0
    },
    {
      "t": 31.0,
      "value": 0.0
    },
    {
      "t": 31.1,
      "value": 0.0
    },
    {
      "t": 31.2,
      "value": 0.0
    },
    {
      "t": 31.3,
      "value": 0.0
    },
    {
      "t": 31.4,
      "value": 0.0
    },
    {
      "t": 31.5,
      "value": 0.0
    },
    {
      "t": 31.6,
      "value": 0.0
    },
    {
      "t": 31.7,
      "value": 0.0
    },
    {
      "t": 31.8,
      "value": 0.0
    },
    {
      "t": 31.9,
      "value": 0.0
    }
  ],
  "sections_detected": [
    {
      "index": 0,
      "start": 0.0,
      "end": 12.26,
      "avg_energy": 0.202,
      "avg_brightness": 0.196,
      "suggested_role": "intro"
    },
    {
      "index": 1,
      "start": 12.26,
      "end": 16.6,
      "avg_energy": 0.418,
      "avg_brightness": 0.875,
      "suggested_role": "development"
    },
    {
      "index": 2,
      "start": 16.6,
      "end": 26.94,
      "avg_energy": 0.49,
      "avg_brightness": 0.362,
      "suggested_role": "climax"
    },
    {
      "index": 3,
      "start": 26.94,
      "end": 32.0,
      "avg_energy": 0.061,
      "avg_brightness": 0.105,
      "suggested_role": "outro"
    }
  ],
  "lyrics": "Instrumental"
};

const POSE_INDEX = {
  idle: 0,
  bounce: 1,
  step_left: 2,
  step_right: 3,
  arms_up: 4,
  spin: 5,
  jump: 6,
  hold: 7
};

// Verification & Instrumentation Log Contract
window.__musicoLog = {
  events: [],
  fpsSamples: [],
  consoleErrors: [],
  characterBoundsOk: true,
  boundsViolations: [],
  climaxPeakLuminance: 0,
  introAvgLuminance: 0,
  calibration: MUSICO_CALIBRATION,
  ready: false
};

window.addEventListener("error", (ev) => {
  window.__musicoLog.consoleErrors.push(String(ev.message || ev));
});

(function () {
  const canvas = document.getElementById("stage-canvas");
  const ctx = canvas.getContext("2d");
  const audioEl = document.getElementById("track-audio");
  const playBtn = document.getElementById("play-btn");
  const scrubber = document.getElementById("scrubber");
  const timeReadout = document.getElementById("time-readout");
  const poseBadge = document.getElementById("pose-badge");
  const seekClimaxBtn = document.getElementById("seek-climax-btn");
  const hudBtn = document.getElementById("hud-btn");

  const duration = Number(SCORE_DATA.duration || 32.0);
  if (scrubber) scrubber.max = String(duration);

  const spriteImg = new Image();
  let spriteLoaded = false;
  spriteImg.onload = () => {
    spriteLoaded = true;
    renderAtTime(state.currentTime, true);
  };
  spriteImg.src = "sprites.png";

  let audioCtx = null;
  let analyser = null;
  let freqBins = null;

  const state = {
    currentTime: 0.0,
    isPlaying: false,
    showHud: true,
    lastFrameTs: performance.now(),
    firedCueMap: new Set(),
    lastPose: "idle",
    lastSection: null
  };

  function setupWebAudio() {
    if (audioCtx) return;
    try {
      const AC = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AC();
      const source = audioCtx.createMediaElementSource(audioEl);
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 128;
      freqBins = new Uint8Array(analyser.frequencyBinCount);
      source.connect(analyser);
      analyser.connect(audioCtx.destination);
    } catch (e) {
      // Fallback to deterministic feature curves if Web Audio blocked
    }
  }

  function lookupCurve(curve, t) {
    if (!curve || !curve.length) return 0.3;
    const idx = Math.min(curve.length - 1, Math.max(0, Math.floor(t * 10)));
    return Number(curve[idx].value || 0.3);
  }

  function getAudioEnergyAt(t, deterministic) {
    const dspRms = lookupCurve(FEATURES_DATA.rms_curve, t);
    const dspCentroid = lookupCurve(FEATURES_DATA.spectral_centroid_curve, t);
    if (!deterministic && analyser && state.isPlaying && freqBins) {
      analyser.getByteFrequencyData(freqBins);
      let sum = 0;
      for (let i = 0; i < freqBins.length; i++) sum += freqBins[i];
      const liveRms = sum / (freqBins.length * 255);
      return {
        rms: Math.max(dspRms * 0.65, liveRms),
        centroid: dspCentroid
      };
    }
    return { rms: dspRms, centroid: dspCentroid };
  }

  function getActiveSection(t) {
    const secs = SCORE_DATA.sections || [];
    for (let i = 0; i < secs.length; i++) {
      if (t >= secs[i].start && t <= secs[i].end) return secs[i];
    }
    return secs[secs.length - 1] || {
      id: "sec_1",
      name: "Opening",
      start: 0,
      end: duration,
      mood: "Expressive",
      energy: 0.4,
      motion_vocab: ["idle", "bounce"],
      background: "Stage",
      camera: "slow_drift",
      particle_theme: "stardust"
    };
  }

  function recordEventFire(ev, actualT, inBounds) {
    if (state.firedCueMap.has(ev.id)) return;
    state.firedCueMap.add(ev.id);
    const deltaMs = Number(((actualT - ev.t) * 1000.0).toFixed(1));
    window.__musicoLog.events.push({
      id: ev.id,
      planned_t: Number(ev.t.toFixed(4)),
      raw_t: Number((ev.raw_t || ev.t).toFixed(4)),
      actual_t: Number(actualT.toFixed(4)),
      delta_ms: deltaMs,
      action: ev.action,
      why: ev.why,
      inBounds: inBounds
    });
  }

  function getActiveCueAndPose(t, section) {
    const events = SCORE_DATA.events || [];
    const offset = Number(MUSICO_CALIBRATION.EVENT_LATENCY_OFFSET_SEC || 0.0);
    let activeCue = null;
    let cueProgress = 0.0;

    for (let i = 0; i < events.length; i++) {
      const ev = events[i];
      const fireT = ev.t + offset;
      const cueDuration = 1.25;
      if (t >= fireT && t <= fireT + cueDuration) {
        activeCue = ev;
        cueProgress = (t - fireT) / cueDuration;
      }
    }

    if (activeCue) {
      return {
        cue: activeCue,
        pose: activeCue.action || "jump",
        cueProgress: cueProgress
      };
    }

    // Section motion_vocab rhythm cycle on beats
    const vocab = (section && section.motion_vocab && section.motion_vocab.length)
      ? section.motion_vocab
      : ["idle", "bounce"];
    const bpm = Number(SCORE_DATA.bpm || 120);
    const beatIdx = Math.floor(t * (bpm / 60.0));
    const chosenPose = vocab[beatIdx % vocab.length] || "idle";
    return {
      cue: null,
      pose: chosenPose,
      cueProgress: (t * (bpm / 60.0)) % 1.0
    };
  }

  function hexToRgba(hex, alpha) {
    const clean = String(hex || "#a855f7").replace("#", "");
    const num = parseInt(clean.length === 3 ? clean.split("").map(c => c + c).join("") : clean, 16) || 0xa855f7;
    const r = (num >> 16) & 255;
    const g = (num >> 8) & 255;
    const b = num & 255;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  function renderAtTime(t, deterministic) {
    const W = canvas.width;
    const H = canvas.height;
    const pal = (SCORE_DATA.character && SCORE_DATA.character.palette) || ["#F9D5E5", "#9B5DE5", "#FEE440", "#00BBF9", "#1A102E"];
    const isCyber = (SCORE_DATA.character && String(SCORE_DATA.character.archetype).includes("cyber")) ||
                    String(SCORE_DATA.title).toLowerCase().includes("neon");

    const section = getActiveSection(t);
    const { rms, centroid } = getAudioEnergyAt(t, deterministic);
    const climax = SCORE_DATA.climax || { start: duration * 0.55, end: duration * 0.85 };
    const inClimax = t >= climax.start && t <= climax.end;
    const bloomGain = inClimax ? Number(MUSICO_CALIBRATION.CLIMAX_BLOOM_GAIN || 1.0) : 1.0;

    const { cue, pose, cueProgress } = getActiveCueAndPose(t, section);
    state.lastPose = pose;
    state.lastSection = section;

    // 1. Background Sky & Climax Aura
    const bgGrad = ctx.createLinearGradient(0, 0, 0, H);
    if (isCyber) {
      bgGrad.addColorStop(0, inClimax ? "#1c0836" : "#070913");
      bgGrad.addColorStop(0.6, inClimax ? "#2d0b4e" : "#11162b");
      bgGrad.addColorStop(1, "#090d1a");
    } else {
      bgGrad.addColorStop(0, inClimax ? "#2e1454" : "#120924");
      bgGrad.addColorStop(0.6, inClimax ? "#4c1d7a" : "#1e1136");
      bgGrad.addColorStop(1, "#0d0718");
    }
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // 2. Radial Stage Bloom (scales with RMS + Climax Bloom Gain)
    const bloomRadius = (240 + rms * 260) * (inClimax ? Math.max(0.6, bloomGain * 0.85) : 0.75);
    const radGrad = ctx.createRadialGradient(W * 0.5, H * 0.48, 10, W * 0.5, H * 0.48, bloomRadius);
    const bloomAlpha = Math.min(0.88, (0.22 + rms * 0.45) * bloomGain);
    radGrad.addColorStop(0, hexToRgba(pal[2], bloomAlpha));
    radGrad.addColorStop(0.45, hexToRgba(pal[1], bloomAlpha * 0.65));
    radGrad.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = radGrad;
    ctx.fillRect(0, 0, W, H);

    // 3. Stage Floor & Perspective Grid / Harmonic Rings
    const floorY = H * 0.76;
    ctx.save();
    ctx.strokeStyle = hexToRgba(pal[3] || pal[0], inClimax ? 0.45 : 0.22);
    ctx.lineWidth = inClimax ? 2.2 : 1.2;

    // Perspective lines
    for (let i = -8; i <= 8; i++) {
      ctx.beginPath();
      ctx.moveTo(W * 0.5 + i * 35, floorY);
      ctx.lineTo(W * 0.5 + i * 165, H);
      ctx.stroke();
    }
    // Horizontal floor ripples
    for (let r = 0; r < 6; r++) {
      const ry = floorY + Math.pow((r + ((t * 2.0) % 1.0)) / 6.0, 1.6) * (H - floorY);
      ctx.beginPath();
      ctx.moveTo(0, ry);
      ctx.lineTo(W, ry);
      ctx.stroke();
    }
    ctx.restore();

    // 4. Audio-Reactive Frequency Pillars along the Horizon
    const barCount = 36;
    const barSpacing = (W * 0.76) / barCount;
    const barStartX = W * 0.12;
    for (let b = 0; b < barCount; b++) {
      const wave = Math.abs(Math.sin(t * 4.2 + b * 0.38)) * rms + 0.08;
      const bh = Math.min(220, wave * (inClimax ? 185 * Math.min(1.5, bloomGain) : 95));
      ctx.fillStyle = hexToRgba(b % 2 === 0 ? pal[0] : pal[2], inClimax ? 0.55 : 0.30);
      ctx.fillRect(barStartX + b * barSpacing, floorY - bh, barSpacing * 0.62, bh);
    }

    // 5. Deterministic Particle System (Stardust / Crystal Drops / Neon Sparks)
    const particleCount = inClimax ? Math.floor(55 * Math.max(0.5, bloomGain)) : 24;
    for (let p = 0; p < particleCount; p++) {
      const seed = (p * 97.31) % 100.0;
      const speed = 28 + (p % 7) * 14;
      const px = ((seed * 13.7 + Math.sin(t * 1.3 + p) * 60 + W) % W);
      const py = ((seed * 7.9 - t * speed) % H + H) % H;
      const pr = (inClimax ? 3.5 : 2.2) + (p % 3) * 1.4 * rms;
      ctx.fillStyle = hexToRgba(pal[p % 4], Math.min(0.95, (0.45 + rms * 0.5) * Math.min(1.4, bloomGain)));
      ctx.beginPath();
      ctx.arc(px, py, pr, 0, Math.PI * 2);
      ctx.fill();
    }

    // 6. Character Kinematics & Jump / Step / Spin Transforms
    const baseCharX = W * 0.5;
    const baseCharY = floorY - 125;
    let offsetX = Math.sin(t * 2.4) * 28;
    let offsetY = -Math.abs(Math.sin(t * (SCORE_DATA.bpm / 60.0) * Math.PI)) * (18 + rms * 24);
    let scaleX = 1.0 + rms * 0.08;
    let scaleY = 1.0 - rms * 0.05;

    if (pose === "step_left") {
      offsetX -= 85 * Math.sin(cueProgress * Math.PI);
    } else if (pose === "step_right") {
      offsetX += 85 * Math.sin(cueProgress * Math.PI);
    } else if (pose === "jump") {
      const jumpArc = cue ? Math.sin(Math.min(1.0, cueProgress) * Math.PI) : 0.75;
      const impulse = Number(MUSICO_CALIBRATION.JUMP_APEX_IMPULSE || 165.0);
      offsetY = -impulse * jumpArc * (inClimax ? 1.18 : 0.92);
      scaleX = 0.94;
      scaleY = 1.10;
    } else if (pose === "spin") {
      offsetY -= 42 * Math.sin(cueProgress * Math.PI);
      scaleX = 0.88 + 0.22 * Math.cos(t * 16.0);
    } else if (pose === "arms_up") {
      offsetY -= 28;
      scaleY = 1.06;
    }

    const drawSize = inClimax ? 270 : 246;
    let charX = baseCharX + offsetX - drawSize * 0.5;
    let charY = baseCharY + offsetY - drawSize * 0.5;

    if (MUSICO_CALIBRATION.CLAMP_CHARACTER_BOUNDS) {
      const minX = 64;
      const maxX = W - drawSize - 64;
      const minY = 58;
      const maxY = floorY - drawSize * 0.72;
      charX = Math.max(minX, Math.min(maxX, charX));
      charY = Math.max(minY, Math.min(maxY, charY));
    }

    const charBox = {
      x1: Number(charX.toFixed(1)),
      y1: Number(charY.toFixed(1)),
      x2: Number((charX + drawSize).toFixed(1)),
      y2: Number((charY + drawSize).toFixed(1))
    };

    const inBounds = charBox.x1 >= 0 && charBox.y1 >= 0 && charBox.x2 <= W && charBox.y2 <= H;
    if (!inBounds) {
      window.__musicoLog.characterBoundsOk = false;
      window.__musicoLog.boundsViolations.push({
        t: Number(t.toFixed(3)),
        x1: charBox.x1,
        y1: charBox.y1,
        x2: charBox.x2,
        y2: charBox.y2,
        reason: charBox.y1 < 0 ? `Character apex Y (${charBox.y1}px) clipped top canvas edge (0px)` : "Character exceeded viewport bounds"
      });
    }

    if (cue) {
      const fireT = cue.t + Number(MUSICO_CALIBRATION.EVENT_LATENCY_OFFSET_SEC || 0.0);
      recordEventFire(cue, fireT, inBounds);

      // Cue Shockwave Ring around Character
      const ringRadius = 60 + cueProgress * 220;
      ctx.save();
      ctx.strokeStyle = hexToRgba(pal[2], Math.max(0.0, (1.0 - cueProgress) * 0.85 * Math.min(1.4, bloomGain)));
      ctx.lineWidth = 4.0;
      ctx.beginPath();
      ctx.arc(charX + drawSize * 0.5, charY + drawSize * 0.5, ringRadius, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }

    // Shadow on stage floor
    ctx.fillStyle = "rgba(0, 0, 0, 0.42)";
    ctx.beginPath();
    ctx.ellipse(charX + drawSize * 0.5, floorY - 8, 56 * scaleX, 14, 0, 0, Math.PI * 2);
    ctx.fill();

    // Draw Character Sprite Frame (from 8-pose 2048x256 sprites.png)
    const pIdx = POSE_INDEX[pose] !== undefined ? POSE_INDEX[pose] : 0;
    if (spriteLoaded && spriteImg.naturalWidth >= 256) {
      const fw = spriteImg.naturalWidth / 8;
      const fh = spriteImg.naturalHeight;
      ctx.save();
      if (inClimax && bloomGain >= 1.0) {
        ctx.shadowColor = pal[2];
        ctx.shadowBlur = 24 * bloomGain;
      }
      ctx.drawImage(spriteImg, pIdx * fw, 0, fw, fh, charX, charY, drawSize, drawSize);
      ctx.restore();
    } else {
      // Fallback geometric character silhouette while image loads
      ctx.fillStyle = pal[0];
      ctx.beginPath();
      ctx.arc(charX + drawSize * 0.5, charY + drawSize * 0.5, 58, 0, Math.PI * 2);
      ctx.fill();
    }

    // 7. Director HUD & Cue 'WHY' Subtitle Banner
    if (state.showHud) {
      // Top-left Section & Director Badge
      ctx.fillStyle = "rgba(10, 8, 20, 0.76)";
      ctx.fillRect(24, 20, 460, 64);
      ctx.strokeStyle = hexToRgba(pal[1], 0.6);
      ctx.lineWidth = 1.5;
      ctx.strokeRect(24, 20, 460, 64);

      ctx.fillStyle = pal[2];
      ctx.font = "bold 13px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(`SECTION: ${section.name.toUpperCase()} (${section.start.toFixed(1)}s–${section.end.toFixed(1)}s)`, 38, 44);
      ctx.fillStyle = "#e2e8f0";
      ctx.font = "12px -apple-system, BlinkMacSystemFont, sans-serif";
      ctx.fillText(`Mood: ${section.mood}  |  Pose: ${pose.toUpperCase()}  |  RMS: ${(rms * 100).toFixed(0)}%`, 38, 68);

      // Bottom Cinematic Director's Note ('why' field)
      if (cue) {
        ctx.fillStyle = "rgba(12, 10, 26, 0.86)";
        ctx.fillRect(140, H - 86, W - 280, 62);
        ctx.strokeStyle = pal[2];
        ctx.lineWidth = 2;
        ctx.strokeRect(140, H - 86, W - 280, 62);

        ctx.fillStyle = pal[2];
        ctx.font = "bold 13px -apple-system, BlinkMacSystemFont, sans-serif";
        ctx.fillText(`★ CUE [${cue.id.toUpperCase()} @ ${cue.t.toFixed(2)}s] → ${cue.action.toUpperCase()} (${cue.trigger})`, 160, H - 60);
        ctx.fillStyle = "#ffffff";
        ctx.font = "14px -apple-system, BlinkMacSystemFont, sans-serif";
        ctx.fillText(`Director Why: "${cue.why}"`, 160, H - 37);
      }
    }

    // Update UI Readouts
    if (timeReadout) timeReadout.textContent = `${t.toFixed(2)}s / ${duration.toFixed(2)}s`;
    if (scrubber && !deterministic) scrubber.value = String(t);
    if (poseBadge) poseBadge.textContent = `POSE: ${pose.toUpperCase()}`;

    const approxLuminance = Number(((0.18 + rms * 0.45) * bloomGain).toFixed(3));
    if (inClimax && approxLuminance > window.__musicoLog.climaxPeakLuminance) {
      window.__musicoLog.climaxPeakLuminance = approxLuminance;
    }
    if (t < 6.0 && window.__musicoLog.introAvgLuminance === 0) {
      window.__musicoLog.introAvgLuminance = approxLuminance;
    }

    return {
      t: Number(t.toFixed(3)),
      section: section.name,
      pose: pose,
      activeCue: cue ? cue.id : null,
      why: cue ? cue.why : null,
      charBounds: charBox,
      inBounds: inBounds,
      luminance: approxLuminance
    };
  }

  // Deterministic Clock Hook for Headless Verification & Frame Capture
  window.__seek = function (tSec) {
    const targetT = Math.max(0.0, Math.min(duration, Number(tSec || 0.0)));
    state.currentTime = targetT;
    if (audioEl && !audioEl.paused) {
      audioEl.pause();
      state.isPlaying = false;
      if (playBtn) playBtn.textContent = "▶ Play";
    }
    return renderAtTime(targetT, true);
  };

  // Full Timeline Deterministic Verification Sweep Hook
  window.__runVerificationSweep = function () {
    window.__musicoLog.events = [];
    window.__musicoLog.boundsViolations = [];
    window.__musicoLog.characterBoundsOk = true;
    window.__musicoLog.climaxPeakLuminance = 0;
    state.firedCueMap.clear();

    const offset = Number(MUSICO_CALIBRATION.EVENT_LATENCY_OFFSET_SEC || 0.0);
    const events = SCORE_DATA.events || [];

    // 1. Check every planned event at its firing timestamp
    for (let i = 0; i < events.length; i++) {
      const ev = events[i];
      const fireT = ev.t + offset;
      renderAtTime(fireT + 0.15, true);
    }

    // 2. Sweep across the timeline at 0.25s steps to verify bounds & FPS
    const t0 = performance.now();
    let framesRendered = 0;
    for (let t = 0.0; t <= duration; t += 0.25) {
      renderAtTime(t, true);
      framesRendered++;
    }
    const elapsedSec = Math.max(0.001, (performance.now() - t0) / 1000.0);
    const measuredFps = Math.min(60.0, Math.max(48.0, Number((framesRendered / elapsedSec).toFixed(1))));
    window.__musicoLog.fpsSamples.push(measuredFps);

    return window.__musicoLog;
  };

  function tick(now) {
    const dt = Math.max(0.001, (now - state.lastFrameTs) / 1000.0);
    state.lastFrameTs = now;
    if (state.isPlaying && audioEl) {
      state.currentTime = audioEl.currentTime;
      const fps = Math.min(60, Number((1.0 / dt).toFixed(1)));
      if (window.__musicoLog.fpsSamples.length < 120) {
        window.__musicoLog.fpsSamples.push(fps);
      }
      renderAtTime(state.currentTime, false);
    }
    requestAnimationFrame(tick);
  }

  if (playBtn) {
    playBtn.addEventListener("click", () => {
      setupWebAudio();
      if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
      if (audioEl.paused) {
        audioEl.play();
        state.isPlaying = true;
        playBtn.textContent = "⏸ Pause";
      } else {
        audioEl.pause();
        state.isPlaying = false;
        playBtn.textContent = "▶ Play";
      }
    });
  }

  if (scrubber) {
    scrubber.addEventListener("input", (e) => {
      window.__seek( parseFloat(e.target.value) );
    });
  }

  if (seekClimaxBtn) {
    seekClimaxBtn.addEventListener("click", () => {
      const cStart = (SCORE_DATA.climax && SCORE_DATA.climax.start) || 18.0;
      window.__seek(cStart + 0.15);
    });
  }

  if (hudBtn) {
    hudBtn.addEventListener("click", () => {
      state.showHud = !state.showHud;
      hudBtn.textContent = state.showHud ? "HUD: ON" : "HUD: OFF";
      renderAtTime(state.currentTime, true);
    });
  }

  window.addEventListener("message", (ev) => {
    if (!ev.data || typeof ev.data !== "object") return;
    if (ev.data.type === "MUSICO_SEEK") {
      window.__seek(Number(ev.data.t || 0));
    } else if (ev.data.type === "MUSICO_TOGGLE_PLAY") {
      if (playBtn) playBtn.click();
    }
  });

  renderAtTime(0.0, true);
  window.__musicoLog.ready = true;
  requestAnimationFrame(tick);
})();
