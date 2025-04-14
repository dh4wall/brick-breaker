import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 8
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
BRICK_ROWS, BRICK_COLS = 5, 10
POWERUP_SIZE = 20
LASER_WIDTH, LASER_HEIGHT = 4, 10
LASER_SPEED = -10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Game state
class Game:
    def __init__(self):
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.reset()

    def reset(self):
        self.paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.balls = []
        self.bricks = []
        self.powerups = []
        self.lasers = []  # Track active lasers
        self.score = 0
        self.lives = 3
        self.laser_active = False
        self.speed = 1.0
        self.paddle_width = PADDLE_WIDTH
        self.state = "waiting"
        self.powerup_message = None
        self.powerup_message_time = 0
        self.powerup_timers = {
            'laser': 0,
            'speed': 0,
            'bigger': 0
        }
        self.init_bricks()

    def init_bricks(self):
        colors = [RED, GREEN, BLUE, YELLOW]
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50, BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
                self.bricks.append({'rect': brick, 'color': random.choice(colors)})

    def spawn_ball(self):
        self.balls.append({'pos': [self.paddle.centerx, self.paddle.top - BALL_RADIUS], 'speed': [5, -5]})

    def shoot_laser(self):
        if self.laser_active:
            self.lasers.append({
                'rect': pygame.Rect(self.paddle.centerx - LASER_WIDTH // 2, self.paddle.top - LASER_HEIGHT, LASER_WIDTH, LASER_HEIGHT)
            })

    def update(self, paddle_pos=None, keys=None, action=None, shoot_laser=False):
        current_time = time.time()

        if action == "start" and self.state == "waiting":
            self.state = "playing"
            if not self.balls:
                self.spawn_ball()
        elif action == "reset" and self.state == "game_over":
            self.reset()
            return self.get_state()
        elif action == "quit" and self.state == "playing":
            self.state = "game_over"
            return self.get_state()

        if self.state != "playing":
            return self.get_state()

        # Update power-up timers
        for powerup in ['laser', 'speed', 'bigger']:
            if self.powerup_timers[powerup] > 0:
                if current_time - self.powerup_timers[powerup] >= 10:
                    self.deactivate_powerup(powerup)
                elif powerup == 'laser':
                    self.laser_active = True
                elif powerup == 'speed':
                    self.speed = 1.5
                elif powerup == 'bigger':
                    self.paddle_width = PADDLE_WIDTH * 1.5

        # Clear power-up message after 2 seconds
        if self.powerup_message and current_time - self.powerup_message_time >= 2:
            self.powerup_message = None

        # Paddle movement
        if paddle_pos:
            self.paddle.centerx = max(self.paddle_width // 2, min(WIDTH - self.paddle_width // 2, paddle_pos))
        elif keys:
            if keys.get('left') and self.paddle.left > 0:
                self.paddle.x -= 5 * self.speed
            if keys.get('right') and self.paddle.right < WIDTH:
                self.paddle.x += 5 * self.speed
        self.paddle.width = self.paddle_width

        # Update lasers
        for laser in self.lasers[:]:
            laser['rect'].y += LASER_SPEED
            if laser['rect'].bottom < 0:
                self.lasers.remove(laser)
                continue
            for brick in self.bricks[:]:
                if brick['rect'].colliderect(laser['rect']):
                    self.bricks.remove(brick)
                    self.lasers.remove(laser)
                    self.score += 10
                    break

        # Update balls
        for ball in self.balls[:]:
            ball['pos'][0] += ball['speed'][0]
            ball['pos'][1] += ball['speed'][1]

            # Wall collisions
            if ball['pos'][0] <= BALL_RADIUS or ball['pos'][0] >= WIDTH - BALL_RADIUS:
                ball['speed'][0] = -ball['speed'][0]
            if ball['pos'][1] <= BALL_RADIUS:
                ball['speed'][1] = -ball['speed'][1]
            if ball['pos'][1] >= HEIGHT:
                self.balls.remove(ball)
                if not self.balls:
                    self.lives -= 1
                    if self.lives > 0:
                        self.spawn_ball()
                    else:
                        self.state = "game_over"
                break

            # Paddle collision
            if self.paddle.collidepoint(ball['pos']):
                ball['speed'][1] = -ball['speed'][1]

            # Brick collisions
            for brick in self.bricks[:]:
                if brick['rect'].collidepoint(ball['pos']):
                    self.bricks.remove(brick)
                    ball['speed'][1] = -ball['speed'][1]
                    self.score += 10
                    if random.random() < 0.2:
                        self.powerups.append({
                            'type': random.choice(['laser', 'speed', 'bigger', 'multi']),
                            'pos': [brick['rect'].centerx, brick['rect'].centery]
                        })
                    break

        # Regenerate bricks if none remain
        if not self.bricks:
            self.init_bricks()
            self.score += 100  # Bonus for clearing stage

        # Update powerups
        for powerup in self.powerups[:]:
            powerup['pos'][1] += 3
            if self.paddle.collidepoint(powerup['pos']):
                self.apply_powerup(powerup['type'], current_time)
                self.powerups.remove(powerup)
            elif powerup['pos'][1] > HEIGHT:
                self.powerups.remove(powerup)

        # Handle laser shooting
        if shoot_laser:
            self.shoot_laser()

        return self.get_state()

    def apply_powerup(self, powerup_type, current_time):
        self.powerup_message = f"{powerup_type.capitalize()} Grabbed!"
        self.powerup_message_time = current_time
        if powerup_type == 'laser':
            self.powerup_timers['laser'] = current_time
        elif powerup_type == 'speed':
            self.powerup_timers['speed'] = current_time
        elif powerup_type == 'bigger':
            self.powerup_timers['bigger'] = current_time
        elif powerup_type == 'multi':
            self.spawn_ball()

    def deactivate_powerup(self, powerup_type):
        if powerup_type == 'laser':
            self.laser_active = False
        elif powerup_type == 'speed':
            self.speed = 1.0
        elif powerup_type == 'bigger':
            self.paddle_width = PADDLE_WIDTH
        self.powerup_timers[powerup_type] = 0

    def get_state(self):
        return {
            'paddle': list(self.paddle),
            'balls': self.balls,
            'bricks': [{'rect': list(b['rect']), 'color': b['color']} for b in self.bricks],
            'powerups': self.powerups,
            'lasers': [{'rect': list(l['rect'])} for l in self.lasers],
            'score': self.score,
            'lives': self.lives,
            'state': self.state,
            'powerup_message': self.powerup_message,
            'laser_active': self.laser_active
        }

game_instance = Game()

def start_game(data):
    global game_instance
    paddle_pos = data.get('paddle_pos')
    keys = data.get('keys')
    action = data.get('action')
    shoot_laser = data.get('shoot_laser', False)
    game_state = game_instance.update(paddle_pos, keys, action, shoot_laser)
    return game_state