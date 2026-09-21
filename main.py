import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="A Dance of Fire and Ice - Ultra Engine",
    page_icon="⚡",
    layout="centered"
)

# 스트림릿 테마 커스텀
st.markdown("""
<style>
    .stApp {
        background-color: #06090e;
        color: #ffffff;
    }
    h1 {
        text-align: center;
        background: linear-gradient(135deg, #ff0055 0%, #00e5ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 0.1rem;
    }
    .stCaption {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ A Dance of Fire and Ice ❄️")
st.caption("초고속 난이도 지원 & 타일 위치/각도 완전 정렬 엔진")

# 난이도 설정 (초고속 옵션 추가)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    speed_option = st.selectbox(
        "🎮 회전 속도 (BPM / 난이도)",
        options=[
            "Easy (BPM 110)", 
            "Normal (BPM 150)", 
            "Hard (BPM 200)", 
            "Insane (BPM 260)", 
            "Sonic (BPM 320)", 
            "Overclock (BPM 400)"
        ],
        index=1
    )

speed_map = {
    "Easy (BPM 110)": 0.040,
    "Normal (BPM 150)": 0.055,
    "Hard (BPM 200)": 0.075,
    "Insane (BPM 260)": 0.098,
    "Sonic (BPM 320)": 0.125,
    "Overclock (BPM 400)": 0.155
}
selected_speed = speed_map[speed_option]

game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            padding: 0;
            background-color: #06090e;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            user-select: none;
            overflow: hidden;
        }}
        #gameContainer {{
            position: relative;
            margin-top: 10px;
        }}
        #gameCanvas {{
            border: 2px solid #1e293b;
            border-radius: 20px;
            background: radial-gradient(circle at center, #0f172a 0%, #06090e 100%);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9), 0 0 30px rgba(0, 229, 255, 0.15);
            cursor: pointer;
        }}
        #info {{
            margin-top: 15px;
            text-align: center;
        }}
        .stats {{
            font-size: 19px;
            color: #64748b;
            letter-spacing: 0.5px;
        }}
        .stats span {{
            color: #f8fafc;
            font-weight: bold;
        }}
        .status {{
            font-size: 24px;
            font-weight: 800;
            margin-top: 6px;
            height: 36px;
            text-shadow: 0 0 12px rgba(255,255,255,0.25);
        }}
        #restartBtn {{
            display: none;
            margin-top: 10px;
            padding: 12px 30px;
            font-size: 16px;
            font-weight: bold;
            color: #ffffff;
            background: linear-gradient(135deg, #ff0055, #ff527b);
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 6px 20px rgba(255, 0, 85, 0.4);
            transition: all 0.2s ease;
        }}
        #restartBtn:hover {{
            transform: translateY(-2px) scale(1.03);
            box-shadow: 0 8px 25px rgba(255, 0, 85, 0.6);
        }}
    </style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas" width="680" height="400"></canvas>
</div>

<div id="info">
    <div class="stats">점수: <span id="score">0</span> &nbsp;|&nbsp; 콤보: <span id="combo">0</span> &nbsp;|&nbsp; 최고 콤보: <span id="maxCombo">0</span></div>
    <div id="feedback" class="status" style="color: #00e5ff;">클릭하거나 아무 키나 눌러 시작하세요!</div>
    <button id="restartBtn" onclick="initGame()">🔄 다시 도전하기</button>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const comboEl = document.getElementById('combo');
const maxComboEl = document.getElementById('maxCombo');
const feedbackEl = document.getElementById('feedback');
const restartBtn = document.getElementById('restartBtn');

// Web Audio API 오디오 엔진
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function initAudio() {{
    if (!audioCtx) {{
        audioCtx = new AudioContext();
    }}
}}

function playSound(type) {{
    if (!audioCtx) return;
    
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    
    const now = audioCtx.currentTime;

    if (type === 'PERFECT') {{
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, now); // D5
        osc.frequency.exponentialRampToValueAtTime(1174.66, now + 0.1); // D6
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
        osc.start(now);
        osc.stop(now + 0.1);
    }} else if (type === 'GREAT') {{
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(493.88, now); // B4
        gain.gain.setValueAtTime(0.25, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
        osc.start(now);
        osc.stop(now + 0.08);
    }} else if (type === 'MISS') {{
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(160, now);
        osc.frequency.linearRampToValueAtTime(50, now + 0.22);
        gain.gain.setValueAtTime(0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
        osc.start(now);
        osc.stop(now + 0.22);
    }} else if (type === 'BEAT') {{
        osc.type = 'sine';
        osc.frequency.setValueAtTime(261.63, now);
        gain.gain.setValueAtTime(0.05, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
        osc.start(now);
        osc.stop(now + 0.04);
    }}
}}

// 게임 엔진 상수
const R = 46; 
const TILE_W = 62;
const TILE_H = 36;

let tiles = [];
let currentTileIdx = 0;
let pivotPos = {{ x: 0, y: 0 }};
let activePos = {{ x: 0, y: 0 }};

// 각도 정밀 제어
let currentAngle = 0;
let targetAngle = 0;
let rotDirection = 1; 
let baseRotSpeed = {selected_speed};

let activePlanetType = 1; // 0: 불(Red), 1: 얼음(Blue)

// 카메라 및 이펙트 제어
let camX = 0;
let camY = 0;
const camLerpFactor = 0.1; 
let shakeAmount = 0;

let score = 0;
let combo = 0;
let maxCombo = 0;
let gameState = "READY";

let particles = [];
let planetTrails = [];

function addExplosion(x, y, color) {{
    for (let i = 0; i < 28; i++) {{
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 7 + 2;
        particles.push({{
            x: x,
            y: y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            radius: Math.random() * 4 + 2,
            color: color,
            alpha: 1,
            decay: Math.random() * 0.035 + 0.02
        }});
    }}
}}

function addTrail(x, y, color) {{
    planetTrails.push({{
        x: x,
        y: y,
        radius: 12,
        color: color,
        alpha: 0.6,
        decay: 0.06
    }});
}}

// 다양한 각도 경로(직각, 대각선, 대각선 복합) 생성 알고리즘
function generateComplexMap() {{
    tiles = [];
    let cx = 200;
    let cy = 200;
    
    // 8방향 벡터 정의 (직진, 직각, 대각선 포함)
    const possibleDirs = [
        {{ x: 1, y: 0 }},   // 우
        {{ x: 1, y: 0 }},   // 우 (직진 가중치)
        {{ x: 0, y: 1 }},   // 하
        {{ x: 0, y: -1 }},  // 상
        {{ x: 1, y: 1 }},   // 우하 대각선
        {{ x: 1, y: -1 }},  // 우상 대각선
        {{ x: -1, y: 1 }},  // 좌하 대각선
        {{ x: -1, y: -1 }}  // 좌상 대각선
    ];

    tiles.push({{ x: cx, y: cy, isSwirl: false }});
    let lastDir = possibleDirs[0];

    for (let i = 0; i < 300; i++) {{
        let d;
        do {{
            d = possibleDirs[Math.floor(Math.random() * possibleDirs.length)];
        }} while (d.x === -lastDir.x && d.y === -lastDir.y); // 완전 반대 방향(역주행) 방지

        lastDir = d;
        
        // 대각선 이동 시 거리 보정 (동일한 속도감 유지)
        const distanceFactor = (d.x !== 0 && d.y !== 0) ? (Math.SQRT2 * R * 1.3) : (2 * R);
        
        cx += d.x * distanceFactor;
        cy += d.y * distanceFactor;
        
        const isSwirl = Math.random() < 0.10 && i > 4;
        tiles.push({{ x: cx, y: cy, isSwirl: isSwirl }});
    }}
}}

function initGame() {{
    generateComplexMap();
    
    currentTileIdx = 0;
    score = 0;
    combo = 0;
    maxCombo = 0;
    rotDirection = 1;
    gameState = "READY";
    particles = [];
    planetTrails = [];

    // 출발 타일 위치 세팅
    pivotPos = {{ x: tiles[0].x, y: tiles[0].y }};
    camX = pivotPos.x;
    camY = pivotPos.y;
    
    const nextTile = tiles[1];
    
    // 타일 사이의 명확한 벡터 각도 산출
    const targetDirAngle = Math.atan2(nextTile.y - pivotPos.y, nextTile.x - pivotPos.x);
    
    // 정확히 이전 타일 위치에서 행성이 출발하도록 180도 뒤에서 시작
    currentAngle = targetDirAngle - Math.PI;
    targetAngle = targetDirAngle;

    activePlanetType = 1; // 얼음 행성이 회전하며 시작
    updateActivePos();

    scoreEl.innerText = "0";
    comboEl.innerText = "0";
    maxComboEl.innerText = "0";
    feedbackEl.innerText = "클릭하거나 아무 키나 눌러 시작하세요!";
    feedbackEl.style.color = "#00e5ff";
    restartBtn.style.display = "none";
}}

function updateActivePos() {{
    activePos.x = pivotPos.x + Math.cos(currentAngle) * (2 * R);
    activePos.y = pivotPos.y + Math.sin(currentAngle) * (2 * R);
}}

function update() {{
    if (gameState !== "PLAYING") return;

    currentAngle += baseRotSpeed * rotDirection;
    updateActivePos();

    const curColor = activePlanetType === 1 ? '#00e5ff' : '#ff0055';
    addTrail(activePos.x, activePos.y, curColor);

    // 판정 초과 체크
    const passed = rotDirection === 1 
        ? (currentAngle > targetAngle + 0.65) 
        : (currentAngle < targetAngle - 0.65);

    if (passed) {{
        triggerGameOver("타이밍 초과! (MISS)");
    }}

    if (shakeAmount > 0) shakeAmount *= 0.88;
}}

function handleInput() {{
    initAudio();

    if (gameState === "READY") {{
        gameState = "PLAYING";
        feedbackEl.innerText = "START!";
        feedbackEl.style.color = "#4ade80";
        playSound('BEAT');
        return;
    }}

    if (gameState === "GAMEOVER") return;

    const diff = Math.abs(currentAngle - targetAngle);

    if (diff < 0.35) {{
        // PERFECT
        score += 100 + (combo * 15);
        combo++;
        if (combo > maxCombo) maxCombo = combo;
        
        feedbackEl.innerText = "PERFECT!!";
        feedbackEl.style.color = "#4ade80";
        shakeAmount = 4;
        
        const curColor = activePlanetType === 1 ? '#00e5ff' : '#ff0055';
        addExplosion(activePos.x, activePos.y, curColor);
        playSound('PERFECT');
        
        advanceToNextTile();
    }} else if (diff < 0.60) {{
        // GREAT
        score += 50;
        combo++;
        if (combo > maxCombo) maxCombo = combo;
        
        feedbackEl.innerText = "GREAT";
        feedbackEl.style.color = "#facc15";
        shakeAmount = 2;
        playSound('GREAT');
        
        advanceToNextTile();
    }} else {{
        // MISS
        triggerGameOver("타이밍 불일치! (MISS)");
    }}

    scoreEl.innerText = score;
    comboEl.innerText = combo;
    maxComboEl.innerText = maxCombo;
}}

function triggerGameOver(reason) {{
    gameState = "GAMEOVER";
    feedbackEl.innerText = `GAME OVER - ${{reason}}`;
    feedbackEl.style.color = "#ff4d4d";
    shakeAmount = 12;
    playSound('MISS');
    restartBtn.style.display = "inline-block";
}}

// 허공 시작 현상을 완벽 차단하는 절대 타일 정렬 연산
function advanceToNextTile() {{
    currentTileIdx++;
    const nextPivot = tiles[currentTileIdx];
    if (!nextPivot) return;

    // 회전 반전 타일(Swirl) 처리
    if (nextPivot.isSwirl) {{
        rotDirection *= -1;
    }}

    // [핵심] 이전 착지 타일 좌표로 피벗 완전 스냅 (허공 점프 방지)
    pivotPos = {{ x: nextPivot.x, y: nextPivot.y }};
    activePlanetType = activePlanetType === 0 ? 1 : 0;

    const futureTile = tiles[currentTileIdx + 1];
    if (futureTile) {{
        // 현재 타일에서 다음 타일로 가는 정확한 벡터 방향각 연산
        let nextTargetDir = Math.atan2(futureTile.y - pivotPos.y, futureTile.x - pivotPos.x);
        
        // 입력 시점의 미세 오차 값 계산
        let angleOffset = currentAngle - targetAngle;

        // 회전 벡터 정규화 연산 (대각선/직각 각도 차이 보정)
        let diff = nextTargetDir - targetAngle;
        while (diff < -Math.PI) diff += Math.PI * 2;
        while (diff > Math.PI) diff -= Math.PI * 2;

        if (rotDirection === 1) {{
            targetAngle = targetAngle + (diff < 0 ? diff + Math.PI * 2 : diff);
            // 다음 회전은 이전 타일 위치(현재 Pivot)에 연결된 반대편(-PI)에서 연속성 있게 출발
            currentAngle = targetAngle - Math.PI + angleOffset;
        }} else {{
            targetAngle = targetAngle + (diff > 0 ? diff - Math.PI * 2 : diff);
            currentAngle = targetAngle + Math.PI + angleOffset;
        }}
    }}
    
    // 즉시 정렬된 위치 업데이트
    updateActivePos();
}}

// 렌더링 루프
function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    
    // 카메라 Lerp + 화면 흔들림(Shake)
    camX += (pivotPos.x - camX) * camLerpFactor;
    camY += (pivotPos.y - camY) * camLerpFactor;

    const shakeX = (Math.random() - 0.5) * shakeAmount;
    const shakeY = (Math.random() - 0.5) * shakeAmount;

    ctx.translate(canvas.width / 2 - camX + shakeX, canvas.height / 2 - camY + shakeY);

    // 1. 경로 선 (대각선/직각 부드럽게 잇기)
    ctx.beginPath();
    for (let i = 0; i < tiles.length; i++) {{
        if (i === 0) ctx.moveTo(tiles[i].x, tiles[i].y);
        else ctx.lineTo(tiles[i].x, tiles[i].y);
    }}
    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
    ctx.lineWidth = 10;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.stroke();

    // 2. 타일 그리기
    for (let i = 0; i < tiles.length; i++) {{
        const t = tiles[i];
        
        ctx.save();
        ctx.translate(t.x, t.y);

        ctx.beginPath();
        ctx.roundRect(-TILE_W / 2, -TILE_H / 2, TILE_W, TILE_H, 8);

        if (i < currentTileIdx) {{
            ctx.fillStyle = "rgba(255, 255, 255, 0.06)";
            ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
        }} else if (i === currentTileIdx + 1) {{
            // 목표 착지 타일 가이드
            ctx.fillStyle = "#fbbf24";
            ctx.strokeStyle = "#ffffff";
            ctx.shadowColor = "#fbbf24";
            ctx.shadowBlur = 20;
        }} else if (i === currentTileIdx) {{
            // 현재 타일
            ctx.fillStyle = "rgba(255, 255, 255, 0.35)";
            ctx.strokeStyle = "#ffffff";
        }} else {{
            ctx.fillStyle = "#1e293b";
            ctx.strokeStyle = "#334155";
        }}

        ctx.lineWidth = 2;
        ctx.fill();
        ctx.stroke();

        if (t.isSwirl && i >= currentTileIdx) {{
            ctx.beginPath();
            ctx.arc(0, 0, 8, 0, Math.PI * 2);
            ctx.strokeStyle = "#a855f7";
            ctx.lineWidth = 3;
            ctx.stroke();
        }}

        ctx.restore();
    }}

    // 3. 행성 트레일(잔상)
    for (let i = planetTrails.length - 1; i >= 0; i--) {{
        const pt = planetTrails[i];
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, pt.radius, 0, Math.PI * 2);
        ctx.fillStyle = pt.color;
        ctx.globalAlpha = pt.alpha;
        ctx.fill();
        ctx.globalAlpha = 1.0;

        pt.radius *= 0.93;
        pt.alpha -= pt.decay;
        if (pt.alpha <= 0) planetTrails.splice(i, 1);
    }}

    const redPos = activePlanetType === 1 ? pivotPos : activePos;
    const bluePos = activePlanetType === 1 ? activePos : pivotPos;

    // 4. 행성 연결 축
    ctx.beginPath();
    ctx.moveTo(redPos.x, redPos.y);
    ctx.lineTo(bluePos.x, bluePos.y);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.65)";
    ctx.lineWidth = 4;
    ctx.stroke();

    // 5. 불 행성
    ctx.beginPath();
    ctx.arc(redPos.x, redPos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#ff0055";
    ctx.shadowColor = "#ff0055";
    ctx.shadowBlur = activePlanetType === 0 ? 22 : 8;
    ctx.fill();

    // 6. 얼음 행성
    ctx.beginPath();
    ctx.arc(bluePos.x, bluePos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#00e5ff";
    ctx.shadowColor = "#00e5ff";
    ctx.shadowBlur = activePlanetType === 1 ? 22 : 8;
    ctx.fill();

    // 7. 파티클 효과
    for (let i = particles.length - 1; i >= 0; i--) {{
        const p = particles[i];
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.fill();
        ctx.globalAlpha = 1.0;

        p.x += p.vx;
        p.y += p.vy;
        p.alpha -= p.decay;
        if (p.alpha <= 0) particles.splice(i, 1);
    }}

    ctx.restore();
}}

function loop() {{
    update();
    draw();
    requestAnimationFrame(loop);
}}

window.addEventListener('keydown', (e) => {{
    if (e.code === 'Space' || e.key !== '') {{
        handleInput();
    }}
}});

canvas.addEventListener('mousedown', handleInput);

initGame();
loop();
</script>
</body>
</html>
"""

components.html(game_html, height=580)
