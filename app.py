import pygame
import random
import game

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake")

currentGame = game.Game(screen)

pygame.quit()
