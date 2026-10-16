import json
import logging
import shutil
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger("yourdancer.game_generator")

JUDGE_JS = r"""// YourDancer — 4-Lane Rhythm Game Judgement & Combo Engine (judge.js)
(function (global) {
  class RhythmJudge {
    constructor(notes) {
      this.PERFECT_WINDOW = 0.050; // ±50ms -> 300 pts
      this.GOOD_WINDOW = 0.100;    // ±100ms -> 100 pts
      this.reset(notes || []);
    }

    reset(notes) {
      this.notes = (notes || []).map((n, idx) => ({
        id: n.id || ('n_' + idx),
        t: Number(n.t),
        end_t: Number(n.end_t != null ? n.end_t : n.t),
        lane: Number(n.lane),
        key: n.key || ['D', 'F', 'J', 'K'][Number(n.lane)] || 'D',
        type: n.type || 'hit',
        part: n.part || 'L_arm',
        label: n.label || 'Move',
        raw_t: Number(n.raw_t != null ? n.raw_t : n.t),
        snap_distance_ms: Number(n.snap_distance_ms || 0),
        energy: Number(n.energy || 0.75),
        judged: false,
        holding: false,
        completedHold: false,
        result: null,
        hitDeltaMs: null,
      }));
      this.score = 0;
      this.combo = 0;
      this.maxCombo = 0;
      this.perfect = 0;
      this.good = 0;
      this.miss = 0;
      this.missedMoves = [];
      this.lastJudgement = null;
    }

    getMultiplier() {
      return Number(Math.min(2.0, 1.0 + Math.floor(this.combo / 10) * 0.1).toFixed(1));
    }

    _recordHit(note, kind, deltaSec, currentTime) {
      note.judged = true;
      note.result = kind;
      note.hitDeltaMs = Math.round(deltaSec * 1000);
      if (kind === 'PERFECT') {
        this.perfect += 1;
        this.combo += 1;
        if (this.combo > this.maxCombo) this.maxCombo = this.combo;
        const mult = this.getMultiplier();
        const holdBonus = note.type === 'hold' ? 50 : 0;
        this.score += Math.round((300 + holdBonus) * mult);
        if (note.type === 'hold') {
          note.holding = true;
        }
      } else if (kind === 'GOOD') {
        this.good += 1;
        this.combo += 1;
        if (this.combo > this.maxCombo) this.maxCombo = this.combo;
        const mult = this.getMultiplier();
        this.score += Math.round(100 * mult);
        if (note.type === 'hold') {
          note.holding = true;
        }
      } else {
        this._recordMiss(note, 'timing_error', currentTime);
        return;
      }
      this.lastJudgement = {
        kind: kind,
        lane: note.lane,
        label: note.label,
        part: note.part,
        deltaMs: note.hitDeltaMs,
        time: currentTime,
      };
    }

    _recordMiss(note, reason, currentTime) {
      if (note.judged) return;
      note.judged = true;
      note.holding = false;
      note.result = 'MISS';
      this.miss += 1;
      this.combo = 0;
      this.missedMoves.push({
        id: note.id,
        t: note.t,
        end_t: note.end_t,
        lane: note.lane,
        key: note.key,
        part: note.part,
        label: note.label,
        type: note.type,
        reason: reason || 'late_miss',
      });
      this.lastJudgement = {
        kind: 'MISS',
        lane: note.lane,
        label: note.label,
        part: note.part,
        deltaMs: null,
        time: currentTime,
      };
    }

    onKeyDown(lane, currentTime) {
      let bestNote = null;
      let bestAbs = Infinity;
      for (let i = 0; i < this.notes.length; i++) {
        const n = this.notes[i];
        if (n.judged || n.lane !== lane) continue;
        const delta = currentTime - n.t;
        const absDelta = Math.abs(delta);
        if (absDelta <= this.GOOD_WINDOW + 1e-6 && absDelta < bestAbs) {
          bestAbs = absDelta;
          bestNote = n;
        }
      }
      if (!bestNote) {
        return null;
      }
      const delta = currentTime - bestNote.t;
      const absDelta = Math.abs(delta);
      if (absDelta <= this.PERFECT_WINDOW + 1e-6) {
        this._recordHit(bestNote, 'PERFECT', delta, currentTime);
        return 'PERFECT';
      } else if (absDelta <= this.GOOD_WINDOW + 1e-6) {
        this._recordHit(bestNote, 'GOOD', delta, currentTime);
        return 'GOOD';
      }
      return null;
    }

    step(currentTime, activeKeys) {
      for (let i = 0; i < this.notes.length; i++) {
        const n = this.notes[i];
        if (!n.judged && currentTime - n.t > this.GOOD_WINDOW + 0.002) {
          this._recordMiss(n, 'passed_judgement_line', currentTime);
        }
        if (n.holding && !n.completedHold) {
          if (currentTime >= n.end_t) {
            n.holding = false;
            n.completedHold = true;
            this.score += 50;
          }
        }
      }
    }

    getAccuracy() {
      const total = this.perfect + this.good + this.miss;
      if (total === 0) return 100.0;
      return Number((((this.perfect * 1.0 + this.good * 0.5) / total) * 100.0).toFixed(2));
    }

    getRank() {
      const acc = this.getAccuracy();
      if (acc >= 95.0 && this.miss === 0) return 'S';
      if (acc >= 85.0) return 'A';
      if (acc >= 70.0) return 'B';
      return 'C';
    }

    getSummary(difficulty) {
      return {
        difficulty: difficulty || 'Normal',
        totalNotes: this.notes.length,
        perfect: this.perfect,
        good: this.good,
        miss: this.miss,
        maxCombo: this.maxCombo,
        score: this.score,
        accuracy: this.getAccuracy(),
        rank: this.getRank(),
        missedMoves: this.missedMoves.slice(),
      };
    }
  }

  global.RhythmJudge = RhythmJudge;
})(window);
"""

