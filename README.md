# 🎮 Brick Breaker Game - Neon Edition 🎮

Welcome to the **Neon Brick Breaker Game**—a slick, high-energy arcade experience with glowing neon visuals, laser power-ups, and a killer soundtrack! Built with Python/Flask, powered by Neon PostgreSQL for high scores, and packed with retro vibes. Check out the action below with a live bouncing ball, and stay tuned for the full game demo video!

---

## 🚀 Live Bouncing Ball Animation

Watch this neon ball bounce to get a taste of the game’s vibe! (No interaction needed—just pure eye candy.)

<div align="center">
  <div id="ball-animation">
    <div class="ball"></div>
  </div>
</div>

<style>
#ball-animation {
  width: 200px;
  height: 200px;
  border: 2px solid #00ffcc;
  border-radius: 10px;
  overflow: hidden;
  background: linear-gradient(45deg, #1a001a, #000033);
  position: relative;
}

.ball {
  width: 20px;
  height: 20px;
  background: radial-gradient(circle, #ff00ff, #00ffcc);
  border-radius: 50%;
  position: absolute;
  box-shadow: 0 0 10px #00ffcc, 0 0 20px #ff00ff;
  animation: bounce 1.5s infinite;
}

@keyframes bounce {
  0% { top: 0; left: 0; }
  25% { top: 180px; left: 180px; }
  50% { top: 180px; left: 0; }
  75% { top: 0; left: 180px; }
  100% { top: 0; left: 0; }
}
</style>

<script>
document.addEventListener("DOMContentLoaded", () => {
  const ball = document.querySelector('.ball');
  let posX = 0;
  let posY = 0;
  let speedX = 2;
  let speedY = 2;

  function animate() {
    posX += speedX;
    posY += speedY;

    if (posX + 20 > 200 || posX < 0) speedX = -speedX;
    if (posY + 20 > 200 || posY < 0) speedY = -speedY;

    ball.style.left = posX + "px";
    ball.style.top = posY + "px";

    requestAnimationFrame(animate);
  }

  animate();
});
</script>

---

## 🌟 About the Game

- **Neon Theme**: Glowing visuals with a futuristic edge.
- **Laser Power-Up**: Blast through bricks with style!
- **Audio**: Epic sound effects for every hit and break.
- **High Scores**: Saved in Neon PostgreSQL for bragging rights.
- **Tech Stack**: Python/Flask, JavaScript, HTML/CSS, Neon DB.

This project was a labor of love to bring arcade nostalgia into the neon age. Originally hosted on Railway, but due to web rendering limits, I’m sharing a demo video instead—stay tuned!

---

## 🎥 Game Demo Video
[Add your video link here once recorded!]  
*(Upload your `brick-breaker-demo.mp4` to this repo and link it, or host on YouTube and paste the URL.)*

---

## 🚧 Current Status
- **Interactive Game**: Paused due to web performance issues (laggy ball).
- **Demo**: Video coming soon to showcase the full experience!
- **Future Plans**: Maybe a desktop version or mobile app—let me know what you think!

---

## 💡 How to Contribute
Love the neon vibes? Want to help?
1. Fork this repo!
2. Star it to show some love! 🌟
3. Suggest features (e.g., more power-ups, multiplayer) in Issues.
4. Submit a pull request with your code!

---

## 🙌 Shoutouts
Big thanks to the xAI community and my coding crew for the support. Special nod to Neon for the slick DB setup!

---

## 📜 License
MIT License—free to use, modify, and share. Check the [LICENSE](LICENSE) file for details.
