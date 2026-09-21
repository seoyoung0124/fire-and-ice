import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="A Dance of Fire and Ice - Streamlit Edition",
    page_icon="❄️",
    layout="centered"
)

# 스트림릿 다크 테마
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
    }
    .stCaption {
        text-align: center;
        color: #9aa0a6;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔥 A Dance of Fire and Ice ❄️")
st.caption("행성이 타일 직상단에 올 때 스페이스바/클릭으로 맞추세요!")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; }
        body {
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
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="650" height="400"></canvas>
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
// 핵심 게임 메커니즘 변수
// -------------------------------------------------------------
const R = 45;              // 피벗 중심 간격 (행성 반지름)
const TILE_W = 60;         // 타일 가로 길이
const TILE_H = 34;         // 타일 세로 길이

let tiles = [];
let currentTileIdx = 0;

let pivotPos = { x: 0, y: 0 };
let activePos = { x: 0, y: 0 };

let currentAngle = 0;       // 현재 진행 각도
let startAngle = 0;         // 이번 회전의 시작 각도
let targetAngle = Math.PI;  // 목표 착지 각도 (항상 180도)
let rotSpeed = 0.05;        // 회전 속도

let activePlanetType = 1;   // 0: Red(불), 1: Blue(얼음) 회전 중
let score = 0;
let combo = 0;
let gameStarted = false;

// -------------------------------------------------------------
// 직교 타일 트랙 생성 (상/하/좌/우 연쇄 구조)
// -------------------------------------------------------------
function generateMap() {
    tiles = [];
    let cx = 150;
    let cy = 200;
    
    // 이동 방향 패턴 (0: 우, 1: 하, 2: 우, 3: 상)
    const dirs = [
        { x: 1, y: 0 }, { x: 1, y: 0 }, { x: 0, y: 1 },
        { x: 1, y: 0 }, { x: 1, y: 0 }, { x: 0, y: -1 }
    ];

    tiles.push({ x: cx, y: cy });

    for (let i = 0; i < 200; i++) {
        let d = dirs[i % dirs.length];
        cx += d.x * (2 * R);
        cy += d.y * (2 * R);
        tiles.push({ x: cx, y: cy });
    }

    resetGame();
}

function resetGame() {
    currentTileIdx = 0;
    pivotPos = { x: tiles[0].x, y: tiles[0].y };
    
    // 첫번째 목표 타일 방향으로 오프셋 연산
    const nextTile = tiles[1];
    const baseAngle = Math.atan2(nextTile.y - pivotPos.y, nextTile.x - pivotPos.x);
    
    startAngle = baseAngle - Math.PI;
    currentAngle = startAngle;
    targetAngle = baseAngle;

    activePlanetType = 1; // Blue 회전 시작
    updateActivePos();
}

function updateActivePos() {
    activePos.x = pivotPos.x + Math.cos(currentAngle) * (2 * R);
    activePos.y = pivotPos.y + Math.sin(currentAngle) * (2 * R);
}

generateMap();

// -------------------------------------------------------------
// 프레임 루프 및 위치 계산
// -------------------------------------------------------------
function update() {
    if (!gameStarted) return;

    currentAngle += rotSpeed;
    updateActivePos();

    // 입력 없이 목표 각도를 너무 지나치면 오버슈트(MISS)
    if (currentAngle > targetAngle + 0.8) {
        combo = 0;
        feedbackEl.innerText = "TOO LATE!";
        feedbackEl.style.color = "#ff5252";
        comboEl.innerText = combo;
        
        // 각도 재설정 (다시 회전하도록)
        startAngle = targetAngle;
        targetAngle += Math.PI;
    }
}

// -------------------------------------------------------------
// 판정 로직 (각도 차이 기반 정밀 판정)
// -------------------------------------------------------------
function handleInput() {
    if (!gameStarted) {
        gameStarted = true;
        feedbackEl.innerText = "START!";
        feedbackEl.style.color = "#4caf50";
        return;
    }

    const diff = Math.abs(currentAngle - targetAngle);

    if (diff < 0.25) {
        score += 100 + (combo * 10);
        combo++;
        feedbackEl.innerText = "PERFECT!";
        feedbackEl.style.color = "#00e676";
        advanceToNextTile();
    } else if (diff < 0.45) {
        score += 50;
        combo++;
        feedbackEl.innerText = "GREAT";
        feedbackEl.style.color = "#ffeb3b";
        advanceToNextTile();
    } else {
        combo = 0;
        feedbackEl.innerText = "MISS!";
        feedbackEl.style.color = "#ff5252";
    }

    scoreEl.innerText = score;
    comboEl.innerText = combo;
}

function advanceToNextTile() {
    currentTileIdx++;
    const nextPivot = tiles[currentTileIdx];
    if (!nextPivot) return;

    // 피벗을 성공한 다음 타일 위치로 강제 고정
    pivotPos = { x: nextPivot.x, y: nextPivot.y };
    activePlanetType = activePlanetType === 0 ? 1 : 0;

    const futureTile = tiles[currentTileIdx + 1];
    if (futureTile) {
        const baseAngle = Math.atan2(futureTile.y - pivotPos.y, futureTile.x - pivotPos.x);
        startAngle = baseAngle - Math.PI;
        currentAngle = startAngle;
        targetAngle = baseAngle;
    }
    updateActivePos();
}

// -------------------------------------------------------------
// Canvas 그래픽 렌더링
// -------------------------------------------------------------
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    // 피벗 타일을 카메라 중심에 고정
    ctx.translate(canvas.width / 2 - pivotPos.x, canvas.height / 2 - pivotPos.y);

    // 1. 경로 라인
    ctx.beginPath();
    for (let i = 0; i < tiles.length; i++) {
        if (i === 0) ctx.moveTo(tiles[i].x, tiles[i].y);
        else ctx.lineTo(tiles[i].x, tiles[i].y);
    }
    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
    ctx.lineWidth = 6;
    ctx.stroke();

    // 2. 직사각형 타일 렌더링
    for (let i = 0; i < tiles.length; i++) {
        const t = tiles[i];
        
        ctx.save();
        ctx.translate(t.x, t.y);

        ctx.beginPath();
        ctx.roundRect(-TILE_W / 2, -TILE_H / 2, TILE_W, TILE_H, 6);

        if (i < currentTileIdx) {
            ctx.fillStyle = "rgba(255, 255, 255, 0.1)";
            ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
        } else if (i === currentTileIdx + 1) {
            ctx.fillStyle = "#ffd700";
            ctx.strokeStyle = "#ffffff";
            ctx.shadowColor = "#ffd700";
            ctx.shadowBlur = 12;
        } else if (i === currentTileIdx) {
            ctx.fillStyle = "rgba(255, 255, 255, 0.35)";
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

    // 위치 할당 (Red/Blue 구분)
    const redPos = activePlanetType === 1 ? pivotPos : activePos;
    const bluePos = activePlanetType === 1 ? activePos : pivotPos;

    // 3. 행성 연결 선
    ctx.beginPath();
    ctx.moveTo(redPos.x, redPos.y);
    ctx.lineTo(bluePos.x, bluePos.y);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
    ctx.lineWidth = 4;
    ctx.stroke();

    // 4. 불 행성 (Red)
    ctx.beginPath();
    ctx.arc(redPos.x, redPos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#ff3366";
    ctx.shadowColor = "#ff3366";
    ctx.shadowBlur = 14;
    ctx.fill();

    // 5. 얼음 행성 (Blue)
    ctx.beginPath();
    ctx.arc(bluePos.x, bluePos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#33ccff";
    ctx.shadowColor = "#33ccff";
    ctx.shadowBlur = 14;
    ctx.fill();

    ctx.restore();
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

// 이벤트 바인딩
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
