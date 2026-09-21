import streamlit as st
import streamlit.components.v1 as components

# Configure page settings
st.set_page_config(
    page_title="A Dance of Fire and Ice - Streamlit Edition",
    page_icon="❄️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        /* Dark theme override for Streamlit wrapper */
        .stApp {
            background-color: #0b0d14;
            color: #f0f2f8;
        }
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 800px;
        }
        h1 {
            background: linear-gradient(135deg, #ff3366 0%, #ff9900 50%, #33ccff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            text-align: center;
            margin-bottom: 0.2rem !important;
        }
        .subtitle {
            text-align: center;
            color: #8a93b0;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>A DANCE OF FIRE AND ICE</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>🔥 얼음과 불의 춤 — Streamlit Cloud 웹 에디션 ❄️</div>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A Dance of Fire and Ice</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #0b0d14;
            color: #e2e8f0;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
            user-select: none;
            -webkit-user-select: none;
        }
        #game-container {
            position: relative;
            width: 100%;
            max-width: 680px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        #canvas-wrapper {
            position: relative;
            width: 100%;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.7), 0 0 20px rgba(51, 204, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: #111420;
        }
        canvas {
            display: block;
            width: 100%;
            height: 420px;
            cursor: pointer;
        }
        .ui-panel {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 14px;
            padding: 12px 20px;
            background: rgba(17, 20, 32, 0.8);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(10px);
        }
        .stat-box {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .stat-label {
            font-size: 0.75rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 2px;
        }
        .stat-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: #f8fafc;
            font-family: 'Courier New', monospace;
        }
        #feedback-display {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: 1.5px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-shadow: 0 0 12px currentColor;
            transition: transform 0.1s ease;
        }
        .controls-hint {
            margin-top: 12px;
            font-size: 0.85rem;
            color: #64748b;
            text-align: center;
        }
        .controls-hint kbd {
            background: #1e2338;
            color: #33ccff;
            padding: 3px 8px;
            border-radius: 4px;
            border: 1px solid rgba(51, 204, 255, 0.3);
            font-family: inherit;
            font-weight: 600;
        }
        #restart-btn {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 14px 28px;
            font-size: 1.1rem;
            font-weight: 700;
            color: #ffffff;
            background: linear-gradient(135deg, #ff3366, #ff9900);
            border: none;
            border-radius: 30px;
            box-shadow: 0 0 20px rgba(255, 51, 102, 0.5);
            cursor: pointer;
            display: none;
            z-index: 10;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        #restart-btn:hover {
            transform: translate(-50%, -50%) scale(1.05);
            box-shadow: 0 0 30px rgba(255, 51, 102, 0.8);
        }
    </style>
</head>
<body>

<div id="game-container">
    <div id="canvas-wrapper">
        <canvas id="gameCanvas" width="680" height="420"></canvas>
        <button id="restart-btn" onclick="resetGame()">다시 시작 (Restart)</button>
    </div>

    <div class="ui-panel">
        <div class="stat-box">
            <span class="stat-label">Score</span>
            <span id="score" class="stat-value">0</span>
        </div>
        
        <div id="feedback-display" style="color: #33ccff;">PRESS SPACE TO START</div>
        
        <div class="stat-box">
            <span class="stat-label">Combo</span>
            <span id="combo" class="stat-value">0</span>
        </div>
    </div>

    <div class="controls-hint">
        조작법: <kbd>SPACE</kbd> 키 또는 <kbd>화면 클릭</kbd>으로 타이밍에 맞춰 타일을 딛으세요!
    </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const scoreEl = document.getElementById('score');
const comboEl = document.getElementById('combo');
const feedbackEl = document.getElementById('feedback-display');
const restartBtn = document.getElementById('restart-btn');

// Game Engine Constants
// Key logic: ORBIT_RADIUS MUST EQUAL TILE_SPACING for 180 deg rotation alignment!
const TILE_SIZE = 44;          // Tile visual size (Square)
const TILE_SPACING = 60;       // Center-to-center distance between consecutive tiles
const ORBIT_RADIUS = 60;       // Exact radius equal to TILE_SPACING
const ROTATION_SPEED = 0.055;  // Speed of orbital rotation (radians per frame)

// Directions for Rectangular path construction (0: Right, 1: Down, 2: Left, 3: Up)
const DIR_VECTORS = [
    { x: 1, y: 0, angle: 0 },              // Right (0 radians)
    { x: 0, y: 1, angle: Math.PI / 2 },    // Down (PI/2 radians)
    { x: -1, y: 0, angle: Math.PI },       // Left (PI radians)
    { x: 0, y: -1, angle: -Math.PI / 2 }   // Up (-PI/2 radians)
];

