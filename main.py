import pygame, sys
import os, random

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos, 900))
    screen.blit(floor_surface,(floor_x_pos + 576, 900))


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
        
        if bird_rect.top <= -100 or bird_rect.bottom >= 900:
            death_sound.play()
            return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3,1)
    return new_bird


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    new_pipe = pipe_surface.get_rect(midtop = (700 , random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return new_pipe, top_pipe


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1028:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
        
        hi_score_surface = game_font.render('High Score: ' + str(int(hi_score)),True,(255,255,255))
        hi_score_rect = hi_score_surface.get_rect(center = (288, 200))
        screen.blit(hi_score_surface, hi_score_rect)


def update_score(score, hi_score):
    if score > hi_score:
        hi_score = score
    return hi_score


#Path Location
current = os.path.dirname(__file__)
image_dir = os.path.join(current, 'assets')
sound_dir = os.path.join(current, 'sound')

pygame.mixer.pre_init(frequency = 44100, size = 16, channels=1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

# Game Variables
gravity = 0.30  
bird_movement = 0
game_active = True
score = 0
hi_score = 0

# Import background Images and scale
bg_surface = pygame.image.load(os.path.join(image_dir, 'background-day.png')).convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# Import floor surface image and scale
floor_surface = pygame.image.load(os.path.join(image_dir, 'base.png')).convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# Import bird images and scale
# bird_surface = pygame.image.load(os.path.join(image_dir, 'bluebird-midflap.png')).convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100, 512))
bird_downflap = pygame.transform.scale2x(pygame.image.load(os.path.join(image_dir, 'bluebird-downflap.png')).convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(os.path.join(image_dir, 'bluebird-midflap.png')).convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(os.path.join(image_dir, 'bluebird-upflap.png')).convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Import pipe image and scale
pipe_surface = pygame.image.load(os.path.join(image_dir, 'pipe-green.png')).convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load(os.path.join(image_dir,'message.png'))).convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'sfx_wing.wav'))
hit_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'sfx_hit.wav'))
score_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'sfx_point.wav'))
death_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'sfx_die.wav'))
score_sound_count = 180

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface,(0,0))
    
    if game_active == True:    
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)
        
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.006
        score_sound_count -= 1
        if score_sound_count <= 0:
            score_sound.play()
            score_sound_count = 180
        score_display('main_game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        hi_score = update_score(score, hi_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)