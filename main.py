import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="A Dance of Fire and Ice - Ultimate Engine",
    page_icon="🔥",
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
        background: linear-gradient(135deg, #ff3366 0%, #33ccff 50%, #a855f7 100%);
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

st.title("🔥 A Dance of Fire and Ice ❄️")
st.caption("대각선 삼각비 보정 엔진 & 초고속 모드 탑재")

# 난이도 설정 (더 빠른 속도 옵션 추가)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    speed_option = st.selectbox(
        "🎮 회전 속도 (BPM / 난이도) 선택",
        options=[
            "Easy (BPM 120)", 
            "Normal (BPM 160)", 
            "Hard (BPM 220)", 
            "Insane (BPM 280)",
            "Extreme (BPM 320) 🔥",
            "Speed Demon (BPM 400) ⚡"
        ],
        index=1
    )

speed_map = {
    "Easy (BPM 120)": 0.045,
    "Normal (BPM 160)": 0.060,
    "Hard (BPM 220)": 0.082,
    "Insane (BPM 280)": 0.105,
    "Extreme (BPM 320) 🔥": 0.125,
    "Speed Demon (BPM 400) ⚡": 0.155
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
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9), 0 0 25px rgba(56, 189, 248, 0.15);
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
            padding: 12px 32px;
            font-size: 16px;
            font-weight: bold;
            color: #ffffff;
            background: linear-gradient(135deg, #ff3366, #a855f7);
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 6px 20px rgba(255, 51, 102, 0.4);
            transition: all 0.2s ease;
        }}
        #restartBtn:hover {{
            transform: translateY(-2px) scale(1.04);
            box-shadow: 0 8px 25px rgba(255, 51, 102, 0.6);
        }}
    </style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas" width="700" height="420"></canvas>
</div>

<div id="info">
    <div class="stats">점수: <span id="score">0</span> &nbsp;|&nbsp; 콤보: <span id="combo">0</span> &nbsp;|&nbsp; 최고 콤보: <span id="maxCombo">0</span></div>
    <div id="feedback" class="status" style="color: #38bdf8;">화면을 클릭하거나 아무 키나 누르세요!</div>
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

// Web Audio API 오디오 내장
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
        osc.frequency.setValueAtTime(523.25, now);
        osc.frequency.exponentialRampToValueAtTime(1046.50, now + 0.12);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
        osc.start(now);
        osc.stop(now + 0.12);
    }} else if (type === 'GREAT') {{
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, now);
        gain.gain.setValueAtTime(0.25, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
        osc.start(now);
        osc.stop(now + 0.1);
    }} else if (type === 'MISS') {{
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(160, now);
        osc.frequency.linearRampToValueAtTime(50, now + 0.25);
        gain.gain.setValueAtTime(0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
        osc.start(now);
        osc.stop(now + 0.25);
    }} else if (type === 'BEAT') {{
        osc.type = 'sine';
        osc.frequency.setValueAtTime(220, now);
        gain.gain.setValueAtTime(0.05, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
        osc.start(now);
        osc.stop(now + 0.05);
    }}
}}

// 게임 정밀 상수
const R = 45; // 행성 회전 반지름 (두 행성 사이 거리 = 2 * R = 90)
const TILE_W = 58;
const TILE_H = 32;

let tiles = [];
let currentTileIdx = 0;
let pivotPos = {{ x: 0, y: 0 }};
let activePos = {{ x: 0, y: 0 }};

let currentAngle = 0;
let targetAngle = 0;
let rotDirection = 1; // 1: 시계 방향, -1: 반시계 방향
let baseRotSpeed = {selected_speed};

let activePlanetType = 1; // 0: Fire(Red), 1: Ice(Blue)

// 고정밀 카메라, 줌, 쉐이크
let camX = 0;
let camY = 0;
const camLerpFactor = 0.09;
let shakeAmount = 0;
let cameraZoom = 1.0;

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
            decay: Math.random() * 0.03 + 0.02
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
        decay: 0.045
    }});
}}