GAME_JS = r"""// YourDancer — 4-Lane HTML5 Canvas Rhythm Game + Deterministic Auto-Player (game.js)
(function (global) {
  const LANE_COLORS = ['#00f5d4', '#ff2a85', '#fee440', '#a855f7'];
  const LANE_KEYS = ['D', 'F', 'J', 'K'];
  const LANE_LABELS = ['L_ARM', 'R_ARM', 'L_LEG', 'R_LEG'];
  const KEY_TO_LANE = { KeyD: 0, KeyF: 1, KeyJ: 2, KeyK: 3, d: 0, f: 1, j: 2, k: 3, D: 0, F: 1, J: 2, K: 3 };

  const state = {
    chartData: null,
    difficulty: 'Normal',
    judge: null,
    playing: false,
    autoPlayLive: false,
    currentTime: 0.0,
    duration: 35.0,
    approachTime: 1.65,
    pressedLanes: [false, false, false, false],
    laneFlashes: [0, 0, 0, 0],
    consoleErrors: [],
    practiceLoop: null,
    rafId: null,
  };

  window.addEventListener('error', (ev) => {
    state.consoleErrors.push(String(ev.message || ev));
  });

  const canvas = document.getElementById('game-canvas');
  const ctx = canvas.getContext('2d');
  const videoEl = document.getElementById('dance-video');

  async function initGame() {
    const params = new URLSearchParams(window.location.search);
    const reqDiff = params.get('difficulty');
    if (reqDiff && ['Easy', 'Normal', 'Hard'].includes(reqDiff)) {
      state.difficulty = reqDiff;
    }
    if (params.get('autoplay') === '1') {
      state.autoPlayLive = true;
    }

    const res = await fetch('chart.json');
    state.chartData = await res.json();
    state.duration = Number(state.chartData.duration || 35.0);

    document.getElementById('song-title').textContent = state.chartData.title || 'Dance Practice';
    document.getElementById('song-meta').textContent =
      `${state.chartData.bpm} BPM · ${state.chartData.choreo_style}`;

    selectDifficulty(state.difficulty);
    bindControls();
    renderFrame(0.0);
    startRenderLoop();
  }

  function selectDifficulty(diff) {
    state.difficulty = diff;
    document.querySelectorAll('.diff-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.diff === diff);
    });
    const notes = (state.chartData && state.chartData.difficulties && state.chartData.difficulties[diff]) || [];
    state.judge = new window.RhythmJudge(notes);
    updateHUD();
    hideResultsModal();
  }

  function bindControls() {
    document.querySelectorAll('.diff-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        selectDifficulty(btn.dataset.diff);
        if (state.playing) restartGame();
      });
    });

    const startBtn = document.getElementById('btn-start');
    if (startBtn) {
      startBtn.addEventListener('click', () => {
        if (state.playing) {
          pauseGame();
        } else {
          startGame();
        }
      });
    }

    const autoBtn = document.getElementById('btn-autoplay');
    if (autoBtn) {
      autoBtn.classList.toggle('active', state.autoPlayLive);
      autoBtn.addEventListener('click', () => {
        state.autoPlayLive = !state.autoPlayLive;
        autoBtn.classList.toggle('active', state.autoPlayLive);
        autoBtn.textContent = state.autoPlayLive ? 'AUTO-PLAY: ON' : 'AUTO-PLAY: OFF';
      });
    }

    const finishBtn = document.getElementById('btn-results');
    if (finishBtn) {
      finishBtn.addEventListener('click', () => {
        showResultsModal(state.judge.getSummary(state.difficulty));
      });
    }

    const closeResBtn = document.getElementById('btn-close-results');
    if (closeResBtn) {
      closeResBtn.addEventListener('click', () => {
        hideResultsModal();
      });
    }

    window.addEventListener('keydown', (e) => {
      const lane = KEY_TO_LANE[e.code] != null ? KEY_TO_LANE[e.code] : KEY_TO_LANE[e.key];
      if (lane != null && !e.repeat) {
        triggerLaneInput(lane, state.currentTime);
      }
    });

    window.addEventListener('keyup', (e) => {
      const lane = KEY_TO_LANE[e.code] != null ? KEY_TO_LANE[e.code] : KEY_TO_LANE[e.key];
      if (lane != null) {
        state.pressedLanes[lane] = false;
      }
    });

    document.querySelectorAll('.touch-pad').forEach((pad) => {
      const lane = Number(pad.dataset.lane);
      pad.addEventListener('pointerdown', (e) => {
        e.preventDefault();
        triggerLaneInput(lane, state.currentTime);
      });
      pad.addEventListener('pointerup', () => {
        state.pressedLanes[lane] = false;
      });
    });
  }

  function triggerLaneInput(lane, t) {
    state.pressedLanes[lane] = true;
    state.laneFlashes[lane] = 1.0;
    if (state.judge) {
      state.judge.onKeyDown(lane, t);
      updateHUD();
    }
  }

  function startGame() {
    state.practiceLoop = null;
    hideResultsModal();
    if (state.currentTime >= state.duration - 0.5) {
      state.currentTime = 0.0;
      selectDifficulty(state.difficulty);
    }
    state.playing = true;
    const btn = document.getElementById('btn-start');
    if (btn) btn.textContent = 'PAUSE';
    if (videoEl) {
      videoEl.currentTime = state.currentTime;
      videoEl.playbackRate = 1.0;
      videoEl.play().catch(() => {});
    }
  }

  function pauseGame() {
    state.playing = false;
    const btn = document.getElementById('btn-start');
    if (btn) btn.textContent = 'PLAY ROUTINE';
    if (videoEl) videoEl.pause();
  }

  function restartGame() {
    state.currentTime = 0.0;
    selectDifficulty(state.difficulty);
    if (videoEl) {
      videoEl.currentTime = 0.0;
    }
    startGame();
  }

  function updateHUD() {
    if (!state.judge) return;
    document.getElementById('hud-score').textContent = state.judge.score.toLocaleString();
    document.getElementById('hud-combo').textContent = state.judge.combo + 'x';
    document.getElementById('hud-mult').textContent = state.judge.getMultiplier().toFixed(1) + 'x';
    document.getElementById('hud-acc').textContent = state.judge.getAccuracy().toFixed(1) + '%';
  }

  function startRenderLoop() {
    let lastWall = performance.now();
    function tick(now) {
      const dt = Math.min(0.1, (now - lastWall) / 1000.0);
      lastWall = now;

      if (state.practiceLoop && videoEl) {
        if (videoEl.currentTime >= state.practiceLoop.end) {
          videoEl.currentTime = state.practiceLoop.start;
          videoEl.play().catch(() => {});
        }
        state.currentTime = videoEl.currentTime;
      } else if (state.playing) {
        if (videoEl && !videoEl.paused && !videoEl.ended) {
          state.currentTime = videoEl.currentTime;
        } else {
          state.currentTime += dt;
        }

        // If live auto-play toggle is active, automatically fire notes at exact timing
        if (state.autoPlayLive && state.judge) {
          for (let i = 0; i < state.judge.notes.length; i++) {
            const n = state.judge.notes[i];
            if (!n.judged && state.currentTime >= n.t - 0.008) {
              triggerLaneInput(n.lane, n.t);
            }
          }
        }

        if (state.judge) {
          state.judge.step(state.currentTime, state.pressedLanes);
          updateHUD();
        }

        if (state.currentTime >= state.duration - 0.15) {
          pauseGame();
          showResultsModal(state.judge.getSummary(state.difficulty));
        }
      }

      for (let i = 0; i < 4; i++) {
        state.laneFlashes[i] = Math.max(0, state.laneFlashes[i] - dt * 4.5);
      }

      renderFrame(state.currentTime);
      state.rafId = requestAnimationFrame(tick);
    }
    state.rafId = requestAnimationFrame(tick);
  }

  function renderFrame(t) {
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    // Semi-transparent arcade track highway on left/center (0..500), Dancer HUD on right (510..w)
    const trackX = 36;
    const trackW = 440;
    const laneW = trackW / 4;
    const judgeY = h - 68;

    ctx.fillStyle = 'rgba(10, 14, 26, 0.76)';
    ctx.fillRect(trackX, 0, trackW, h);

    // Draw lanes & grid lines
    for (let ln = 0; ln < 4; ln++) {
      const lx = trackX + ln * laneW;
      const col = LANE_COLORS[ln];
      if (state.laneFlashes[ln] > 0.02 || state.pressedLanes[ln]) {
        const alpha = Math.max(0.18, state.laneFlashes[ln] * 0.35);
        ctx.fillStyle = hexToRgba(col, alpha);
        ctx.fillRect(lx + 2, 0, laneW - 4, judgeY);
      }
      ctx.strokeStyle = 'rgba(120, 145, 195, 0.24)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(lx, 0);
      ctx.lineTo(lx, h);
      ctx.stroke();

      // Receptor box at judgement line
      ctx.strokeStyle = col;
      ctx.lineWidth = state.pressedLanes[ln] ? 3 : 2;
      ctx.fillStyle = state.pressedLanes[ln] ? hexToRgba(col, 0.35) : 'rgba(16, 20, 36, 0.85)';
      ctx.fillRect(lx + 8, judgeY - 12, laneW - 16, 24);
      ctx.strokeRect(lx + 8, judgeY - 12, laneW - 16, 24);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 13px Inter, system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`${LANE_KEYS[ln]} · ${LANE_LABELS[ln]}`, lx + laneW / 2, judgeY + 34);
    }

    // Judgement line glow
    ctx.strokeStyle = '#00f5d4';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(trackX, judgeY);
    ctx.lineTo(trackX + trackW, judgeY);
    ctx.stroke();

    // Draw approaching notes & holds
    let activeMove = null;
    if (state.judge) {
      const notes = state.judge.notes;
      for (let i = 0; i < notes.length; i++) {
        const n = notes[i];
        if (Math.abs(t - n.t) <= 0.25 || (n.type === 'hold' && t >= n.t && t <= n.end_t)) {
          activeMove = n;
        }
        if (n.judged && (!n.holding || t > n.end_t)) continue;

        const dt = n.t - t;
        if (dt > state.approachTime || (n.end_t - t) < -0.15) continue;

        const lx = trackX + n.lane * laneW;
        const col = LANE_COLORS[n.lane];
        const headY = judgeY - (dt / state.approachTime) * (judgeY - 24);

        if (n.type === 'hold') {
          const endDt = n.end_t - t;
          const tailY = judgeY - (endDt / state.approachTime) * (judgeY - 24);
          const clampedHeadY = n.holding ? judgeY : headY;
          ctx.fillStyle = hexToRgba(col, 0.42);
          ctx.fillRect(lx + 20, Math.min(tailY, clampedHeadY), laneW - 40, Math.abs(clampedHeadY - tailY));
          ctx.strokeStyle = col;
          ctx.lineWidth = 2;
          ctx.strokeRect(lx + 20, Math.min(tailY, clampedHeadY), laneW - 40, Math.abs(clampedHeadY - tailY));
        }

        if (!n.judged) {
          ctx.fillStyle = col;
          ctx.fillRect(lx + 10, headY - 9, laneW - 20, 18);
          ctx.fillStyle = '#0b0e1a';
          ctx.font = 'bold 10px Inter, sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText(n.part.toUpperCase(), lx + laneW / 2, headY + 4);
        }
      }

      // Draw last judgement toast
      const lj = state.judge.lastJudgement;
      if (lj && t - lj.time <= 0.55) {
        ctx.save();
        ctx.textAlign = 'center';
        ctx.font = 'bold 26px Inter, system-ui, sans-serif';
        ctx.fillStyle = lj.kind === 'PERFECT' ? '#00f5d4' : lj.kind === 'GOOD' ? '#fee440' : '#ff2a85';
        ctx.fillText(lj.kind, trackX + trackW / 2, judgeY - 88);
        ctx.font = '13px Inter, system-ui, sans-serif';
        ctx.fillStyle = '#e2e8f0';
        ctx.fillText(`${lj.label} (${lj.part})`, trackX + trackW / 2, judgeY - 64);
        ctx.restore();
      }
    }

    // Draw Right-Side Live Dancer Pose HUD & Section Telemetry
    drawDancerPoseHUD(ctx, 496, 18, w - 512, h - 36, t, activeMove);
  }

  function drawDancerPoseHUD(ctx, x, y, w, h, t, activeMove) {
    ctx.fillStyle = 'rgba(12, 16, 30, 0.82)';
    ctx.strokeStyle = 'rgba(0, 245, 212, 0.35)';
    ctx.lineWidth = 1.5;
    ctx.fillRect(x, y, w, h);
    ctx.strokeRect(x, y, w, h);

    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 11px Inter, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('LIVE LIMB TELEMETRY HUD', x + 14, y + 22);

    ctx.fillStyle = '#00f5d4';
    ctx.font = 'bold 13px monospace';
    ctx.fillText(`CLOCK: ${t.toFixed(2)}s / ${state.duration.toFixed(1)}s`, x + 14, y + 42);

    // Stick dancer mirror silhouette
    const cx = x + w / 2;
    const cy = y + h * 0.54;
    const part = activeMove ? activeMove.part : null;

    // Head & Torso
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(cx, cy - 64, 14, 0, Math.PI * 2);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(cx, cy - 50);
    ctx.lineTo(cx, cy + 10);
    ctx.stroke();

    // Left Arm (Lane 0)
    ctx.strokeStyle = part === 'L_arm' || part === 'both' ? LANE_COLORS[0] : '#475569';
    ctx.lineWidth = part === 'L_arm' || part === 'both' ? 6 : 3;
    ctx.beginPath();
    ctx.moveTo(cx, cy - 42);
    ctx.lineTo(cx - 38, part === 'L_arm' || part === 'both' ? cy - 72 : cy - 15);
    ctx.stroke();

    // Right Arm (Lane 1)
    ctx.strokeStyle = part === 'R_arm' || part === 'both' ? LANE_COLORS[1] : '#475569';
    ctx.lineWidth = part === 'R_arm' || part === 'both' ? 6 : 3;
    ctx.beginPath();
    ctx.moveTo(cx, cy - 42);
    ctx.lineTo(cx + 38, part === 'R_arm' || part === 'both' ? cy - 72 : cy - 15);
    ctx.stroke();

    // Left Leg (Lane 2)
    ctx.strokeStyle = part === 'L_leg' || part === 'both' ? LANE_COLORS[2] : '#475569';
    ctx.lineWidth = part === 'L_leg' || part === 'both' ? 6 : 3;
    ctx.beginPath();
    ctx.moveTo(cx, cy + 10);
    ctx.lineTo(cx - 28, part === 'L_leg' ? cy + 48 : cy + 68);
    ctx.stroke();

    // Right Leg (Lane 3)
    ctx.strokeStyle = part === 'R_leg' || part === 'both' ? LANE_COLORS[3] : '#475569';
    ctx.lineWidth = part === 'R_leg' || part === 'both' ? 6 : 3;
    ctx.beginPath();
    ctx.moveTo(cx, cy + 10);
    ctx.lineTo(cx + 28, part === 'R_leg' ? cy + 48 : cy + 68);
    ctx.stroke();

    // Current move badge
    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 12px Inter, sans-serif';
    ctx.textAlign = 'center';
    const moveText = activeMove ? `${activeMove.label} [${activeMove.key}]` : 'READY STANCE';
    ctx.fillText(moveText, cx, y + h - 36);

    if (state.practiceLoop) {
      ctx.fillStyle = '#fee440';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.fillText(`PRACTICE LOOP: ${state.practiceLoop.start.toFixed(1)}s - ${state.practiceLoop.end.toFixed(1)}s`, cx, y + h - 16);
    }
  }

  function showResultsModal(summary) {
    const modal = document.getElementById('results-modal');
    if (!modal) return;
    modal.classList.remove('hidden');
    document.getElementById('res-rank').textContent = summary.rank;
    document.getElementById('res-score').textContent = summary.score.toLocaleString();
    document.getElementById('res-acc').textContent = summary.accuracy.toFixed(2) + '%';
    document.getElementById('res-combo').textContent = summary.maxCombo + 'x';
    document.getElementById('res-breakdown').textContent =
      `PERFECT: ${summary.perfect}  ·  GOOD: ${summary.good}  ·  MISS: ${summary.miss}`;

    const listEl = document.getElementById('missed-moves-list');
    listEl.innerHTML = '';

    // Show missed moves, or if 0 missed moves (100% Perfect!), show high-energy choreography checkpoints to practice
    const items = summary.missedMoves.length > 0
      ? summary.missedMoves
      : (state.judge ? state.judge.notes.filter((n) => n.energy >= 0.88).slice(0, 5) : []);

    const headerEl = document.getElementById('missed-section-title');
    if (headerEl) {
      headerEl.textContent = summary.missedMoves.length > 0
        ? `Missed Move Practice Timestamps (${summary.missedMoves.length} Moves — Click to Loop Video)`
        : '100% Perfect Clear! Key High-Energy Choreography Checkpoints (Click to Loop Video)';
    }

    items.forEach((mv) => {
      const btn = document.createElement('button');
      btn.className = 'practice-chip';
      btn.innerHTML = `<span class="chip-time">[00:${mv.t.toFixed(2)}s]</span> <strong>${mv.label}</strong> <em>(${mv.part} · Key ${mv.key})</em> → Loop Move`;
      btn.addEventListener('click', () => {
        startPracticeLoop(mv);
      });
      listEl.appendChild(btn);
    });
  }

  function hideResultsModal() {
    const modal = document.getElementById('results-modal');
    if (modal) modal.classList.add('hidden');
  }

  function startPracticeLoop(mv) {
    hideResultsModal();
    const startT = Math.max(0.0, Number(mv.t) - 0.9);
    const endT = Math.min(state.duration, Number(mv.end_t || mv.t) + 1.5);
    state.practiceLoop = { start: startT, end: endT, move: mv };
    state.currentTime = startT;
    if (videoEl) {
      videoEl.currentTime = startT;
      videoEl.playbackRate = 0.8;
      videoEl.play().catch(() => {});
    }
  }

  function hexToRgba(hex, alpha) {
    const c = hex.replace('#', '');
    const r = parseInt(c.substring(0, 2), 16);
    const g = parseInt(c.substring(2, 4), 16);
    const b = parseInt(c.substring(4, 6), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  // Deterministic clock seek hook for verification
  global.__seek = function (t) {
    state.playing = false;
    state.currentTime = Number(t);
    if (videoEl) {
      try {
        videoEl.currentTime = state.currentTime;
      } catch (_) {}
    }
    renderFrame(state.currentTime);
    return {
      currentTime: state.currentTime,
      difficulty: state.difficulty,
      score: state.judge ? state.judge.score : 0,
    };
  };

  // Deterministic Auto-Player verification hook
  global.__runAutoPlayer = async function (mode = 'perfect', difficulty = null) {
    while (!state.chartData) {
      await new Promise((r) => setTimeout(r, 30));
    }
    const targetDiff = difficulty || state.difficulty || 'Normal';
    selectDifficulty(targetDiff);
    state.playing = false;

    const judge = state.judge;
    const offsetSec = mode === 'jitter_120ms' ? 0.120 : 0.0;
    const dt = 0.010; // 10ms deterministic simulation step
    let noteCursor = 0;
    const sortedNotes = judge.notes.slice().sort((a, b) => a.t - b.t);

    for (let t = 0.0; t <= state.duration + 0.25; t = Number((t + dt).toFixed(4))) {
      // Inject scheduled inputs at note.t + offsetSec
      while (noteCursor < sortedNotes.length && t >= sortedNotes[noteCursor].t + offsetSec - 1e-5) {
        const targetNote = sortedNotes[noteCursor];
        const injectTime = Number((targetNote.t + offsetSec).toFixed(4));
        judge.onKeyDown(targetNote.lane, injectTime);
        noteCursor += 1;
      }
      judge.step(t, [true, true, true, true]);
    }

    // Render sample frames & show results screen
    state.currentTime = state.duration * 0.5;
    renderFrame(state.currentTime);
    updateHUD();
    const summary = judge.getSummary(targetDiff);
    showResultsModal(summary);

    return Object.assign({}, summary, {
      mode: mode,
      offsetMs: Math.round(offsetSec * 1000),
      consoleErrors: state.consoleErrors.slice(),
    });
  };

  initGame();
})(window);
"""

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>YourDancer — 4-Lane Choreography Rhythm Game</title>
  <style>
    :root {
      --bg: #070913;
      --panel: rgba(15, 20, 38, 0.88);
      --cyan: #00f5d4;
      --magenta: #ff2a85;
      --amber: #fee440;
      --violet: #a855f7;
      --text: #f8fafc;
      --muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      overflow: hidden;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 16px;
      background: rgba(10, 14, 28, 0.95);
      border-bottom: 1px solid rgba(0, 245, 212, 0.25);
      z-index: 10;
      gap: 12px;
      flex-wrap: wrap;
    }
    .song-info h1 { font-size: 15px; font-weight: 700; color: var(--cyan); }
    .song-info p { font-size: 11px; color: var(--muted); }
    .hud-stats {
      display: flex;
      gap: 18px;
      align-items: center;
    }
    .stat-box { text-align: center; }
    .stat-box span { display: block; font-size: 10px; color: var(--muted); text-transform: uppercase; }
    .stat-box strong { font-size: 16px; font-weight: 800; color: #fff; font-variant-numeric: tabular-nums; }
    .controls-bar {
      display: flex;
      gap: 6px;
      align-items: center;
    }
    button {
      background: rgba(30, 41, 69, 0.9);
      color: #e2e8f0;
      border: 1px solid rgba(148, 163, 184, 0.35);
      border-radius: 6px;
      padding: 5px 10px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }
    button:hover { border-color: var(--cyan); color: #fff; }
    button.active {
      background: var(--cyan);
      color: #060913;
      border-color: var(--cyan);
    }
    .btn-primary {
      background: var(--magenta);
      border-color: var(--magenta);
      color: #fff;
    }
    #stage-container {
      position: relative;
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #05070f;
      overflow: hidden;
    }
    #dance-video {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0.52;
      pointer-events: none;
    }
    #game-canvas {
      position: relative;
      z-index: 2;
      max-width: 100%;
      max-height: 100%;
      border-left: 1px solid rgba(255,255,255,0.1);
      border-right: 1px solid rgba(255,255,255,0.1);
    }
    .touch-controls {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      padding: 6px 16px;
      background: rgba(8, 11, 22, 0.95);
      border-top: 1px solid rgba(255,255,255,0.12);
      z-index: 10;
    }
    .touch-pad {
      padding: 8px 4px;
      text-align: center;
      font-weight: 700;
      font-size: 12px;
      border-radius: 6px;
      user-select: none;
    }
    .pad-0 { border: 1px solid var(--cyan); color: var(--cyan); }
    .pad-1 { border: 1px solid var(--magenta); color: var(--magenta); }
    .pad-2 { border: 1px solid var(--amber); color: var(--amber); }
    .pad-3 { border: 1px solid var(--violet); color: var(--violet); }
    .modal-overlay {
      position: absolute;
      inset: 0;
      background: rgba(5, 8, 18, 0.88);
      backdrop-filter: blur(8px);
      z-index: 30;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .hidden { display: none !important; }
    .results-card {
      background: #0f1629;
      border: 1px solid rgba(0, 245, 212, 0.45);
      border-radius: 12px;
      max-width: 620px;
      width: 100%;
      padding: 20px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.7);
    }
    .results-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }
    .rank-badge {
      font-size: 42px;
      font-weight: 900;
      color: var(--cyan);
      line-height: 1;
      padding: 6px 16px;
      border: 2px solid var(--cyan);
      border-radius: 10px;
    }
    .results-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-bottom: 12px;
    }
    .res-metric {
      background: rgba(255,255,255,0.04);
      padding: 10px;
      border-radius: 8px;
      text-align: center;
    }
    .res-metric span { font-size: 11px; color: var(--muted); display: block; }
    .res-metric strong { font-size: 20px; color: #fff; }
    .missed-box {
      margin-top: 12px;
      border-top: 1px solid rgba(255,255,255,0.12);
      padding-top: 10px;
    }
    .missed-box h3 {
      font-size: 12px;
      color: var(--amber);
      margin-bottom: 8px;
      text-transform: uppercase;
    }
    #missed-moves-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      max-height: 150px;
      overflow-y: auto;
    }
    .practice-chip {
      text-align: left;
      padding: 7px 10px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(254, 228, 64, 0.35);
      font-size: 12px;
      color: #f8fafc;
    }
    .practice-chip .chip-time { color: var(--cyan); font-family: monospace; margin-right: 6px; }
  </style>
