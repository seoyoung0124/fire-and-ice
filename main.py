import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="A Dance of Fire and Ice - Streamlit Edition",
    page_icon="❄️",
    layout="centered"
)

# 스트림릿 전체 어두운 테마 설정
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
st.caption("키보드 아무 키나 누르거나 화면을 클릭하여 박자에 맞추세요!")

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
// 수치 및 기하학 상수
// -------------------------------------------------------------
const R = 45;              // 회전 반지름 (Orbit Radius)
const TILE_STEP = 2 * R;   // 타일 간 거리 (90px - Exact 2R)
const TILE_W = 60;         // 직사각형 타일 너비
const TILE_H = 34;         // 직사각형 타일 높이

let tiles = [];
let currentTileIndex = 0;
let pivotPlanet = 0; // 0: Red Pivot (Blue 회전), 1: Blue Pivot (Red 회전)
let angle = 0;       // 현재 회전 각도 (라디안)
let rotSpeed = 0.045; // 회전 속도

let redPos = { x: 0, y: 0 };
let bluePos = { x: 0, y: 0 };

let score = 0;
let combo = 0;
let gameStarted = false;

// -------------------------------------------------------------
// 이어지는 직사각형 경로(직교 트랙) 생성
// -------------------------------------------------------------
function generateTiles() {
    tiles = [];
    let cx = 150;
    let cy = 200;
    
    // 이동 방향 벡터 (오른쪽, 아래, 오른쪽, 위 ...)
    const dirs = [
        { x: 1, y: 0 }, { x: 1, y: 0 }, { x: 0, y: 1 },
        { x: 1, y: 0 }, { x: 1, y: 0 }, { x: 0, y: -1 }
    ];

    tiles.push({ x: cx, y: cy });

    for (let i = 0; i < 150; i++) {
        let d = dirs[i % dirs.length];
        cx += d.x * TILE_STEP;
        cy += d.y * TILE_STEP;
        tiles.push({ x: cx, y: cy });
    }

    resetGame();
}

function resetGame() {
    currentTileIndex = 0;
    pivotPlanet = 0; // Red 기준
    redPos = { x: tiles[0].x, y: tiles[0].y };
    
    // 다음 타일 방향으로 첫 회전각 시작 정렬
    const nextTile = tiles[1];
    const initialAngle = Math.atan2(nextTile.y - redPos.y, nextTile.x - redPos.x);
    angle = initialAngle - Math.PI; // 반대편에서 출발해서 목표 타일로 회전
    
    bluePos = {
        x: redPos.x + Math.cos(angle) * R,
        y: redPos.y + Math.sin(angle) * R
    };
}

generateTiles();

// -------------------------------------------------------------
// 프레임 업데이트
// -------------------------------------------------------------
function update() {
    if (!gameStarted) return;

    angle += rotSpeed;

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
// 입력 및 판정 처리
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

    // 회전 중인 행성 위치
    const activePlanet = (pivotPlanet === 0) ? bluePos : redPos;
    const dist = Math.hypot(activePlanet.x - nextTile.x, activePlanet.y - nextTile.y);

    // 판정 거리 (타일 크기에 맞춰 완화)
    if (dist < 28) {
        score += 100 + (combo * 10);
        combo++;
        feedbackEl.innerText = "PERFECT!";
        feedbackEl.style.color = "#00e676";
        advanceTile(nextTile);
    } else if (dist < 45) {
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
    // 1. 회전 행성을 목표 타일 중심 위치에 정확히 고정
    if (pivotPlanet === 0) {
        bluePos = { x: nextTile.x, y: nextTile.y };
    } else {
        redPos = { x: nextTile.x, y: nextTile.y };
    }

    // 2. 피벗 전환 (회전하는 공이 새 피벗이 됨)
    pivotPlanet = (pivotPlanet === 0) ? 1 : 0;
    currentTileIndex++;

    // 3. 다가올 그 다음 타일 방향을 찾아 회전 각도 동기화
    const futureTile = tiles[currentTileIndex + 1];
    if (futureTile) {
        const currentPivot = (pivotPlanet === 0) ? redPos : bluePos;
        const targetAngle = Math.atan2(futureTile.y - currentPivot.y, futureTile.x - currentPivot.x);
        
        // 회전하는 공이 반대편에서 타일 방향으로 오도록 180도(PI) 차감
        angle = targetAngle - Math.PI;
    }
}

// -------------------------------------------------------------
// 그래픽 그려주기 (Dark Theme)
// -------------------------------------------------------------
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    const currentTile = tiles[currentTileIndex] || tiles[0];
    
    // 카메라 스무스 추적 (현재 타일을 화면 중앙으로)
    ctx.translate(canvas.width / 2 - currentTile.x, canvas.height / 2 - currentTile.y);

    // 1. 경로 선
    ctx.beginPath();
    for (let i = 0; i < tiles.length; i++) {
        if (i === 0) ctx.moveTo(tiles[i].x, tiles[i].y);
        else ctx.lineTo(tiles[i].x, tiles[i].y);
    }
    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
    ctx.lineWidth = 6;
    ctx.stroke();

    // 2. 직사각형 타일
    for (let i = 0; i < tiles.length; i++) {
        const t = tiles[i];
        
        ctx.save();
        ctx.translate(t.x, t.y);

        ctx.beginPath();
        ctx.roundRect(-TILE_W / 2, -TILE_H / 2, TILE_W, TILE_H, 6);

        if (i < currentTileIndex) {
            ctx.fillStyle = "rgba(255, 255, 255, 0.12)";
            ctx.strokeStyle = "rgba(255, 255, 255, 0.18)";
        } else if (i === currentTileIndex + 1) {
            ctx.fillStyle = "#ffd700";
            ctx.strokeStyle = "#ffffff";
            ctx.shadowColor = "#ffd700";
            ctx.shadowBlur = 12;
        } else if (i === currentTileIndex) {
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

    // 3. 두 행성 간 연결선
    ctx.beginPath();
    ctx.moveTo(redPos.x, redPos.y);
    ctx.lineTo(bluePos.x, bluePos.y);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.6)";
    ctx.lineWidth = 4;
    ctx.stroke();

    // 4. 불 행성 (Red)
    ctx.beginPath();
    ctx.arc(redPos.x, redPos.y, 14, 0, Math.PI * 2);
    ctx.fillStyle = "#ff3366";
    ctx.shadowColor = "#ff3366";
    ctx.shadowBlur = 15;
    ctx.fill();

    // 5. 얼음 행성 (Blue)
    ctx.beginPath();
    ctx.arc(bluePos.x, bluePos.y, 14, 0, Math.PI * 2);
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

// 이벤트 핸들러
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
