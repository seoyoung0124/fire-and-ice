import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="A Dance of Fire and Ice - Streamlit Edition",
    page_icon="❄️",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0b0e14;
        color: #ffffff;
    }
    h1 {
        text-align: center;
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .stCaption {
        text-align: center;
        color: #9aa0a6;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔥 A Dance of Fire and Ice ❄️")
st.caption("박자에 맞춰 타일 위로 행성을 착지시키세요!")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    speed_option = st.selectbox(
        "🎮 회전 속도 (난이도) 선택",
        options=["쉬움 (Slow)", "보통 (Normal)", "빠름 (Fast)", "매우 빠름 (Extreme)"],
        index=1
    )

speed_map = {
    "쉬움 (Slow)": 0.035,
    "보통 (Normal)": 0.05,
    "빠름 (Fast)": 0.07,
    "매우 빠름 (Extreme)": 0.095
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
            background-color: #0b0e14;
            color: #ffffff;
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            user-select: none;
            overflow: hidden;
        }}
        #gameCanvas {{
            border: 2px solid #1f293d;
            border-radius: 16px;
            background-color: #121824;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
            cursor: pointer;
        }}
        #info {{
            margin-top: 15px;
            text-align: center;
        }}
        .stats {{
            font-size: 18px;
            color: #8a99ad;
        }}
        .stats span {{
            color: #ffffff;
            font-weight: bold;
        }}
        .status {{
            font-size: 22px;
            font-weight: 800;
            margin-top: 8px;
            height: 30px;
        }}
        #restartBtn {{
            display: none;
            margin-top: 12px;
            padding: 10px 24px;
            font-size: 16px;
            font-weight: bold;
            color: #ffffff;
            background-color: #ff3366;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(255, 51, 102, 0.4);
            transition: transform 0.1s, background-color 0.2s;
        }}
        #restartBtn:hover {{
            background-color: #ff527b;
            transform: scale(1.05);
        }}
    </style>
</head>
<body>

<canvas id="gameCanvas" width="650" height="380"></canvas>
<div id="info">
    <div class="stats">점수: <span id="score">0</span> | 최고 콤보: <span id="combo">0</span></div>
    <div id="feedback" class="status" style="color: #64b5f6;">클릭하거나 아무 키나 눌러 시작하세요!</div>
    <button id="restartBtn" onclick="initGame()">🔄 다시 시작</button>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const comboEl = document.getElementById('combo');
const feedbackEl = document.getElementById('feedback');
const restartBtn = document.getElementById('restartBtn');

const R = 45; 
const TILE_W = 60;
const TILE_H = 34;

let tiles = [];
let currentTileIdx = 0;
let pivotPos = {{ x: 0, y: 0 }};
let activePos = {{ x: 0, y: 0 }};

// 부드러운 카메라 추적
let camX = 0;
let camY = 0;
const camLerpFactor = 0.1; 

let currentAngle = 0;
let targetAngle = 0;
let baseRotSpeed = {selected_speed};

let activePlanetType = 1;
let score = 0;
let combo = 0;
let maxCombo = 0;

let gameState = "READY";

function generateRandomMap() {{
    tiles = [];
    let cx = 150;
    let cy = 190;
    
    const possibleDirs = [
        {{ x: 1, y: 0 }},
        {{ x: 1, y: 0 }},
        {{ x: 0, y: 1 }},
        {{ x: 0, y: -1 }}
    ];

    tiles.push({{ x: cx, y: cy }});
    let lastDir = possibleDirs[0];

    for (let i = 0; i < 200; i++) {{
        let d;
        do {{
            d = possibleDirs[Math.floor(Math.random() * possibleDirs.length)];
        }} while (d.x === -lastDir.x && d.y === -lastDir.y);

        lastDir = d;
        cx += d.x * (2 * R);
        cy += d.y * (2 * R);
        tiles.push({{ x: cx, y: cy }});
    }}
}}

function initGame() {{
    generateRandomMap();
    
    currentTileIdx = 0;
    score = 0;
    combo = 0;
    maxCombo = 0;
    gameState = "READY";

    pivotPos = {{ x: tiles[0].x, y: tiles[0].y }};
    camX = pivotPos.x;
    camY = pivotPos.y;
    
    const nextTile = tiles[1];
    let targetDirAngle = Math.atan2(nextTile.y - pivotPos.y, nextTile.x - pivotPos.x);
    
    currentAngle = targetDirAngle - Math.PI;
    targetAngle = targetDirAngle;

    activePlanetType = 1;
    updateActivePos();

    scoreEl.innerText = "0";
    comboEl.innerText = "0";
    feedbackEl.innerText = "클릭하거나 아무 키나 눌러 시작하세요!";
    feedbackEl.style.color = "#64b5f6";
    restartBtn.style.display = "none";
}}

function updateActivePos() {{
    activePos.x = pivotPos.x + Math.cos(currentAngle) * (2 * R);
    activePos.y = pivotPos.y + Math.sin(currentAngle) * (2 * R);
}}

function update() {{
    if (gameState !== "PLAYING") return;

    // 시계 방향으로 일정하게 회전
    currentAngle += baseRotSpeed;
    updateActivePos();

    if (currentAngle > targetAngle + 0.6) {{
        triggerGameOver("시간 초과! (Miss)");
    }}
}}