</head>
<body>
  <header>
    <div class="song-info">
      <h1 id="song-title">Loading Chart...</h1>
      <p id="song-meta">4-Lane Limb Choreography Rhythm Game</p>
    </div>
    <div class="hud-stats">
      <div class="stat-box"><span>Score</span><strong id="hud-score">0</strong></div>
      <div class="stat-box"><span>Combo</span><strong id="hud-combo">0x</strong></div>
      <div class="stat-box"><span>Mult</span><strong id="hud-mult">1.0x</strong></div>
      <div class="stat-box"><span>Accuracy</span><strong id="hud-acc">100.0%</strong></div>
    </div>
    <div class="controls-bar">
      <button class="diff-btn" data-diff="Easy">Easy</button>
      <button class="diff-btn active" data-diff="Normal">Normal</button>
      <button class="diff-btn" data-diff="Hard">Hard</button>
      <button id="btn-autoplay">AUTO-PLAY: OFF</button>
      <button id="btn-start" class="btn-primary">PLAY ROUTINE</button>
      <button id="btn-results">RESULTS</button>
    </div>
  </header>

  <div id="stage-container">
    <video id="dance-video" src="video.mp4" playsinline preload="auto" muted></video>
    <canvas id="game-canvas" width="760" height="430"></canvas>

    <div id="results-modal" class="modal-overlay hidden">
      <div class="results-card">
        <div class="results-header">
          <div>
            <h2 style="font-size: 18px;">Routine Performance Report</h2>
            <p id="res-breakdown" style="font-size: 12px; color: var(--muted); margin-top: 4px;"></p>
          </div>
          <div id="res-rank" class="rank-badge">S</div>
        </div>
        <div class="results-grid">
          <div class="res-metric"><span>Total Score</span><strong id="res-score">0</strong></div>
          <div class="res-metric"><span>Accuracy</span><strong id="res-acc">100.0%</strong></div>
          <div class="res-metric"><span>Max Combo</span><strong id="res-combo">0x</strong></div>
        </div>
        <div class="missed-box">
          <h3 id="missed-section-title">Missed Move Practice Timestamps</h3>
          <div id="missed-moves-list"></div>
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 14px;">
          <button id="btn-close-results" class="btn-primary">Resume / Practice Video</button>
        </div>
      </div>
    </div>
  </div>

  <div class="touch-controls">
    <button class="touch-pad pad-0" data-lane="0">[D] LEFT ARM</button>
    <button class="touch-pad pad-1" data-lane="1">[F] RIGHT ARM</button>
    <button class="touch-pad pad-2" data-lane="2">[J] LEFT LEG</button>
    <button class="touch-pad pad-3" data-lane="3">[K] RIGHT LEG</button>
  </div>

  <script src="judge.js"></script>
  <script src="game.js"></script>
</body>
</html>
"""


def generate_rhythm_game_bundle(
    job_dir: Path,
    video_path: Path,
    chart_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Writes the multi-file HTML5 Canvas 2D rhythm game bundle into `job_dir / "game"`:
      - index.html
      - judge.js
      - game.js
      - chart.json
      - video.mp4
    """
    game_dir = job_dir / "game"
    game_dir.mkdir(parents=True, exist_ok=True)

    chart_path = game_dir / "chart.json"
    chart_path.write_text(json.dumps(chart_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    (game_dir / "judge.js").write_text(JUDGE_JS.strip() + "\n", encoding="utf-8")
    (game_dir / "game.js").write_text(GAME_JS.strip() + "\n", encoding="utf-8")
    (game_dir / "index.html").write_text(INDEX_HTML.strip() + "\n", encoding="utf-8")

    target_video = game_dir / "video.mp4"
    if not target_video.exists() or target_video.stat().st_size != video_path.stat().st_size:
        shutil.copy2(video_path, target_video)

    return {
        "game_dir": str(game_dir),
        "files": ["index.html", "game.js", "judge.js", "chart.json", "video.mp4"],
    }