let tiles = [];
let currentTileIndex = 0;
let angle = 0;             // Orbital angle relative to current track direction
let pivotPlanet = 0;       // 0: Fire (Red) is pivot, Ice (Blue) rotates; 1: Ice is pivot, Fire rotates
let isClockwise = true;    // Orbit rotation direction
let cameraPos = { x: 0, y: 0 };

let redPos = { x: 0, y: 0 };
let bluePos = { x: 0, y: 0 };

let score = 0;
let combo = 0;
let maxCombo = 0;
let gameState = 'START';   // 'START', 'PLAYING', 'GAMEOVER', 'CLEAR'
let particles = [];

function generateRectangularTrack() {
    tiles = [];
    let curX = 100;
    let curY = 210;

    // First tile
    tiles.push({
        x: curX,
        y: curY,
        dirIndex: 0, // Initial direction: Right
        entryAngle: 0
    });

    // Rectangular sequence pattern (Right, Down, Right, Up, Right, etc.)
    const pattern = [
        0, 0, 0, 1, 1, 0, 0, 3, 3, 0, 0, 1, 1, 2, 2, 1, 1, 0, 0, 0, 3, 3, 0, 0, 1, 1, 0, 0, 3, 3, 0, 0, 0
    ];

    let currentDir = 0;

    for (let i = 0; i < pattern.length; i++) {
        currentDir = pattern[i];
        const vec = DIR_VECTORS[currentDir];
        
        curX += vec.x * TILE_SPACING;
        curY += vec.y * TILE_SPACING;

        tiles.push({
            x: curX,
            y: curY,
            dirIndex: currentDir,
            entryAngle: vec.angle
        });
    }

    // Add extra straight buffer tiles at the end
    for (let i = 0; i < 10; i++) {
        curX += DIR_VECTORS[0].x * TILE_SPACING;
        curY += DIR_VECTORS[0].y * TILE_SPACING;
        tiles.push({
            x: curX,
            y: curY,
            dirIndex: 0,
            entryAngle: 0
        });
    }
}

function initGame() {
    generateRectangularTrack();
    currentTileIndex = 0;
    pivotPlanet = 0; // Red is initial pivot
    
    // Set initial pivot planet position on first tile
    redPos = { x: tiles[0].x, y: tiles[0].y };
    
    // Position rotating planet (Blue) relative to initial tile direction (Right)
    const targetDir = tiles[0].dirIndex;
    const baseAngle = DIR_VECTORS[targetDir].angle;
    
    // Start rotating planet opposite to movement direction (180 deg / PI radians out)
    angle = baseAngle + Math.PI;
    bluePos = {
        x: redPos.x + Math.cos(angle) * ORBIT_RADIUS,
        y: redPos.y + Math.sin(angle) * ORBIT_RADIUS
    };

    cameraPos = { x: tiles[0].x, y: tiles[0].y };
    score = 0;
    combo = 0;
    maxCombo = 0;
    gameState = 'START';
    particles = [];

    scoreEl.innerText = score;
    comboEl.innerText = combo;
    feedbackEl.innerText = "PRESS SPACE TO START";
    feedbackEl.style.color = "#33ccff";
    restartBtn.style.display = "none";
}

function createExplosion(x, y, color) {
    for (let i = 0; i < 16; i++) {
        const pAngle = Math.random() * Math.PI * 2;
        const speed = 2 + Math.random() * 5;
        particles.push({
            x: x,
            y: y,
            vx: Math.cos(pAngle) * speed,
            vy: Math.sin(pAngle) * speed,
            life: 1.0,
            color: color,
            size: 3 + Math.random() * 4
        });
    }
}

function updateParticles() {
    for (let i = particles.length - 1; i >= 0; i--) {
        let p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life -= 0.03;
        if (p.life <= 0) {
            particles.splice(i, 1);
        }
    }
}

function update() {
    if (gameState !== 'PLAYING') return;

    // Increment rotation angle
    angle += ROTATION_SPEED;

    // Calculate orbiting planet position around current pivot
    const pivot = pivotPlanet === 0 ? redPos : bluePos;
    const currentOrbiterPos = {
        x: pivot.x + Math.cos(angle) * ORBIT_RADIUS,
        y: pivot.y + Math.sin(angle) * ORBIT_RADIUS
    };

    if (pivotPlanet === 0) {
        bluePos = currentOrbiterPos;
    } else {
        redPos = currentOrbiterPos;
    }

    // Smooth camera tracking to current tile
    const currentTile = tiles[currentTileIndex];
    if (currentTile) {
        cameraPos.x += (currentTile.x - cameraPos.x) * 0.1;
        cameraPos.y += (currentTile.y - cameraPos.y) * 0.1;
    }

    // Automatic miss condition if rotated too far past the target tile (passed by over ~90 degrees)
    const nextTile = tiles[currentTileIndex + 1];
    if (nextTile) {
        const orbiter = pivotPlanet === 0 ? bluePos : redPos;
        const dist = Math.hypot(orbiter.x - nextTile.x, orbiter.y - nextTile.y);
        
        // If orbiter moves away after passing close enough
        if (dist > ORBIT_RADIUS * 1.8 && angle > Math.PI * 2.5) {
            triggerMiss("TOO LATE!");
        }
    }
}

