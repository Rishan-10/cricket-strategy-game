"""
This is a cricket strategy game created by Rishan Banerjee.
Started on Monday 20th of October 2025.
"""

# All libraries that I imported
import pygame
import pygame_menu
import cv2
from sys import exit
import json
import os
import random

# Setting up pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1450, 890))
pygame.display.set_caption("Cricket Strategy Game")
clock = pygame.time.Clock()
running = True

# Custom event for end of music
end_music = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(end_music)

# Importing my videos for my menu
main_background_video = cv2.VideoCapture("menu/main_background_video.mp4")
play_background_video = cv2.VideoCapture("menu/play_background_video.mp4")

# Function for putting video on the screen
def get_video_frame(video):
    ret, frame = video.read()
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video.read()
    frame = cv2.resize(frame, (1450, 890))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    return frame

# Variable to determine whether the user wants to play single or double player
# 1 = 1 player, 2 = 2 player
game_mode = 0

# Default value for volume
volume = 0.5

# Default value for mute
muted = 0

# List which holds the items for the muted button
mute_list = [("On", 0), ("Off", 1)]

# Check if there are already saved settings
if os.path.exists("settings.json"):
    with open("settings.json", "r") as file:
        saved = json.load(file)
        volume = saved.get("volume", 0.5)
        muted = saved.get("mute", 0)
        fullscreen = saved.get("fullscreen", False)

# Set the saved settings if there were saved settings
pygame.mixer.music.set_volume(volume)
if muted == 1:
    pygame.mixer.music.set_volume(0)
    mute_list = [("Off", 1), ("On", 0)]

# Music playlist
playlist = [
    "music/break-the-chains.mp3", "music/fire-and-ice.mp3", "music/flat_earth.mp3",
    "music/glory-to-me.mp3", "music/god_mode.mp3", "music/on-the-highway.mp3",
    "music/rock_hero.mp3", "music/ruthless.mp3", "music/shockwave.mp3",
    "music/smoke_sizzle.mp3", "music/the_one.mp3", "music/wrecked.mp3",
]

# To know which song to play next
music_index = 0

# Playing the music function
def play_music(index):
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(end_music)

# Game Menu Functions
def game():
    main_menu._open(play)
    play_background_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
def settings():
    main_menu._open(settings)

# Function for changing volume of music
def set_volume(value):
    global volume
    volume = value
    pygame.mixer.music.set_volume(volume)

# Function for muting music
def mute(argument, mute_value):
    global volume, muted
    muted = mute_value
    if muted == 1:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(volume)

# Function for fullscreen
def toggle_fullscreen(value, mode):
    global screen
    if mode == 1:
        screen = pygame.display.set_mode((1450, 890), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1450, 890))

# Function for saving settings
def save_settings():
    with open("settings.json", "w") as file:
        json.dump({
            "volume": volume,
            "mute": muted,
        }, file)

    # Shows users that the settings have been saved
    save_label.set_title("Settings Saved!")
    pygame.time.set_timer(pygame.USEREVENT + 2, 1500)

# Function for deleting settings
def delete_saved_settings():
    if os.path.exists("settings.json"):
        os.remove("settings.json")
        delete_label.set_title("Saved settings deleted!")
        pygame.time.set_timer(pygame.USEREVENT + 3, 1500)  # hide after 1.5s
    else:
        delete_label.set_title("No saved settings found.")
        pygame.time.set_timer(pygame.USEREVENT + 3, 1500)

# Function for resetting the toss menu
def reset_toss_menu():
    toss_menu.clear()
    toss_menu.add.label("Choose Heads or Tails:", font_size=60)
    toss_menu.add.button("Heads", heads)
    toss_menu.add.button("Tails", tails)

# Functions for single and double player mode menus
def single_player_mode():
    play._open(single_player)
    game_mode = 1
def double_player_mode():
    play._open(double_player)
    game_mode = 2

# Functions for 1 over, 2 overs, and 5 overs
def one_over():
    reset_toss_menu()
    single_player._open(toss_menu)
def two_overs():
    reset_toss_menu()
    single_player._open(toss_menu)
def five_overs():
    reset_toss_menu()
    single_player._open(toss_menu)

# Heads = 0, Tails = 1
# Bat = 0, Bowl = 1
# Function if the user chose heads
def heads():
    toss_menu.clear()
    main_menu._open(play)
    play._open(single_player)
    single_player._open(toss_menu)
    if random.randint(0,1) == 0:
        toss_menu.add.label("You won.")
        toss_menu.add.label("Do you want to bat or bowl?: ", font_size=80)
        toss_menu.add.button("Bat")
        toss_menu.add.button("Bowl")
    else:
        toss_menu.add.label("You lost.")
        if random.randint(0,1) == 0:
            toss_menu.add.label("You have to bat.")
        else:
            toss_menu.add.label("You have to bowl.")
# Function if the user chose heads
def tails():
    toss_menu.clear()
    main_menu._open(play)
    play._open(single_player)
    single_player._open(toss_menu)
    if random.randint(0, 1) == 0:
        toss_menu.add.label("You lost.")
        if random.randint(0,1) == 0:
            toss_menu.add.label("You have to bat.")
        else:
            toss_menu.add.label("You have to bowl.")
    else:
        toss_menu.add.label("You won.")
        toss_menu.add.label("Do you want to bat or bowl?: ", font_size=80)
        toss_menu.add.button("Bat")
        toss_menu.add.button("Bowl")

# Making a custom theme for my main menu
main_custom_theme = pygame_menu.themes.THEME_DARK.copy()
main_custom_theme.background_color = (0, 0, 0, 0)
main_custom_theme.widget_font_size = 70
main_custom_theme.widget_padding = 25
main_custom_theme.widget_margin = (0, 40)
main_custom_theme.title_font_size = 90
main_custom_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
main_custom_theme.title_font_color = (255, 255, 255)

