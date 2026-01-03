# Imports
from sys import exit
import pygame
import cv2
import random

pygame.init()
pygame.font.init()

class RectButton:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont(None, 40)

    def draw(self, screen, hovered=False, selected=False):
        color = (40, 40, 40)
        border = (0, 135, 245)

        if hovered:
            border = (235, 64, 52)

        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, border, self.rect, 3, border_radius=12)

        label = self.font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class CircleButton:
    def __init__(self, x, y, radius, text):
        self.x = x
        self.y = y
        self.radius = radius
        self.text = text
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, screen, hovered=False):
        pygame.draw.circle(screen, (30, 30, 30), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (0, 135, 245), (self.x, self.y), self.radius, 3)

        if hovered:
            pygame.draw.circle(screen, (235, 64, 52), (self.x, self.y), self.radius + 6, 4)

        label = self.font.render(self.text, True, (255, 255, 255))
        rect = label.get_rect(center=(self.x, self.y))
        screen.blit(label, rect)

    def is_clicked(self, mouse_pos):
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        return dx * dx + dy * dy <= self.radius * self.radius

# Setting up font for title
title_font = pygame.font.SysFont(None, 100)
player_font = pygame.font.SysFont(None, 50)

# Chosen bowling type
bowling_type = ""

# Buttons for selecting line and length
up_button = CircleButton(200, 500, 40, "^")
down_button = CircleButton(200, 620, 40, "v")
left_button = CircleButton(140, 560, 40, "<")
right_button = CircleButton(260, 560, 40, ">")
ok_button_line_length = CircleButton(1200, 560, 40, "OK")

line_length_buttons = [up_button, down_button, left_button, right_button, ok_button_line_length]

# Buttons for selecting type of pace ball
straight = CircleButton(250, 500, 40, "STRAIGHT")
in_swing = CircleButton(250, 620, 40, "IN SWING")
out_swing = CircleButton(100, 500, 40, "OUT SWING")
slower = CircleButton(100, 620, 40, "SLOWER")
ok_button_pace = CircleButton(1200, 560, 40, "OK")

pace_buttons = [straight, in_swing, out_swing, slower, ok_button_pace]

# Buttons for selecting type of leg spin ball
leg_spin = CircleButton(250, 500, 40, "LEG SPIN")
googly = CircleButton(250, 620, 40, "GOOGLY")
top_spin = CircleButton(100, 500, 40, "TOP SPIN")
slider = CircleButton(100, 620, 40, "SLIDER")
ok_button_leg_spin = CircleButton(1200, 560, 40, "OK")

leg_spin_buttons = [leg_spin, googly, top_spin, slider, ok_button_leg_spin]

# Buttons for selecting type of off spin ball
off_spin = CircleButton(250, 500, 40, "OFF SPIN")
doosra = CircleButton(250, 620, 40, "DOOSRA")
carrom = CircleButton(100, 500, 40, "CARROM")
arm_ball = CircleButton(100, 620, 40, "ARM BALL")
ok_button_off_spin = CircleButton(1200, 560, 40, "OK")

off_spin_buttons = [off_spin, doosra, carrom, arm_ball, ok_button_off_spin]

# Bowling Game states
choose_bowling_type = True
choose_length_line = False
choose_ball_type = False

pace_button = RectButton(335, 445, 220, 70, "PACE")
leg_spin_button = RectButton(615, 445, 220, 70, "LEG SPIN")
off_spin_button = RectButton(875, 445, 220, 70, "OFF SPIN")

bowling_type_buttons = [pace_button, leg_spin_button, off_spin_button]

# Different types of shots
front_foot_shots = ["forward defense", "sweep", "reverse sweep", "scoop", "cover drive", "straight drive", "flick shot"]
back_foot_shots = ["backward defense", "pull shot", "backfoot punch", "square cut", "upper cut"]
leave_shot = "leave"

# Front Foot Shot Buttons
forward_defence = CircleButton(350, 500, 40, "FORWARD DEFENSE")
sweep = CircleButton(350, 620, 40, "SWEEP")
scoop = CircleButton(150, 500, 40, "SCOOP")
reverse_sweep = CircleButton(150, 620, 40, "REVERSE SWEEP")
cover_drive = CircleButton(1100, 500, 40, "COVER DRIVE")
straight_drive = CircleButton(1100, 620, 40, "STRAIGHT DRIVE")
flick = CircleButton(1350, 500, 40, "FLICK")
leave = CircleButton(1350, 620, 40, "LEAVE")

