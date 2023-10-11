import pygame

# Constants and Variables

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH = 600
HEIGHT = 600

pygame.init()
game_font = pygame.font.SysFont('Ubuntu', 40)

delay = 30
paddle_speed = 12
paddle_width = 10
paddle_height = 100

p1_x_pos = 10
p1_y_pos = HEIGHT // 2 - paddle_height // 2

p2_x_pos = WIDTH - paddle_width - 10
p2_y_pos = HEIGHT // 2 - paddle_height // 2

p1_score = p2_score = 0

p1_up = False
p1_down = False
p2_up = False
p2_down = False

ball_x = WIDTH // 2
ball_y = HEIGHT // 2

ball_width = 8

ball_x_vel = -8
ball_y_vel = 0

# Screen

screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Drawing Objects

def draw_objects():
    pygame.draw.rect(screen, WHITE, (p1_x_pos, p1_y_pos, paddle_width, paddle_height))

    pygame.draw.rect(screen, WHITE, (p2_x_pos, p2_y_pos, paddle_width, paddle_height))

    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_width)
    score = game_font.render(f'{p1_score} : {p2_score}', False, WHITE)
    screen.blit(score, (WIDTH // 2, 30))


def player_movement():
    global p1_y_pos, p2_y_pos

    if p1_up:
        p1_y_pos -= max(paddle_speed, 0)
    if p1_down:
        p1_y_pos += min(paddle_speed, HEIGHT)
    if p2_up:
        p2_y_pos -= max(paddle_speed, 0)
    if p2_down:
        p2_y_pos += min(paddle_speed, HEIGHT)


def ball_movement():
    global ball_x, ball_y, ball_x_vel, ball_y_vel, p1_score, p2_score

    if (ball_x_vel + ball_x < p1_x_pos + paddle_width) and \
            (p1_y_pos < ball_y + ball_y_vel + ball_width < p1_y_pos + paddle_height):
        ball_x_vel = -ball_x_vel
        ball_y_vel = (p1_y_pos + paddle_height // 2 - ball_y) // 15
        ball_y_vel = -ball_y_vel

    elif ball_x + ball_x_vel < 0:
        p2_score += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_x_vel = 10
        ball_y_vel = 0

    if (ball_x_vel + ball_x > p2_x_pos - paddle_width) and \
            (p2_y_pos < ball_y + ball_y_vel + ball_width < p2_y_pos + paddle_height):
        ball_x_vel = -ball_x_vel
        ball_y_vel = (p2_y_pos + paddle_height // 2 - ball_y) // 15
        ball_y_vel = -ball_y_vel

    elif ball_x + ball_x_vel > HEIGHT:
        p1_score += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_x_vel = -10
        ball_y_vel = 0

    if (ball_y + ball_y_vel > HEIGHT) or \
            (ball_y + ball_y_vel < 0):
        ball_y_vel = -ball_y_vel

    ball_x += ball_x_vel
    ball_y += ball_y_vel


pygame.display.set_caption('Pong --S.U.P.E.R.B.O.T')
screen.fill(BLACK)
pygame.display.flip()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_w:
                p1_up = True

            if event.key == pygame.K_s:
                p1_down = True

            if event.key == pygame.K_UP:
                p2_up = True

            if event.key == pygame.K_DOWN:
                p2_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                p1_up = False

            if event.key == pygame.K_s:
                p1_down = False

            if event.key == pygame.K_UP:
                p2_up = False

            if event.key == pygame.K_DOWN:
                p2_down = False

    screen.fill(BLACK)
    player_movement()
    ball_movement()
    draw_objects()
    pygame.display.flip()
    pygame.time.wait(delay)