function handleInput() {
    if (gameState === 'START') {
        gameState = 'PLAYING';
        feedbackEl.innerText = "START!";
        feedbackEl.style.color = "#00e676";
        return;
    }

    if (gameState !== 'PLAYING') return;

    const nextTile = tiles[currentTileIndex + 1];
    if (!nextTile) return;

    const orbiter = pivotPlanet === 0 ? bluePos : redPos;
    const distanceToNext = Math.hypot(orbiter.x - nextTile.x, orbiter.y - nextTile.y);

    // Strict distance-based timing thresholds
    if (distanceToNext < 14) {
        // Perfect hit
        score += 100 + (combo * 15);
        combo++;
        feedbackEl.innerText = "PERFECT!!";
        feedbackEl.style.color = "#00e676";
        createExplosion(nextTile.x, nextTile.y, pivotPlanet === 0 ? "#33ccff" : "#ff3366");
        advanceTile(nextTile);
    } else if (distanceToNext < 28) {
        // Great hit
        score += 60 + (combo * 5);
        combo++;
        feedbackEl.innerText = "GREAT!";
        feedbackEl.style.color = "#ffd700";
        createExplosion(nextTile.x, nextTile.y, "#ffd700");
        advanceTile(nextTile);
    } else if (distanceToNext < 42) {
        // Early / Late warning (Missed combo but survive)
        combo = 0;
        feedbackEl.innerText = "TOO EARLY / LATE";
        feedbackEl.style.color = "#ff9900";
        advanceTile(nextTile);
    } else {
        // Complete Miss - Game Over
        triggerMiss("MISS!");
    }

    scoreEl.innerText = score;
    comboEl.innerText = combo;
}

function advanceTile(nextTile) {
    currentTileIndex++;

    // Lock orbiter precisely to the target tile center
    if (pivotPlanet === 0) {
        bluePos = { x: nextTile.x, y: nextTile.y };
    } else {
        redPos = { x: nextTile.x, y: nextTile.y };
    }

    // Switch pivot planet
    pivotPlanet = pivotPlanet === 0 ? 1 : 0;

    // Adjust angle for the new orbit around the new pivot
    // Target direction vector angle from new pivot to upcoming tile
    const upcomingTile = tiles[currentTileIndex + 1];
    if (upcomingTile) {
        const dx = upcomingTile.x - nextTile.x;
        const dy = upcomingTile.y - nextTile.y;
        const targetDirectionAngle = Math.atan2(dy, dx);

        // Start orbit from the current pivot position relative angle
        angle = targetDirectionAngle + Math.PI;
    } else {
        // Level Complete
        gameState = 'CLEAR';
        feedbackEl.innerText = "STAGE CLEAR!! 🎉";
        feedbackEl.style.color = "#00e676";
        restartBtn.style.display = "block";
    }
}

function triggerMiss(reason) {
    combo = 0;
    comboEl.innerText = combo;
    feedbackEl.innerText = reason;
    feedbackEl.style.color = "#ff3366";
    gameState = 'GAMEOVER';
    
    const orbiter = pivotPlanet === 0 ? bluePos : redPos;
    createExplosion(orbiter.x, orbiter.y, "#ff3366");
    restartBtn.style.display = "block";
}

