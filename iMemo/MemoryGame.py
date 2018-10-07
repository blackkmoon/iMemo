import pygame
import time
import random
import os

from box import Box, Button

pygame.init()

display_height, display_width = 600, 800
# Setting colors:
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
lightgreen = (160, 240, 20)
black = (0, 0, 0)
# Setting level vars:
L1, L2, L3, L4, L5 = 3, 4, 5, 6, 7


game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Memory Game')
clock = pygame.time.Clock()
# Creating the home button:
home_img = pygame.image.load("home.png")
home_x = 7
home_y = 7

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


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text, center):
    largeText = pygame.font.Font('freesansbold.ttf', 50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = center
    game_display.blit(TextSurf, TextRect)

    pygame.display.update()


def start_screen():

    game_display.fill(white)

    # Creating the start button:
    start_button = Button(**start_button_config)  # (surface, color, startx, starty, width, height)

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
                    gameloop()

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
    # Creating the boxes/sprites:
    global all_sprites_list
    all_sprites_list = pygame.sprite.Group()
    objects = [all_sprites_list.add(Box()) for i in range(n)]
    halfLen = len(all_sprites_list) / 2

    #images_list = []
    #images_list = [random.choice(os.listdir("Images/")) for k in range(level - 1) if k not in locals()]

    # Creating a list of images for the sprites:
    images_list = []
    while len(images_list) != (level - 1):
        rand_img = random.choice(os.listdir("Images/"))
        if rand_img not in images_list:
            images_list.append(rand_img)

    # Giving each box its image/value and making them unknown for the start of the game:
    past_images = []
    for sprite in all_sprites_list:
        assigning = True
        while assigning:
            current_choice = random.choice(images_list)
            if past_images.count(current_choice) < 2:
                past_images.append(current_choice)
                sprite.img_list = [pygame.image.load("question_mark"), pygame.image.load("Images/" + current_choice)]
                sprite.image = sprite.img_list[0]
                sprite.rect = sprite.image.get_rect()
                # Removing the images which are already used:
                if past_images.count(current_choice) == 2:
                    images_list.remove(current_choice)
                assigning = False
    # ----------------

    # Making the boxes unknown:
    # for i in all_sprites_list:
    #     i.image = pygame.image.load("question_mark")  # i.image =
    #     i.rect = i.image.get_rect()

    # ----------------

    # Positioning the boxes:
    w = display_width / level
    h = display_height / 3
    count = 1
    for k in all_sprites_list:
        if count <= halfLen:
            # print(w)
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


def refresh():
    time.sleep(0.5)
    for i in all_sprites_list:
        i.image = pygame.image.load("question_mark")


def show():
    # current_sprite.image = pygame.image.load("1.png")  # current_sprite.image = img[]
    current_sprite.image = current_sprite.img_list[1]


def gameloop():
    global level
    level = L3
    start_boxes((level - 1) * 2)
    clicks = 0
    done = True
    while done:
        if clicks == 2:
            clicks = 0
            refresh()
        # Write event handlers here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for box in all_sprites_list:
                    # print(box.rect)
                    if box.rect.collidepoint(pos):
                        clicks += 1
                        global current_sprite
                        current_sprite = box
                        show()

                    if home_img.get_rect().collidepoint(pos):
                        start_screen()

        # write game logic here

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
