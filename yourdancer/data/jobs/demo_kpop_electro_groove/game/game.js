// YourDancer — 4-Lane HTML5 Canvas Rhythm Game + Deterministic Auto-Player (game.js)
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