frontfoot_shot_buttons = [forward_defence, sweep, reverse_sweep, scoop, cover_drive, straight_drive, flick, leave]

# Back Foot Shot Buttons
backward_defence = CircleButton(350, 380, 40, "BACKWARD DEFENSE")
pull_shot = CircleButton(150, 380, 40, "PULL")
upper_cut = CircleButton(1100, 380, 40, "UPPER CUT")
square_cut = CircleButton(1350, 380, 40, "SQUARE CUT")

backfoot_shot_buttons = [backward_defence, pull_shot, square_cut, upper_cut]

# List with all the shots
all_shots = [forward_defence, sweep, reverse_sweep, scoop, cover_drive, straight_drive, flick, leave, backward_defence, pull_shot, square_cut, upper_cut]

# Bowling Final choices of the user
final_length = ""
final_line = ""
selected_ball_variation = ""

# Final batting shot chosen by user
chosen_shot = ""

# Target circle coordinates
target_x = 0
target_y = 0

# Background images
pitch = pygame.image.load("pitch_background.png")
blurred_pitch = pygame.image.load("blurred_pitch.png")

# Different types of length and line
lengths = ["yorker", "full", "good", "short"]
lines = ["leg_stump", "stumps", "outside_off"]

length_index = 2
line_index = 1

# Bowling errors chances
no_ball_chance = 2
wide_chance = {
    "outside_off": {
        "short": 6,
        "good": 4,
        "full": 3,
        "yorker": 2,
    },
    "leg_stump": {
        "short": 7,
        "good": 5,
        "full": 4,
        "yorker": 3,
    },
    "stumps": {
        "short": 2,
        "good": 1,
        "full": 1,
        "yorker": 0,
    }
}

# Zones in which each shot is good
good_shot_zones = {
    "cover_drive": {
        "full": ["outside_off"],
        "good": ["outside_off"],
    },
    "straight_drive": {
        "full": ["stumps"],
        "good": ["stumps"],
    },
    "flick_shot": {
        "full": ["leg_stump", "stumps"],
        "good": ["leg_stump", "stumps"],
    },
    "square_cut": {
        "short": ["outside_off"],
    },
    "leave": {
        "short": ["outside_off"],
        "good": ["outside_off"],
        "full": ["outside_off"],
        "yorker": ["outside_off"],
    },
    "forward_defence": {
        "good": ["stumps"],
        "yorker": ["stumps"],
    },
    "backward_defence": {
        "short": ["stumps"],
        "good": ["stumps"],
    },
    "pull_shot": {
        "short": ["stumps", "leg_stump"],
    },
    "upper_cut": {
        "short": ["outside_off"],
    },
    "sweep": {
        "good": ["stumps", "leg_stump"],
        "full": ["stumps", "leg_stump"],
    },
    "reverse_sweep": {
        "good": ["outside_off"],
        "full": ["outside_off"],
    },
    "scoop": {
        "full": ["stumps", "outside_off", "leg_stump"],
        "yorker": ["stumps", "outside_off", "leg_stump"],
    },
}

def check_bowling_error_chances(line, length):
    global no_ball_chance, wide_chance

    # Checking for no ball
    if random.randint(1, 100) <= no_ball_chance:
        return "no_ball"

    # Checking for wide
    current_wide_chance = wide_chance[line][length]
    if random.randint(1, 100) <= current_wide_chance:
        return "wide"

    # Legal delivery has been bowled
    return None

# Draw circle to show where user is bowling
def draw_target_circle(screen, x, y):
    # Outer glow
    pygame.draw.circle(screen, (0, 135, 245), (x, y), 80, 10)

length_positions = {
    "short": 620,
    "good": 540,
    "full": 450,
    "yorker": 300
}

line_positions = {
    "outside_off": 550,
    "stumps": 715,
    "leg_stump": 850
}

# Different types of outcomes
outcomes = ["Dot Ball", "1 run", "2 runs", "3 runs", "4 runs", "6 runs", "Bowled out", "Caught out", "LBW", "Run out", "Wide", "No ball"]

