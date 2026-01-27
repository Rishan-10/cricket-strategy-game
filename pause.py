import pygame_menu
import pygame
from sys import exit

blurred_pitch = pygame.image.load("blurred_pitch.png")

pause_custom_theme = pygame_menu.themes.THEME_DARK.copy()
pause_custom_theme.background_color = (0, 0, 0, 0)
pause_custom_theme.widget_font_size = 64
pause_custom_theme.widget_padding = 25
pause_custom_theme.widget_margin = (0, 40)
pause_custom_theme.title_font_size = 90
pause_custom_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
pause_custom_theme.title_font_color = (255, 255, 255)

class PauseMenu:
    def __init__(self, screen, on_resume, main_menu):
        self.screen = screen
        self.enabled = False

        self.menu = pygame_menu.Menu(title='Paused',width=1450,height=890,theme=pause_custom_theme)

        self.menu.add.button('Resume', on_resume)
        # self.menu.add.button("Main Menu", main_menu)
        self.menu.add.button('Exit', exit)

    def open(self):
        self.enabled = True

    def close(self):
        self.enabled = False

    def update_and_draw(self, events):
        if self.enabled:
            self.menu.update(events)
            self.menu.draw(self.screen)