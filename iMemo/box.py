import pygame


class Box(pygame.sprite.Sprite):
    def __init__(self):  # display_width, display_height, w, h
        super().__init__()
       # self.image = pygame.image.load("sa")
       # self.rect = self.image.get_rect()
       # self.rect.centerx = (display_width) / w
       # self.rect.centery = (display_height) / h


class Button(object):
    def __init__(self, surface, color, x, y, width, height, text, textcolor):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))

        # Setting the text:
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.textSurface = self.font.render(text, True, textcolor)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (400, 310)
        self.surface.blit(self.textSurface, self.textRect)
        self.draw_text = "yes"

    def highlight(self, color, y):
        self.surface.fill((255, 255, 255))
        self.rect = pygame.draw.rect(self.surface, color, (self.x, y, self.width, self.height))
        if self.draw_text == "yes":
            self.surface.blit(self.textSurface, self.textRect)

    def highlight_text(self):
        self.textRect.center = (400, 317)
        self.surface.blit(self.textSurface, self.textRect)
        self.textRect.center = (400, 310)
