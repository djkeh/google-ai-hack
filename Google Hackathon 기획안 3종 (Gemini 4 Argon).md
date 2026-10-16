# Google Hackathon 기획안 3종 (Gemini 4 Argon)

Oct 16, 2026 · @Uno Kim

## 0. 공통 전제 (세 안 모두에 적용)

세 기획안은 각각 독립적으로 새 AI 에이전트 세션(Antigravity, AI Studio Build, agy CLI)에 붙여 넣어 바로 구체화·구현을 시작할 수 있게 작성했다. 선택한 안의 섹션 전체와 이 0절을 함께 넘기면 된다.

### 해커톤 규칙 요약

- Google AI 기술 필수 사용, Google Cloud에 배포해 서비스 형태로 시연·검증 가능해야 함.
- 제출물 3종(모두 영어): Project Description, Public GitHub Repository, Demo Video(YouTube/Drive 링크).
- 시연 코드는 해커톤 기간 내 작성. 오픈소스 라이브러리·스타터 템플릿은 허용. 데모용 입력 데이터(영상, 음원, 버그 심은 레포)는 코드가 아니므로 사전 준비 가능하나 README에 명시.
- 금지: 기존 프로젝트 재제출, 단순 PDF 챗봇·Q&A 봇, 자율 추론·검증 루프·멀티모달 워크플로우 없는 정적 페이지, Human-in-the-loop 없는 의료·정신건강·금융 봇.

### 심사 기준과 각 안이 답해야 할 질문

| 기준 | 심사위원이 묻는 것 | 기획안에서 확보할 증거 |
| --- | --- | --- |
| Working Live Demo | 실제 입력으로 에러 없이 3분 내 구동되는가, Argon·Managed Agents·컴패니언 모델을 검증 루프와 함께 썼는가 | 데모 대본, 사전 실행 범위 명시, 실패→패치→통과 로그 1건 이상 |
| Problem & Impact | 특정 사용자의 구체적 문제인가, 오늘 이후 쓰일 제품이 되는가 | 이름 붙일 수 있는 사용자 1명(가능하면 본인), 현재 소요 시간·비용 수치 |
| Originality | 기존에 없던 접근인가, Argon의 1M 컨텍스트·long decode·frontier reasoning·멀티모달 오케스트레이션 덕에 가능한가 | 기존 제품과의 차이를 첫 문장에, Argon 전용 기능 매핑표 |
| Clarity | 소개글·영상에서 타겟과 가치가 명확한가 | 영문 설명 초안, 3분 영상 대본 |

### 공통 빌드 원칙

1. 의도 정렬 먼저: Argon에게 목표를 주고 질문·엣지 케이스·아키텍처 트레이드오프를 먼저 받은 뒤 승인하고, 그다음 멀티파일 빌드를 통째로 맡긴다.
2. 검증 루프는 구체적 pass/fail 신호(테스트, 콘솔 에러 0, 수치 임계값)로 정의한다. 신호가 없으면 심사에서 검증 루프로 인정되지 않는다.
3. 느린 모델(gemini-omni 비디오, 1M 이상 long decode, 10분 넘는 렌더)은 라이브 데모의 크리티컬 패스에 두지 않는다. 사전 실행 결과를 보여주고 빠른 단계만 라이브로 돌린다.
4. 외부 시스템·돈·개인정보를 건드리는 액션에는 사람 승인 단계를 둔다.
5. 타임박스를 지킨다. 각 안의 시간표에 적힌 폴백으로 전환하는 기준 시각을 넘기면 미련 없이 전환한다.
6. Argon 호출 규칙(builder guide 기준): Interactions API, google-genai 2.3.0 이상, thinking\_level(low/medium/high) 사용, temperature·top\_p·top\_k·thinking\_budget·cached\_content 제거, 긴 작업은 background=True와 max\_output\_tokens 상향, HTTP 타임아웃 15\~20분.
7. 코딩 에이전트에 Gemini API 스킬을 먼저 설치한다: `npx skills add google-gemini/gemini-skills --skill gemini-api-dev`, `--skill gemini-live-api-dev`, 또는 `agy plugin install https://github.com/google-gemini/gemini-skills`.
8. 저장소 구조는 처음부터 공개 가능하게: README(영문, 아키텍처 그림, 실행 방법, 데모 데이터 출처), LICENSE, `.env.example`, 비밀값 커밋 금지.

### 공통 GCP 구성

- Cloud Run(API, 컨테이너), Cloud Run Jobs(긴 파이프라인·샌드박스 대체), Cloud Storage(입력·출력 파일, 정적 호스팅), Firestore(잡 상태·실시간 대시보드), Firebase Auth(필요 시 로그인).
- Antigravity managed agent(antigravity-preview-09-2026)는 킥오프에서 샌드박스 안 브라우저 구동 여부를 확인한 뒤 쓴다. 안 되면 Cloud Run Job 안에서 Argon API를 직접 호출하는 루프로 대체한다. 둘 다 검증 루프로 인정된다.

### 새 에이전트 세션에 넘기는 방법

1. 선택한 안의 섹션과 이 0절을 복사해 첫 메시지로 붙인다.
2. 각 안에 있는 "첫 프롬프트"를 이어서 보내고, 에이전트가 낸 질문에 답한 뒤 빌드를 승인한다.
3. 에이전트가 비표준 설정 문제를 풀 때마다 AGENTS.md에 기록하게 한다.
4. 마지막 1시간은 데모 영상·영문 설명·README에 쓴다. 코드 완성도보다 제출물 3종이 우선이다.

## A. Choreograph — 곡을 이해해 캐릭터 연출 프로그램을 쓰고 스스로 검수하는 AI 모션그래픽 디렉터 (트랙 1)

