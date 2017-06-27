import pygame
import time
import random
import os

from box import Box, Button

pygame.init()

display_height, display_width = 600, 800
blue = (0, 0, 255)
white = (230, 240, 240)
black = (0, 0, 0)
green = (0,255,0)
lightgreen = (160,240,20)
L1, L2, L3, L4, L5 = 3, 4, 5, 6, 7


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Memory Game')
clock = pygame.time.Clock()
all_sprites_list = pygame.sprite.Group()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text, center):
    largeText = pygame.font.Font('freesansbold.ttf', 50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = center
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


def start_screen():
    pressed = True
    gameDisplay.fill(white)

    # Creating the start button:
    start_button = Button(gameDisplay, green, 365, 300, 70, 30)

    

    while pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                pressed = False

            # Checking if the user starts the game:    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if start_button.name.collidepoint(pos):
                    pressed = False
                    gameloop()

            
            pos = pygame.mouse.get_pos()
            start_button.highlight(green, start_button.y,)

            if start_button.name.collidepoint(pos):
                start_button.highlight(lightgreen, (start_button.y + 10))

            message_display("Welcome to iMemo!", ((display_width / 2), (display_height / 3.5)))


        pygame.display.update()
        clock.tick(30)


def start_boxes(n):
    # Creating the boxes:
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
        # write event handlers here
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

        # write game logic here

        # clear the screen before drawing
        gameDisplay.fill(white)
        # write draw code here
        # pygame.draw.line(gameDisplay, blue, (display_width / 2, 0), (display_width / 2, display_height), 5)
        # pygame.draw.line(gameDisplay, blue, (0, display_height / 2), (display_width, display_height / 2), 5)

        all_sprites_list.draw(gameDisplay)  # Draw all boxes to the screen.

        # display what’s drawn. this might change.
        pygame.display.update()
        # run at 30 fps
        clock.tick(30)

    # close the window and quit
    pygame.quit()

# gameloop()
start_screen()
