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


#REVIEW: I strongly suggest using the same naming style everywhere, either snake_case or camelCase. You probably want to use snake_case, since it's python's standard
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Memory Game')
clock = pygame.time.Clock()
# Creating the home button:
home_img = pygame.image.load("home.png")
home_x = 7
home_y = 7


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text, center):
    largeText = pygame.font.Font('freesansbold.ttf', 50)
    #REVIEW: Usually python reserves Capitalised names for classes
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = center
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


def start_screen():

    gameDisplay.fill(white)

    # Creating the start button:
    start_button = Button(gameDisplay, green, 335, 290, 130, 35, "Start", black)  # (surface, color, startx, starty, width, height)
    '''
    #REVIEW:

    # When functions have too many arguments, it might work better to use named arguments:
    start_button = Button(gameDisplay, color=green, startx=335, starty=290, width=130, height=35, ...)

    # Or even better, keyword arguments:
    # You can declare this variable somewhere easy to access
    start_button_config = {
        'surface': gameDisplay,
        'color': green,
        'startx': 335,
        ...
    }
    start_button = Button(**start_button_config)

    # Check this -> https://docs.python.org/2/tutorial/controlflow.html#keyword-arguments
    '''
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
            gameDisplay.blit(home_img, (home_x, home_y))
            message_display("Welcome to iMemo!", ((display_width / 2), (display_height / 3.5)))

        pygame.display.update()
        clock.tick(30)


def start_boxes(n):
    '''
    #REVIEW:
    In this function you are doing four things at the same time:
    1. Creating a list of sprite objects
    2. Loading images from disk
    3. Choosing a random image for each sprite
    4. Initialising each sprite

    Ideally, you want the initialisation of sprites and the loading of images to be independent from each other, even different functions.
    I suggest trying to organise this function into the following steps:
    1. Load the images you are going to use from disk
    2. Have a single loop that does the following for each sprite:
        1. Create the sprite object.
        2. Assign to the sprite the images it needs.
        3. Position the sprite.
    '''
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
        '''
        #REVIEW:
        # This is accessing the filesystem everytime you choose an image, it's not a big deal here, but it would be better to just read the filenames once:
        all_images = os.listdir('Images/')
        while len(images_list) != (level - 1):
            rand_img = random.choice(all_images)
            ...
        
        # A shorter option would be using random.shuffle
        all_images = os.listdir('Images/')
        random.shuffle(all_images)
        images_list = all_images[:level]
        '''
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
        '''
        #REVIEW:
        # I think that pygame.image.load loads the image from the disk every time. You might want to cache all your images when starting the level:
        image_cache = {
            'question_mark': pygame.image.load('question_mark'),
            'sprite_1': pygame.image.load('sprite_1),
            ...
        }

        # And then here you can just query the cache:
        i.image = image_cache['question_mark']

        # Also, the question mark is already in sprite.img_list, so you can do this as well:
        i.image = i.img_list[0]
        '''


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
                        '''
                        #REVIEW:
                        Don't declare global variables in your functions, it's error prone and makes your code harder to reason about.
                        Instead, you want pass the current_sprite to your show() function, that way it doesn't need to be global.
                        Same about the level var above, instead of making it global, pass it as an argument to the functions that need it.
                        '''
                        current_sprite = box
                        show()

                    if home_img.get_rect().collidepoint(pos):
                        start_screen()

        # write game logic here

        # clear the screen before drawing
        gameDisplay.fill(white)
        # write draw code here
        # pygame.draw.line(gameDisplay, blue, (display_width / 2, 0), (display_width / 2, display_height), 5)
        # pygame.draw.line(gameDisplay, blue, (0, display_height / 2), (display_width, display_height / 2), 5)

        # Draw all boxes to the screen.
        all_sprites_list.draw(gameDisplay)

        # Highlighting the home button:
        pos = pygame.mouse.get_pos()
        home_y = 7
        if home_img.get_rect().collidepoint(pos):
            home_y += 3
        gameDisplay.blit(home_img, (home_x, home_y))

        # display what’s drawn. this might change.
        pygame.display.update()
        # run at 30 fps
        clock.tick(30)

    # close the window and quit
    pygame.quit()

start_screen()