곡 하나를 올리면 Argon이 곡을 듣고 주인공 캐릭터와 시간별 연출 대본(Visual Score)을 쓰고, 그 대본을 실행하는 2D 스프라이트 애니메이션 페이지를 생성한 뒤, 결과를 스스로 시청하며 고친다. 1차 산출물은 음악과 함께 재생되는 웹 페이지, mp4 내보내기는 스트레치.

### 사용자와 문제

- 타겟: 클래식·인디 음악을 YouTube에 올리는 1인 크리에이터. 본인이 드뷔시 달빛, 고도프스키 식물원 영상을 직접 만든 경험이 사례다.
- 문제: 곡의 특정 구간(예: 2:06의 피아노 고음에 물방울)에 이유 있는 연출을 넣고 동기화하는 작업은 전부 수작업이며 한 편에 수 시간이 든다. 피치에서는 실제 소요 시간을 수치로 말한다.
- 기존 제품(Neural Frames, Freebeat, Compeller)은 AI가 픽셀을 생성하고 음량으로 변조한다. 곡의 의미를 읽고 "왜 이 순간에 이 연출인가"를 결정하는 제품은 없다. 제출명과 첫 문장에서 "AI music video generator가 아니라 AI motion-graphics director"로 못 박는다.

### Argon 전용 기능 매핑

| Argon 기능 | 이 제품에서의 역할 |
| --- | --- |
| 오디오 네이티브 멀티모달 이해 + 1M 컨텍스트 | 원본 오디오, librosa 특징, 가사, 사용자 설명을 한 컨텍스트에서 읽고 Visual Score 작성 |
| long decode 멀티파일 생성 | index.html, scene.js, motion.js, score.json을 한 번에 생성 |
| agentic video understanding | 자기 렌더 결과(프록시 영상)를 오디오와 함께 시청하고 체크리스트 채점 |
| 오케스트레이션 | gemini-nano-banana-2.1(캐릭터 시트), gemini-3.5-transcribe(가사), gemini-3.8-flash(채점 보조) 호출 |

### 파이프라인

1. 업로드: mp3/wav + 선택 입력(설명 텍스트, 레퍼런스 이미지 1장). GCS 서명 URL로 직접 업로드, Firestore에 잡 생성.
2. 분석: librosa로 BPM, beats, onsets, RMS 곡선, 스펙트럴 센트로이드, 섹션 경계(novelty 기반)를 JSON으로 추출. 가사가 있으면 gemini-3.5-transcribe. Argon(thinking\_level high)에 원본 오디오 + 특징 JSON + 사용자 텍스트를 넣어 Visual Score JSON을 받는다.
3. 캐릭터 시트: Argon이 캐릭터 콘셉트와 8개 포즈 목록(idle, bounce, step-L, step-R, arms-up, spin, jump, hold)을 쓰고, gemini-nano-banana-2.1로 동일 캐릭터 8장을 단색 #00FF00 배경에 생성한다. 코드에서 크로마키로 배경을 제거한다. 멀티턴 편집으로 일관성을 유지한다.
4. 씬 생성: Argon(background=True, max\_output\_tokens 상향)이 Score와 시트를 받아 Three.js 또는 Canvas 2D 페이지를 멀티파일로 생성한다. 캐릭터 모션은 Score의 섹션별 motion\_vocab과 이벤트 타임라인으로, 미세 반응(스쿼시·스트레치, 파티클 강도, 카메라 줌)은 Web Audio AnalyserNode의 실시간 특징으로 구동한다. 페이지는 `window.__seek(t)`와 고정 스텝 클록을 노출해 결정론적 렌더가 가능하게 한다.
5. 검증 루프(Cloud Run Job, Playwright chromium `--use-angle=swiftshader`), 최대 3회:
   - a. 콘솔 에러 0, 곡 전체 길이 재생 완료, 평균 fps 24 이상.
   - b. 씬에 계측 훅을 넣어 Score의 모든 이벤트가 계획 시각 ±50ms에 발화했는지 단언.
   - c. 320p/10fps 프록시 렌더를 만들고 Argon이 오디오와 함께 시청해 체크리스트를 채점한다: 각 이벤트가 눈에 보이는가, 클라이맥스 구간의 밝기·움직임이 실제로 커지는가, 섹션 전환이 음악 전환과 일치하는가, 캐릭터가 프레임 밖으로 나가지 않는가. 불합격 항목을 코드 패치 후 재실행.
6. 결과: 생성 폴더를 GCS 정적 호스팅에 올리고 재생 링크를 발급. 스트레치: 1080p/30fps 헤드리스 프레임 캡처 + ffmpeg 오디오 먹싱으로 mp4 백그라운드 생성(3분 곡 기준 10\~15분).

### Visual Score 스키마

```json
{
  "title": "Dance of the Sugar Plum Fairy",
  "bpm": 120,
  "duration": 112.0,
  "character": {"concept": "sugar-plum fairy, tiny, glittering", "palette": ["#F9D5E5", "#6A4C93", "#FFF1B5"]},
  "sections": [
    {"start": 0.0, "end": 18.2, "mood": "hushed, curious", "energy": 0.2,
     "motion_vocab": ["tiptoe", "sway"], "background": "deep violet gradient, slow drift"}
  ],
  "events": [
    {"t": 54.3, "action": "jump", "trigger": "onset>0.8", "why": "celesta accent opens the B section"}
  ],
  "climax": {"start": 80.0, "end": 96.5}
}
```

`why` 필드는 심사에서 "이유 있는 연출"의 근거이고, 검증 c단계에서 Argon이 자기 의도를 확인하는 기준이다.

### 아키텍처

