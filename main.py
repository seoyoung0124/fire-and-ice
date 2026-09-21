import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="A Dance of Fire and Ice - Streamlit Edition",
    page_icon="❄️",
    layout="centered"
)

st.title("🔥 A Dance of Fire and Ice ❄️")
st.caption("스트림릿 클라우드에서 바로 플레이 가능한 '얼음과 불의 춤' 미니 게임입니다.")

# 게임 가이드
st.markdown("""
**🎮 게임 방법:**
- **아무 키**나 눌러서(또는 화면 클릭) 궤도를 도는 행성을 다음 타일에 맞추세요!
- 박자에 정확히 맞춰 누르면 점수가 올라갑니다.
- 실패하면 **'PERFECT'**, **'GREAT'**, **'TOO EARLY / LATE'** 또는 **'MISS'** 판정이 나타납니다.
""")

# HTML/JS 게임 엔진
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #0e1117;
            color: white;
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            user-select: none;
        }
        #gameCanvas {
            border: 2px solid #333;
            border-radius: 12px;
            background-color: #1a1c23;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        }
        #info {
            margin-top: 10px;
            text-align: center;
            font-size: 16px;
        }
        .status {
            font-size: 20px;
            font-weight: bold;
            margin-top: 5px;
            height: 24px;
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="600" height="400"></canvas>
<div id="info">
    <div>점수: <span id="score">0</span> | 콤보: <span id="combo">0</span></div>
    <div id="feedback" class="status">아무 키나 눌러 시작하세요!</div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const comboEl = document.getElementById('combo');
const feedbackEl = document.getElementById('feedback');

// 게임 변수
const tileSize = 40;
const orbitRadius = 45;
let rotationSpeed = 0.05; // 회전 속도 (BPM과 유사)

// 타일 맵 (경로)
let tiles = [];
function generateTiles() {
    tiles = [{ x: 100, y: 200 }];
    const directions = [0, 0, 0, Math.PI/2, Math.PI/2, 0, 0, -Math.PI/2, -Math.PI/2, 0, 0]; 
    let cx = 100;
    let cy = 200;

    // 긴 무한 경로 생성
    for (let i = 0; i < 100; i++) {
        let dir = directions[i % directions.length];
        cx += Math.cos(dir) * (orbitRadius * 2);
        cy += Math.sin(dir) * (orbitRadius * 2);
        tiles.push({ x: cx, y: cy });
    }
}
generateTiles();

let currentTileIndex = 0;
let angle = 0; // 현재 회전 각도
let pivotPlanet = 0; // 0: Red가 Pivot (Blue가 회전), 1: Blue가 Pivot (Red가 회전)

// 행성 위치
let redPos = { x: tiles[0].x, y: tiles[0].y };
let bluePos = { x: tiles[0].x + orbitRadius, y: tiles[0].y };

let score = 0;
let combo = 0;
let gameStarted = false;

function update() {
    if (!gameStarted) return;

    angle += rotationSpeed;

    // Pivot 축을 기준으로 회전하는 행성의 위치 업데이트
    const pivot = pivotPlanet === 0 ? redPos : bluePos;
    const orbiterAngle = angle;
    
    const targetX = pivot.x + Math.cos(orbiterAngle) * orbitRadius;
    const targetY = pivot.y + Math.sin(orbiterAngle) * orbitRadius;

    if (pivotPlanet === 0) {
        bluePos = { x: targetX, y: targetY };
    } else {
        redPos = { x: targetX, y: targetY };
    }
}

function handleInput() {
    if (!gameStarted) {
        gameStarted = true;
        feedbackEl.innerText = "START!";
        feedbackEl.style.color = "#4CAF50";
        return;
    }

    const nextTile = tiles[currentTileIndex + 1];
    if (!nextTile) return;

    // 현재 회전 중인 행성의 위치
    const activePlanet = pivotPlanet === 0 ? bluePos : redPos;

    // 목표 타일과의 거리 계산
    const dist = Math.hypot(activePlanet.x - nextTile.x, activePlanet.y - nextTile.y);

    if (dist < 20) {
        // 성공 (Perfect)
        score += 100 + (combo * 10);
        combo++;
        feedbackEl.innerText = "PERFECT!";
        feedbackEl.style.color = "#00E676";
        advanceTile(nextTile);
    } else if (dist < 35) {
        // 성공 (Great)
        score += 50;
        combo++;
        feedbackEl.innerText = "GREAT";
        feedbackEl.style.color = "#FFEB3B";
        advanceTile(nextTile);
    } else {
        // 실패 (Miss)
        combo = 0;
        feedbackEl.innerText = "MISS!";
        feedbackEl.style.color = "#FF5252";
    }

    scoreEl.innerText = score;
    comboEl.innerText = combo;
}

function advanceTile(nextTile) {
    // 회전 중이던 행성을 타일 중심 위치에 정확히 고정
    if (pivotPlanet === 0) {
        bluePos = { x: nextTile.x, y: nextTile.y };
    } else {
        redPos = { x: nextTile.x, y: nextTile.y };
    }

    // Pivot 축 교체 (다음 행성이 회전)
    pivotPlanet = pivotPlanet === 0 ? 1 : 0;
    currentTileIndex++;
    
    // 각도 반전 (상대 회전 방향 정렬)
    angle = angle + Math.PI;
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 카메라 추적 (현재 타일 기준)
    ctx.save();
    const currentTile = tiles[currentTileIndex] || tiles[0];
    ctx.translate(canvas.width / 2 - currentTile.x, canvas.height / 2 - currentTile.y);

    // 1. 타일 그리기
    for (let i = 0; i < tiles.length; i++) {
        const t = tiles[i];
        ctx.beginPath();
        ctx.arc(t.x, t.y, 12, 0, Math.PI * 2);
        
        if (i < currentTileIndex) {
            ctx.fillStyle = "rgba(255, 255, 255, 0.2)"; // 지나온 타일
        } else if (i === currentTileIndex + 1) {
            ctx.fillStyle = "#FFD700"; // 목표 타일
        } else {
            ctx.fillStyle = "rgba(255, 255, 255, 0.6)"; // 대기 타일
        }
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#444";
        ctx.stroke();
    }

    // 2. 행성 간 연결 선
    ctx.beginPath();
    ctx.moveTo(redPos.x, redPos.y);
    ctx.lineTo(bluePos.x, bluePos.y);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
    ctx.lineWidth = 3;
    ctx.stroke();

    // 3. 불 행성 (Red)
    ctx.beginPath();
    ctx.arc(redPos.x, redPos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#FF3366";
    ctx.shadowColor = "#FF3366";
    ctx.shadowBlur = 12;
    ctx.fill();

    // 4. 얼음 행성 (Blue)
    ctx.beginPath();
    ctx.arc(bluePos.x, bluePos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#33CCFF";
    ctx.shadowColor = "#33CCFF";
    ctx.shadowBlur = 12;
    ctx.fill();

    ctx.restore();
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

// 키보드 및 클릭 이벤트
window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' || e.key !== '') {
        handleInput();
    }
});

canvas.addEventListener('click', handleInput);

loop();
</script>
</body>
</html>
"""

# Streamlit 화면에 HTML 컴포넌트로 내장
components.html(game_html, height=520)

st.divider()
st.caption("Streamlit Cloud 배포 안내: `requirements.txt`에 `streamlit`만 추가하고 바로 배포하세요.")