function handleInput() {{
    if (gameState === "READY") {{
        gameState = "PLAYING";
        feedbackEl.innerText = "START!";
        feedbackEl.style.color = "#4caf50";
        return;
    }}

    if (gameState === "GAMEOVER") return;

    const diff = Math.abs(currentAngle - targetAngle);

    if (diff < 0.38) {{
        score += 100 + (combo * 10);
        combo++;
        if (combo > maxCombo) maxCombo = combo;
        feedbackEl.innerText = "PERFECT!";
        feedbackEl.style.color = "#00e676";
        advanceToNextTile();
    }} else if (diff < 0.65) {{
        score += 50;
        combo++;
        if (combo > maxCombo) maxCombo = combo;
        feedbackEl.innerText = "GREAT";
        feedbackEl.style.color = "#ffeb3b";
        advanceToNextTile();
    }} else {{
        triggerGameOver("MISS!");
    }}

    scoreEl.innerText = score;
    comboEl.innerText = combo;
}}

function triggerGameOver(reason) {{
    gameState = "GAMEOVER";
    feedbackEl.innerText = `GAME OVER - ${{reason}}`;
    feedbackEl.style.color = "#ff5252";
    restartBtn.style.display = "inline-block";
}}

function advanceToNextTile() {{
    currentTileIdx++;
    const nextPivot = tiles[currentTileIdx];
    if (!nextPivot) return;

    // 새로운 Pivot으로 전환
    pivotPos = {{ x: nextPivot.x, y: nextPivot.y }};
    activePlanetType = activePlanetType === 0 ? 1 : 0;

    const futureTile = tiles[currentTileIdx + 1];
    if (futureTile) {{
        // 새로운 목표 타일과의 상대 각도 연산
        let nextTargetDirAngle = Math.atan2(futureTile.y - pivotPos.y, futureTile.x - pivotPos.x);

        // 이전 회전 각도의 연속성을 위해 오프셋을 유지
        let sweepNeeded = nextTargetDirAngle - (currentAngle - Math.PI);

        // 시계 방향 최소 회전각 조정 (각도가 뒤로 튀는 현상 방지)
        while (sweepNeeded <= 0) {{
            sweepNeeded += Math.PI * 2;
        }}

        targetAngle = currentAngle + sweepNeeded;
    }}
    updateActivePos();
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    
    // 두 중심점 사이를 선형 보간하여 화면 튀는 현상 방지
    const targetCamX = (pivotPos.x + activePos.x) / 2;
    const targetCamY = (pivotPos.y + activePos.y) / 2;

    camX += (targetCamX - camX) * camLerpFactor;
    camY += (targetCamY - camY) * camLerpFactor;

    ctx.translate(Math.round(canvas.width / 2 - camX), Math.round(canvas.height / 2 - camY));

    // 1. 타일 연결 선
    ctx.beginPath();
    for (let i = 0; i < tiles.length; i++) {{
        if (i === 0) ctx.moveTo(tiles[i].x, tiles[i].y);
        else ctx.lineTo(tiles[i].x, tiles[i].y);
    }}
    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
    ctx.lineWidth = 6;
    ctx.stroke();

    // 2. 타일 그리기
    for (let i = 0; i < tiles.length; i++) {{
        const t = tiles[i];
        
        ctx.save();
        ctx.translate(t.x, t.y);

        ctx.beginPath();
        ctx.roundRect(-TILE_W / 2, -TILE_H / 2, TILE_W, TILE_H, 6);

        if (i < currentTileIdx) {{
            ctx.fillStyle = "rgba(255, 255, 255, 0.1)";
            ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
        }} else if (i === currentTileIdx + 1) {{
            ctx.fillStyle = "#ffd700";
            ctx.strokeStyle = "#ffffff";
            ctx.shadowColor = "#ffd700";
            ctx.shadowBlur = 12;
        }} else if (i === currentTileIdx) {{
            ctx.fillStyle = "rgba(255, 255, 255, 0.35)";
            ctx.strokeStyle = "#ffffff";
        }} else {{
            ctx.fillStyle = "#1e293b";
            ctx.strokeStyle = "#334155";
        }}

        ctx.lineWidth = 2;
        ctx.fill();
        ctx.stroke();
        ctx.restore();
    }}

    const redPos = activePlanetType === 1 ? pivotPos : activePos;
    const bluePos = activePlanetType === 1 ? activePos : pivotPos;

    // 3. 행성 간 연결선
    ctx.beginPath();
    ctx.moveTo(redPos.x, redPos.y);
    ctx.lineTo(bluePos.x, bluePos.y);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
    ctx.lineWidth = 4;
    ctx.stroke();

    // 4. 불 행성
    ctx.beginPath();
    ctx.arc(redPos.x, redPos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#ff3366";
    ctx.shadowColor = "#ff3366";
    ctx.shadowBlur = 14;
    ctx.fill();

    // 5. 얼음 행성
    ctx.beginPath();
    ctx.arc(bluePos.x, bluePos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#33ccff";
    ctx.shadowColor = "#33ccff";
    ctx.shadowBlur = 14;
    ctx.fill();

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

components.html(game_html, height=540)