function resetGame() {
    initGame();
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Deep Dark Grid Background
    ctx.save();
    ctx.fillStyle = "#0b0d14";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Subtle background grid lines
    ctx.strokeStyle = "rgba(255, 255, 255, 0.03)";
    ctx.lineWidth = 1;
    const gridSize = 40;
    const offsetX = (-cameraPos.x + canvas.width / 2) % gridSize;
    const offsetY = (-cameraPos.y + canvas.height / 2) % gridSize;

    for (let x = offsetX; x < canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    for (let y = offsetY; y < canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }

    // Camera transform centering on current progress
    ctx.translate(canvas.width / 2 - cameraPos.x, canvas.height / 2 - cameraPos.y);

    // 1. Draw Connecting Track Paths (Connected Rectangular Path)
    for (let i = 0; i < tiles.length - 1; i++) {
        const t1 = tiles[i];
        const t2 = tiles[i + 1];

        ctx.beginPath();
        ctx.moveTo(t1.x, t1.y);
        ctx.lineTo(t2.x, t2.y);
        
        if (i < currentTileIndex) {
            ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
            ctx.lineWidth = 14;
        } else {
            ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
            ctx.lineWidth = 14;
        }
        ctx.stroke();
    }

    // 2. Draw Rectangular Connected Tiles
    for (let i = 0; i < tiles.length; i++) {
        const t = tiles[i];
        const isPassed = i < currentTileIndex;
        const isCurrent = i === currentTileIndex;
        const isNext = i === currentTileIndex + 1;

        ctx.save();
        ctx.translate(t.x, t.y);

        if (isCurrent) {
            // Active current tile glow
            ctx.shadowColor = "#ffffff";
            ctx.shadowBlur = 12;
            ctx.fillStyle = "#ffffff";
        } else if (isNext) {
            // Target tile golden neon glow
            ctx.shadowColor = "#ffd700";
            ctx.shadowBlur = 16;
            ctx.fillStyle = "#ffd700";
        } else if (isPassed) {
            ctx.fillStyle = "rgba(255, 255, 255, 0.25)";
        } else {
            ctx.fillStyle = "rgba(255, 255, 255, 0.5)";
        }

        // Draw square rounded tiles forming continuous paths
        const half = TILE_SIZE / 2;
        ctx.beginPath();
        ctx.roundRect(-half, -half, TILE_SIZE, TILE_SIZE, 8);
        ctx.fill();

        // Inner tile accent border
        ctx.strokeStyle = isNext ? "#ffffff" : "rgba(0, 0, 0, 0.4)";
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.restore();
    }

    // 3. Draw Connecting Orbit Line between Red & Blue planets
    ctx.beginPath();
    ctx.moveTo(redPos.x, redPos.y);
    ctx.lineTo(bluePos.x, bluePos.y);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
    ctx.lineWidth = 3;
    ctx.setLineDash([4, 4]);
    ctx.stroke();
    ctx.setLineDash([]);

    // 4. Draw Particles
    for (let p of particles) {
        ctx.save();
        ctx.globalAlpha = Math.max(0, p.life);
        ctx.fillStyle = p.color;
        ctx.shadowColor = p.color;
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // 5. Draw Fire Planet (Red / Orange)
    ctx.save();
    ctx.shadowColor = "#ff3366";
    ctx.shadowBlur = pivotPlanet === 0 ? 20 : 10;
    ctx.fillStyle = "#ff3366";
    ctx.beginPath();
    ctx.arc(redPos.x, redPos.y, 15, 0, Math.PI * 2);
    ctx.fill();
    // Inner core
    ctx.fillStyle = "#ffcc00";
    ctx.beginPath();
    ctx.arc(redPos.x, redPos.y, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // 6. Draw Ice Planet (Cyan / Blue)
    ctx.save();
    ctx.shadowColor = "#33ccff";
    ctx.shadowBlur = pivotPlanet === 1 ? 20 : 10;
    ctx.fillStyle = "#33ccff";
    ctx.beginPath();
    ctx.arc(bluePos.x, bluePos.y, 15, 0, Math.PI * 2);
    ctx.fill();
    // Inner core
    ctx.fillStyle = "#ffffff";
    ctx.beginPath();
    ctx.arc(bluePos.x, bluePos.y, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    ctx.restore(); // Restore camera matrix
}

function gameLoop() {
    update();
    updateParticles();
    draw();
    requestAnimationFrame(gameLoop);
}

// Key & Event Listeners
window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' || e.key === ' ') {
        e.preventDefault();
        handleInput();
    }
});

canvas.addEventListener('mousedown', (e) => {
    e.preventDefault();
    handleInput();
});

// Start game on window load
initGame();
gameLoop();
</script>
</body>
</html>
"""

# Render embedded HTML component with exact dimensions
components.html(game_html, height=540)

st.markdown("""
---
### 🛠️ 수정사항 안내:
1. **간격 정확도 개선**: 행성 회전 반지름(`ORBIT_RADIUS = 60`)과 타일 간격(`TILE_SPACING = 60`)을 1:1로 일치시켜, 180도 회전 시 다음 타일 중심에 정확히 착지합니다.
2. **직각 연결 타일 트랙**: 타일이 끊어지지 않는 90도 직속/꺾임 구조의 연속된 사각형 타일 트랙으로 생성됩니다.
3. **네온 다크 테마**: 어두운 트론 스타일 배경(`0b0d14`) 및 불(Red/Orange), 얼음(Cyan/Blue), 황금색 목표 타일 Glow 효과가 적용되었습니다.
""")
```

```text:Requirements specification:requirements.txt
streamlit
