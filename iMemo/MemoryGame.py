import pygame
import time
import random
import os

from itertools import cycle
from box import Box, Button

pygame.init()

# Setting colors:
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
lightgreen = (160, 240, 20)

# Setting level vars:
L1, L2, L3, L4, L5 = 3, 4, 5, 6, 7

# Level chosen:
level = L5

display_height, display_width = 600, 800
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Memory Game')
clock = pygame.time.Clock()

# Creating the home button:
home_img = pygame.image.load("home.png")
home_x = 7
home_y = 7

unknown_sprite = pygame.image.load("question_mark")

start_button_config = {
    'surface': game_display,
    'color': green,
    'x': 335,
    'y': 290,
    'width': 130,
    'height': 35,
    'text': "Start",
    'textcolor': black
}


def message_display(text, center):
    text_surface = pygame.font.Font('freesansbold.ttf', 50).render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = center
    game_display.blit(text_surface, text_rect)

    pygame.display.update()


def start_screen():

    game_display.fill(white)

    # Creating the start button:
    start_button = Button(**start_button_config)

    # Waiting for user input:
    pressed = True
    while pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                pressed = False

            # Checking if the user starts the game:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if start_button.rect.collidepoint(pos):
                    pressed = False
                    gameloop(level)

            # Highlighting the button:
            pos = pygame.mouse.get_pos()
            start_button.highlight(green, start_button.y)
            if start_button.rect.collidepoint(pos):
                start_button.draw_text = "no"
                start_button.highlight(lightgreen, (start_button.y + 7))
                start_button.highlight_text()
            start_button.draw_text = "yes"

            # Displaying the home button:
            game_display.blit(home_img, (home_x, home_y))
            message_display("Welcome to iMemo!", ((display_width / 2), (display_height / 3.5)))

        pygame.display.update()
        clock.tick(30)


def start_boxes(n):

    # Creating the sprites:
    all_sprites_list = pygame.sprite.Group()
    objects = [all_sprites_list.add(Box()) for i in range(n)]

    # Loading all images from disk, choosing and randomizing the needed for the level:
    all_images = os.listdir('Images/')
    random.shuffle(all_images)
    all_images = all_images[:level - 1] * 2
    random.shuffle(all_images)
    images_list = cycle(all_images)

    # Configuring the stripes:
    for sprite in all_sprites_list:

        sprite.id = next(images_list)  # Contains the name of the image as a string: '6.jpg'
        sprite.cache = {
            'img': pygame.image.load('Images/' + sprite.id),
            'unknown': unknown_sprite

        }
        sprite.image = sprite.cache['unknown']
        sprite.rect = sprite.image.get_rect()
        sprite.guessed = False

    # Positioning the boxes:
    halfLen = len(all_sprites_list) / 2
    w = display_width / level
    h = display_height / 3
    count = 1
    for k in all_sprites_list:
        if count <= halfLen:
            k.rect.centerx = w
            k.rect.centery = h
            w += display_width / level
        if count == halfLen:
            w = display_width / level
            h = (display_height / 3) * 2
        if count > halfLen:
            k.rect.centerx = w
            k.rect.centery = h
            w += display_width / level
        count += 1
    return all_sprites_list


def refresh(all_sprites_list):

    # Before refreshing, pausing to show the 2 selected boxes:
    # (Using time.time() since time.sleep() causes a bug)
    # time.sleep(0.5)
    start = time.time()
    while time.time() - start < 0.35:
        pass

    for sprite in all_sprites_list:
        if sprite.guessed == False:
            sprite.image = sprite.cache['unknown']


def gameloop(level):
    all_sprites_list = start_boxes((level - 1) * 2)
    clicks = 0
    first_check = 0
    done = True
    while done:
        if clicks == 2:
            clicks = 0
            first_check = 0
            refresh(all_sprites_list)
        # Write event handlers here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for sprite in all_sprites_list:

                    if sprite.rect.collidepoint(pos):

                        # Revealing the each selected box:
                        sprite.image = sprite.cache['img']

                        # Game logic (is there a match or no):
                        if first_check == 0:
                            state = sprite.id
                            state_rect = sprite.rect
                            first_check += 1
                            clicks += 1
                        else:
                            if sprite.id != state:
                                clicks += 1
                            else:
                                if state_rect != sprite.rect:
                                    for sprite in all_sprites_list:
                                        if sprite.id == state:
                                            sprite.guessed = True
                                clicks += 1
                            state = sprite.id
                            state_rect = sprite.rect

                    if home_img.get_rect().collidepoint(pos):
                        start_screen()

        # clear the screen before drawing
        game_display.fill(white)
        # write draw code here
        # pygame.draw.line(game_display, blue, (display_width / 2, 0), (display_width / 2, display_height), 5)
        # pygame.draw.line(game_display, blue, (0, display_height / 2), (display_width, display_height / 2), 5)

        # Draw all boxes to the screen.
        all_sprites_list.draw(game_display)

        # Highlighting the home button:
        pos = pygame.mouse.get_pos()
        home_y = 7
        if home_img.get_rect().collidepoint(pos):
            home_y += 3
        game_display.blit(home_img, (home_x, home_y))

        # display what’s drawn. this might change.
        pygame.display.update()
        # run at 30 fps
        clock.tick(30)

    # close the window and quit
    pygame.quit()


start_screen()
