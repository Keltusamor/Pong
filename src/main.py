import pygame

WINDOW_WIDTH = 320 * 3
WINDOW_HEIGHT = 240 * 3
WINDOW_NAME = "Pong"
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8

BALL_RADIUS = 10
BALL_SPEED = 5

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_NAME)

clock = pygame.time.Clock()

left_paddle = pygame.Rect(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
left_paddle.midleft = (15, window.get_rect().centery)
right_paddle = pygame.Rect(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle.midright = (WINDOW_WIDTH - 15, window.get_rect().centery)
ball = pygame.Rect(0, 0, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball.center = window.get_rect().center
ball_velocity = pygame.math.Vector2(BALL_SPEED, BALL_SPEED)

bounce_sound = pygame.mixer.Sound("assets/audio/ping_pong_8bit_beeep.ogg")
bounce_sound.set_volume(0.5)
score_sound = pygame.mixer.Sound("assets/audio/ping_pong_8bit_peeeeeep.ogg")
score_sound.set_volume(0.5)

# SCORE_FONT = pygame.font.Font(None, 64)
SCORE_FONT = pygame.font.Font("assets/font/pixeloid-font/PixeloidSans-JR6qo.ttf", 48)
left_score = 0
right_score = 0

is_running = True
while is_running:
    delta_time = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < WINDOW_HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < WINDOW_HEIGHT:
        right_paddle.y += PADDLE_SPEED

    ball.move_ip(ball_velocity)

    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_velocity.x *= -1

        if ball.colliderect(left_paddle):
            paddle = left_paddle
            ball.left = left_paddle.right
        else:
            paddle = right_paddle
            ball.right = right_paddle.left

        paddle_third = PADDLE_HEIGHT // 3
        collision_pos = ball.centery - paddle.top

        if collision_pos <= paddle_third:
            # Top segment
            ball_velocity.y = -BALL_SPEED
        elif collision_pos >= 2 * paddle_third:
            # Bottom segment
            ball_velocity.y = BALL_SPEED
        else:
            # Middle segment
            ball_velocity.y = 0

        bounce_sound.play()

    if ball.top <= 0 or ball.bottom >= WINDOW_HEIGHT:
        ball_velocity.y *= -1
        bounce_sound.play()

    if ball.left <= 0 or ball.right >= WINDOW_WIDTH:
        if ball.left <= 0:
            right_score += 1
        else:
            left_score += 1

        ball.center = window.get_rect().center
        ball_velocity.x *= -1

        score_sound.play()

    window.fill(BLACK)

    pygame.draw.aaline(window, WHITE, window.get_rect().midtop, window.get_rect().midbottom)
    pygame.draw.rect(window, WHITE, left_paddle)
    pygame.draw.rect(window, WHITE, right_paddle)
    pygame.draw.ellipse(window, WHITE, ball)

    left_score_text = SCORE_FONT.render(str(left_score), True, WHITE)
    right_score_text = SCORE_FONT.render(str(right_score), True, WHITE)
    window.blit(left_score_text, left_score_text.get_rect(midtop=(WINDOW_WIDTH // 4, 15)))
    window.blit(right_score_text, left_score_text.get_rect(midtop=(WINDOW_WIDTH // 4 * 3, 15)))

    pygame.display.update()

pygame.quit()