def bowling(bowler, screen):
    global line_index, length_index, final_line, final_length, choose_length_line, choose_ball_type, selected_ball_variation, bowling_type, pace_buttons, leg_spin_buttons, off_spin_buttons, choose_bowling_type, bowling_type_buttons, title_font, player_font, target_y, target_x
    running = True
    clock = pygame.time.Clock()
    show_bowler = True

    bowling_type = ""
    choose_bowling_type = True
    choose_length_line = False
    choose_ball_type = False
    final_length = ""
    final_line = ""
    selected_ball_variation = ""
    length_index = 2
    line_index = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and choose_bowling_type:
                mouse_pos = pygame.mouse.get_pos()

                if pace_button.is_clicked(mouse_pos):
                    bowling_type = "pace"
                    choose_length_line = True
                    choose_bowling_type = False

                elif leg_spin_button.is_clicked(mouse_pos):
                    bowling_type = "leg_spin"
                    choose_length_line = True
                    choose_bowling_type = False

                elif off_spin_button.is_clicked(mouse_pos):
                    bowling_type = "off_spin"
                    choose_length_line = True
                    choose_bowling_type = False

            elif event.type == pygame.MOUSEBUTTONDOWN and choose_length_line:
                mouse_pos = pygame.mouse.get_pos()

                if up_button.is_clicked(mouse_pos):
                    length_index = max(0, length_index - 1)

                elif down_button.is_clicked(mouse_pos):
                    length_index = min(3, length_index + 1)

                elif left_button.is_clicked(mouse_pos):
                    line_index = min(2, line_index + 1)

                elif right_button.is_clicked(mouse_pos):
                    line_index = max(0, line_index - 1)

                elif ok_button_line_length.is_clicked(mouse_pos) and choose_length_line:
                    final_length = lengths[length_index]
                    final_line = lines[line_index]
                    choose_length_line = False
                    choose_ball_type = True

            elif event.type == pygame.MOUSEBUTTONDOWN and choose_ball_type:
                mouse_pos = pygame.mouse.get_pos()

                if bowling_type == "pace":
                    if straight.is_clicked(mouse_pos):
                        selected_ball_variation = "Straight"
                    elif in_swing.is_clicked(mouse_pos):
                        selected_ball_variation = "In Swing"
                    elif out_swing.is_clicked(mouse_pos):
                        selected_ball_variation = "Out Swing"
                    elif slower.is_clicked(mouse_pos):
                        selected_ball_variation = "Slower"
                    elif ok_button_pace.is_clicked(mouse_pos):
                        if selected_ball_variation != "":
                            choose_ball_type = False
                            show_bowler = False

                elif bowling_type == "leg_spin":
                    if leg_spin.is_clicked(mouse_pos):
                        selected_ball_variation = "Leg Spin"
                    elif googly.is_clicked(mouse_pos):
                        selected_ball_variation = "Googly"
                    elif slider.is_clicked(mouse_pos):
                        selected_ball_variation = "Slider"
                    elif top_spin.is_clicked(mouse_pos):
                        selected_ball_variation = "Top Spin"
                    elif ok_button_leg_spin.is_clicked(mouse_pos):
                        if selected_ball_variation == "":
                            pass
                        else:
                            choose_ball_type = False
                            show_bowler = False

                elif bowling_type == "off_spin":
                    if off_spin.is_clicked(mouse_pos):
                        selected_ball_variation = "Off Spin"
                    elif doosra.is_clicked(mouse_pos):
                        selected_ball_variation = "Doosra"
                    elif carrom.is_clicked(mouse_pos):
                        selected_ball_variation = "Carrom"
                    elif arm_ball.is_clicked(mouse_pos):
                        selected_ball_variation = "Arm Ball"
                    elif ok_button_off_spin.is_clicked(mouse_pos):
                        if selected_ball_variation != "":
                            choose_ball_type = False
                            show_bowler = False

        current_length = lengths[length_index]
        current_line = lines[line_index]

        target_x = line_positions[current_line]
        target_y = length_positions[current_length]

        if choose_bowling_type:
            title_text = "What type of bowling do you want to do?"
            title_surface = title_font.render(title_text, True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(725, 400))
            screen.blit(blurred_pitch, (0, 0))
            screen.blit(title_surface, title_rect)
        else:
            screen.blit(pitch, (0, 0))
            draw_target_circle(screen, target_x, target_y)

        mouse_pos = pygame.mouse.get_pos()

        if choose_bowling_type:
            for button in bowling_type_buttons:
                hovered = button.is_clicked(mouse_pos)
                button.draw(screen, hovered)

        if choose_length_line:
            for button in line_length_buttons:
                hovered = button.is_clicked(mouse_pos)
                button.draw(screen, hovered)

        if choose_ball_type:
            if bowling_type == "pace":
                for button in pace_buttons:
                    hovered = button.is_clicked(mouse_pos)
                    button.draw(screen, hovered)
            elif bowling_type == "leg_spin":
                for button in leg_spin_buttons:
                    hovered = button.is_clicked(mouse_pos)
                    button.draw(screen, hovered)
            elif bowling_type == "off_spin":
                for button in off_spin_buttons:
                    hovered = button.is_clicked(mouse_pos)
                    button.draw(screen, hovered)

        if choose_ball_type and bowling_type == "pace":
            if selected_ball_variation == "straight":
                pygame.draw.circle(screen, (235, 64, 52), (250, 500), 46, 4)
            elif selected_ball_variation == "in_swing":
                pygame.draw.circle(screen, (235, 64, 52), (250, 620), 46, 4)
            elif selected_ball_variation == "out_swing":
                pygame.draw.circle(screen, (235, 64, 52), (100, 500), 46, 4)
            elif selected_ball_variation == "slower":
                pygame.draw.circle(screen, (235, 64, 52), (100, 620), 46, 4)

        if choose_ball_type and bowling_type == "leg_spin":
            if selected_ball_variation == "leg_spin":
                pygame.draw.circle(screen, (235, 64, 52), (250, 500), 46, 4)
            elif selected_ball_variation == "googly":
                pygame.draw.circle(screen, (235, 64, 52), (250, 620), 46, 4)
            elif selected_ball_variation == "top_spin":
                pygame.draw.circle(screen, (235, 64, 52), (100, 500), 46, 4)
            elif selected_ball_variation == "slider":
                pygame.draw.circle(screen, (235, 64, 52), (100, 620), 46, 4)

        if choose_ball_type and bowling_type == "off_spin":
            if selected_ball_variation == "off_spin":
                pygame.draw.circle(screen, (235, 64, 52), (250, 500), 46, 4)
            elif selected_ball_variation == "doosra":
                pygame.draw.circle(screen, (235, 64, 52), (250, 620), 46, 4)
            elif selected_ball_variation == "carrom":
                pygame.draw.circle(screen, (235, 64, 52), (100, 500), 46, 4)
            elif selected_ball_variation == "arm_ball":
                pygame.draw.circle(screen, (235, 64, 52), (100, 620), 46, 4)

        if show_bowler:
            player_text = f"{bowler} bowling"
            player_surface = player_font.render(player_text, True, (255, 255, 255))
            screen.blit(player_surface, (0, 0))

            pygame.display.update()
            clock.tick(38)
        else:
            pygame.display.update()
            clock.tick(38)

            return