- 프론트: 업로드 폼 + 잡 상태 대시보드(Firestore 구독) + 결과 플레이어. Argon이 생성, GCS 정적 호스팅 또는 Cloud Run.
- API(Cloud Run, FastAPI): 서명 URL 발급, 잡 생성, 상태 조회, 결과 링크.
- 파이프라인(Cloud Run Job, 타임아웃 60분): librosa, Playwright, ffmpeg, Argon·Nano Banana·transcribe 호출, 검증 루프.
- 저장: GCS(오디오, 시트, 씬 폴더, 프록시·최종 영상), Firestore(잡 상태·단계 로그·채점 결과).
- 로그인: Firebase Auth 구글 로그인(30분, 후순위). YouTube 업로드는 범위 밖.

### 범위 결정

- 포함: 음악 분석, Visual Score, 2D 키프레임 스프라이트 캐릭터, 씬 생성, 검증 루프 a·b·c, 웹 플레이어, 설명 텍스트 입력, 레퍼런스 이미지 1장(팔레트 추출).
- 스트레치: mp4 내보내기, 구글 로그인.
- 제외: 레퍼런스 비주얼라이저 모드, 샘플 영상 입력, 저작권 프리 이미지 검색(생성으로 대체), 3D 캐릭터, YouTube 업로드.
- 폴백: 캐릭터 시트가 2시간 안에 안 나오면 같은 모션 코드로 테마 파티클(사탕 결정)을 움직인다. Playwright WebGL이 안 뜨면 Canvas 2D로 생성한다. 검증 c가 시간 부족이면 a·b만.

### 데모 데이터

- CC0 녹음 클래식 1곡(Musopen 등) + lyria-3.5 생성곡 1곡. YouTube 원곡은 녹음 저작권 때문에 데모 영상에 쓰지 않는다.
- 두 곡 모두 킥오프 후 사전 실행해 두고 라이브에서는 같은 곡을 다시 업로드해 단계 진행을 보여준다.

### 시간표 (킥오프 = H+0, 9시간)

| 시간 | 작업 | 통과 기준·폴백 |
| --- | --- | --- |
| H+0\~0.5 | 멘토 확인 4건(아래), 데모 곡 확보, 레포·GCP 프로젝트 생성 |  |
| H+0.5\~1.5 | 분석 파이프라인, Score 프롬프트 | 곡 1개로 Score JSON 생성 |
| H+1.5\~3.5 | 캐릭터 시트 생성, 크로마키 확인 | 2시간 초과 시 파티클 폴백 |
| H+3.5\~5.5 | 씬 생성, 브라우저 재생 확인 | 캐릭터 없이도 돌아가는 구조 유지 |
| H+5.5\~7 | 검증 루프 a·b·c, 실패→패치→통과 로그 1건 확보 | c 미완 시 a·b만 |
| H+7\~8 | Cloud Run 배포, 업로드 UI, 대시보드, 곡 2개 사전 실행 |  |
| H+8\~9 | 데모 영상, 영문 설명, README | mp4 잡은 여유 있을 때만 |

### 킥오프 확인 사항

- [ ] Argon에 3\~5분 오디오를 그대로 넣을 수 있는가(안 되면 섹션 분할 + librosa 특징 중심)
- [ ] Nano Banana 멀티턴 편집으로 캐릭터 일관성을 유지하는 권장 프롬프트 패턴
- [ ] Cloud Run Job 컨테이너에서 Playwright WebGL 구동 여부(안 되면 Canvas 2D)
- [ ] Antigravity 샌드박스에서 브라우저 구동 여부(되면 검증 루프를 샌드박스로)

### 새 에이전트 세션용 첫 프롬프트 (영어)

```text
I'm building "Choreograph" in a 1-day hackathon, solo, for Google's Gemini 4 Argon track 1 (entertainment).
Goal: a creator uploads a song; the system listens, writes a "Visual Score" (sections, mood, a themed 2D
character, timed events each with a reason), generates a Three.js/Canvas page that plays the song and animates
the character from the score plus live Web Audio features, then verifies its own output (headless run, event
timing assertions within 50 ms, a 320p proxy render that you review against the audio) and patches until
all checks pass. Primary output is the playable page; MP4 export is a stretch goal.

Stack: Python FastAPI on Cloud Run, a Cloud Run Job for the pipeline (librosa, Playwright chromium with
swiftshader, ffmpeg), GCS, Firestore, gemini-4-argon via the Interactions API, gemini-nano-banana-2.1 for an
8-pose character sheet on a flat #00FF00 background (chroma-keyed in the shader), gemini-3.5-transcribe for lyrics.

Before writing code: (1) list clarifying questions and edge cases, (2) propose the Visual Score JSON schema and
the contract between score.json and the generated scene (how events bind to onsets, how motion vocab maps to
sprite poses, how the page exposes a deterministic clock for rendering), (3) propose the verification checks
with concrete pass/fail signals, (4) flag the riskiest step and its fallback. Then wait for my go-ahead before
generating files. Record any non-obvious setup lessons in AGENTS.md as we go.
```

### 3분 라이브 데모 대본

1. 0:00 문제: 본인이 만든 달빛 영상 10초. "이 물방울 하나를 넣는 결정과 동기화에 N시간."
2. 0:30 업로드: 사전 실행된 곡을 라이브로 다시 업로드. 대시보드에 단계 진행.
3. 0:50 Score: 생성된 `events[].why`를 띄워 클라이맥스 연출의 이유를 읽는다.
4. 1:20 검증 루프: 실패→패치→통과 로그와 Argon이 프록시 렌더를 보고 쓴 검수 코멘트.
5. 1:50 결과: 생성 페이지 라이브 재생, 클라이맥스 30초.
6. 2:30 두 번째 장르(Lyria 전자음악) 결과 10초. "곡이 바뀌면 캐릭터와 연출이 바뀐다."
7. 2:50 마무리: 링크 전달, 텍스트 한 줄로 재생성, mp4 내보내기(있으면).

### 영문 Project Description 초안

