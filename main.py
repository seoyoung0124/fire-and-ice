import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="A Dance of Fire and Ice - Streamlit Edition",
    page_icon="❄️",
    layout="centered"
)

# 스트림릿 페이지 스타일 (어두운 테마)
st.markdown("""
<style>
    .stApp {
        background-color: #0b0e14;
        color: #f0f2f5;
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
st.caption("스트림릿 클라우드용 '얼음과 불의 춤' 미니 게임입니다.")

# 게임 HTML/JS 엔진
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            padding: 0;
            background-color: #0b0e14;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            user-select: none;
            overflow: hidden;
        }
        #gameCanvas {
            border: 2px solid #1f293d;
            border-radius: 16px;
            background-color: #121824;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
            cursor: pointer;
        }
        #info {
            margin-top: 15px;
            text-align: center;
        }
        .stats {
            font-size: 18px;
            color: #8a99ad;
            letter-spacing: 1px;
        }
        .stats span {
            color: #ffffff;
            font-weight: bold;
        }
        .status {
            font-size: 22px;
            font-weight: 800;
            margin-top: 8px;
            height: 30px;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="650" height="420"></canvas>
<div id="info">
    <div class="stats">점수: <span id="score">0</span> | 콤보: <span id="combo">0</span></div>
    <div id="feedback" class="status" style="color: #64b5f6;">클릭하거나 아무 키나 눌러 시작하세요!</div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const comboEl = document.getElementById('combo');
const feedbackEl = document.getElementById('feedback');

// -------------------------------------------------------------
// 핵심 게임 수치 및 기하학 설정
// -------------------------------------------------------------
const R = 45;              // 행성 회전 반지름 (Orbit Radius)
const TILE_STEP = 2 * R;   // 타일 간격 (정확히 2R = 90px)
const TILE_W = 56;         // 직사각형 타일 가로
const TILE_H = 32;         // 직사각형 타일 세로
const rotationSpeed = 0.052; // 회전 속도

let tiles = [];
let currentTileIndex = 0;
let angle = 0;
let pivotPlanet = 0; // 0: Red Pivot (Blue 회전), 1: Blue Pivot (Red 회전)

let redPos = { x: 0, y: 0 };
let bluePos = { x: 0, y: 0 };

let score = 0;
let combo = 0;
let gameStarted = false;

// -------------------------------------------------------------
// 직사각형 타일 경로 생성 (이어지는 직사각형 구조)
// -------------------------------------------------------------
function generateTiles() {
    tiles = [];
    let cx = 120;
    let cy = 210;
    
    // 격자 방향 벡터 (우, 하, 좌, 상)
    const dirs = [
        { x: 1, y: 0 },
        { x: 0, y: 1 },
        { x: -1, y: 0 },
        { x: 0, y: -1 }
    ];

    // 직사각형 회로 패턴 (오른쪽 3칸, 아래 2칸, 오른쪽 3칸, 위 2칸 ...)
    const pattern = [0, 0, 0, 1, 1, 0, 0, 0, 3, 3];
    
    tiles.push({ x: cx, y: cy });

    for (let i = 0; i < 120; i++) {
        let dirIdx = pattern[i % pattern.length];
        let d = dirs[dirIdx];
        cx += d.x * TILE_STEP;
        cy += d.y * TILE_STEP;
        tiles.push({ x: cx, y: cy });
    }

    // 초기 행성 위치 배치 (첫 타일 중심에 Red, 오른쪽 R 거리 위치에 Blue)
    redPos = { x: tiles[0].x, y: tiles[0].y };
    bluePos = { x: tiles[0].x + R, y: tiles[0].y };
    angle = 0;
}

generateTiles();

// -------------------------------------------------------------
// 프레임 업데이트
// -------------------------------------------------------------
function update() {
    if (!gameStarted) return;

    angle += rotationSpeed;

    const pivot = (pivotPlanet === 0) ? redPos : bluePos;
    const targetX = pivot.x + Math.cos(angle) * R;
    const targetY = pivot.y + Math.sin(angle) * R;

    if (pivotPlanet === 0) {
        bluePos = { x: targetX, y: targetY };
    } else {
        redPos = { x: targetX, y: targetY };
    }
}

// -------------------------------------------------------------
// 판정 및 입력 처리
// -------------------------------------------------------------
function handleInput() {
    if (!gameStarted) {
        gameStarted = true;
        feedbackEl.innerText = "START!";
        feedbackEl.style.color = "#4caf50";
        return;
    }

    const nextTile = tiles[currentTileIndex + 1];
    if (!nextTile) return;

    const activePlanet = (pivotPlanet === 0) ? bluePos : redPos;
    const dist = Math.hypot(activePlanet.x - nextTile.x, activePlanet.y - nextTile.y);

    if (dist < 18) {
        score += 100 + (combo * 10);
        combo++;
        feedbackEl.innerText = "PERFECT!";
        feedbackEl.style.color = "#00e676";
        advanceTile(nextTile);
    } else if (dist < 32) {
        score += 50;
        combo++;
        feedbackEl.innerText = "GREAT";
        feedbackEl.style.color = "#ffeb3b";
        advanceTile(nextTile);
    } else {
        combo = 0;
        feedbackEl.innerText = "MISS!";
        feedbackEl.style.color = "#ff5252";
    }

    scoreEl.innerText = score;
    comboEl.innerText = combo;
}

function advanceTile(nextTile) {
    if (pivotPlanet === 0) {
        bluePos = { x: nextTile.x, y: nextTile.y };
    } else {
        redPos = { x: nextTile.x, y: nextTile.y };
    }

    pivotPlanet = (pivotPlanet === 0) ? 1 : 0;
    currentTileIndex++;

    // 다음 회전 축 기준 각도 정렬
    const currentPivot = (pivotPlanet === 0) ? redPos : bluePos;
    const otherPlanet = (pivotPlanet === 0) ? bluePos : redPos;
    angle = Math.atan2(otherPlanet.y - currentPivot.y, otherPlanet.x - currentPivot.x);
}

// -------------------------------------------------------------
// 그래픽 렌더링
// -------------------------------------------------------------
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    const currentTile = tiles[currentTileIndex] || tiles[0];
    
    // 카메라 스무스 추적
    ctx.translate(canvas.width / 2 - currentTile.x, canvas.height / 2 - currentTile.y);

    // 1. 타일 연결 선 그리기
    ctx.beginPath();
    for (let i = 0; i < tiles.length; i++) {
        if (i === 0) ctx.moveTo(tiles[i].x, tiles[i].y);
        else ctx.lineTo(tiles[i].x, tiles[i].y);
    }
    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
    ctx.lineWidth = 6;
    ctx.stroke();

    // 2. 직사각형 타일 그리기
    for (let i = 0; i < tiles.length; i++) {
        const t = tiles[i];
        
        ctx.save();
        ctx.translate(t.x, t.y);

        ctx.beginPath();
        ctx.roundRect(-TILE_W / 2, -TILE_H / 2, TILE_W, TILE_H, 6);

        if (i < currentTileIndex) {
            ctx.fillStyle = "rgba(255, 255, 255, 0.15)";
            ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
        } else if (i === currentTileIndex + 1) {
            ctx.fillStyle = "#ffd700";
            ctx.strokeStyle = "#ffffff";
            ctx.shadowColor = "#ffd700";
            ctx.shadowBlur = 12;
        } else if (i === currentTileIndex) {
            ctx.fillStyle = "rgba(255, 255, 255, 0.4)";
            ctx.strokeStyle = "#ffffff";
        } else {
            ctx.fillStyle = "#1e293b";
            ctx.strokeStyle = "#334155";
        }

        ctx.lineWidth = 2;
        ctx.fill();
        ctx.stroke();
        ctx.restore();
    }

    // 3. 행성 연결 봉 (Link)
    ctx.beginPath();
    ctx.moveTo(redPos.x, redPos.y);
    ctx.lineTo(bluePos.x, bluePos.y);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.6)";
    ctx.lineWidth = 4;
    ctx.stroke();

    // 4. 불 행성 (Red)
    ctx.beginPath();
    ctx.arc(redPos.x, redPos.y, 13, 0, Math.PI * 2);
    ctx.fillStyle = "#ff3366";
    ctx.shadowColor = "#ff3366";
    ctx.shadowBlur = 15;
    ctx.fill();

    // 5. 얼음 행성 (Blue)
    ctx.beginPath();
    ctx.arc(bluePos.x, bluePos.y, 13, 0, Math.PI * 2);
    ctx.fillStyle = "#33ccff";
    ctx.shadowColor = "#33ccff";
    ctx.shadowBlur = 15;
    ctx.fill();

    ctx.restore();
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

// 입력 이벤트 연동
window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' || e.key !== '') {
        handleInput();
    }
});

canvas.addEventListener('mousedown', handleInput);

loop();
</script>
</body>
</html>
"""

components.html(game_html, height=520)
