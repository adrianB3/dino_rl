import pygame

scr_size = (width, height) = (600, 150)
fps = 60
gravity = 0.7
black = (0, 0, 0)
white = (255, 255, 255)
background_col = (235, 235, 235)
pteras_on = False
game_speed = 4

jump_sound = pygame.mixer.Sound('sprites/jump.wav')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')
