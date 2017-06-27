import pygame


class Box(pygame.sprite.Sprite):
    def __init__(self):  # display_width, display_height, w, h
        super().__init__()
       # self.image = pygame.image.load("sa")
       # self.rect = self.image.get_rect()
       # self.rect.centerx = (display_width) / w
       # self.rect.centery = (display_height) / h


class Button(object):
	def __init__(self, surface, color, x, y, width, height):
		self.surface = surface
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.name = pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
		
	def highlight(self, color, y):
		self.surface.fill((255,255,255))
		self.name = pygame.draw.rect(self.surface, color, (self.x, y, self.width, self.height))
