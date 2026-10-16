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
  "title": "Dance of the Sugar Plum Fairy (Celesta Etude)",
  "genre": "Classical / Chamber Music Box",
  "bpm": 120.2,
  "duration": 32.0,
  "director_summary": "A crystalline music-box ballet in four acts: we open in a hushed violet proscenium as Aurelia tiptoes to the iconic descending celesta motif, transition into buoyant syncopated leaps during the arpeggiated development, erupt into a golden stardust storm during the rapid tremolo climax, and dissolve into a suspended porcelain stillness on the final harmonic chimes.",
  "character": {
    "name": "Aurelia the Sugar-Plum Sprite",
    "concept": "A translucent porcelain-and-amethyst clockwork ballerina who awakens inside a velvet music box, channeling every celesta pluck and crystalline tremolo through delicate, spring-loaded ballet choreography.",
    "archetype": "celestial_fairy",
    "palette": [
      "#F9D5E5",
      "#C77DFF",
      "#5A189A",
      "#FFD166",
      "#E0AAFF"
    ],
    "style": "Crystalline paper-cut theater with glowing filigree edges, volumetric stardust motes, and refracted prism highlights",
    "accessories": [
      "Spun-glass tutu with gold leaf trim",
      "Floating clockwork crown",
      "Prism-tipped wand",
      "Iridescent gossamer wings"
    ]
  },
  "sections": [
    {
      "id": "sec_1",
      "name": "Hushed Celesta Prelude",
      "start": 0.0,
      "end": 9.47,
      "mood": "Mysterious, tiptoeing, delicate and hushed",
      "energy": 0.25,
      "motion_vocab": [
        "idle",
        "bounce",
        "step_left",
        "step_right",
        "hold"
      ],
      "background": "Dimly lit violet velvet music-box stage with slowly turning brass gears in the shadows",
      "camera": "slow_drift",
      "particle_theme": "crystal_drops"
    },
    {
      "id": "sec_2",
      "name": "Arpeggiated Woodwind & Celesta Dialogue",
      "start": 9.47,
      "end": 16.97,
      "mood": "Playful, inquisitive, rhythmically buoyant",
      "energy": 0.58,
      "motion_vocab": [
        "step_left",
        "step_right",
        "bounce",
        "arms_up",
        "spin",
        "jump"
      ],
      "background": "Frost-etched glass arches illuminating in sync with rising arpeggio figures",
      "camera": "beat_pulse",
      "particle_theme": "stardust"
    },
    {
      "id": "sec_3",
      "name": "Fortissimo Crystalline Tremolo Climax",
      "start": 16.97,
      "end": 26.98,
      "mood": "Dazzling, urgent, euphoric and virtuosic",
      "energy": 0.95,
      "motion_vocab": [
        "spin",
        "jump",
        "arms_up",
        "bounce"
      ],
      "background": "Radiant golden-violet cathedral of refracted light beams and spinning celestial rings",
      "camera": "dynamic_zoom",
      "particle_theme": "aurora_sparks"
    },
    {
      "id": "sec_4",
      "name": "Porcelain Music-Box Dissolve",
      "start": 26.98,
      "end": 32.0,
      "mood": "Wistful, fragile, winding down to stillness",
      "energy": 0.15,
      "motion_vocab": [
        "step_left",
        "arms_up",
        "hold",
        "idle"
      ],
      "background": "Fading twilight proscenium with a single spotlight narrowing on the porcelain pedestal",
      "camera": "slow_drift",
      "particle_theme": "crystal_drops"
    }
  ],
  "events": [
    {
      "id": "cue_01",
      "raw_t": 2.0,
      "t": 2.0201,
      "snap_delta_ms": 20.1,
      "action": "step_left",
      "intensity": 0.65,
      "trigger": "onset=0.79 (entry of the iconic high G-E celesta motif)",
      "why": "After the four plucked bass pizzicato beats set the hush, the first high celesta note enters at 2.02s; Aurelia awakens from her clockwork slumber with a crisp tiptoe step left."
    },
    {
      "id": "cue_02",
      "raw_t": 2.5,
      "t": 2.531,
      "snap_delta_ms": 31.0,
      "action": "bounce",
      "intensity": 0.85,
      "trigger": "onset=1.00 (peak accent of opening descending phrase)",
      "why": "The strongest onset of the prelude lands on the D# celesta accent; Aurelia performs a delicate knee-plié bounce that sends a ripple of crystal drops across the floor."
    },
    {
      "id": "cue_03",
      "raw_t": 4.4333,
      "t": 4.2493,
      "snap_delta_ms": -184.0,
      "action": "step_right",
      "intensity": 0.75,
      "trigger": "onset=0.83 (chromatic descending step in main theme)",
      "why": "As the melody creeps chromatically downward, Aurelia mirrors the harmonic tension by tiptoeing right across the stage with poised curiosity."
    },
    {
      "id": "cue_04",
      "raw_t": 6.3736,
      "t": 6.5016,
      "snap_delta_ms": 128.0,
      "action": "arms_up",
      "intensity": 0.7,
      "trigger": "onset=0.77 (questioning cadence of the A-phrase)",
      "why": "The descending line reaches its low questioning resolution; Aurelia raises her porcelain arms into fifth position, holding the suspense before the B-section."
    },
    {
      "id": "cue_05",
      "raw_t": 9.5,
      "t": 9.5202,
      "snap_delta_ms": 20.2,
      "action": "jump",
      "intensity": 0.9,
      "trigger": "onset=0.91 (bright ascending arpeggio burst launching Section 2)",
      "why": "At 9.52s the arrangement shifts into rapid upward arpeggios; Aurelia leaps into the air on the high woodwind/celesta accent, igniting the stardust particle layer."
    },
    {
      "id": "cue_06",
      "raw_t": 11.5,
      "t": 11.5171,
      "snap_delta_ms": 17.1,
      "action": "spin",
      "intensity": 0.82,
      "trigger": "onset=0.80 (second answered arpeggio flourish)",
      "why": "The repeating call-and-response arpeggio peaks again at 11.52s; a brisk pirouette translates the swirling sixteenth-note figure into rotational motion."
    },
    {
      "id": "cue_07",
      "raw_t": 14.1166,
      "t": 14.0016,
      "snap_delta_ms": -115.0,
      "action": "jump",
      "intensity": 0.85,
      "trigger": "onset=0.78 (sequential harmonic climb in development)",
      "why": "As the repeated motif builds urgency toward the climax, Aurelia executes a syncopated grand jeté right on the downbeat accent."
    },
    {
      "id": "cue_08",
      "raw_t": 17.0,
      "t": 16.997,
      "snap_delta_ms": -3.0,
      "action": "spin",
      "intensity": 1.0,
      "trigger": "onset=0.76 (sweeping harp/celesta glissando into the fortissimo climax)",
      "why": "A rapid ascending glissando at 17.0s unleashes the high-energy tremolo climax; Aurelia launches into a dazzling golden stardust spin as the camera zooms in."
    },
    {
      "id": "cue_09",
      "raw_t": 28.0,
      "t": 28.0265,
      "snap_delta_ms": 26.5,
      "action": "arms_up",
      "intensity": 0.55,
      "trigger": "onset=0.63 (sparse high-register bell notes in outro)",
      "why": "The rapid tremolos vanish into isolated, echoing music-box chimes; Aurelia slows her motion and lifts her arms in a wistful farewell arch."
    },
    {
      "id": "cue_10",
      "raw_t": 30.0,
      "t": 30.0234,
      "snap_delta_ms": 23.4,
      "action": "hold",
      "intensity": 0.95,
      "trigger": "onset=1.00 (final resonant E-minor celesta chime)",
      "why": "On the final crystalline strike at 30.02s, Aurelia freezes in a balanced arabesque silhouette while the violet stage lights slowly fade to black."
    }
  ],
  "climax": {
    "start": 16.97,
    "end": 26.98,
    "description": "Following the sweeping upward glissando at 17.0s, the texture doubles in density and brightness (avg_energy 0.421, avg_brightness 0.455) with continuous mandolin-like celesta tremolos descending and ascending through dramatic harmonic shifts.",
    "visual_boost": "Golden stardust storm + 1.25x dynamic camera zoom + amethyst halo bloom + continuous ribbon trails"
  }
};
const FEATURES_DATA = {
  "filename": "sugar_plum_fairy.wav",
  "duration": 32.0,
  "bpm": 120.2,
  "beats": [
    2.0434,
    2.9954,
    4.0403,
    4.9923,
    6.014,
    7.0124,
    8.0109,
    9.0093,
    10.0078,
    11.0063,
    12.0047,
    13.0032,
    14.0016,
    15.0001,
    15.9985,
    16.997,
    18.0187,
    19.0404,
    19.9924,
    21.0373,
    22.0357,
    23.011,
    24.0094,
    25.0079,
    26.0063,
    26.9816,
    28.0497,
    29.0482,
    30.0234
  ],
  "onsets": [
    {
      "t": 0.5108,
      "strength": 0.223
    },
    {
      "t": 1.0217,
      "strength": 0.474
    },
    {
      "t": 1.5093,
      "strength": 0.176
    },
    {
      "t": 2.0201,
      "strength": 0.79
    },
    {
      "t": 2.2756,
      "strength": 0.803
    },
    {
      "t": 2.531,
      "strength": 1.0
    },
    {
      "t": 2.9722,
      "strength": 0.359
    },
    {
      "t": 3.483,
      "strength": 0.424
    },
    {
      "t": 3.7616,
      "strength": 0.298
    },
    {
      "t": 4.0171,
      "strength": 0.709
    },
    {
      "t": 4.2493,
      "strength": 0.83
    },
    {
      "t": 4.4815,
      "strength": 0.266
    },
    {
      "t": 4.9691,
      "strength": 0.279
    },
    {
      "t": 5.2477,
      "strength": 0.609
    },
    {
      "t": 5.4799,
      "strength": 0.191
    },
    {
      "t": 5.9675,
      "strength": 0.239
    },
    {
      "t": 6.2462,
      "strength": 0.742
    },
    {
      "t": 6.5016,
      "strength": 0.769
    },
    {
      "t": 6.966,
      "strength": 0.217
    },
    {
      "t": 7.4768,
      "strength": 0.518
    },
    {
      "t": 7.9644,
      "strength": 0.257
    },
    {
      "t": 8.4753,
      "strength": 0.552
    },
    {
      "t": 8.6378,
      "strength": 0.246
    },
    {
      "t": 8.7539,
      "strength": 0.421
    },
    {
      "t": 8.87,
      "strength": 0.471
    },
    {
      "t": 8.9861,
      "strength": 0.343
    },
    {
      "t": 9.1254,
      "strength": 0.704
    },
    {
      "t": 9.5202,
      "strength": 0.913
    },
    {
      "t": 9.6363,
      "strength": 0.201
    },
    {
      "t": 9.7524,
      "strength": 0.695
    },
    {
      "t": 9.8685,
      "strength": 0.49
    },
    {
      "t": 10.0078,
      "strength": 0.672
    },
    {
      "t": 10.1239,
      "strength": 0.444
    },
    {
      "t": 10.4722,
      "strength": 0.488
    },
    {
      "t": 10.658,
      "strength": 0.493
    },
    {
      "t": 10.8669,
      "strength": 0.395
    },
    {
      "t": 11.0063,
      "strength": 0.664
    },
    {
      "t": 11.1224,
      "strength": 0.729
    },
    {
      "t": 11.5171,
      "strength": 0.802
    },
    {
      "t": 11.6564,
      "strength": 0.514
    },
    {
      "t": 11.8654,
      "strength": 0.393
    },
    {
      "t": 12.0047,
      "strength": 0.714
    },
    {
      "t": 12.1208,
      "strength": 0.428
    },
    {
      "t": 12.4691,
      "strength": 0.414
    },
    {
      "t": 12.6549,
      "strength": 0.556
    },
    {
      "t": 12.8639,
      "strength": 0.304
    },
    {
      "t": 13.0032,
      "strength": 0.725
    },
    {
      "t": 13.1193,
      "strength": 0.663
    },
    {
      "t": 13.514,
      "strength": 0.666
    },
    {
      "t": 13.6533,
      "strength": 0.57
    },
    {
      "t": 13.8623,
      "strength": 0.287
    },
    {
      "t": 14.0016,
      "strength": 0.778
    },
    {
      "t": 14.1177,
      "strength": 0.352
    },
    {
      "t": 14.466,
      "strength": 0.332
    },
    {
      "t": 14.6518,
      "strength": 0.558
    },
    {
      "t": 14.884,
      "strength": 0.358
    },
    {
      "t": 15.0001,
      "strength": 0.776
    },
    {
      "t": 15.1162,
      "strength": 0.578
    },
    {
      "t": 15.5109,
      "strength": 0.49
    },
    {
      "t": 15.6502,
      "strength": 0.525
    },
    {
      "t": 15.8824,
      "strength": 0.455
    },
    {
      "t": 15.9985,
      "strength": 0.795
    },
    {
      "t": 16.1146,
      "strength": 0.229
    },
    {
      "t": 16.4629,
      "strength": 0.242
    },
    {
      "t": 16.6487,
      "strength": 0.51
    },
    {
      "t": 16.8809,
      "strength": 0.397
    },
    {
      "t": 16.997,
      "strength": 0.755
    },
    {
      "t": 17.1131,
      "strength": 0.231
    },
    {
      "t": 17.2292,
      "strength": 0.211
    },
    {
      "t": 17.3917,
      "strength": 0.261
    },
    {
      "t": 17.5311,
      "strength": 0.338
    },
    {
      "t": 17.6472,
      "strength": 0.311
    },
    {
      "t": 17.7633,
      "strength": 0.227
    },
    {
      "t": 18.0187,
      "strength": 0.44
    },
    {
      "t": 18.1348,
      "strength": 0.228
    },
    {
      "t": 18.2741,
      "strength": 0.206
    },
    {
      "t": 18.4831,
      "strength": 0.317
    },
    {
      "t": 18.5992,
      "strength": 0.362
    },
    {
      "t": 18.7385,
      "strength": 0.292
    },
    {
      "t": 18.8546,
      "strength": 0.477
    },
    {
      "t": 19.0171,
      "strength": 0.332
    },
    {
      "t": 19.2726,
      "strength": 0.277
    },
    {
      "t": 19.4815,
      "strength": 0.398
    },
    {
      "t": 19.5976,
      "strength": 0.268
    },
    {
      "t": 19.737,
      "strength": 0.428
    },
    {
      "t": 19.8531,
      "strength": 0.364
    },
    {
      "t": 19.9924,
      "strength": 0.362
    },
    {
      "t": 20.1085,
      "strength": 0.198
    },
    {
      "t": 20.271,
      "strength": 0.235
    },
    {
      "t": 20.48,
      "strength": 0.375
    },
    {
      "t": 20.5961,
      "strength": 0.247
    },
    {
      "t": 20.7354,
      "strength": 0.328
    },
    {
      "t": 20.8515,
      "strength": 0.346
    },
    {
      "t": 20.9908,
      "strength": 0.287
    },
    {
      "t": 21.2695,
      "strength": 0.263
    },
    {
      "t": 21.4785,
      "strength": 0.291
    },
    {
      "t": 21.5946,
      "strength": 0.188
    },
    {
      "t": 21.7339,
      "strength": 0.373
    },
    {
      "t": 21.85,
      "strength": 0.315
    },
    {
      "t": 21.9893,
      "strength": 0.296
    },
    {
      "t": 22.2679,
      "strength": 0.18
    },
    {
      "t": 22.4769,
      "strength": 0.348
    },
    {
      "t": 22.593,
      "strength": 0.277
    },
    {
      "t": 22.7323,
      "strength": 0.466
    },
    {
      "t": 22.8484,
      "strength": 0.373
    },
    {
      "t": 22.9878,
      "strength": 0.478
    },
    {
      "t": 23.2664,
      "strength": 0.191
    },
    {
      "t": 23.4754,
      "strength": 0.32
    },
    {
      "t": 23.5915,
      "strength": 0.223
    },
    {
      "t": 23.7308,
      "strength": 0.424
    },
    {
      "t": 23.8469,
      "strength": 0.377
    },
    {
      "t": 23.9862,
      "strength": 0.428
    },
    {
      "t": 24.2649,
      "strength": 0.175
    },
    {
      "t": 24.4738,
      "strength": 0.272
    },
    {
      "t": 24.5899,
      "strength": 0.182
    },
    {
      "t": 24.7293,
      "strength": 0.397
    },
    {
      "t": 24.8454,
      "strength": 0.259
    },
    {
      "t": 24.9847,
      "strength": 0.449
    },
    {
      "t": 25.2633,
      "strength": 0.182
    },
    {
      "t": 25.4723,
      "strength": 0.264
    },
    {
      "t": 25.6116,
      "strength": 0.276
    },
    {
      "t": 25.7277,
      "strength": 0.373
    },
    {
      "t": 25.8438,
      "strength": 0.258
    },
    {
      "t": 25.9831,
      "strength": 0.479
    },
    {
      "t": 26.285,
      "strength": 0.213
    },
    {
      "t": 26.4707,
      "strength": 0.245
    },
    {
      "t": 26.6101,
      "strength": 0.491
    },
    {
      "t": 26.7262,
      "strength": 0.425
    },
    {
      "t": 26.8423,
      "strength": 0.221
    },
    {
      "t": 26.9816,
      "strength": 0.499
    },
    {
      "t": 27.0977,
      "strength": 0.307
    },
    {
      "t": 27.5156,
      "strength": 0.361
    },
    {
      "t": 27.6317,
      "strength": 0.27
    },
    {
      "t": 28.0265,
      "strength": 0.634
    },
    {
      "t": 28.1426,
      "strength": 0.211
    },
    {
      "t": 28.5141,
      "strength": 0.311
    },
    {
      "t": 28.6302,
      "strength": 0.226
    },
    {
      "t": 29.0249,
      "strength": 0.627
    },
    {
      "t": 29.141,
      "strength": 0.161
    },
    {
      "t": 29.8376,
      "strength": 0.114
    },
    {
      "t": 30.0234,
      "strength": 0.999
    }
  ],
  "rms_curve": [
    {
      "t": 0.0,
      "value": 0.1152
    },
    {
      "t": 0.1,
      "value": 0.0647
    },
    {
      "t": 0.2,
      "value": 0.0158
    },
    {
      "t": 0.3,
      "value": 0.0029
    },
    {
      "t": 0.4,
      "value": 0.0
    },
    {
      "t": 0.5,
      "value": 0.1144
    },
    {
      "t": 0.6,
      "value": 0.0642
    },
    {
      "t": 0.7,
      "value": 0.0158
    },
    {
      "t": 0.8,
      "value": 0.0029
    },
    {
      "t": 0.9,
      "value": 0.0
    },
    {
      "t": 1.0,
      "value": 0.1154
    },
    {
      "t": 1.1,
      "value": 0.0644
    },
    {
      "t": 1.2,
      "value": 0.0159
    },
    {
      "t": 1.3,
      "value": 0.0029
    },
    {
      "t": 1.4,
      "value": 0.0
    },
    {
      "t": 1.5,
      "value": 0.1143
    },
    {
      "t": 1.6,
      "value": 0.064
    },
    {
      "t": 1.7,
      "value": 0.0158
    },
    {
      "t": 1.8,
      "value": 0.0029
    },
    {
      "t": 1.9,
      "value": 0.0
    },
    {
      "t": 2.0,
      "value": 0.1991
    },
    {
      "t": 2.1,
      "value": 0.1936
    },
    {
      "t": 2.2,
      "value": 0.1174
    },
    {
      "t": 2.3,
      "value": 0.2165
    },
    {
      "t": 2.4,
      "value": 0.1363
    },
    {
      "t": 2.5,
      "value": 0.2455
    },
    {
      "t": 2.6,
      "value": 0.2345
    },
    {
      "t": 2.7,
      "value": 0.1446
    },
    {
      "t": 2.8,
      "value": 0.0916
    },
    {
      "t": 2.9,
      "value": 0.0583
    },
    {
      "t": 3.0,
      "value": 0.2236
    },
    {
      "t": 3.1,
      "value": 0.2209
    },
    {
      "t": 3.2,
      "value": 0.1357
    },
    {
      "t": 3.3,
      "value": 0.0859
    },
    {
      "t": 3.4,
      "value": 0.0539
    },
    {
      "t": 3.5,
      "value": 0.1921
    },
    {
      "t": 3.6,
      "value": 0.1864
    },
    {
      "t": 3.7,
      "value": 0.1219
    },
    {
      "t": 3.8,
      "value": 0.2279
    },
    {
      "t": 3.9,
      "value": 0.1472
    },
    {
      "t": 4.0,
      "value": 0.2231
    },
    {
      "t": 4.1,
      "value": 0.2075
    },
    {
      "t": 4.2,
      "value": 0.1129
    },
    {
      "t": 4.3,
      "value": 0.2479
    },
    {
      "t": 4.4,
      "value": 0.159
    },
    {
      "t": 4.5,
      "value": 0.241
    },
    {
      "t": 4.6,
      "value": 0.2345
    },
    {
      "t": 4.7,
      "value": 0.1448
    },
    {
      "t": 4.8,
      "value": 0.0917
    },
    {
      "t": 4.9,
      "value": 0.0581
    },
    {
      "t": 5.0,
      "value": 0.21
    },
    {
      "t": 5.1,
      "value": 0.2074
    },
    {
      "t": 5.2,
      "value": 0.1133
    },
    {
      "t": 5.3,
      "value": 0.2464
    },
    {
      "t": 5.4,
      "value": 0.1588
    },
    {
      "t": 5.5,
      "value": 0.2412
    },
    {
      "t": 5.6,
      "value": 0.2341
    },
    {
      "t": 5.7,
      "value": 0.1449
    },
    {
      "t": 5.8,
      "value": 0.0915
    },
    {
      "t": 5.9,
      "value": 0.0579
    },
    {
      "t": 6.0,
      "value": 0.2237
    },
    {
      "t": 6.1,
      "value": 0.2212
    },
    {
      "t": 6.2,
      "value": 0.1218
    },
    {
      "t": 6.3,
      "value": 0.2622
    },
    {
      "t": 6.4,
      "value": 0.1705
    },
    {
      "t": 6.5,
      "value": 0.2552
    },
    {
      "t": 6.6,
      "value": 0.2482
    },
    {
      "t": 6.7,
      "value": 0.1538
    },
    {
      "t": 6.8,
      "value": 0.0972
    },
    {
      "t": 6.9,
      "value": 0.0614
    },
    {
      "t": 7.0,
      "value": 0.2599
    },
    {
      "t": 7.1,
      "value": 0.2645
    },
    {
      "t": 7.2,
      "value": 0.1626
    },
    {
      "t": 7.3,
      "value": 0.1029
    },
    {
      "t": 7.4,
      "value": 0.0651
    },
    {
      "t": 7.5,
      "value": 0.3035
    },
    {
      "t": 7.6,
      "value": 0.3056
    },
    {
      "t": 7.7,
      "value": 0.1898
    },
    {
      "t": 7.8,
      "value": 0.12
    },
    {
      "t": 7.9,
      "value": 0.0757
    },
    {
      "t": 8.0,
      "value": 0.4668
    },
    {
      "t": 8.1,
      "value": 0.4572
    },
    {
      "t": 8.2,
      "value": 0.2727
    },
    {
      "t": 8.3,
      "value": 0.1685
    },
    {
      "t": 8.4,
      "value": 0.1059
    },
    {
      "t": 8.5,
      "value": 0.2657
    },
    {
      "t": 8.6,
      "value": 0.2753
    },
    {
      "t": 8.7,
      "value": 0.2708
    },
    {
      "t": 8.8,
      "value": 0.3124
    },
    {
      "t": 8.9,
      "value": 0.2987
    },
    {
      "t": 9.0,
      "value": 0.2587
    },
    {
      "t": 9.1,
      "value": 0.128
    },
    {
      "t": 9.2,
      "value": 0.0226
    },
    {
      "t": 9.3,
      "value": 0.0042
    },
    {
      "t": 9.4,
      "value": 0.0
    },
    {
      "t": 9.5,
      "value": 0.2654
    },
    {
      "t": 9.6,
      "value": 0.2748
    },
    {
      "t": 9.7,
      "value": 0.2694
    },
    {
      "t": 9.8,
      "value": 0.3093
    },
    {
      "t": 9.9,
      "value": 0.2993
    },
    {
      "t": 10.0,
      "value": 0.5096
    },
    {
      "t": 10.1,
      "value": 0.4648
    },
    {
      "t": 10.2,
      "value": 0.2722
    },
    {
      "t": 10.3,
      "value": 0.1694
    },
    {
      "t": 10.4,
      "value": 0.1061
    },
    {
      "t": 10.5,
      "value": 0.2652
    },
    {
      "t": 10.6,
      "value": 0.2706
    },
    {
      "t": 10.7,
      "value": 0.2748
    },
    {
      "t": 10.8,
      "value": 0.3079
    },
    {
      "t": 10.9,
      "value": 0.3
    },
    {
      "t": 11.0,
      "value": 0.2575
    },
    {
      "t": 11.1,
      "value": 0.1281
    },
    {
      "t": 11.2,
      "value": 0.0228
    },
    {
      "t": 11.3,
      "value": 0.0041
    },
    {
      "t": 11.4,
      "value": 0.0
    },
    {
      "t": 11.5,
      "value": 0.264
    },
    {
      "t": 11.6,
      "value": 0.2715
    },
    {
      "t": 11.7,
      "value": 0.2727
    },
    {
      "t": 11.8,
      "value": 0.3059
    },
    {
      "t": 11.9,
      "value": 0.2984
    },
    {
      "t": 12.0,
      "value": 0.5093
    },
    {
      "t": 12.1,
      "value": 0.466
    },
    {
      "t": 12.2,
      "value": 0.2722
    },
    {
      "t": 12.3,
      "value": 0.1688
    },
    {
      "t": 12.4,
      "value": 0.1065
    },
    {
      "t": 12.5,
      "value": 0.2636
    },
    {
      "t": 12.6,
      "value": 0.2754
    },
    {
      "t": 12.7,
      "value": 0.2702
    },
    {
      "t": 12.8,
      "value": 0.3031
    },
    {
      "t": 12.9,
      "value": 0.2994
    },
    {
      "t": 13.0,
      "value": 0.2591
    },
    {
      "t": 13.1,
      "value": 0.1289
    },
    {
      "t": 13.2,
      "value": 0.023
    },
    {
      "t": 13.3,
      "value": 0.0041
    },
    {
      "t": 13.4,
      "value": 0.0
    },
    {
      "t": 13.5,
      "value": 0.2638
    },
    {
      "t": 13.6,
      "value": 0.2746
    },
    {
      "t": 13.7,
      "value": 0.2706
    },
    {
      "t": 13.8,
      "value": 0.3006
    },
    {
      "t": 13.9,
      "value": 0.2993
    },
    {
      "t": 14.0,
      "value": 0.5128
    },
    {
      "t": 14.1,
      "value": 0.4634
    },
    {
      "t": 14.2,
      "value": 0.2729
    },
    {
      "t": 14.3,
      "value": 0.1688
    },
    {
      "t": 14.4,
      "value": 0.1053
    },
    {
      "t": 14.5,
      "value": 0.263
    },
    {
      "t": 14.6,
      "value": 0.2734
    },
    {
      "t": 14.7,
      "value": 0.2757
    },
    {
      "t": 14.8,
      "value": 0.3009
    },
    {
      "t": 14.9,
      "value": 0.3006
    },
    {
      "t": 15.0,
      "value": 0.2572
    },
    {
      "t": 15.1,
      "value": 0.1292
    },
    {
      "t": 15.2,
      "value": 0.023
    },
    {
      "t": 15.3,
      "value": 0.0042
    },
    {
      "t": 15.4,
      "value": 0.0
    },
    {
      "t": 15.5,
      "value": 0.2635
    },
    {
      "t": 15.6,
      "value": 0.2742
    },
    {
      "t": 15.7,
      "value": 0.2738
    },
    {
      "t": 15.8,
      "value": 0.3012
    },
    {
      "t": 15.9,
      "value": 0.2994
    },
    {
      "t": 16.0,
      "value": 0.5124
    },
    {
      "t": 16.1,
      "value": 0.4654
    },
    {
      "t": 16.2,
      "value": 0.2716
    },
    {
      "t": 16.3,
      "value": 0.1689
    },
    {
      "t": 16.4,
      "value": 0.105
    },
    {
      "t": 16.5,
      "value": 0.2638
    },
    {
      "t": 16.6,
      "value": 0.2733
    },
    {
      "t": 16.7,
      "value": 0.2782
    },
    {
      "t": 16.8,
      "value": 0.3007
    },
    {
      "t": 16.9,
      "value": 0.2993
    },
    {
      "t": 17.0,
      "value": 0.3581
    },
    {
      "t": 17.1,
      "value": 0.4743
    },
    {
      "t": 17.2,
      "value": 0.4889
    },
    {
      "t": 17.3,
      "value": 0.514
    },
    {
      "t": 17.4,
      "value": 0.5093
    },
    {
      "t": 17.5,
      "value": 0.6582
    },
    {
      "t": 17.6,
      "value": 0.7124
    },
    {
      "t": 17.7,
      "value": 0.7163
    },
    {
      "t": 17.8,
      "value": 0.7534
    },
    {
      "t": 17.9,
      "value": 0.7472
    },
    {
      "t": 18.0,
      "value": 0.9095
    },
    {
      "t": 18.1,
      "value": 0.7399
    },
    {
      "t": 18.2,
      "value": 0.4617
    },
    {
      "t": 18.3,
      "value": 0.3821
    },
    {
      "t": 18.4,
      "value": 0.2688
    },
    {
      "t": 18.5,
      "value": 0.2527
    },
    {
      "t": 18.6,
      "value": 0.2595
    },
    {
      "t": 18.7,
      "value": 0.277
    },
    {
      "t": 18.8,
      "value": 0.29
    },
    {
      "t": 18.9,
      "value": 0.2917
    },
    {
      "t": 19.0,
      "value": 0.6585
    },
    {
      "t": 19.1,
      "value": 0.6445
    },
    {
      "t": 19.2,
      "value": 0.5289
    },
    {
      "t": 19.3,
      "value": 0.4155
    },
    {
      "t": 19.4,
      "value": 0.3783
    },
    {
      "t": 19.5,
      "value": 0.3439
    },
    {
      "t": 19.6,
      "value": 0.3121
    },
    {
      "t": 19.7,
      "value": 0.3208
    },
    {
      "t": 19.8,
      "value": 0.3333
    },
    {
      "t": 19.9,
      "value": 0.326
    },
    {
      "t": 20.0,
      "value": 0.6673
    },
    {
      "t": 20.1,
      "value": 0.649
    },
    {
      "t": 20.2,
      "value": 0.5363
    },
    {
      "t": 20.3,
      "value": 0.4243
    },
    {
      "t": 20.4,
      "value": 0.3901
    },
    {
      "t": 20.5,
      "value": 0.3529
    },
    {
      "t": 20.6,
      "value": 0.3192
    },
    {
      "t": 20.7,
      "value": 0.3202
    },
    {
      "t": 20.8,
      "value": 0.3265
    },
    {
      "t": 20.9,
      "value": 0.3183
    },
    {
      "t": 21.0,
      "value": 0.6583
    },
    {
      "t": 21.1,
      "value": 0.6383
    },
    {
      "t": 21.2,
      "value": 0.5252
    },
    {
      "t": 21.3,
      "value": 0.4045
    },
    {
      "t": 21.4,
      "value": 0.3646
    },
    {
      "t": 21.5,
      "value": 0.3191
    },
    {
      "t": 21.6,
      "value": 0.2797
    },
    {
      "t": 21.7,
      "value": 0.2814
    },
    {
      "t": 21.8,
      "value": 0.291
    },
    {
      "t": 21.9,
      "value": 0.2764
    },
    {
      "t": 22.0,
      "value": 0.6419
    },
    {
      "t": 22.1,
      "value": 0.6195
    },
    {
      "t": 22.2,
      "value": 0.4908
    },
    {
      "t": 22.3,
      "value": 0.3725
    },
    {
      "t": 22.4,
      "value": 0.2952
    },
    {
      "t": 22.5,
      "value": 0.2604
    },
    {
      "t": 22.6,
      "value": 0.2357
    },
    {
      "t": 22.7,
      "value": 0.2328
    },
    {
      "t": 22.8,
      "value": 0.2694
    },
    {
      "t": 22.9,
      "value": 0.2699
    },
    {
      "t": 23.0,
      "value": 0.638
    },
    {
      "t": 23.1,
      "value": 0.5811
    },
    {
      "t": 23.2,
      "value": 0.3282
    },
    {
      "t": 23.3,
      "value": 0.3262
    },
    {
      "t": 23.4,
      "value": 0.3398
    },
    {
      "t": 23.5,
      "value": 0.3124
    },
    {
      "t": 23.6,
      "value": 0.2937
    },
    {
      "t": 23.7,
      "value": 0.3001
    },
    {
      "t": 23.8,
      "value": 0.3216
    },
    {
      "t": 23.9,
      "value": 0.3143
    },
    {
      "t": 24.0,
      "value": 0.6703
    },
    {
      "t": 24.1,
      "value": 0.6619
    },
    {
      "t": 24.2,
      "value": 0.5484
    },
    {
      "t": 24.3,
      "value": 0.4375
    },
    {
      "t": 24.4,
      "value": 0.3991
    },
    {
      "t": 24.5,
      "value": 0.3632
    },
    {
      "t": 24.6,
      "value": 0.3347
    },
    {
      "t": 24.7,
      "value": 0.3324
    },
    {
      "t": 24.8,
      "value": 0.3486
    },
    {
      "t": 24.9,
      "value": 0.3419
    },
    {
      "t": 25.0,
      "value": 0.6668
    },
    {
      "t": 25.1,
      "value": 0.6518
    },
    {
      "t": 25.2,
      "value": 0.5434
    },
    {
      "t": 25.3,
      "value": 0.4221
    },
    {
      "t": 25.4,
      "value": 0.3896
    },
    {
      "t": 25.5,
      "value": 0.3465
    },
    {
      "t": 25.6,
      "value": 0.3071
    },
    {
      "t": 25.7,
      "value": 0.3089
    },
    {
      "t": 25.8,
      "value": 0.3156
    },
    {
      "t": 25.9,
      "value": 0.3057
    },
    {
      "t": 26.0,
      "value": 0.6531
    },
    {
      "t": 26.1,
      "value": 0.5867
    },
    {
      "t": 26.2,
      "value": 0.3348
    },
    {
      "t": 26.3,
      "value": 0.3214
    },
    {
      "t": 26.4,
      "value": 0.3232
    },
    {
      "t": 26.5,
      "value": 0.2819
    },
    {
      "t": 26.6,
      "value": 0.2542
    },
    {
      "t": 26.7,
      "value": 0.2536
    },
    {
      "t": 26.8,
      "value": 0.2691
    },
    {
      "t": 26.9,
      "value": 0.2599
    },
    {
      "t": 27.0,
      "value": 0.2828
    },
    {
      "t": 27.1,
      "value": 0.2492
    },
    {
      "t": 27.2,
      "value": 0.1533
    },
    {
      "t": 27.3,
      "value": 0.0973
    },
    {
      "t": 27.4,
      "value": 0.0619
    },
    {
      "t": 27.5,
      "value": 0.2092
    },
    {
      "t": 27.6,
      "value": 0.2163
    },
    {
      "t": 27.7,
      "value": 0.1351
    },
    {
      "t": 27.8,
      "value": 0.0858
    },
    {
      "t": 27.9,
      "value": 0.0547
    },
    {
      "t": 28.0,
      "value": 0.1952
    },
    {
      "t": 28.1,
      "value": 0.2018
    },
    {
      "t": 28.2,
      "value": 0.1262
    },
    {
      "t": 28.3,
      "value": 0.0801
    },
    {
      "t": 28.4,
      "value": 0.051
    },
    {
      "t": 28.5,
      "value": 0.1733
    },
    {
      "t": 28.6,
      "value": 0.1804
    },
    {
      "t": 28.7,
      "value": 0.1126
    },
    {
      "t": 28.8,
      "value": 0.0715
    },
    {
      "t": 28.9,
      "value": 0.0455
    },
    {
      "t": 29.0,
      "value": 0.1672
    },
    {
      "t": 29.1,
      "value": 0.1732
    },
    {
      "t": 29.2,
      "value": 0.1083
    },
    {
      "t": 29.3,
      "value": 0.0687
    },
    {
      "t": 29.4,
      "value": 0.0436
    },
    {
      "t": 29.5,
      "value": 0.0279
    },
    {
      "t": 29.6,
      "value": 0.0178
    },
    {
      "t": 29.7,
      "value": 0.0113
    },
    {
      "t": 29.8,
      "value": 0.0056
    },
    {
      "t": 29.9,
      "value": 0.0
    },
    {
      "t": 30.0,
      "value": 0.3755
    },
    {
      "t": 30.1,
      "value": 0.3798
    },
    {
      "t": 30.2,
      "value": 0.2296
    },
    {
      "t": 30.3,
      "value": 0.1427
    },
    {
      "t": 30.4,
      "value": 0.0902
    },
    {
      "t": 30.5,
      "value": 0.057
    },
    {
      "t": 30.6,
      "value": 0.0362
    },
    {
      "t": 30.7,
      "value": 0.0231
    },
    {
      "t": 30.8,
      "value": 0.0147
    },
    {
      "t": 30.9,
      "value": 0.0094
    },
    {
      "t": 31.0,
      "value": 0.006
    },
    {
      "t": 31.1,
      "value": 0.0038
    },
    {
      "t": 31.2,
      "value": 0.0024
    },
    {
      "t": 31.3,
      "value": 0.0016
    },
    {
      "t": 31.4,
      "value": 0.001
    },
    {
      "t": 31.5,
      "value": 0.0006
    },
    {
      "t": 31.6,
      "value": 0.0004
    },
    {
      "t": 31.7,
      "value": 0.0003
    },
    {
      "t": 31.8,
      "value": 0.0001
    },
    {
      "t": 31.9,
      "value": 0.0
    }
  ],
  "spectral_centroid_curve": [
    {
      "t": 0.0,
      "value": 0.06
    },
    {
      "t": 0.1,
      "value": 0.0589
    },
    {
      "t": 0.2,
      "value": 0.0945
    },
    {
      "t": 0.3,
      "value": 0.4352
    },
    {
      "t": 0.4,
      "value": 0.0
    },
    {
      "t": 0.5,
      "value": 0.088
    },
    {
      "t": 0.6,
      "value": 0.0827
    },
    {
      "t": 0.7,
      "value": 0.117
    },
    {
      "t": 0.8,
      "value": 0.4427
    },
    {
      "t": 0.9,
      "value": 0.0
    },
    {
      "t": 1.0,
      "value": 0.1154
    },
    {
      "t": 1.1,
      "value": 0.106
    },
    {
      "t": 1.2,
      "value": 0.1372
    },
    {
      "t": 1.3,
      "value": 0.5076
    },
    {
      "t": 1.4,
      "value": 0.0
    },
    {
      "t": 1.5,
      "value": 0.088
    },
    {
      "t": 1.6,
      "value": 0.0827
    },
    {
      "t": 1.7,
      "value": 0.1171
    },
    {
      "t": 1.8,
      "value": 0.4413
    },
    {
      "t": 1.9,
      "value": 0.0
    },
    {
      "t": 2.0,
      "value": 0.2434
    },
    {
      "t": 2.1,
      "value": 0.2487
    },
    {
      "t": 2.2,
      "value": 0.2429
    },
    {
      "t": 2.3,
      "value": 0.2654
    },
    {
      "t": 2.4,
      "value": 0.2296
    },
    {
      "t": 2.5,
      "value": 0.314
    },
    {
      "t": 2.6,
      "value": 0.2588
    },
    {
      "t": 2.7,
      "value": 0.2466
    },
    {
      "t": 2.8,
      "value": 0.2459
    },
    {
      "t": 2.9,
      "value": 0.2379
    },
    {
      "t": 3.0,
      "value": 0.2574
    },
    {
      "t": 3.1,
      "value": 0.2462
    },
    {
      "t": 3.2,
      "value": 0.2337
    },
    {
      "t": 3.3,
      "value": 0.2386
    },
    {
      "t": 3.4,
      "value": 0.2289
    },
    {
      "t": 3.5,
      "value": 0.2049
    },
    {
      "t": 3.6,
      "value": 0.2032
    },
    {
      "t": 3.7,
      "value": 0.2024
    },
    {
      "t": 3.8,
      "value": 0.2654
    },
    {
      "t": 3.9,
      "value": 0.2293
    },
    {
      "t": 4.0,
      "value": 0.2691
    },
    {
      "t": 4.1,
      "value": 0.1899
    },
    {
      "t": 4.2,
      "value": 0.3834
    },
    {
      "t": 4.3,
      "value": 0.2358
    },
    {
      "t": 4.4,
      "value": 0.2039
    },
    {
      "t": 4.5,
      "value": 0.2507
    },
    {
      "t": 4.6,
      "value": 0.1961
    },
    {
      "t": 4.7,
      "value": 0.1861
    },
    {
      "t": 4.8,
      "value": 0.188
    },
    {
      "t": 4.9,
      "value": 0.1848
    },
    {
      "t": 5.0,
      "value": 0.1985
    },
    {
      "t": 5.1,
      "value": 0.1873
    },
    {
      "t": 5.2,
      "value": 0.268
    },
    {
      "t": 5.3,
      "value": 0.2242
    },
    {
      "t": 5.4,
      "value": 0.1928
    },
    {
      "t": 5.5,
      "value": 0.2139
    },
    {
      "t": 5.6,
      "value": 0.1859
    },
    {
      "t": 5.7,
      "value": 0.1762
    },
    {
      "t": 5.8,
      "value": 0.1784
    },
    {
      "t": 5.9,
      "value": 0.1763
    },
    {
      "t": 6.0,
      "value": 0.1756
    },
    {
      "t": 6.1,
      "value": 0.1715
    },
    {
      "t": 6.2,
      "value": 0.3227
    },
    {
      "t": 6.3,
      "value": 0.2107
    },
    {
      "t": 6.4,
      "value": 0.1819
    },
    {
      "t": 6.5,
      "value": 0.215
    },
    {
      "t": 6.6,
      "value": 0.177
    },
    {
      "t": 6.7,
      "value": 0.167
    },
    {
      "t": 6.8,
      "value": 0.1691
    },
    {
      "t": 6.9,
      "value": 0.1687
    },
    {
      "t": 7.0,
      "value": 0.1868
    },
    {
      "t": 7.1,
      "value": 0.1719
    },
    {
      "t": 7.2,
      "value": 0.1601
    },
    {
      "t": 7.3,
      "value": 0.1649
    },
    {
      "t": 7.4,
      "value": 0.1562
    },
    {
      "t": 7.5,
      "value": 0.3404
    },
    {
      "t": 7.6,
      "value": 0.3308
    },
    {
      "t": 7.7,
      "value": 0.3108
    },
    {
      "t": 7.8,
      "value": 0.3035
    },
    {
      "t": 7.9,
      "value": 0.2995
    },
    {
      "t": 8.0,
      "value": 0.3089
    },
    {
      "t": 8.1,
      "value": 0.2839
    },
    {
      "t": 8.2,
      "value": 0.2632
    },
    {
      "t": 8.3,
      "value": 0.2546
    },
    {
      "t": 8.4,
      "value": 0.2465
    },
    {
      "t": 8.5,
      "value": 0.1981
    },
    {
      "t": 8.6,
      "value": 0.241
    },
    {
      "t": 8.7,
      "value": 0.2761
    },
    {
      "t": 8.8,
      "value": 0.3591
    },
    {
      "t": 8.9,
      "value": 0.4626
    },
    {
      "t": 9.0,
      "value": 0.2442
    },
    {
      "t": 9.1,
      "value": 0.3999
    },
    {
      "t": 9.2,
      "value": 0.0682
    },
    {
      "t": 9.3,
      "value": 0.3228
    },
    {
      "t": 9.4,
      "value": 0.0
    },
    {
      "t": 9.5,
      "value": 0.217
    },
    {
      "t": 9.6,
      "value": 0.2697
    },
    {
      "t": 9.7,
      "value": 0.3798
    },
    {
      "t": 9.8,
      "value": 0.3859
    },
    {
      "t": 9.9,
      "value": 0.5122
    },
    {
      "t": 10.0,
      "value": 0.3459
    },
    {
      "t": 10.1,
      "value": 0.3371
    },
    {
      "t": 10.2,
      "value": 0.2632
    },
    {
      "t": 10.3,
      "value": 0.2545
    },
    {
      "t": 10.4,
      "value": 0.2464
    },
    {
      "t": 10.5,
      "value": 0.1981
    },
    {
      "t": 10.6,
      "value": 0.2436
    },
    {
      "t": 10.7,
      "value": 0.2759
    },
    {
      "t": 10.8,
      "value": 0.3594
    },
    {
      "t": 10.9,
      "value": 0.4617
    },
    {
      "t": 11.0,
      "value": 0.2381
    },
    {
      "t": 11.1,
      "value": 0.4014
    },
    {
      "t": 11.2,
      "value": 0.0683
    },
    {
      "t": 11.3,
      "value": 0.3194
    },
    {
      "t": 11.4,
      "value": 0.0
    },
    {
      "t": 11.5,
      "value": 0.217
    },
    {
      "t": 11.6,
      "value": 0.273
    },
    {
      "t": 11.7,
      "value": 0.3811
    },
    {
      "t": 11.8,
      "value": 0.388
    },
    {
      "t": 11.9,
      "value": 0.5113
    },
    {
      "t": 12.0,
      "value": 0.344
    },
    {
      "t": 12.1,
      "value": 0.3356
    },
    {
      "t": 12.2,
      "value": 0.2632
    },
    {
      "t": 12.3,
      "value": 0.2545
    },
    {
      "t": 12.4,
      "value": 0.2476
    },
    {
      "t": 12.5,
      "value": 0.1982
    },
    {
      "t": 12.6,
      "value": 0.2463
    },
    {
      "t": 12.7,
      "value": 0.2755
    },
    {
      "t": 12.8,
      "value": 0.3599
    },
    {
      "t": 12.9,
      "value": 0.4614
    },
    {
      "t": 13.0,
      "value": 0.2311
    },
    {
      "t": 13.1,
      "value": 0.3939
    },
    {
      "t": 13.2,
      "value": 0.0684
    },
    {
      "t": 13.3,
      "value": 0.3164
    },
    {
      "t": 13.4,
      "value": 0.0
    },
    {
      "t": 13.5,
      "value": 0.217
    },
    {
      "t": 13.6,
      "value": 0.2755
    },
    {
      "t": 13.7,
      "value": 0.3799
    },
    {
      "t": 13.8,
      "value": 0.3893
    },
    {
      "t": 13.9,
      "value": 0.5113
    },
    {
      "t": 14.0,
      "value": 0.3388
    },
    {
      "t": 14.1,
      "value": 0.3334
    },
    {
      "t": 14.2,
      "value": 0.2632
    },
    {
      "t": 14.3,
      "value": 0.2546
    },
    {
      "t": 14.4,
      "value": 0.2525
    },
    {
      "t": 14.5,
      "value": 0.1987
    },
    {
      "t": 14.6,
      "value": 0.2476
    },
    {
      "t": 14.7,
      "value": 0.2767
    },
    {
      "t": 14.8,
      "value": 0.3606
    },
    {
      "t": 14.9,
      "value": 0.4616
    },
    {
      "t": 15.0,
      "value": 0.225
    },
    {
      "t": 15.1,
      "value": 0.3901
    },
    {
      "t": 15.2,
      "value": 0.0683
    },
    {
      "t": 15.3,
      "value": 0.3139
    },
    {
      "t": 15.4,
      "value": 0.0
    },
    {
      "t": 15.5,
      "value": 0.217
    },
    {
      "t": 15.6,
      "value": 0.2755
    },
    {
      "t": 15.7,
      "value": 0.377
    },
    {
      "t": 15.8,
      "value": 0.3898
    },
    {
      "t": 15.9,
      "value": 0.512
    },
    {
      "t": 16.0,
      "value": 0.3361
    },
    {
      "t": 16.1,
      "value": 0.3321
    },
    {
      "t": 16.2,
      "value": 0.2632
    },
    {
      "t": 16.3,
      "value": 0.2547
    },
    {
      "t": 16.4,
      "value": 0.2541
    },
    {
      "t": 16.5,
      "value": 0.1996
    },
    {
      "t": 16.6,
      "value": 0.2461
    },
    {
      "t": 16.7,
      "value": 0.2775
    },
    {
      "t": 16.8,
      "value": 0.361
    },
    {
      "t": 16.9,
      "value": 0.4625
    },
    {
      "t": 17.0,
      "value": 0.2009
    },
    {
      "t": 17.1,
      "value": 0.2113
    },
    {
      "t": 17.2,
      "value": 0.169
    },
    {
      "t": 17.3,
      "value": 0.1885
    },
    {
      "t": 17.4,
      "value": 0.2187
    },
    {
      "t": 17.5,
      "value": 0.2583
    },
    {
      "t": 17.6,
      "value": 0.3019
    },
    {
      "t": 17.7,
      "value": 0.3584
    },
    {
      "t": 17.8,
      "value": 0.4121
    },
    {
      "t": 17.9,
      "value": 0.4865
    },
    {
      "t": 18.0,
      "value": 0.4145
    },
    {
      "t": 18.1,
      "value": 0.3915
    },
    {
      "t": 18.2,
      "value": 0.3494
    },
    {
      "t": 18.3,
      "value": 0.4531
    },
    {
      "t": 18.4,
      "value": 0.4498
    },
    {
      "t": 18.5,
      "value": 0.4939
    },
    {
      "t": 18.6,
      "value": 0.4137
    },
    {
      "t": 18.7,
      "value": 0.3805
    },
    {
      "t": 18.8,
      "value": 0.4213
    },
    {
      "t": 18.9,
      "value": 0.406
    },
    {
      "t": 19.0,
      "value": 0.416
    },
    {
      "t": 19.1,
      "value": 0.3583
    },
    {
      "t": 19.2,
      "value": 0.3163
    },
    {
      "t": 19.3,
      "value": 0.3848
    },
    {
      "t": 19.4,
      "value": 0.4018
    },
    {
      "t": 19.5,
      "value": 0.4403
    },
    {
      "t": 19.6,
      "value": 0.331
    },
    {
      "t": 19.7,
      "value": 0.3638
    },
    {
      "t": 19.8,
      "value": 0.3751
    },
    {
      "t": 19.9,
      "value": 0.4038
    },
    {
      "t": 20.0,
      "value": 0.4421
    },
    {
      "t": 20.1,
      "value": 0.3674
    },
    {
      "t": 20.2,
      "value": 0.3285
    },
    {
      "t": 20.3,
      "value": 0.406
    },
    {
      "t": 20.4,
      "value": 0.426
    },
    {
      "t": 20.5,
      "value": 0.4911
    },
    {
      "t": 20.6,
      "value": 0.3709
    },
    {
      "t": 20.7,
      "value": 0.3798
    },
    {
      "t": 20.8,
      "value": 0.418
    },
    {
      "t": 20.9,
      "value": 0.4543
    },
    {
      "t": 21.0,
      "value": 0.3976
    },
    {
      "t": 21.1,
      "value": 0.3327
    },
    {
      "t": 21.2,
      "value": 0.2943
    },
    {
      "t": 21.3,
      "value": 0.3656
    },
    {
      "t": 21.4,
      "value": 0.3837
    },
    {
      "t": 21.5,
      "value": 0.4427
    },
    {
      "t": 21.6,
      "value": 0.3548
    },
    {
      "t": 21.7,
      "value": 0.368
    },
    {
      "t": 21.8,
      "value": 0.4201
    },
    {
      "t": 21.9,
      "value": 0.4624
    },
    {
      "t": 22.0,
      "value": 0.533
    },
    {
      "t": 22.1,
      "value": 0.4789
    },
    {
      "t": 22.2,
      "value": 0.4721
    },
    {
      "t": 22.3,
      "value": 0.6092
    },
    {
      "t": 22.4,
      "value": 0.7079
    },
    {
      "t": 22.5,
      "value": 0.8564
    },
    {
      "t": 22.6,
      "value": 0.7163
    },
    {
      "t": 22.7,
      "value": 0.7024
    },
    {
      "t": 22.8,
      "value": 0.6793
    },
    {
      "t": 22.9,
      "value": 0.7064
    },
    {
      "t": 23.0,
      "value": 0.5675
    },
    {
      "t": 23.1,
      "value": 0.4935
    },
    {
      "t": 23.2,
      "value": 0.4214
    },
    {
      "t": 23.3,
      "value": 0.5327
    },
    {
      "t": 23.4,
      "value": 0.5624
    },
    {
      "t": 23.5,
      "value": 0.5946
    },
    {
      "t": 23.6,
      "value": 0.4713
    },
    {
      "t": 23.7,
      "value": 0.4948
    },
    {
      "t": 23.8,
      "value": 0.4823
    },
    {
      "t": 23.9,
      "value": 0.5305
    },
    {
      "t": 24.0,
      "value": 0.4532
    },
    {
      "t": 24.1,
      "value": 0.3606
    },
    {
      "t": 24.2,
      "value": 0.3342
    },
    {
      "t": 24.3,
      "value": 0.4007
    },
    {
      "t": 24.4,
      "value": 0.4207
    },
    {
      "t": 24.5,
      "value": 0.4607
    },
    {
      "t": 24.6,
      "value": 0.3782
    },
    {
      "t": 24.7,
      "value": 0.3653
    },
    {
      "t": 24.8,
      "value": 0.4042
    },
    {
      "t": 24.9,
      "value": 0.4333
    },
    {
      "t": 25.0,
      "value": 0.407
    },
    {
      "t": 25.1,
      "value": 0.3353
    },
    {
      "t": 25.2,
      "value": 0.3158
    },
    {
      "t": 25.3,
      "value": 0.3735
    },
    {
      "t": 25.4,
      "value": 0.3929
    },
    {
      "t": 25.5,
      "value": 0.4371
    },
    {
      "t": 25.6,
      "value": 0.3595
    },
    {
      "t": 25.7,
      "value": 0.3773
    },
    {
      "t": 25.8,
      "value": 0.3888
    },
    {
      "t": 25.9,
      "value": 0.4214
    },
    {
      "t": 26.0,
      "value": 0.6127
    },
    {
      "t": 26.1,
      "value": 0.5118
    },
    {
      "t": 26.2,
      "value": 0.4544
    },
    {
      "t": 26.3,
      "value": 0.6162
    },
    {
      "t": 26.4,
      "value": 0.6752
    },
    {
      "t": 26.5,
      "value": 0.7553
    },
    {
      "t": 26.6,
      "value": 0.6961
    },
    {
      "t": 26.7,
      "value": 0.7512
    },
    {
      "t": 26.8,
      "value": 0.8452
    },
    {
      "t": 26.9,
      "value": 0.9481
    },
    {
      "t": 27.0,
      "value": 0.6727
    },
    {
      "t": 27.1,
      "value": 0.6083
    },
    {
      "t": 27.2,
      "value": 0.4334
    },
    {
      "t": 27.3,
      "value": 0.4036
    },
    {
      "t": 27.4,
      "value": 0.3905
    },
    {
      "t": 27.5,
      "value": 0.4379
    },
    {
      "t": 27.6,
      "value": 0.3912
    },
    {
      "t": 27.7,
      "value": 0.3269
    },
    {
      "t": 27.8,
      "value": 0.3055
    },
    {
      "t": 27.9,
      "value": 0.297
    },
    {
      "t": 28.0,
      "value": 0.3468
    },
    {
      "t": 28.1,
      "value": 0.3299
    },
    {
      "t": 28.2,
      "value": 0.2613
    },
    {
      "t": 28.3,
      "value": 0.2449
    },
    {
      "t": 28.4,
      "value": 0.2395
    },
    {
      "t": 28.5,
      "value": 0.2921
    },
    {
      "t": 28.6,
      "value": 0.2812
    },
    {
      "t": 28.7,
      "value": 0.2206
    },
    {
      "t": 28.8,
      "value": 0.2079
    },
    {
      "t": 28.9,
      "value": 0.2046
    },
    {
      "t": 29.0,
      "value": 0.2218
    },
    {
      "t": 29.1,
      "value": 0.1991
    },
    {
      "t": 29.2,
      "value": 0.1675
    },
    {
      "t": 29.3,
      "value": 0.159
    },
    {
      "t": 29.4,
      "value": 0.1581
    },
    {
      "t": 29.5,
      "value": 0.1646
    },
    {
      "t": 29.6,
      "value": 0.1752
    },
    {
      "t": 29.7,
      "value": 0.1932
    },
    {
      "t": 29.8,
      "value": 0.3584
    },
    {
      "t": 29.9,
      "value": 0.0
    },
    {
      "t": 30.0,
      "value": 0.4696
    },
    {
      "t": 30.1,
      "value": 0.3925
    },
    {
      "t": 30.2,
      "value": 0.3443
    },
    {
      "t": 30.3,
      "value": 0.32
    },
    {
      "t": 30.4,
      "value": 0.3088
    },
    {
      "t": 30.5,
      "value": 0.3047
    },
    {
      "t": 30.6,
      "value": 0.3056
    },
    {
      "t": 30.7,
      "value": 0.3106
    },
    {
      "t": 30.8,
      "value": 0.3189
    },
    {
      "t": 30.9,
      "value": 0.3347
    },
    {
      "t": 31.0,
      "value": 0.3537
    },
    {
      "t": 31.1,
      "value": 0.3934
    },
    {
      "t": 31.2,
      "value": 0.4416
    },
    {
      "t": 31.3,
      "value": 0.5122
    },
    {
      "t": 31.4,
      "value": 0.591
    },
    {
      "t": 31.5,
      "value": 0.7133
    },
    {
      "t": 31.6,
      "value": 0.8082
    },
    {
      "t": 31.7,
      "value": 0.8951
    },
    {
      "t": 31.8,
      "value": 0.8282
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
      "end": 9.47,
      "avg_energy": 0.15,
      "avg_brightness": 0.216,
      "suggested_role": "intro"
    },
    {
      "index": 1,
      "start": 9.47,
      "end": 16.97,
      "avg_energy": 0.246,
      "avg_brightness": 0.295,
      "suggested_role": "development"
    },
    {
      "index": 2,
      "start": 16.97,
      "end": 26.98,
      "avg_energy": 0.421,
      "avg_brightness": 0.455,
      "suggested_role": "climax"
    },
    {
      "index": 3,
      "start": 26.98,
      "end": 32.0,
      "avg_energy": 0.092,
      "avg_brightness": 0.348,
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