// 대각선 위치 수학적 정렬 맵 생성기
function generateAccurateMap() {{
    tiles = [];
    let cx = 200;
    let cy = 210;

    // 각도 오차 없는 8방향 선택지 (각도 각격: 0, 45, 90, 135, -45, -90, -135도)
    const angleChoices = [
        0,                  // 우 (Right)
        0,                  // 우 (가중치)
        Math.PI / 4,        // 우하 대각선 (45 deg)
        -Math.PI / 4,       // 우상 대각선 (-45 deg)
        Math.PI / 2,        // 하 (Down)
        -Math.PI / 2        // 상 (Up)
    ];

    tiles.push({{ x: cx, y: cy, angle: 0, isSwirl: false }});
    let lastAngle = 0;

    for (let i = 0; i < 300; i++) {{
        let chosenAngle;
        
        // 역주행(180도 반대) 방지 알고리즘
        do {{
            chosenAngle = angleChoices[Math.floor(Math.random() * angleChoices.length)];
        }} while (Math.abs(chosenAngle - (lastAngle + Math.PI)) < 0.1);

        lastAngle = chosenAngle;

        // 정확한 삼각비 연산으로 대각선 위치 배치 (거리: 2 * R)
        cx += Math.cos(chosenAngle) * (2 * R);
        cy += Math.sin(chosenAngle) * (2 * R);

        const isSwirl = Math.random() < 0.10 && i > 3;
        tiles.push({{ 
            x: cx, 
            y: cy, 
            angle: chosenAngle, 
            isSwirl: isSwirl 
        }});
    }}
}}

function initGame() {{
    generateAccurateMap();
    
    currentTileIdx = 0;
    score = 0;
    combo = 0;
    maxCombo = 0;
    rotDirection = 1;
    gameState = "READY";
    particles = [];
    planetTrails = [];
    cameraZoom = 1.0;

    pivotPos = {{ x: tiles[0].x, y: tiles[0].y }};
    camX = pivotPos.x;
    camY = pivotPos.y;
    
    const nextTile = tiles[1];
    const targetDirAngle = Math.atan2(nextTile.y - pivotPos.y, nextTile.x - pivotPos.x);
    
    currentAngle = targetDirAngle - Math.PI;
    targetAngle = targetDirAngle;

    activePlanetType = 1;
    updateActivePos();

    scoreEl.innerText = "0";
    comboEl.innerText = "0";
    maxComboEl.innerText = "0";
    feedbackEl.innerText = "클릭하거나 아무 키나 눌러 시작하세요!";
    feedbackEl.style.color = "#38bdf8";
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

    const curColor = activePlanetType === 1 ? '#38bdf8' : '#ff3366';
    addTrail(activePos.x, activePos.y, curColor);

    // 판정 한계 오버런 검사
    const passed = rotDirection === 1 
        ? (currentAngle > targetAngle + 0.65) 
        : (currentAngle < targetAngle - 0.65);

    if (passed) {{
        triggerGameOver("시간 초과! (MISS)");
    }}

    // 쉐이크 및 줌 부드러운 감소
    if (shakeAmount > 0) shakeAmount *= 0.88;
    cameraZoom += (1.0 - cameraZoom) * 0.05;
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
        cameraZoom = 1.03; // 바운스 줌
        
        const curColor = activePlanetType === 1 ? '#38bdf8' : '#ff3366';
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
    feedbackEl.style.color = "#f87171";
    shakeAmount = 14;
    playSound('MISS');
    restartBtn.style.display = "inline-block";
}}