```text
Choreograph — an AI motion-graphics director for music creators

Existing AI visualizers generate pixels and modulate them with loudness. Choreograph does what a human animator
does: it listens to the whole song, decides who the character is, writes a timed Visual Score with a reason for
every cue ("1:47 — climax, the fairy leaps on the fortissimo chord"), and then generates a complete animation
program that performs that score in sync with live audio features. Gemini 4 Argon is the director: it reads the
raw audio and lyrics in one context, emits the score and the multi-file scene in a single long decode, and then
verifies its own work — running the scene headlessly, asserting every cue fires within 50 ms, watching a proxy
render against the audio, and patching until all checks pass. Built for independent and classical music creators
who publish on YouTube and today spend hours hand-syncing visuals. Output is a playable page today and a 1080p
MP4 export as a background job.
```

### 리스크

| 리스크 | 영향 | 대응 |
| --- | --- | --- |
| 범위 과다 | 미완성 데모 | 범위 결정 표의 제외 항목을 건드리지 않는다 |
| 캐릭터 일관성 실패 | 테마성 상실 | 파티클 폴백, 모션 코드는 공유 |
| LLM 타임스탬프 해상도(약 1초) | 이벤트 싱크 어긋남 | 모든 이벤트 시각을 librosa 온셋에 스냅 |
| 헤드리스 WebGL | 검증·렌더 불가 | Canvas 2D 생성, swiftshader |
| 음원 저작권 | 제출물 문제 | CC0 녹음·Lyria만 사용 |

## B. MoveChart — 안무 영상 한 편을 플레이 가능한 리듬게임으로 바꾸는 생성기 (트랙 1)

댄스 연습 영상을 올리면 Argon이 영상을 스크럽해 댄서의 동작 단위(어느 팔·다리가 언제 움직이는가)를 뽑고, 그것을 4레인 노트 차트로 바꾼 뒤, 그 차트를 플레이하는 리듬게임을 멀티파일로 생성한다. 검증은 차트 규칙 검사와 헤드리스 오토플레이어로 한다.

### 사용자와 문제

- 타겟: 커버댄스 연습생과 댄스 크루. 안무를 외울 때 "어느 박에 어느 동작"을 몸에 붙이는 과정이 길다.
- 문제: 리듬게임 차트 제작은 곡당 수 시간이 들고(Beat Saber 커스텀 맵 커뮤니티가 그렇다), 기존 자동 생성기(Beat Sage, Melokai, DeepSaber 연구)는 전부 오디오만 보고 노트를 찍는다. 안무 영상에서 동작을 노트로 바꾸는 제품은 없다.
- 결과 화면의 "가장 많이 놓친 동작 구간"을 영상 타임스탬프로 보여 주면 연습 도구가 된다.

### 게임 규칙

- 4레인: 왼팔·오른팔·왼발·오른발. 키보드 D·F·J·K, 모바일은 4분할 터치. 점프·턴 같은 전신 동작은 양손 동시 노트.
- 배경에 원본 안무 영상이 재생되고, 노트는 댄서가 그 동작을 치는 순간(임팩트 프레임)에 판정선에 도달한다. 플레이어는 댄서를 보며 다음 노트를 예측할 수 있다.
- 판정: Perfect ±50ms 300점, Good ±100ms 100점, Miss 0점. 콤보 10마다 배율 +0.1(최대 2.0). 홀드 노트는 동작이 지속되는 구간(웨이브, 슬라이드).
- 난이도 Easy/Normal/Hard: 같은 영상에서 노트 밀도만 다르다. Easy는 소절 단위 주요 동작, Hard는 8분음표 단위 세부 동작.
- 결과: 점수, 최대 콤보, 정확도(%), 랭크(S/A/B/C), 놓친 동작 구간 타임스탬프.

### Argon 전용 기능 매핑

| Argon 기능 | 이 제품에서의 역할 |
| --- | --- |
| agentic video understanding | 영상을 스크럽해 동작 단위와 신체 부위, 임팩트 시각을 JSON으로 추출 |
| long decode 멀티파일 생성 | 게임 전체(index.html, game.js, judge.js, chart.json, 결과 화면)를 한 번에 생성 |
| frontier reasoning | 난이도별 밀도 조절과 차트 규칙 위반 수정 |
| 오케스트레이션 | lyria-3.5(데모용 음원), gemini-3.8-flash(차트 규칙 검사 보조) |

### 파이프라인

1. 업로드: 안무 영상(mp4, 1\~2분) GCS 업로드, Gemini Files API 등록, Firestore 잡 생성.
2. 동작 추출: Argon(thinking\_level high)이 영상을 보고 `{t, part: L_arm|R_arm|L_leg|R_leg|both, type: hit|hold, end, label}` 목록과 구간별 에너지를 출력한다.
3. 정밀도 보정: LLM 타임스탬프는 1초 내외 해상도라 ±50ms 판정에 직접 쓸 수 없다. librosa로 오디오 온셋과 비트 그리드를 뽑아 Argon이 찍은 시각을 가장 가까운 온셋에 스냅한다. Argon은 의미(어떤 동작), 신호처리는 정밀도(언제)를 맡는다.
4. 차트 생성: 스냅된 이벤트를 난이도별 규칙으로 필터·확장해 chart.json 3개를 만든다.
5. 게임 생성: Argon(background=True)이 chart.json 스키마를 읽는 Canvas 2D 리듬게임을 멀티파일로 생성한다. 영상 배경은 `<video>` 요소와 오디오 클록으로 동기화한다.
6. 검증 루프, 최대 3회:
   - a. 차트 규칙 검사(Python): 같은 레인 80ms 이내 중복 금지, 난이도별 초당 노트 수 상한(Easy 2, Normal 4, Hard 7), 홀드 겹침 금지, 모든 노트가 영상 길이 안. 위반 시 Argon이 차트 재생성.
   - b. 헤드리스 오토플레이어(Playwright): 생성된 게임을 띄우고 chart.json대로 완벽 타이밍에 키 입력을 주입해 정확도 100%, 콘솔 에러 0을 확인. 실패하면 게임 코드 버그이므로 Argon이 패치.
   - c. 선택: 오토플레이어를 ±120ms로 흔들어 Miss가 발생하는지 확인(판정 로직이 실제로 동작하는 증거).
