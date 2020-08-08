import pygame, sys, random

# Controls ball movement
def ball_animation():
    global ball_speed_x,ball_speed_y,player_score,opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
    if ball.left <= 0 :
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        ball_restart()
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score +=1
        ball_restart()
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 5:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 5 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 5 and ball_speed_y <0:
            ball_speed_y *= -1
    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 5:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 5 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 5 and ball_speed_y < 0:
            ball_speed_y *= -1

# Controls player movement
def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

# Controls opponent movement
def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global  ball_speed_x,ball_speed_y
    ball.center = (screen_width/2,screen_height/2)
    ball_speed_y *= random.choice([-1,1])
    ball_speed_x *= random.choice([1,-1])


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Display
screen_width = 940
screen_height = 480
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

ball = pygame.Rect(screen_width/2 - 8, screen_height/2 - 8, 16, 16)
player = pygame.Rect(screen_width-20, screen_height/2 - 45,8,90)
opponent  = pygame.Rect(20,screen_height/2 - 45,8,90)

# Game Variables
ball_speed_x = 5*random.choice([1,-1])
ball_speed_y = 5*random.choice([1,-1])
player_speed = 0
opponent_speed = 7

# Score
player_score = 0
opponent_score = 0
text_font = pygame.font.Font('freesansbold.ttf',20)

# Sound load
pong_sound = pygame.mixer.Sound('pong.ogg')
score_sound = pygame.mixer.Sound('score.ogg')

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()

    player_animation()

    opponent_ai()

    screen.fill(pygame.Color('grey12'))
    pygame.draw.ellipse(screen, (200,200,200), ball)
    pygame.draw.rect(screen, (200,200,200), player)
    pygame.draw.rect(screen, (200, 200, 200), opponent)
    # pygame.ellipse uses its frame to color only the ellipse inside the Rect provided
    pygame.draw.aaline(screen,(200,200,200),(screen_width/2, 0),(screen_width/2, screen_height))

    player_text = text_font.render(f"{player_score}",False,(255,255,255))
    screen.blit(player_text,(screen_width/2 + 9, screen_height/2))
    opponent_text = text_font.render(f"{opponent_score}",False,(255,255,255))
    screen.blit(opponent_text,(screen_width/2 - 24,screen_height/2))

    pygame.display.flip()
    clock.tick(70)