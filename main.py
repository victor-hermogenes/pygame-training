import pygame
import os

# Window Display
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Counter Battle!")
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Window Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game details
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Hit mechanics 
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# Function to create Display
def draw_window(red, yellow, red_bullets, yellow_bullets):
    """Function will get variables from above and draw the display"""
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
         pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
         pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

# Yellow ship movement control
def yellow_handle_movement(keys_pressed, yellow):
        """Function will define wich keys will control yellow ship"""
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
            yellow.x -= VEL
        elif keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # Right
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
            yellow.y -= VEL
        elif keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: # DOWN
            yellow.y += VEL

# Red ship movement control
def red_handle_movement(keys_pressed, red):
        """Function will define wich kews will control red ship"""
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width + 15: # LEFT
            red.x -= VEL
        elif keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 15: # Right
            red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
            red.y -= VEL
        elif keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: # DOWN
            red.y += VEL

# Function to create bullets mechanics
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
     """Function will define how bullets are fired and collision efects as well"""
     for bullet in yellow_bullets:
          bullet.x += BULLET_VEL
          if red.colliderect(bullet):
               pygame.event.post(pygame.event.Event(RED_HIT))
               yellow_bullets.remove(bullet)
          elif bullet.x > WIDTH:
               yellow_bullets.remove(bullet)

     for bullet in red_bullets:
          bullet.x -= BULLET_VEL
          if yellow.colliderect(bullet):
               pygame.event.post(pygame.event.Event(YELLOW_HIT))
               red_bullets.remove(bullet)
          elif bullet.x < 0:
               red_bullets.remove(bullet)

# Function to define main game mechanics
def main():
    """This function will define main games rules"""
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                      bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 + 5, 10, 5)
                      yellow_bullets.append(bullet)

                 if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                      bullet = pygame.Rect(red.x, red.y + red.height//2 + 5, 10, 5)
                      red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets)
        
    pygame.quit()

if __name__ == "__main__":
    main()