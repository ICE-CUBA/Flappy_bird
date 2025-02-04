"""
    CS5001_5003 Fall 2023 SV
    final project
    Linyan Fu
"""


import pygame
from sys import exit
import random
from pygame import Surface, SurfaceType


pygame.init()
pygame.mixer.init()

# Control time of the loop, can regulate the fps by click method
clock = pygame.time.Clock()
fps = 60
score = 0
level = 0
test = 0

# create game window
size = WIDTH, HEIGHT = 550, 720
screen: Surface | SurfaceType = pygame.display.set_mode(size)
pygame.display.set_caption('Flappy bird')

# Input Image
background = pygame.image.load('images/world.webp')
ground = pygame.image.load('images/ground.png')
bird_mid = pygame.image.load('images/bird_mid.png')
bird_up = pygame.image.load('images/bird_up.png')
bird_down = pygame.image.load('images/bird_down.png')
bird_images = [bird_mid, bird_up, bird_down]
pipe_bottom = pygame.image.load('images/pipe_bottom.png')
pipe_top = pygame.image.load('images/pipe_top.png')
game_over = pygame.image.load('images/game_over.png')
start = pygame.image.load('images/start.png')

# Input Sound
flap_sound = pygame.mixer.Sound('music/flap.wav')
level_up_sound = pygame.mixer.Sound('music/level_up.wav')
hit_sound = pygame.mixer.Sound('music/hit.wav')
point_sound = pygame.mixer.Sound('music/point.wav')

# Speed setting
scroll_speed_1 = 1
# bird initial position
bird_star_position = (100, 250)
font = pygame.font.SysFont('Lato', 29, 'bold')
font_2 = pygame.font.SysFont('Courier', 30, 'bold')


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the bird object
        param self: the bird
        return: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_star_position
        self.image_index = 0
        self.gravity = 0
        self.flap = False
        self.alive = True

    def update(self, user_input):
        """
        control the bird states
        param user_input: the user input key SPACE to control bird
        return: None
        """
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = bird_images[self.image_index // 10]

        # Gravity
        self.gravity += 0.5
        if self.gravity > 7:
            self.gravity = 7
        if self.rect.y < 500:
            self.rect.y += int(self.gravity)
        if self.gravity == 0:
            self.flap = False

        self.image = pygame.transform.rotate(self.image, self.gravity * -7)

        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.gravity = -7
            flap_sound.play()


class Ground(pygame.sprite.Sprite):
    """
    representing the ground object
    """
    def __init__(self, x, y):
        """
        initialize the ground
        param x: starting x position (int)
        param y: starting y position (int)
        return: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = ground
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        """
        Move the ground
        return: None
        """
        self.rect.x -= scroll_speed_1
        if level == 2:
            self.rect.x -= 0.6 * scroll_speed_1
        if level >= 3:
            self.rect.x -= 1.2 * scroll_speed_1
        if self.rect.x <= -551:
            self.kill()


class Pipes(pygame.sprite.Sprite):
    """
    represents the pipes object
    """
    def __init__(self, x, y, image, pipe_type):
        """
        initialize the pipes
        param x: starting x position (int)
        param y: starting y position (int)
        param image: the pipes images
        pipe_type: bottom or top pipe type
        return: None
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.enter = False
        self.exit = False
        self.passed = False
        self.pipe_type = pipe_type

    def update(self):
        """
        Move Pipes and update the score
        return: None
        """
        self.rect.x -= scroll_speed_1
        if level == 2:
            self.rect.x -= 0.6 * scroll_speed_1
        if level >= 3:
            self.rect.x -= 1.2 * scroll_speed_1
        if self.rect.x <= -WIDTH:
            self.kill()

        global score
        if self.pipe_type == 'bottom':
            if bird_star_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if bird_star_position[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1
                point_sound.play()


def game_quit():
    '''
    quit the game
    return: None
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def main():
    global score, level
    # Initial ground
    x_position_ground, y_position_ground = 0, 520
    the_ground = pygame.sprite.Group()
    the_ground.add(Ground(x_position_ground, y_position_ground))

    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    pipes = pygame.sprite.Group()
    timer = 0

    running = True
    while running:
        game_quit()
        # reset screen black
        screen.fill((0, 0, 0))

        # draw window
        screen.blit(background, (0, 0))

        # draw background setting - pipes, ground and bird
        the_ground.draw(screen)
        bird.draw(screen)
        pipes.draw(screen)
        user_input = pygame.key.get_pressed()

        # Spawn Ground
        if len(the_ground) <= 2:
            the_ground.add(Ground(WIDTH, y_position_ground))

        # update -pipe, ground and bird
        if bird.sprite.alive:
            the_ground.update()
            pipes.update()
        bird.update(user_input)

        # Show Score
        score_text = font.render('Score: ' + str(score), True, pygame.Color(255, 255, 40))
        screen.blit(score_text, (20, 20))

        # Show level
        if 10 > score >= 5:
            level = 1
        if score >= 10:
            level = (score // 10) + 1
        if score == 5:
            level_up_sound.play()
        if score / 10 in [1, 2, 3, 4, 5]:
            level_up_sound.play()

        level_text = font_2.render('LEVEL ' + str(level), True, pygame.Color(255, 255, 255))
        screen.blit(level_text, (200, 90))

        # Spawn Pipes
        if timer <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -488)
            y_bottom = y_top + random.randint(105, 145) + pipe_bottom.get_height()
            pipes.add(Pipes(x_bottom, y_bottom, pipe_bottom, 'top'))
            pipes.add(Pipes(x_top, y_top, pipe_top, 'bottom'))
            timer = random.randint(200, 250)
            if level == 1:
                timer = random.randint(160, 200)
            if level == 2:
                timer = random.randint(80, 120)
            if level == 3:
                timer = random.randint(60, 80)
            if level >= 4:
                timer = random.randint(40, 60)
        timer -= 1

        # Collision Detection
        global test
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], the_ground, False)
        if collision_pipes or collision_ground:
            bird.sprite.alive = False
            screen.blit(game_over, [180, 300])
            if test == 0:
                hit_sound.play()
                test = 1
            if user_input[pygame.K_r]:
                score = 0
                level = 0
                test = 0
                main()

        # set fps limit 60
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()


def menu():
    running = True

    while running:
        game_quit()

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(ground, Ground(0, 520))
        screen.blit(bird_images[0], (100, 250))
        screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2 - start.get_height() // 2))

        # check input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()

        pygame.display.update()


if __name__ == '__main__':
    menu()