# Main menu creation
main_menu = pygame_menu.Menu('Cricket Strategy Game', 1450, 890, theme=main_custom_theme)
main_menu.add.button('Play', game)
main_menu.add.button('Settings', settings)
main_menu.add.button('Exit', pygame_menu.events.EXIT)

# Making a custom theme for my settings menu
settings_custom_theme = pygame_menu.themes.THEME_GREEN.copy()
settings_custom_theme.widget_font_size = 30
settings_custom_theme.widget_padding = 10
settings_custom_theme.widget_margin = (0, 20)
settings_custom_theme.title_font_size = 50
settings_custom_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
settings_custom_theme.title_font_color = (255, 255, 255)

# Settings menu creation
settings = pygame_menu.Menu('Settings', 1450, 890, theme=settings_custom_theme)
settings.add.label("Audio Settings", max_char=-1, font_size=70)
settings.add.range_slider("Volume", volume, (0,1), increment=0.1, onchange=set_volume)
settings.add.selector("Music", mute_list, onchange=mute)
settings.add.label("Display Settings", max_char=-1, font_size=70)
settings.add.selector("Display Mode", [("Windowed", 0), ("Fullscreen", 1)], onchange=toggle_fullscreen)

# Save settings button
settings.add.button("Save Settings", save_settings)
save_label = settings.add.label("", font_size=25, font_color=(0, 255, 0))

# Delete saved settings button
settings.add.button("Delete Saved Settings", delete_saved_settings)
delete_label = settings.add.label("", font_size=25, font_color=(255, 0, 0))

# Making a custom theme for my play menu
play_custom_theme = pygame_menu.themes.THEME_DARK.copy()
play_custom_theme.background_color = (0, 0, 0, 0)
play_custom_theme.widget_font_size = 70
play_custom_theme.widget_padding = 25
play_custom_theme.widget_margin = (0, 40)
play_custom_theme.title_font_size = 90
play_custom_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
play_custom_theme.title_font_color = (255, 255, 255)

# Play menu creation
play = pygame_menu.Menu('Play', 1450, 890, theme=play_custom_theme)
play.add.button('Single Player Mode', single_player_mode)
play.add.button('Double Player Mode', double_player_mode)

# Making a custom theme for my single and double player menu
mode_custom_theme = pygame_menu.themes.THEME_DARK.copy()
mode_custom_theme.background_color = (0, 0, 0, 0)
mode_custom_theme.widget_font_size = 70
mode_custom_theme.widget_padding = 25
mode_custom_theme.widget_margin = (0, 40)
mode_custom_theme.title_font_size = 90
mode_custom_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
mode_custom_theme.title_font_color = (255, 255, 255)

# Single player menu creation
single_player = pygame_menu.Menu("Single Player Mode", 1450, 890, theme=mode_custom_theme)
single_player.add.button('1 over', one_over)
single_player.add.button('2 overs', two_overs)
single_player.add.button('5 overs', five_overs)

# Double player menu creation
double_player = pygame_menu.Menu("Double Player Mode", 1450, 890, theme=mode_custom_theme)
double_player.add.button('1 over', one_over)
double_player.add.button('2 overs', two_overs)
double_player.add.button('5 overs', five_overs)

# Making a custom theme for toss menu
toss_custom_theme = pygame_menu.themes.THEME_BLUE.copy()
toss_custom_theme.widget_font_size = 70
toss_custom_theme.widget_padding = 25
toss_custom_theme.widget_margin = (0, 40)
toss_custom_theme.title_font_size = 90
toss_custom_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
toss_custom_theme.title_font_color = (255, 255, 255)


# Toss menu creation
toss_menu = pygame_menu.Menu("Toss", 1450, 890, theme=toss_custom_theme, onclose=reset_toss_menu)
toss_menu.add.label("Choose Heads or Tails:", font_size=80)
toss_menu.add.button("Heads", heads)
toss_menu.add.button("Tails", tails)

# Back arrow creation
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

# Starting the music
play_music(music_index)

# Main Game Loop
while running:
    # Pygame events
    events = pygame.event.get()
    for event in events:
        # Ending the game
        if event.type == pygame.QUIT:
            save_settings()
            pygame.quit()
            exit()
            pygame.mixer.music.stop()
            running = False
        # Event to change the song, when the one song ends
        elif event.type == end_music:
            music_index += 1
            if music_index >= len(playlist):
                music_index = 0
            pygame.mixer.music.load(playlist[music_index])
            play_music(music_index)
        # Event to remove settings have been saved message
        elif event.type == pygame.USEREVENT + 2:
            save_label.set_title("")
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)
        # Event to remove settings have been deleted message
        elif event.type == pygame.USEREVENT + 3:
            delete_label.set_title("")
            pygame.time.set_timer(pygame.USEREVENT + 3, 0)

    # Checking which menu screen I am on
    if main_menu.get_current() == main_menu:
        # Playing main menu background menu screen video if on main menu screen
        frame = get_video_frame(main_background_video)
    else:
        # Playing play menu background menu screen video if on play menu screen
        frame = get_video_frame(play_background_video)

    # Adding the video to the screen
    screen.blit(frame, (0, 0))

    # Adding dark overlay so that I can read the text on the screen
    overlay = pygame.Surface((1450, 890))
    overlay.set_alpha(100)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Adding menus to the screen
    if main_menu.is_enabled():
        main_menu.update(events)
        main_menu.draw(screen)
        if main_menu.get_current().get_selected_widget():
            arrow.draw(screen, main_menu.get_current().get_selected_widget())

    # Updating screen
    pygame.display.update()
    # Limiting screen to 38 fps
    clock.tick(38)
