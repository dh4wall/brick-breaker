const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startButton = document.getElementById('startButton');
const playAgainButton = document.getElementById('playAgainButton');
const quitButton = document.getElementById('quitButton');
const livesDisplay = document.getElementById('livesDisplay');

const paddleHitSound = document.getElementById('paddleHitSound');
const brickBreakSound = document.getElementById('brickBreakSound');
const powerupSound = document.getElementById('powerupSound');
const gameOverSound = document.getElementById('gameOverSound');

let paddlePos = canvas.width / 2;
let keys = { left: false, right: false };
let gameRunning = false;
let lastState = { bricks: [], powerups: [], balls: [], lasers: [] };

document.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    paddlePos = e.clientX - rect.left;
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') keys.left = true;
    if (e.key === 'ArrowRight') keys.right = true;
});

document.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowLeft') keys.left = false;
    if (e.key === 'ArrowRight') keys.right = false;
});

canvas.addEventListener('click', () => {
    if (gameRunning && lastState.laser_active) {
        fetch('/game/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paddle_pos: paddlePos, keys, shoot_laser: true })
        })
        .then(response => response.json())
        .then(state => {
            lastState = { ...state, bricks: [...state.bricks], powerups: [...state.powerups], balls: [...state.balls], lasers: [...state.lasers] };
        });
    }
});

startButton.addEventListener('click', () => {
    startButton.style.display = 'none';
    quitButton.style.display = 'block';
    playAgainButton.style.display = 'none';
    fetch('/game/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'start' })
    })
    .then(response => response.json())
    .then(state => {
        gameRunning = true;
        updateGame();
    });
});

playAgainButton.addEventListener('click', () => {
    playAgainButton.style.display = 'none';
    quitButton.style.display = 'block';
    startButton.style.display = 'block';
    fetch('/game/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'reset' })
    })
    .then(response => response.json())
    .then(state => {
        gameRunning = true;
    });
});

quitButton.addEventListener('click', () => {
    fetch('/game/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'quit' })
    })
    .then(response => response.json())
    .then(state => {
        gameRunning = false;
        window.location.href = '/';
    });
});

function playSound(sound) {
    if (sound) {
        try {
            sound.currentTime = 0;
            sound.play().catch(err => console.error('Audio play error:', err));
        } catch (err) {
            console.error('Sound playback failed:', err);
        }
    }
}

function drawGame(state) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (state.state === 'waiting') {
        ctx.fillStyle = '#00ffff';
        ctx.font = '40px Orbitron';
        ctx.textAlign = 'center';
        ctx.fillText('Press Start to Play', canvas.width / 2, canvas.height / 2 - 50);
        startButton.style.display = 'block';
        playAgainButton.style.display = 'none';
        quitButton.style.display = 'none';
        return;
    }

    if (state.state === 'game_over') {
        playSound(gameOverSound);
        ctx.fillStyle = '#ff4444';
        ctx.font = '40px Orbitron';
        ctx.textAlign = 'center';
        ctx.fillText('Game Over', canvas.width / 2, canvas.height / 2 - 50);
        ctx.fillText(`Score: ${state.score}`, canvas.width / 2, canvas.height / 2);
        startButton.style.display = 'none';
        playAgainButton.style.display = 'block';
        quitButton.style.display = 'none';
        gameRunning = false;
        return;
    }

    // Update lives
    livesDisplay.textContent = state.lives;

    // Draw paddle
    const paddleGradient = ctx.createLinearGradient(state.paddle[0], state.paddle[1], state.paddle[0] + state.paddle[2], state.paddle[1]);
    paddleGradient.addColorStop(0, '#00ffff');
    paddleGradient.addColorStop(1, '#ff00ff');
    ctx.fillStyle = paddleGradient;
    ctx.fillRect(state.paddle[0], state.paddle[1], state.paddle[2], state.paddle[3]);
    ctx.shadowColor = '#00ffff';
    ctx.shadowBlur = 10;

    // Detect paddle hits
    state.balls.forEach(ball => {
        if (lastState.balls.some(b => b.pos[1] > state.paddle[1] && ball.pos[1] <= state.paddle[1] && state.paddle[0] <= ball.pos[0] <= state.paddle[0] + state.paddle[2])) {
            playSound(paddleHitSound);
        }
    });

    // Draw balls
    state.balls.forEach(ball => {
        ctx.beginPath();
        ctx.arc(ball.pos[0], ball.pos[1], 8, 0, Math.PI * 2);
        ctx.fillStyle = '#fff';
        ctx.fill();
        ctx.shadowColor = '#ff00ff';
        ctx.shadowBlur = 15;
        ctx.closePath();
    });

    // Draw bricks
    state.bricks.forEach(brick => {
        ctx.fillStyle = `rgb(${brick.color[0]},${brick.color[1]},${brick.color[2]})`;
        ctx.fillRect(brick.rect[0], brick.rect[1], brick.rect[2], brick.rect[3]);
        ctx.strokeStyle = '#00ffff';
        ctx.strokeRect(brick.rect[0], brick.rect[1], brick.rect[2], brick.rect[3]);
    });

    // Detect brick breaks
    if (lastState.bricks.length > state.bricks.length) {
        playSound(brickBreakSound);
    }

    // Draw powerups
    state.powerups.forEach(powerup => {
        ctx.fillStyle = 'yellow';
        ctx.fillRect(powerup.pos[0] - 10, powerup.pos[1] - 10, 20, 20);
        ctx.strokeStyle = '#ff00ff';
        ctx.strokeRect(powerup.pos[0] - 10, powerup.pos[1] - 10, 20, 20);
    });

    // Draw lasers
    state.lasers.forEach(laser => {
        ctx.fillStyle = '#00ffff';
        ctx.fillRect(laser.rect[0], laser.rect[1], laser.rect[2], laser.rect[3]);
        ctx.shadowColor = '#00ffff';
        ctx.shadowBlur = 5;
    });

    // Power-up message
    if (lastState.powerups.length > state.powerups.length && state.powerup_message) {
        playSound(powerupSound);
        const messageDiv = document.createElement('div');
        messageDiv.className = 'powerup-message';
        messageDiv.textContent = state.powerup_message;
        document.querySelector('.game-area').appendChild(messageDiv);
        setTimeout(() => messageDiv.remove(), 2000);
    }

    // Draw score
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#fff';
    ctx.font = '20px Orbitron';
    ctx.textAlign = 'left';
    ctx.fillText(`Score: ${state.score}`, 10, 20);

    lastState = { ...state, bricks: [...state.bricks], powerups: [...state.powerups], balls: [...state.balls], lasers: [...state.lasers] };
}

function updateGame() {
    if (!gameRunning) return;

    fetch('/game/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ paddle_pos: paddlePos, keys })
    })
    .then(response => response.json())
    .then(state => {
        drawGame(state);
        if (state.state === 'game_over') {
            gameRunning = false;
        } else {
            requestAnimationFrame(updateGame);
        }
    });
}

// Initial render
fetch('/game/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({})
})
.then(response => response.json())
.then(drawGame);