7. 결과: 게임 폴더를 GCS 정적 호스팅에 올리고 플레이 링크 발급.

### 아키텍처

- 프론트: 업로드 + 잡 상태 + 플레이 링크. Argon 생성.
- API(Cloud Run, FastAPI): 서명 URL, 잡 생성·조회.
- 파이프라인(Cloud Run Job): Files API 업로드, Argon 호출, librosa, 차트 검사, Playwright 오토플레이어.
- 저장: GCS(영상, 차트, 게임 폴더), Firestore(잡 상태·검증 로그).

### 범위 결정

- 포함: 동작 추출, 온셋 스냅, 3단계 난이도 차트, 키보드 4레인 게임, 검증 a·b, 결과 화면, 플레이 링크.
- 스트레치: 모바일 터치, 웹캠 포즈 비교 모드, 검증 c.
- 제외: 멀티플레이, 리더보드, 사용자 로그인, 3D.
- 폴백: 영상 분석이 늦으면 분석 결과를 캐시해 두고 라이브에서는 게임 생성부터 보여 준다. 오토플레이어가 안 되면 차트 규칙 검사와 수동 플레이 영상으로 대체한다.

### 데모 데이터

- 음원: lyria-3.5로 60\~90초 곡 생성(저작권 회피). 킥오프 직후 생성.
- 영상: 그 곡에 맞춰 본인 또는 동료가 폰으로 촬영한 60초 안무, 또는 CC 라이선스 댄스 영상. YouTube K-pop 연습 영상은 데모 영상에 쓰지 않는다.
- 영상 촬영 30\~40분을 시간표에 넣는다. 코드가 아니므로 규칙 위반이 아니며 README에 출처를 쓴다.

### 시간표 (킥오프 = H+0, 9시간)

| 시간 | 작업 | 통과 기준·폴백 |
| --- | --- | --- |
| H+0\~0.7 | Lyria 곡 생성, 안무 촬영, 레포·GCP 생성, 멘토 확인 |  |
| H+0.7\~2.2 | 동작 추출 프롬프트, librosa 온셋, 스냅 | 이벤트 JSON에서 눈으로 5개 확인 |
| H+2.2\~3.2 | 차트 생성과 규칙 검사기 | 3난이도 모두 검사 통과 |
| H+3.2\~5.2 | 게임 생성과 수동 플레이 확인 | 오디오·영상 싱크가 체감상 맞음 |
| H+5.2\~6.2 | 오토플레이어, 실패→패치→통과 로그 확보 | 미완 시 규칙 검사만 |
| H+6.2\~7 | Cloud Run 배포, 업로드 UI, 사전 실행 |  |
| H+7\~8 | 두 번째 영상으로 재현성 확인, 결과 화면 다듬기 |  |
| H+8\~9 | 데모 영상, 영문 설명, README |  |

### 킥오프 확인 사항

- [ ] Argon 영상 입력 길이·해상도 한도와 타임스탬프 출력 형식
- [ ] Files API 업로드 후 처리 대기 시간
- [ ] Lyria 생성곡의 라이선스 범위(데모 영상 공개 가능 여부)
- [ ] 샌드박스에서 Playwright 구동 여부

### 새 에이전트 세션용 첫 프롬프트 (영어)

```text
I'm building "MoveChart" in a 1-day hackathon, solo, for Google's Gemini 4 Argon track 1 (entertainment).
Goal: a user uploads a 1-2 minute dance practice video; Argon scrubs the video and extracts the dancer's
move units (which limb, impact time, hold duration); we snap those times to audio onsets from librosa; we
build 4-lane rhythm-game charts (L arm, R arm, L leg, R leg) at three difficulties; Argon generates the whole
Canvas 2D rhythm game (video background, timing judgement, scoring, results screen) in one multi-file pass;
and a verification loop checks chart rules and runs a headless Playwright auto-player that must score 100%
with zero console errors before the game is published.

Stack: Python FastAPI on Cloud Run, Cloud Run Job for the pipeline (Gemini Files API, librosa, Playwright),
GCS static hosting for generated games, Firestore for job state, gemini-4-argon via the Interactions API,
lyria-3.5 for the demo track.

Before writing code: (1) list clarifying questions and edge cases, (2) propose the move-event JSON schema and
the chart.json schema, (3) propose the chart rule checks and the auto-player protocol (how the game exposes
a deterministic clock and accepts injected key events), (4) flag the riskiest step and its fallback. Wait for
my go-ahead before generating files. Record setup lessons in AGENTS.md.
```

### 3분 라이브 데모 대본

1. 0:00 문제: 커버댄스 연습생의 암기 과정과 차트 수작업 시간.
2. 0:25 업로드: 사전 분석된 영상을 라이브로 업로드, 대시보드에 추출된 동작 목록이 영상 타임스탬프와 함께 뜸.
3. 0:55 검증: 차트 규칙 위반 1건이 잡혀 재생성되는 로그, 오토플레이어 100% 통과 화면.
4. 1:25 플레이: 심사위원 앞에서 Normal 난이도 60초 직접 플레이, 영상 배경과 노트 동기.
5. 2:30 결과 화면: 점수·랭크·놓친 동작 구간 타임스탬프.
6. 2:50 마무리: 어떤 안무 영상이든 몇 분 안에 게임이 된다, 링크 공유.

