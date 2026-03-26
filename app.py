import pygame
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker - 100 Levels")
clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

# Paddle
paddle = pygame.Rect(WIDTH//2-60, HEIGHT-30, 120, 15)
paddle_speed = 7

# Ball
ball = pygame.Rect(WIDTH//2, HEIGHT//2, 15, 15)
ball_speed = [4, -4]
ball_multiplier = 1

# Powerups
powerups = []

# Game state
lives = 3
level = 1

# Create bricks

def create_bricks(level):
    bricks = []
    rows = min(5 + level//2, 10)
    cols = 10
    for r in range(rows):
        for c in range(cols):
            brick = pygame.Rect(c*75+5, r*30+5, 70, 25)
            bricks.append(brick)
    return bricks

bricks = create_bricks(level)

# Powerup types
POWER_TYPES = ["expand", "life", "multi", "fire"]

# Game loop
running = True
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Move ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Collision walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1
    if ball.top <= 0:
        ball_speed[1] *= -1

    # Lose life
    if ball.bottom >= HEIGHT:
        lives -= 1
        ball.center = (WIDTH//2, HEIGHT//2)
        if lives <= 0:
            print("Game Over")
            running = False

    # Paddle collision
    if ball.colliderect(paddle):
        ball_speed[1] *= -1

    # Brick collision
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] *= -1

            # Drop powerup
            if random.random() < 0.2:
                p_type = random.choice(POWER_TYPES)
                powerups.append([brick.x, brick.y, p_type])

    # Powerups movement
    for p in powerups[:]:
        p[1] += 3
        rect = pygame.Rect(p[0], p[1], 20, 20)
        pygame.draw.rect(screen, YELLOW, rect)

        if rect.colliderect(paddle):
            if p[2] == "expand":
                paddle.width += 40
            elif p[2] == "life":
                lives += 1
            elif p[2] == "multi":
                ball_speed[0] *= 1.2
                ball_speed[1] *= 1.2
            elif p[2] == "fire":
                ball_multiplier = 2
            powerups.remove(p)

    # Next level
    if not bricks:
        level += 1
        if level > 100:
            print("You Win!")
            running = False
        else:
            bricks = create_bricks(level)

    # Draw
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
