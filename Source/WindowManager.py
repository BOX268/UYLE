import pygame


display = None


class MainWindow() :

    def __init__(self):
        
        pygame.display.init()

        global display
        display = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        