### 영문 Project Description 초안

```text
MoveChart — turn any dance video into a playable rhythm game

Rhythm-game charts take hours to make by hand, and every automatic generator so far listens only to the
audio. MoveChart watches the dancer. Gemini 4 Argon scrubs a dance practice video, identifies each move
(which limb, when it lands, how long it holds), and we snap those moments to audio onsets for 50 ms
precision. Argon then generates the complete four-lane rhythm game — video background, timing judgement,
combo scoring, results — in a single multi-file pass, and a verification loop refuses to publish until the
chart passes playability rules and a headless auto-player scores 100% with no errors. For cover-dance
learners and crews, the results screen marks the moves they missed with timestamps into the original video.
Built on Cloud Run, Cloud Storage and Firestore.
```

### 리스크

| 리스크 | 영향 | 대응 |
| --- | --- | --- |
| LLM 타임스탬프 해상도 | 판정 불가 수준의 오차 | 온셋 스냅 필수, 스냅 거리 통계를 로그로 남김 |
| 영상 배경과 오디오 싱크 드리프트 | 플레이 체감 저하 | 오디오 클록을 단일 기준으로, 영상은 주기적 재동기 |
| 게임 코드 버그를 본인이 못 고침 | 데모 중단 | 오토플레이어가 잡게 하고 Argon에 패치 위임 |
| 데모 음원·영상 저작권 | 제출 문제 | Lyria + 자체 촬영 |
| 라이브 분석 시간 초과 | 3분 초과 | 분석은 사전 실행, 플레이를 라이브로 |

## C. ReproFix — 버그 화면 녹화만으로 실패하는 테스트를 먼저 만들고, 고치고, PR을 여는 에이전트 (트랙 4)

사용자가 버그 장면을 녹화한 mp4를 올리면 Argon이 영상에서 재현 단계를 뽑아 Playwright 테스트를 작성하고, 그 테스트가 실제로 실패하는 것을 확인한 뒤에만 코드를 고쳐 테스트를 통과시키고, 사람이 머지하는 PR을 연다. 계측 도구나 확장 프로그램 없이 날것의 영상만으로 출발하는 것이 차별점이다.

### 사용자와 문제

- 타겟: 소규모 웹 서비스 개발자. QA나 고객이 보낸 "4분짜리 말 없는 화면 녹화"를 받아 재현 단계를 직접 적고 테스트를 쓰는 데 시간을 쓴다.
- 기존 제품: Jam.dev는 자체 녹화 도구로 클릭·콘솔·네트워크를 계측하고 에이전트가 PR까지 연다. Warp는 에이전트가 재현 과정을 녹화한다. SceneRecap은 Gemini로 녹화 영상에서 버그 리포트를 쓰지만 수정은 안 한다.
- 차별점 세 가지를 피치 첫 문장에 넣는다: 계측 없는 날 영상 입력, 재현 테스트가 반드시 먼저 실패(red)해야 수정으로 넘어가는 검증 루프, 비밀값이 모델 컨텍스트에 들어가지 않는 자격증명 처리.

### Argon 전용 기능 매핑

| Argon 기능 | 이 제품에서의 역할 |
| --- | --- |
| agentic video understanding | 영상을 스크럽해 클릭한 요소의 위치·텍스트, 입력값, 에러 문자열, 버그 발생 타임스탬프 추출 |
| 1M 컨텍스트 | 레포 전체 + 영상 + 콘솔 로그를 한 컨텍스트에서 보고 원인 코드 위치 추정 |
| Antigravity managed agent | 샌드박스에서 clone, 설치, dev 서버, Playwright 실행, 패치, push |
| Credentials API + 네트워크 allowlist | GitHub 토큰을 프록시에서 주입, github.com·npm 레지스트리만 허용 |
| 오케스트레이션 | gemini-3.8-flash(셀렉터 후보 탐색, 기존 테스트 요약), gemini-3.5-flash-lite(단계 분류) |

### 대상 범위

- Node 기반 웹앱만: `npm ci && npm run dev`로 뜨고 Playwright가 붙을 수 있는 레포. 범용 지원은 하루에 불가능하다.
- 데모 레포: 작은 공개 앱(TodoMVC 계열 또는 간단한 Next.js 앱)을 포크해 버그 1\~2개를 심어 둔다. 스타터 템플릿에 해당하므로 README에 명시한다.

### 파이프라인

1. 녹화·업로드: 제품 웹페이지의 "녹화" 버튼이 `getDisplayMedia` + `MediaRecorder`로 탭을 webm으로 녹화해 바로 업로드한다(확장 프로그램 불필요, 50줄 내외). 기존 mp4 업로드도 받는다. 콘솔 로그는 선택 입력으로 붙여넣기.
2. 분석: Cloud Run → GCS 저장 → Gemini Files API 등록 → Argon(thinking\_level high)이 영상 + 레포 메타(URL, 프레임워크, 라우트 목록) + 로그를 받아 구조화 출력: 재현 단계(요소 텍스트·위치·입력값), 기대 동작 vs 실제 동작, 버그 타임스탬프, 화면 에러 문자열, 의심 파일 후보.
3. 사람 확인 1차: 추출된 재현 단계를 사용자에게 보여 주고 승인받는다(잘못 읽은 단계를 이 시점에 고친다).
4. 재현(샌드박스): clone → `npm ci` → dev 서버 기동 → 재현 단계를 Playwright 테스트로 작성 → 실행. 반드시 실패해야 한다. 통과해 버리면 영상을 다시 스크럽해 셀렉터·입력값을 수정, 최대 3회. 3회 후에도 재현이 안 되면 "재현 불가" 리포트와 테스트 초안만 내고 멈춘다.
5. 수정: red 확인 후 Argon이 원인 코드를 수정 → 해당 테스트 green + 기존 테스트 전체 통과까지 루프, 최대 3회.
6. PR: 새 브랜치에 push, PR 본문에 영상 타임스탬프, 재현 테스트 파일, diff 요약, red→green 로그. 머지는 사람이 한다(HITL 2차).
7. 대시보드: Firestore 구독으로 "분석 → 승인 대기 → 재현 red → 패치 → green → PR" 단계를 실시간 표시.

