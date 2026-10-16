// YourDancer — 4-Lane Rhythm Game Judgement & Combo Engine (judge.js)
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