def batting(batter, screen):
    global all_shots, chosen_shot, target_x, target_y, selected_ball_variation, player_font
    running = True
    clock = pygame.time.Clock()
    show_batter = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for button in all_shots:
                    if button.is_clicked(mouse_pos):
                        chosen_shot = button.text.lower()
                        print(chosen_shot)
                        running = False

        screen.blit(pitch, (0, 0))

        draw_target_circle(screen, target_x, target_y)

        mouse_pos = pygame.mouse.get_pos()

        for button in all_shots:
            hovered = button.is_clicked(mouse_pos)
            button.draw(screen, hovered)

        if show_batter:
            player_font = pygame.font.SysFont(None, 50)

            player_text = f"{batter} batting"
            player_surface = player_font.render(player_text, True, (255, 255, 255))
            screen.blit(player_surface, (0, 0))

            player_font = pygame.font.SysFont(None, 35)

            ball_variation_text = f"Ball Variation: {selected_ball_variation}"
            ball_variation_surface = player_font.render(ball_variation_text, True, (255, 255, 255))
            screen.blit(ball_variation_surface, (0, 35))

        pygame.display.update()
        clock.tick(38)

def show_error(error):
    pass

def show_outcome(line, length, ball_variation, shot, screen):
    pass

def double_one(screen, toss_result):
    global final_line, final_length, selected_ball_variation, chosen_shot
    # Setting up the new screen
    pygame.display.set_caption("Double Player - One Over")

    if toss_result == "bowl":
        bowling("Player 1", screen)
        batting("Player 2", screen)

        error = check_bowling_error_chances(final_line, final_length)
        if error == "wide" or error == "no_ball":
            show_error(error)
        else:
            show_outcome(final_line, final_length, selected_ball_variation, chosen_shot, screen)

    elif toss_result == "bat":
        bowling("Player 2", screen)
        batting("Player 1", screen)

        error = check_bowling_error_chances(final_line, final_length)
        if error == "wide" or error == "no_ball":
            show_error(error)
        else:
            show_outcome(final_line, final_length, selected_ball_variation, chosen_shot, screen)

def double_two(screen, toss_result):
    pass
def double_five(screen, toss_result):
    pass