### 권한과 비밀값

- 사용자가 레포 하나로 범위를 제한한 fine-grained GitHub PAT(contents: write, pull requests: write)를 입력한다.
- 토큰은 Credentials API(`client.credentials.create`)에 등록하고 샌드박스 네트워크 allowlist를 github.com, registry.npmjs.org로 제한한다. 토큰은 프록시에서 주입되어 모델 컨텍스트에 들어가지 않는다.
- Antigravity 샌드박스에서 Playwright 브라우저가 안 뜨면 Cloud Run Job에 자체 샌드박스(Node, Playwright, git)를 구성하고 토큰은 Secret Manager에서 주입한다. 이 경우 2시간이 추가된다.

### 아키텍처

- 프론트: 녹화 버튼, 업로드, 레포 URL·PAT 입력, 재현 단계 승인 화면, 단계 대시보드, PR 링크. Argon 생성.
- API(Cloud Run, FastAPI): 서명 URL, 잡 생성, 승인 콜백, 상태 조회.
- 실행: Antigravity managed agent(1순위) 또는 Cloud Run Job 샌드박스(폴백).
- 저장: GCS(영상), Firestore(잡 상태·단계 로그·red/green 결과), Secret Manager(폴백 시 토큰).

### 범위 결정

- 포함: 브라우저 녹화, mp4 업로드, 영상 분석, 재현 단계 승인, red 강제 재현 루프, 패치 루프, PR 생성, 대시보드.
- 스트레치: PR에 수정 전후 스크린샷 첨부, 여러 버그 동시 처리.
- 제외: Chrome 확장 계측, Node 외 스택, 자동 머지, 이슈 트래커 연동.
- 폴백: 샌드박스 브라우저 불가 시 Cloud Run Job. 재현 3회 실패 시 테스트 초안 리포트로 종료. 라이브 3분 초과 시 "영상 → red"까지 라이브, 패치→PR은 사전 실행 결과.

### 데모 데이터

- 포크한 공개 앱에 심은 버그 2개: 하나는 UI 상태 버그(예: 항목 삭제 후 카운터 미갱신), 하나는 폼 제출 시 500 에러. 각각 60\~90초 녹화를 준비한다.
- 샌드박스를 미리 워밍업(clone·설치 완료 상태)해 두고 라이브에서는 분석과 red 확인을 보여 준다.

### 시간표 (킥오프 = H+0, 9시간)

| 시간 | 작업 | 통과 기준·폴백 |
| --- | --- | --- |
| H+0\~0.5 | 멘토에게 샌드박스 브라우저·dev 서버 가능 여부 확인, 데모 레포 포크·버그 심기, 녹화 2개 | 불가 판정 시 즉시 Cloud Run Job 경로 |
| H+0.5\~1.5 | 녹화 버튼·업로드·Files API | webm 업로드 후 Argon이 영상 읽음 |
| H+1.5\~2.5 | 영상 분석 프롬프트·스키마, 승인 화면 | 재현 단계 5개가 정확히 추출 |
| H+2.5\~5 | 샌드박스 구성, clone·설치·dev 서버, Playwright 테스트 생성, red 확인 루프 | 심은 버그 1개에서 red 확보 |
| H+5\~6.5 | 패치 루프, green·회귀 확인, PR 생성 | PR 1개 생성 |
| H+6.5\~7.5 | 대시보드, Cloud Run 배포, 두 번째 버그로 재현성 확인 |  |
| H+7.5\~8.5 | 사전 실행, 샌드박스 워밍업 절차 정리 |  |
| H+8.5\~9 | 데모 영상, 영문 설명, README |  |

### 킥오프 확인 사항

- [ ] Antigravity 샌드박스에서 dev 서버 포트 바인딩과 Playwright 브라우저 실행 가능 여부
- [ ] Credentials API 등록과 allowlist 설정 방법, 샌드박스 수명·재사용(워밍업) 가능 여부
- [ ] Argon 영상 입력 길이 한도와 타임스탬프 정밀도
- [ ] 샌드박스에서 git push가 토큰 주입으로 동작하는지

### 새 에이전트 세션용 첫 프롬프트 (영어)

```text
I'm building "ReproFix" in a 1-day hackathon, solo, for Google's Gemini 4 Argon track 4 (autonomous agents
and developer tools). Goal: a developer uploads a raw screen recording of a bug in a Node web app (no
instrumentation, no extension) plus a repo URL and a repo-scoped GitHub token. Argon scrubs the video and
extracts reproduction steps; the user approves them; an Antigravity sandbox clones the repo, starts the dev
server, writes a Playwright test from the steps, and must see it FAIL before any fix is attempted (re-scrub
up to 3 times if it passes); then Argon patches the code until that test and the existing suite pass, pushes
a branch and opens a PR with timestamps, the test and red-to-green logs. A human merges.

Stack: Python FastAPI on Cloud Run, GCS, Firestore, gemini-4-argon via the Interactions API, Antigravity
managed agent (antigravity-preview-09-2026) with model gemini-4-argon, Credentials API for the GitHub token,
network allowlist github.com and registry.npmjs.org. Fallback if the sandbox cannot run Playwright: a Cloud
Run Job with Node, Playwright and git, token from Secret Manager.

Before writing code: (1) list clarifying questions and edge cases, (2) propose the repro-steps JSON schema
and how steps map to Playwright locators, (3) propose the red-first verification protocol with exact
pass/fail signals and retry limits, (4) flag the riskiest step (sandbox capabilities) and the fallback.
Wait for my go-ahead before generating files. Record setup lessons in AGENTS.md.
```