// 고정밀 각도 수식 엔진
function advanceToNextTile() {{
    currentTileIdx++;
    const nextPivot = tiles[currentTileIdx];
    if (!nextPivot) return;

    if (nextPivot.isSwirl) {{
        rotDirection *= -1;
    }}

    pivotPos = {{ x: nextPivot.x, y: nextPivot.y }};
    activePlanetType = activePlanetType === 0 ? 1 : 0;

    const futureTile = tiles[currentTileIdx + 1];
    if (futureTile) {{
        let nextTargetDir = Math.atan2(futureTile.y - pivotPos.y, futureTile.x - pivotPos.x);
        let angleOffset = currentAngle - targetAngle;

        let diff = nextTargetDir - targetAngle;
        while (diff < -Math.PI) diff += Math.PI * 2;
        while (diff > Math.PI) diff -= Math.PI * 2;

        if (rotDirection === 1) {{
            targetAngle = targetAngle + (diff < 0 ? diff + Math.PI * 2 : diff);
            currentAngle = targetAngle - Math.PI + angleOffset;
        }} else {{
            targetAngle = targetAngle + (diff > 0 ? diff - Math.PI * 2 : diff);
            currentAngle = targetAngle + Math.PI + angleOffset;
        }}
    }}
    updateActivePos();
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    
    // 카메라 추적, 줌, 쉐이크
    camX += (pivotPos.x - camX) * camLerpFactor;
    camY += (pivotPos.y - camY) * camLerpFactor;

    const shakeX = (Math.random() - 0.5) * shakeAmount;
    const shakeY = (Math.random() - 0.5) * shakeAmount;

    ctx.translate(canvas.width / 2 + shakeX, canvas.height / 2 + shakeY);
    ctx.scale(cameraZoom, cameraZoom);
    ctx.translate(-camX, -camY);

    // 1. 타일 연결 선 (길 경로)
    ctx.beginPath();
    for (let i = 0; i < tiles.length; i++) {{
        if (i === 0) ctx.moveTo(tiles[i].x, tiles[i].y);
        else ctx.lineTo(tiles[i].x, tiles[i].y);
    }}
    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
    ctx.lineWidth = 8;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.stroke();

    // 2. 대각선 대응 회전 타일 렌더링
    for (let i = 0; i < tiles.length; i++) {{
        const t = tiles[i];
        
        ctx.save();
        ctx.translate(t.x, t.y);
        ctx.rotate(t.angle); // 진행 방향 각도에 맞춘 회전 렌더링

        ctx.beginPath();
        ctx.roundRect(-TILE_W / 2, -TILE_H / 2, TILE_W, TILE_H, 8);

        if (i < currentTileIdx) {{
            ctx.fillStyle = "rgba(255, 255, 255, 0.07)";
            ctx.strokeStyle = "rgba(255, 255, 255, 0.09)";
        }} else if (i === currentTileIdx + 1) {{
            // 다가오는 다음 타일 (최고 밝기)
            ctx.fillStyle = "#fbbf24";
            ctx.strokeStyle = "#ffffff";
            ctx.shadowColor = "#fbbf24";
            ctx.shadowBlur = 18;
        }} else if (i === currentTileIdx) {{
            // 현재 피벗 타일
            ctx.fillStyle = "rgba(255, 255, 255, 0.35)";
            ctx.strokeStyle = "#ffffff";
        }} else {{
            // 일반 대기 타일
            ctx.fillStyle = "#1e293b";
            ctx.strokeStyle = "#334155";
        }}

        ctx.lineWidth = 2;
        ctx.fill();
        ctx.stroke();

        if (t.isSwirl && i >= currentTileIdx) {{
            ctx.beginPath();
            ctx.arc(0, 0, 8, 0, Math.PI * 2);
            ctx.strokeStyle = "#c084fc";
            ctx.lineWidth = 3;
            ctx.stroke();
        }}

        ctx.restore();
    }}

    // 3. 잔상 (Trail) 파티클
    for (let i = planetTrails.length - 1; i >= 0; i--) {{
        const pt = planetTrails[i];
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, pt.radius, 0, Math.PI * 2);
        ctx.fillStyle = pt.color;
        ctx.globalAlpha = pt.alpha;
        ctx.fill();
        ctx.globalAlpha = 1.0;

        pt.radius *= 0.94;
        pt.alpha -= pt.decay;
        if (pt.alpha <= 0) planetTrails.splice(i, 1);
    }}

    const redPos = activePlanetType === 1 ? pivotPos : activePos;
    const bluePos = activePlanetType === 1 ? activePos : pivotPos;

    // 4. 행성 축 연결선
    ctx.beginPath();
    ctx.moveTo(redPos.x, redPos.y);
    ctx.lineTo(bluePos.x, bluePos.y);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.65)";
    ctx.lineWidth = 4;
    ctx.stroke();

    // 5. 불 행성
    ctx.beginPath();
    ctx.arc(redPos.x, redPos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#ff3366";
    ctx.shadowColor = "#ff3366";
    ctx.shadowBlur = activePlanetType === 0 ? 22 : 8;
    ctx.fill();

    // 6. 얼음 행성
    ctx.beginPath();
    ctx.arc(bluePos.x, bluePos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#38bdf8";
    ctx.shadowColor = "#38bdf8";
    ctx.shadowBlur = activePlanetType === 1 ? 22 : 8;
    ctx.fill();

    // 7. 폭발 파티클
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

components.html(game_html, height=600)