### 3분 라이브 데모 대본

1. 0:00 문제: 고객이 보낸 말 없는 화면 녹화, 재현 단계 적는 데 걸리는 시간.
2. 0:20 녹화 업로드: 준비된 60초 버그 영상 업로드, 레포 URL 입력.
3. 0:50 분석: 추출된 재현 단계와 타임스탬프가 화면에 뜨고 사용자가 승인.
4. 1:20 재현: 워밍업된 샌드박스에서 Playwright 테스트 실행, red 로그가 뜨는 장면.
5. 1:50 수정·PR: 사전 실행 결과로 패치 diff, green 로그, PR 링크를 보여 줌(라이브로 끝나면 그대로).
6. 2:30 안전장치: 승인 단계 두 곳, 토큰이 모델에 안 들어가는 구조 한 문장.
7. 2:50 마무리: 어떤 웹앱 버그 영상이든 PR로, 사람이 머지.

### 영문 Project Description 초안

```text
ReproFix — from a raw bug recording to a red-then-green pull request

Bug reports arrive as silent screen recordings. ReproFix turns one into a pull request without any recorder
plugin or instrumentation: Gemini 4 Argon watches the video, extracts the reproduction steps with timestamps,
and the developer approves them. In an Antigravity sandbox the agent writes a Playwright test from those
steps and refuses to touch the code until that test actually fails — a repro that passes is re-derived from
the video, not trusted. Only then does Argon patch, re-run the new test and the existing suite, and open a PR
carrying the video timestamps, the test and the red-to-green logs. The GitHub token is injected at the
sandbox proxy and never enters the model context; a human merges. Scoped to Node web apps for this
hackathon, deployed on Cloud Run with Cloud Storage and Firestore.
```

### 리스크

| 리스크 | 영향 | 대응 |
| --- | --- | --- |
| 샌드박스에서 브라우저·dev 서버 불가 | 핵심 루프 불가 | 킥오프 30분 내 확인, Cloud Run Job 폴백 |
| 영상에서 셀렉터 매핑 실패 | 재현 불가 | 요소 텍스트 기반 로케이터 우선, 승인 단계에서 사람이 수정 |
| 루프 총 시간 3분 초과 | 라이브 데모 구성 | 샌드박스 워밍업, red까지만 라이브 |
| Jam.dev와의 유사성 | 독창성 감점 | 차별점 3개를 첫 문장에 |
| 토큰 노출 | 보안 사고·감점 | Credentials API, allowlist, 레포 범위 PAT |

## 선택 가이드

세 안 모두 균형 전략(완성도와 Argon 과시의 중간) 안에 들어온다. 차이는 어디서 위험을 지느냐다: A는 범위, B는 타이밍 정밀도, C는 샌드박스 환경.

| 항목 | A. Choreograph | B. MoveChart | C. ReproFix |
| --- | --- | --- | --- |
| 트랙 | 1 엔터테인먼트 | 1 엔터테인먼트 | 4 에이전트·개발도구 |
| 기존 제품과의 거리 | AI 비주얼라이저는 많으나 "연출 프로그램 생성 + 자기 검수"는 없음 | 오디오→차트는 많으나 영상→동작 노트는 없음 | Jam.dev가 거의 동일 흐름, 차별점은 계측 없는 영상·red 강제·비밀값 처리 |
| Argon 필요성 | 오디오 이해 + long decode + 자기 영상 검토 | 영상 이해 + long decode | 영상 이해 + Antigravity 검증 루프 |
| 검증 루프 | 독특함(모델이 자기 결과를 시청) | 구축 필요(오토플레이어) | 본질적(red→green) |
| 사용자·임팩트 피치 | 본인 경험, 강함 | 중간 | 개발자 공감, 강함 |
| 혼자 백엔드 적합성 | 중(게임·씬 코드는 Argon 의존) | 중 | 높음 |
| 예상 시간 | 9h | 8.5h | 8\~10h |
| 라이브 3분 | 생성은 사전, 재생은 라이브, 무대 효과 큼 | 분석은 사전, 플레이는 라이브, 무대 효과 큼 | red까지 라이브, 나머지 사전 |
| 최대 리스크 | 범위 과다, 캐릭터 일관성 | 타임스탬프 정밀도 | 샌드박스 브라우저 미확인 |
| 폴백 후 남는 것 | 파티클 연출 + Score | 차트 + 규칙 검사 | 재현 테스트 초안 리포트 |

### 당일 아침 결정 체크리스트

- [ ] 멘토에게 샌드박스에서 Playwright·dev 서버가 되는지 물었다. 안 되면 C는 2시간이 늘어난다.
- [ ] Argon 오디오·영상 입력 한도를 확인했다. 오디오가 안 들어가면 A는 특징 JSON 중심, 영상 길이 제한이 짧으면 B·C는 구간 분할.
- [ ] 데모 데이터를 1시간 안에 만들 수 있다: A는 CC0 곡, B는 Lyria 곡 + 자체 촬영, C는 버그 심은 포크 레포 + 녹화 2개.
- [ ] 오늘 가장 피하고 싶은 실패가 무엇인지 정했다: 미완성(→ C 또는 B), 평범함(→ A 또는 B), 환경 의존(→ A).

### 선택 후 첫 30분

1. 선택한 안의 섹션과 0절을 새 에이전트 세션에 붙이고 첫 프롬프트를 보낸다.
2. 에이전트의 질문에 답하고 스키마·검증 신호에 합의한다.
3. 레포를 만들고 README 골격, LICENSE, `.env.example`을 먼저 커밋한다.
4. 데모 데이터 준비를 병렬로 시작한다.
