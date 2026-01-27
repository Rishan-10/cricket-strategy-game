# Imports
from sys import exit
import pygame
import random
import cv2
from pause import PauseMenu

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
    def __init__(self, x, y, radius, text, shot_id=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.text = text
        self.shot_id = shot_id
        self.font = pygame.font.SysFont(None, 28)

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

# Importing the videos for my outcomes
dot_ball = cv2.VideoCapture("outcome_videos/DotBall.mov")
one_run = cv2.VideoCapture("outcome_videos/1run.mov")
two_runs = cv2.VideoCapture("outcome_videos/2runs.mov")
three_runs = cv2.VideoCapture("outcome_videos/3runs.mov")
four_runs = cv2.VideoCapture("outcome_videos/4runs.mov")
six_runs = cv2.VideoCapture("outcome_videos/6runs.mov")

wide = cv2.VideoCapture("outcome_videos/Wide.mov")

bowled = cv2.VideoCapture("outcome_videos/BowledOut.mov")
caught = cv2.VideoCapture("outcome_videos/CaughtOut.mov")
lbw = cv2.VideoCapture("outcome_videos/LBW.mov")
run_out = cv2.VideoCapture("outcome_videos/RunOut.mov")

# To track all the balls
ball_log = []

# Pause button image
pause_button = pygame.image.load("menu/pause.png")
pause_button_rect = pause_button.get_rect(topleft=(1390, 10))

paused = False

# Chosen bowling type
bowling_type = ""

# Scoreboard Variables
total_runs_1 = 0
wickets_1 = 0
balls_bowled = 0

total_runs_2 = 0
wickets_2 = 0

run_outcome_values = {
    "dot": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "6": 6,
}

wicket_outcomes = [
    "bowled",
    "caught",
    "lbw",
    "run_out",
]

# Continue button
continue_button = RectButton(615, 445, 220, 70, "Continue")

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

pace_button = RectButton(335, 445, 220, 70, "PACE")
leg_spin_button = RectButton(615, 445, 220, 70, "LEG SPIN")
off_spin_button = RectButton(875, 445, 220, 70, "OFF SPIN")

bowling_type_buttons = [pace_button, leg_spin_button, off_spin_button]

# Front Foot Shot Buttons
forward_defence = CircleButton(350, 500, 40, "FORWARD DEFENSE", "forward_defence")
sweep = CircleButton(350, 620, 40, "SWEEP", "sweep")
scoop = CircleButton(150, 500, 40, "SCOOP", "scoop")
reverse_sweep = CircleButton(150, 620, 40, "REVERSE SWEEP", "reverse_sweep")
cover_drive = CircleButton(1100, 500, 40, "COVER DRIVE", "cover_drive")
straight_drive = CircleButton(1100, 620, 40, "STRAIGHT DRIVE", "straight_drive")
flick = CircleButton(1350, 500, 40, "FLICK", "flick_shot")
leave = CircleButton(1350, 620, 40, "LEAVE", "leave")

# Back Foot Shot Buttons
backward_defence = CircleButton(350, 380, 40, "BACKWARD DEFENSE", "backward_defence")
pull_shot = CircleButton(150, 380, 40, "PULL", "pull_shot")
upper_cut = CircleButton(1100, 380, 40, "UPPER CUT", "upper_cut")
square_cut = CircleButton(1350, 380, 40, "SQUARE CUT", "square_cut")

# List with all the shots
all_shots = [forward_defence, sweep, reverse_sweep, scoop, cover_drive, straight_drive, flick, leave, backward_defence, pull_shot, square_cut, upper_cut]

# Button to return to main menu
main_menu_button = RectButton(575, 445, 300, 100, "Main Menu")

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

# Wide chances
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

# Probabilities if good shots are chosen
fast_bowler_good = {
    "cover_drive": {"dot":10,"1":20,"2":10,"3":2,"4":40,"6":2,"bowled":3,"caught":10,"lbw":1,"run_out":2},
    "straight_drive": {"dot":8,"1":18,"2":8,"3":1,"4":50,"6":3,"bowled":2,"caught":8,"lbw":1,"run_out":1},
    "flick_shot": {"dot":12,"1":25,"2":15,"3":5,"4":25,"6":3,"bowled":2,"caught":7,"lbw":3,"run_out":3},
    "square_cut": {"dot":20,"1":25,"2":8,"3":1,"4":30,"6":2,"bowled":2,"caught":10,"lbw":1,"run_out":1},
    "leave": {"dot":70,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":10,"caught":0,"lbw":20,"run_out":0},
    "forward_defence": {"dot":65,"1":5,"2":1,"3":0,"4":10,"6":0,"bowled":8,"caught":3,"lbw":6,"run_out":2},
    "backward_defence": {"dot":60,"1":8,"2":2,"3":0,"4":10,"6":0,"bowled":7,"caught":3,"lbw":7,"run_out":3},
    "sweep": {"dot":12,"1":20,"2":10,"3":2,"4":35,"6":5,"bowled":2,"caught":10,"lbw":2,"run_out":2},
    "reverse_sweep": {"dot":18,"1":15,"2":10,"3":2,"4":30,"6":5,"bowled":1,"caught":15,"lbw":2,"run_out":2},
    "scoop": {"dot":10,"1":10,"2":8,"3":1,"4":20,"6":25,"bowled":2,"caught":15,"lbw":2,"run_out":7},
    "pull_shot": {"dot":15,"1":20,"2":5,"3":0,"4":30,"6":15,"bowled":2,"caught":10,"lbw":1,"run_out":2},
    "upper_cut": {"dot":20,"1":10,"2":5,"3":0,"4":25,"6":20,"bowled":3,"caught":15,"lbw":1,"run_out":1},
}

leg_spinner_good = {
    "cover_drive": {"dot":10,"1":25,"2":10,"3":2,"4":35,"6":5,"bowled":2,"caught":8,"lbw":2,"run_out":1},
    "straight_drive": {"dot":8,"1":20,"2":8,"3":4,"4":40,"6":10,"bowled":1,"caught":5,"lbw":2,"run_out":2},
    "flick_shot": {"dot":12,"1":20,"2":15,"3":3,"4":30,"6":8,"bowled":3,"caught":5,"lbw":3,"run_out":1},
    "square_cut": {"dot":15,"1":25,"2":5,"3":1,"4":35,"6":7,"bowled":2,"caught":8,"lbw":1,"run_out":1},
    "leave": {"dot":85,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":0,"caught":0,"lbw":15,"run_out":0},
    "forward_defence": {"dot":70,"1":5,"2":0,"3":0,"4":10,"6":0,"bowled":5,"caught":2,"lbw":8,"run_out":0},
    "backward_defence": {"dot":75,"1":5,"2":0,"3":0,"4":5,"6":0,"bowled":5,"caught":2,"lbw":8,"run_out":0},
    "sweep": {"dot":15,"1":10,"2":5,"3":1,"4":20,"6":25,"bowled":2,"caught":15,"lbw":5,"run_out":2},
    "reverse_sweep": {"dot":20,"1":5,"2":3,"3":0,"4":15,"6":35,"bowled":3,"caught":15,"lbw":2,"run_out":2},
    "scoop": {"dot":25,"1":5,"2":3,"3":0,"4":10,"6":40,"bowled":2,"caught":12,"lbw":2,"run_out":1},
    "pull_shot": {"dot":10,"1":15,"2":5,"3":1,"4":20,"6":35,"bowled":3,"caught":10,"lbw":0,"run_out":1},
    "upper_cut": {"dot":15,"1":10,"2":4,"3":1,"4":10,"6":40,"bowled":3,"caught":15,"lbw":0,"run_out":2},
}

off_spinner_good = {
    "cover_drive": {"dot":12,"1":20,"2":10,"3":2,"4":38,"6":6,"bowled":2,"caught":8,"lbw":2,"run_out":2},
    "straight_drive": {"dot":9,"1":22,"2":8,"3":3,"4":40,"6":8,"bowled":1,"caught":5,"lbw":1,"run_out":3},
    "flick_shot": {"dot":15,"1":18,"2":12,"3":3,"4":30,"6":6,"bowled":3,"caught":4,"lbw":5,"run_out":4},
    "square_cut": {"dot":18,"1":22,"2":5,"3":2,"4":32,"6":6,"bowled":3,"caught":8,"lbw":2,"run_out":2},
    "leave": {"dot":90,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":0,"caught":0,"lbw":10,"run_out":0},
    "forward_defence": {"dot":72,"1":4,"2":0,"3":0,"4":10,"6":0,"bowled":5,"caught":2,"lbw":6,"run_out":1},
    "backward_defence": {"dot":74,"1":5,"2":0,"3":0,"4":8,"6":0,"bowled":5,"caught":2,"lbw":5,"run_out":1},
    "sweep": {"dot":12,"1":12,"2":5,"3":1,"4":18,"6":26,"bowled":2,"caught":15,"lbw":6,"run_out":3},
    "reverse_sweep": {"dot":16,"1":8,"2":2,"3":0,"4":14,"6":35,"bowled":3,"caught":17,"lbw":2,"run_out":3},
    "scoop": {"dot":20,"1":8,"2":2,"3":0,"4":10,"6":38,"bowled":2,"caught":15,"lbw":2,"run_out":3},
    "pull_shot": {"dot":12,"1":16,"2":6,"3":1,"4":18,"6":35,"bowled":3,"caught":7,"lbw":1,"run_out":1},
    "upper_cut": {"dot":14,"1":12,"2":4,"3":1,"4":10,"6":40,"bowled":3,"caught":14,"lbw":1,"run_out":1},
}

# Probabilities if bad shots are chosen against pace bowler
fast_bowler_bad_short = {
    "cover_drive": {"dot":20,"1":10,"2":5,"3":0,"4":10,"6":2,"bowled":10,"caught":30,"lbw":10,"run_out":3},
    "straight_drive": {"dot":18,"1":8,"2":4,"3":0,"4":8,"6":2,"bowled":15,"caught":30,"lbw":12,"run_out":3},
    "flick_shot": {"dot":15,"1":12,"2":10,"3":3,"4":10,"6":5,"bowled":8,"caught":22,"lbw":10,"run_out":5},
    "square_cut": {"dot":20,"1":15,"2":10,"3":2,"4":20,"6":5,"bowled":5,"caught":20,"lbw":1,"run_out":2},
    "pull_shot": {"dot":15,"1":15,"2":5,"3":0,"4":25,"6":10,"bowled":5,"caught":20,"lbw":2,"run_out":3},
    "upper_cut": {"dot":18,"1":10,"2":5,"3":0,"4":20,"6":15,"bowled":5,"caught":25,"lbw":1,"run_out":1},
    "leave": {"dot":40,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":20,"caught":0,"lbw":35,"run_out":5},
    "forward_defence": {"dot":35,"1":5,"2":0,"3":0,"4":5,"6":0,"bowled":25,"caught":10,"lbw":15,"run_out":5},
    "backward_defence": {"dot":30,"1":8,"2":2,"3":0,"4":8,"6":0,"bowled":20,"caught":15,"lbw":12,"run_out":5},
    "sweep": {"dot":20,"1":10,"2":5,"3":0,"4":15,"6":5,"bowled":10,"caught":25,"lbw":8,"run_out":2},
    "reverse_sweep": {"dot":22,"1":10,"2":5,"3":0,"4":15,"6":6,"bowled":8,"caught":28,"lbw":4,"run_out":2},
    "scoop": {"dot":15,"1":10,"2":5,"3":0,"4":10,"6":20,"bowled":10,"caught":25,"lbw":5,"run_out":5},
}

fast_bowler_bad_good = {
    "cover_drive": {"dot":18,"1":10,"2":5,"3":1,"4":12,"6":2,"bowled":18,"caught":20,"lbw":12,"run_out":2},
    "straight_drive": {"dot":20,"1":8,"2":4,"3":1,"4":10,"6":2,"bowled":22,"caught":15,"lbw":14,"run_out":4},
    "flick_shot": {"dot":18,"1":10,"2":8,"3":3,"4":12,"6":5,"bowled":12,"caught":18,"lbw":10,"run_out":4},
    "square_cut": {"dot":22,"1":15,"2":10,"3":2,"4":18,"6":4,"bowled":5,"caught":20,"lbw":2,"run_out":2},
    "pull_shot": {"dot":18,"1":15,"2":5,"3":0,"4":22,"6":10,"bowled":5,"caught":20,"lbw":3,"run_out":2},
    "upper_cut": {"dot":20,"1":10,"2":5,"3":0,"4":20,"6":15,"bowled":5,"caught":22,"lbw":2,"run_out":1},
    "leave": {"dot":45,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":15,"caught":0,"lbw":35,"run_out":5},
    "forward_defence": {"dot":40,"1":5,"2":1,"3":0,"4":5,"6":0,"bowled":20,"caught":8,"lbw":18,"run_out":3},
    "backward_defence": {"dot":35,"1":8,"2":2,"3":0,"4":8,"6":0,"bowled":18,"caught":12,"lbw":15,"run_out":2},
    "sweep": {"dot":18,"1":10,"2":5,"3":1,"4":15,"6":6,"bowled":10,"caught":22,"lbw":10,"run_out":3},
    "reverse_sweep": {"dot":20,"1":10,"2":5,"3":1,"4":15,"6":6,"bowled":8,"caught":25,"lbw":7,"run_out":3},
    "scoop": {"dot":15,"1":10,"2":5,"3":0,"4":10,"6":20,"bowled":10,"caught":25,"lbw":5,"run_out":5},
}

fast_bowler_bad_full = {
    "cover_drive": {"dot":20,"1":10,"2":3,"3":1,"4":15,"6":5,"bowled":15,"caught":20,"lbw":10,"run_out":1},
    "straight_drive": {"dot":15,"1":12,"2":3,"3":1,"4":18,"6":4,"bowled":10,"caught":15,"lbw":10,"run_out":2},
    "flick_shot": {"dot":20,"1":10,"2":5,"3":1,"4":10,"6":5,"bowled":10,"caught":10,"lbw":25,"run_out":4},
    "square_cut": {"dot":35,"1":6,"2":1,"3":0,"4":10,"6":3,"bowled":10,"caught":30,"lbw":3,"run_out":2},
    "leave": {"dot":15,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":20,"caught":0,"lbw":60,"run_out":5},
    "forward_defence": {"dot":40,"1":4,"2":1,"3":0,"4":1,"6":0,"bowled":25,"caught":15,"lbw":12,"run_out":2},
    "backward_defence": {"dot":45,"1":3,"2":0,"3":0,"4":1,"6":0,"bowled":30,"caught":10,"lbw":8,"run_out":3},
    "sweep": {"dot":25,"1":6,"2":2,"3":1,"4":12,"6":5,"bowled":10,"caught":20,"lbw":15,"run_out":4},
    "reverse_sweep": {"dot":20,"1":4,"2":1,"3":0,"4":10,"6":8,"bowled":15,"caught":30,"lbw":7,"run_out":5},
    "scoop": {"dot":15,"1":5,"2":1,"3":0,"4":8,"6":10,"bowled":20,"caught":30,"lbw":6,"run_out":5},
    "pull_shot": {"dot":40,"1":6,"2":1,"3":0,"4":10,"6":6,"bowled":10,"caught":20,"lbw":5,"run_out":2},
    "upper_cut": {"dot":35,"1":5,"2":1,"3":0,"4":12,"6":10,"bowled":10,"caught":20,"lbw":5,"run_out":2},
}

fast_bowler_bad_yorker = {
    "cover_drive": {"dot":15,"1":5,"2":1,"3":0,"4":5,"6":1,"bowled":35,"caught":20,"lbw":10,"run_out":8},
    "straight_drive": {"dot":20,"1":8,"2":2,"3":0,"4":6,"6":1,"bowled":30,"caught":15,"lbw":10,"run_out":8},
    "flick_shot": {"dot":10,"1":15,"2":5,"3":2,"4":4,"6":1,"bowled":25,"caught":10,"lbw":20,"run_out":8},
    "square_cut": {"dot":30,"1":10,"2":0,"3":0,"4":5,"6":1,"bowled":30,"caught":15,"lbw":5,"run_out":4},
    "leave": {"dot":5,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":65,"caught":0,"lbw":30,"run_out":0},
    "forward_defence": {"dot":10,"1":5,"2":0,"3":0,"4":0,"6":0,"bowled":50,"caught":5,"lbw":25,"run_out":5},
    "backward_defence": {"dot":15,"1":3,"2":0,"3":0,"4":0,"6":0,"bowled":55,"caught":3,"lbw":20,"run_out":4},
    "sweep": {"dot":20,"1":5,"2":1,"3":0,"4":3,"6":1,"bowled":25,"caught":30,"lbw":10,"run_out":5},
    "reverse_sweep": {"dot":25,"1":3,"2":1,"3":0,"4":2,"6":1,"bowled":20,"caught":35,"lbw":10,"run_out":3},
    "scoop": {"dot":30,"1":3,"2":2,"3":1,"4":3,"6":2,"bowled":10,"caught":40,"lbw":5,"run_out":4},
    "pull_shot": {"dot":30,"1":5,"2":0,"3":0,"4":3,"6":2,"bowled":15,"caught":40,"lbw":2,"run_out":3},
    "upper_cut": {"dot":35,"1":3,"2":0,"3":0,"4":3,"6":2,"bowled":15,"caught":35,"lbw":2,"run_out":5},
}

# Probabilities if bad shots are chosen against leg spin bowler
leg_spinner_bad_short = {
    "cover_drive": {"dot":18,"1":12,"2":4,"3":0,"4":10,"6":3,"bowled":5,"caught":40,"lbw":5,"run_out":3},
    "straight_drive": {"dot":20,"1":10,"2":3,"3":0,"4":8,"6":2,"bowled":8,"caught":42,"lbw":5,"run_out":2},
    "flick_shot": {"dot":15,"1":12,"2":5,"3":0,"4":12,"6":6,"bowled":5,"caught":35,"lbw":7,"run_out":3},
    "square_cut": {"dot":22,"1":15,"2":4,"3":0,"4":12,"6":4,"bowled":4,"caught":35,"lbw":2,"run_out":2},
    "leave": {"dot":85,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":0,"caught":0,"lbw":15,"run_out":0},
    "forward_defence": {"dot":50,"1":5,"2":0,"3":0,"4":6,"6":0,"bowled":18,"caught":6,"lbw":12,"run_out":3},
    "backward_defence": {"dot":48,"1":6,"2":0,"3":0,"4":6,"6":0,"bowled":16,"caught":8,"lbw":13,"run_out":3},
    "sweep": {"dot":15,"1":8,"2":3,"3":0,"4":10,"6":12,"bowled":6,"caught":35,"lbw":8,"run_out":3},
    "reverse_sweep": {"dot":18,"1":6,"2":2,"3":0,"4":8,"6":15,"bowled":5,"caught":38,"lbw":6,"run_out":2},
    "scoop": {"dot":20,"1":5,"2":2,"3":0,"4":6,"6":20,"bowled":4,"caught":38,"lbw":2,"run_out":3},
    "pull_shot": {"dot":15,"1":10,"2":3,"3":0,"4":10,"6":20,"bowled":5,"caught":32,"lbw":3,"run_out":2},
    "upper_cut": {"dot":18,"1":8,"2":2,"3":0,"4":8,"6":22,"bowled":4,"caught":35,"lbw":1,"run_out":2},
}

leg_spinner_bad_good = {
    "cover_drive": {"dot":28,"1":10,"2":3,"3":0,"4":6,"6":1,"bowled":20,"caught":22,"lbw":8,"run_out":2},
    "straight_drive": {"dot":26,"1":8,"2":2,"3":0,"4":5,"6":1,"bowled":22,"caught":22,"lbw":12,"run_out":2},
    "flick_shot": {"dot":22,"1":10,"2":3,"3":0,"4":6,"6":2,"bowled":18,"caught":24,"lbw":12,"run_out":3},
    "square_cut": {"dot":30,"1":12,"2":3,"3":0,"4":6,"6":1,"bowled":15,"caught":28,"lbw":3,"run_out":2},
    "leave": {"dot":90,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":0,"caught":0,"lbw":10,"run_out":0},
    "forward_defence": {"dot":65,"1":3,"2":0,"3":0,"4":4,"6":0,"bowled":18,"caught":3,"lbw":6,"run_out":1},
    "backward_defence": {"dot":60,"1":4,"2":0,"3":0,"4":4,"6":0,"bowled":20,"caught":4,"lbw":6,"run_out":2},
    "sweep": {"dot":20,"1":8,"2":3,"3":0,"4":6,"6":5,"bowled":15,"caught":30,"lbw":11,"run_out":2},
    "reverse_sweep": {"dot":22,"1":6,"2":2,"3":0,"4":6,"6":10,"bowled":12,"caught":34,"lbw":6,"run_out":2},
    "scoop": {"dot":28,"1":5,"2":2,"3":0,"4":5,"6":15,"bowled":10,"caught":33,"lbw":1,"run_out":1},
    "pull_shot": {"dot":22,"1":10,"2":3,"3":0,"4":8,"6":10,"bowled":12,"caught":30,"lbw":3,"run_out":2},
    "upper_cut": {"dot":22,"1":8,"2":2,"3":0,"4":6,"6":15,"bowled":12,"caught":33,"lbw":1,"run_out":1},
}

leg_spinner_bad_full = {
    "cover_drive": {"dot":20,"1":10,"2":5,"3":1,"4":15,"6":2,"bowled":20,"caught":15,"lbw":10,"run_out":2},
    "straight_drive": {"dot":15,"1":10,"2":5,"3":1,"4":20,"6":5,"bowled":25,"caught":10,"lbw":7,"run_out":2},
    "flick_shot": {"dot":10,"1":15,"2":10,"3":2,"4":10,"6":3,"bowled":15,"caught":10,"lbw":20,"run_out":5},
    "square_cut": {"dot":30,"1":5,"2":2,"3":0,"4":10,"6":2,"bowled":10,"caught":30,"lbw":5,"run_out":6},
    "leave": {"dot":80,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":10,"caught":0,"lbw":10,"run_out":0},
    "forward_defence": {"dot":50,"1":5,"2":0,"3":0,"4":2,"6":0,"bowled":20,"caught":5,"lbw":15,"run_out":3},
    "backward_defence": {"dot":60,"1":5,"2":0,"3":0,"4":1,"6":0,"bowled":15,"caught":5,"lbw":10,"run_out":4},
    "sweep": {"dot":15,"1":10,"2":5,"3":1,"4":10,"6":5,"bowled":10,"caught":20,"lbw":20,"run_out":4},
    "reverse_sweep": {"dot":20,"1":5,"2":2,"3":0,"4":10,"6":5,"bowled":10,"caught":30,"lbw":10,"run_out":8},
    "scoop": {"dot":10,"1":5,"2":2,"3":0,"4":5,"6":10,"bowled":15,"caught":35,"lbw":8,"run_out":10},
    "pull_shot": {"dot":25,"1":10,"2":5,"3":1,"4":10,"6":5,"bowled":10,"caught":20,"lbw":5,"run_out":9},
    "upper_cut": {"dot":30,"1":5,"2":2,"3":0,"4":10,"6":5,"bowled":10,"caught":30,"lbw":3,"run_out":5},
}

leg_spinner_bad_yorker = {
    "cover_drive": {"dot":30,"1":5,"2":0,"3":0,"4":10,"6":2,"bowled":15,"caught":23,"lbw":10,"run_out":5},
    "straight_drive": {"dot":35,"1":5,"2":0,"3":0,"4":8,"6":1,"bowled":12,"caught":25,"lbw":12,"run_out":2},
    "flick_shot": {"dot":25,"1":3,"2":0,"3":0,"4":5,"6":2,"bowled":20,"caught":25,"lbw":20,"run_out":0},
    "square_cut": {"dot":20,"1":5,"2":0,"3":0,"4":12,"6":3,"bowled":18,"caught":30,"lbw":10,"run_out":2},
    "leave": {"dot":60,"1":10,"2":0,"3":0,"4":0,"6":0,"bowled":10,"caught":0,"lbw":20,"run_out":0},
    "forward_defence": {"dot":50,"1":10,"2":0,"3":0,"4":0,"6":0,"bowled":15,"caught":15,"lbw":10,"run_out":0},
    "backward_defence": {"dot":55,"1":5,"2":0,"3":0,"4":0,"6":0,"bowled":15,"caught":10,"lbw":15,"run_out":0},
    "sweep": {"dot":25,"1":3,"2":2,"3":0,"4":7,"6":0,"bowled":15,"caught":25,"lbw":15,"run_out":8},
    "reverse_sweep": {"dot":20,"1":2,"2":0,"3":0,"4":5,"6":1,"bowled":25,"caught":30,"lbw":15,"run_out":2},
    "scoop": {"dot":15,"1":3,"2":1,"3":0,"4":4,"6":8,"bowled":30,"caught":30,"lbw":8,"run_out":1},
    "pull_shot": {"dot":35,"1":5,"2":2,"3":0,"4":5,"6":1,"bowled":12,"caught":25,"lbw":10,"run_out":5},
    "upper_cut": {"dot":20,"1":3,"2":0,"3":0,"4":10,"6":3,"bowled":20,"caught":30,"lbw":10,"run_out":4},
}

# Probabilities if bad shots are chosen against off spin bowler
off_spinner_bad_short = {
    "cover_drive": {"dot":20,"1":15,"2":5,"3":0,"4":10,"6":2,"bowled":8,"caught":35,"lbw":3,"run_out":2},
    "straight_drive": {"dot":22,"1":12,"2":4,"3":0,"4":8,"6":2,"bowled":10,"caught":35,"lbw":5,"run_out":2},
    "flick_shot": {"dot":18,"1":15,"2":6,"3":1,"4":12,"6":4,"bowled":6,"caught":30,"lbw":5,"run_out":3},
    "square_cut": {"dot":25,"1":18,"2":5,"3":0,"4":10,"6":2,"bowled":5,"caught":32,"lbw":1,"run_out":2},
    "leave": {"dot":85,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":0,"caught":0,"lbw":15,"run_out":0},
    "forward_defence": {"dot":55,"1":5,"2":0,"3":0,"4":5,"6":0,"bowled":15,"caught":5,"lbw":12,"run_out":3},
    "backward_defence": {"dot":50,"1":6,"2":0,"3":0,"4":6,"6":0,"bowled":14,"caught":8,"lbw":13,"run_out":3},
    "sweep": {"dot":20,"1":10,"2":4,"3":0,"4":10,"6":8,"bowled":6,"caught":32,"lbw":7,"run_out":3},
    "reverse_sweep": {"dot":25,"1":8,"2":2,"3":0,"4":8,"6":10,"bowled":5,"caught":35,"lbw":4,"run_out":3},
    "scoop": {"dot":25,"1":5,"2":2,"3":0,"4":6,"6":15,"bowled":4,"caught":38,"lbw":2,"run_out":3},
    "pull_shot": {"dot":18,"1":12,"2":4,"3":0,"4":10,"6":15,"bowled":6,"caught":30,"lbw":3,"run_out":2},
    "upper_cut": {"dot":20,"1":8,"2":3,"3":0,"4":8,"6":20,"bowled":5,"caught":32,"lbw":2,"run_out":2},
}

off_spinner_bad_good = {
    "cover_drive": {"dot":30,"1":12,"2":4,"3":0,"4":8,"6":1,"bowled":18,"caught":20,"lbw":5,"run_out":2},
    "straight_drive": {"dot":28,"1":10,"2":3,"3":0,"4":6,"6":1,"bowled":20,"caught":20,"lbw":10,"run_out":2},
    "flick_shot": {"dot":25,"1":12,"2":4,"3":0,"4":8,"6":2,"bowled":15,"caught":22,"lbw":10,"run_out":2},
    "square_cut": {"dot":32,"1":14,"2":4,"3":0,"4":8,"6":1,"bowled":12,"caught":25,"lbw":2,"run_out":2},
    "leave": {"dot":90,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":0,"caught":0,"lbw":10,"run_out":0},
    "forward_defence": {"dot":65,"1":3,"2":0,"3":0,"4":4,"6":0,"bowled":15,"caught":3,"lbw":8,"run_out":2},
    "backward_defence": {"dot":60,"1":4,"2":0,"3":0,"4":4,"6":0,"bowled":16,"caught":4,"lbw":10,"run_out":2},
    "sweep": {"dot":22,"1":8,"2":3,"3":0,"4":8,"6":5,"bowled":12,"caught":30,"lbw":10,"run_out":2},
    "reverse_sweep": {"dot":25,"1":6,"2":2,"3":0,"4":6,"6":10,"bowled":10,"caught":33,"lbw":6,"run_out":2},
    "scoop": {"dot":30,"1":5,"2":2,"3":0,"4":5,"6":15,"bowled":8,"caught":33,"lbw":1,"run_out":1},
    "pull_shot": {"dot":25,"1":10,"2":4,"3":0,"4":10,"6":10,"bowled":10,"caught":26,"lbw":3,"run_out":2},
    "upper_cut": {"dot":25,"1":8,"2":2,"3":0,"4":8,"6":15,"bowled":10,"caught":30,"lbw":1,"run_out":1},
}

off_spinner_bad_full = {
    "cover_drive": {"dot":20,"1":10,"2":5,"3":1,"4":15,"6":2,"bowled":20,"caught":15,"lbw":10,"run_out":2},
    "straight_drive": {"dot":15,"1":10,"2":5,"3":1,"4":20,"6":5,"bowled":25,"caught":10,"lbw":7,"run_out":2},
    "flick_shot": {"dot":15,"1":15,"2":10,"3":2,"4":10,"6":3,"bowled":15,"caught":10,"lbw":15,"run_out":5},
    "backfoot_punch": {"dot":25,"1":10,"2":5,"3":1,"4":10,"6":1,"bowled":15,"caught":20,"lbw":10,"run_out":3},
    "square_cut": {"dot":30,"1":5,"2":2,"3":0,"4":10,"6":2,"bowled":10,"caught":30,"lbw":5,"run_out":6},
    "leave": {"dot":80,"1":0,"2":0,"3":0,"4":0,"6":0,"bowled":10,"caught":0,"lbw":10,"run_out":0},
    "forward_defence": {"dot":50,"1":5,"2":0,"3":0,"4":2,"6":0,"bowled":20,"caught":5,"lbw":15,"run_out":3},
    "backward_defence": {"dot":60,"1":5,"2":0,"3":0,"4":1,"6":0,"bowled":15,"caught":5,"lbw":10,"run_out":4},
    "sweep": {"dot":12,"1":12,"2":5,"3":1,"4":10,"6":6,"bowled":10,"caught":20,"lbw":20,"run_out":4},
    "reverse_sweep": {"dot":16,"1":8,"2":2,"3":0,"4":10,"6":6,"bowled":10,"caught":30,"lbw":10,"run_out":8},
    "scoop": {"dot":10,"1":5,"2":2,"3":0,"4":5,"6":10,"bowled":15,"caught":35,"lbw":8,"run_out":10},
    "pull_shot": {"dot":25,"1":10,"2":5,"3":1,"4":10,"6":5,"bowled":10,"caught":20,"lbw":5,"run_out":9},
    "upper_cut": {"dot":30,"1":5,"2":2,"3":0,"4":10,"6":5,"bowled":10,"caught":30,"lbw":3,"run_out":5},
}

off_spinner_bad_yorker = {
    "cover_drive": {"dot":30,"1":5,"2":0,"3":0,"4":10,"6":2,"bowled":15,"caught":23,"lbw":10,"run_out":5},
    "straight_drive": {"dot":35,"1":5,"2":0,"3":0,"4":8,"6":1,"bowled":12,"caught":25,"lbw":12,"run_out":2},
    "flick_shot": {"dot":25,"1":3,"2":0,"3":0,"4":5,"6":2,"bowled":20,"caught":25,"lbw":20,"run_out":0},
    "square_cut": {"dot":20,"1":5,"2":0,"3":0,"4":12,"6":3,"bowled":18,"caught":30,"lbw":10,"run_out":2},
    "leave": {"dot":60,"1":10,"2":0,"3":0,"4":0,"6":0,"bowled":10,"caught":0,"lbw":20,"run_out":0},
    "forward_defence": {"dot":50,"1":10,"2":0,"3":0,"4":0,"6":0,"bowled":15,"caught":15,"lbw":10,"run_out":0},
    "backward_defence": {"dot":55,"1":5,"2":0,"3":0,"4":0,"6":0,"bowled":15,"caught":10,"lbw":15,"run_out":0},
    "sweep": {"dot":25,"1":3,"2":2,"3":0,"4":7,"6":0,"bowled":15,"caught":25,"lbw":15,"run_out":8},
    "reverse_sweep": {"dot":20,"1":2,"2":0,"3":0,"4":5,"6":1,"bowled":25,"caught":30,"lbw":15,"run_out":2},
    "scoop": {"dot":15,"1":3,"2":1,"3":0,"4":4,"6":8,"bowled":30,"caught":30,"lbw":8,"run_out":1},
    "pull_shot": {"dot":35,"1":5,"2":2,"3":0,"4":5,"6":1,"bowled":12,"caught":25,"lbw":10,"run_out":5},
    "upper_cut": {"dot":20,"1":3,"2":0,"3":0,"4":10,"6":3,"bowled":20,"caught":30,"lbw":10,"run_out":4},
}

# tables:
GOOD_TABLES = {
    "pace": fast_bowler_good,
    "leg_spin": leg_spinner_good,
    "off_spin": off_spinner_good,
}

BAD_TABLES = {
    "pace": {
        "yorker": fast_bowler_bad_yorker,
        "full": fast_bowler_bad_full,
        "good": fast_bowler_bad_good,
        "short": fast_bowler_bad_short,
    },
    "leg_spin": {
        "yorker": leg_spinner_bad_yorker,
        "full": leg_spinner_bad_full,
        "good": leg_spinner_bad_good,
        "short": leg_spinner_bad_short,
    },
    "off_spin": {
        "yorker": off_spinner_bad_yorker,
        "full": off_spinner_bad_full,
        "good": off_spinner_bad_good,
        "short": off_spinner_bad_short,
    },
}

# Values matched to videos
outcome_videos = {
    "dot": dot_ball,
    "1": one_run,
    "2": two_runs,
    "3": three_runs,
    "4": four_runs,
    "6": six_runs,
    "bowled": bowled,
    "caught": caught,
    "lbw": lbw,
    "run_out": run_out,
}

def is_good_shot(shot, length, line):
    return (
        shot in good_shot_zones and
        length in good_shot_zones[shot] and
        line in good_shot_zones[shot][length]
    )

def check_bowling_error_chances(line, length):
    global wide_chance

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

def handle_pause(pause_menu):
    global paused
    while paused:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pause_menu.update_and_draw(events)
        pygame.display.update()

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
outcome_possibilities = [
    "dot",
    "1",
    "2",
    "3",
    "4",
    "6",
    "bowled",
    "caught",
    "lbw",
    "run_out"
]

def user_choose_ball_type(bowler, screen):
    global bowling_type, title_font, player_font, bowling_type_buttons, paused

    running = True
    clock = pygame.time.Clock()
    show_bowler = True
    bowling_type = ""

    def resume_game():
        global paused
        paused = False
        pause_menu.close()

    pause_menu = PauseMenu(screen, on_resume=resume_game)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if pace_button.is_clicked(mouse_pos):
                    bowling_type = "pace"
                    show_bowler = False

                elif leg_spin_button.is_clicked(mouse_pos):
                    bowling_type = "leg_spin"
                    show_bowler = False

                elif off_spin_button.is_clicked(mouse_pos):
                    bowling_type = "off_spin"
                    show_bowler = False

                if pause_button_rect.collidepoint(mouse_pos):
                    screen.blit(blurred_pitch, (0, 0))

                    overlay = pygame.Surface((1450, 890))
                    overlay.set_alpha(100)
                    overlay.fill((0, 0, 0))
                    screen.blit(overlay, (0, 0))

                    paused = True
                    pause_menu.open()
                    handle_pause(pause_menu)

        mouse_pos = pygame.mouse.get_pos()

        title_text = "What type of bowling do you want to do?"
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(725, 400))
        screen.blit(blurred_pitch, (0, 0))
        screen.blit(title_surface, title_rect)

        screen.blit(pause_button, pause_button_rect)

        for button in bowling_type_buttons:
            hovered = button.is_clicked(mouse_pos)
            button.draw(screen, hovered)

        if show_bowler:
            player_text = f"{bowler} bowling"
            player_surface = player_font.render(player_text, True, (255, 255, 255))
            screen.blit(player_surface, (0, 0))

            pause_menu.update_and_draw(events)
            pygame.display.update()
            clock.tick(38)
        else:
            pause_menu.update_and_draw(events)
            pygame.display.update()
            clock.tick(38)

            return

def user_choose_line_length(bowler, batter, screen, total_runs, wickets):
    global line_index, length_index, final_line, final_length, target_y, target_x, player_font, paused, total_runs_1, wickets_1

    running = True
    clock = pygame.time.Clock()
    show_bowler = True
    line_index = 1
    length_index = 2
    final_line = ""
    final_length = ""

    def resume_game():
        global paused
        paused = False
        pause_menu.close()

    pause_menu = PauseMenu(screen, on_resume=resume_game)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if up_button.is_clicked(mouse_pos):
                    length_index = max(0, length_index - 1)

                elif down_button.is_clicked(mouse_pos):
                    length_index = min(3, length_index + 1)

                elif left_button.is_clicked(mouse_pos):
                    line_index = min(2, line_index + 1)

                elif right_button.is_clicked(mouse_pos):
                    line_index = max(0, line_index - 1)

                elif ok_button_line_length.is_clicked(mouse_pos):
                    final_length = lengths[length_index]
                    final_line = lines[line_index]
                    show_bowler = False

                if pause_button_rect.collidepoint(mouse_pos):
                    screen.blit(blurred_pitch, (0, 0))

                    overlay = pygame.Surface((1450, 890))
                    overlay.set_alpha(100)
                    overlay.fill((0, 0, 0))
                    screen.blit(overlay, (0, 0))

                    paused = True
                    pause_menu.open()
                    handle_pause(pause_menu)

        handle_pause(pause_menu)
        current_length = lengths[length_index]
        current_line = lines[line_index]

        target_x = line_positions[current_line]
        target_y = length_positions[current_length]

        screen.blit(pitch, (0, 0))
        screen.blit(pause_button, pause_button_rect)
        draw_scoreboard(screen, batter, total_runs, wickets)
        draw_target_circle(screen, target_x, target_y)

        mouse_pos = pygame.mouse.get_pos()

        for button in line_length_buttons:
            hovered = button.is_clicked(mouse_pos)
            button.draw(screen, hovered)

        if show_bowler:
            player_text = f"{bowler} bowling"
            player_surface = player_font.render(player_text, True, (255, 255, 255))
            screen.blit(player_surface, (0, 0))

            pause_menu.update_and_draw(events)
            pygame.display.update()
            clock.tick(38)
        else:
            pause_menu.update_and_draw(events)
            pygame.display.update()
            clock.tick(38)

            return

def user_choose_ball_variation(bowler, batter, screen, total_runs, wickets):
    global selected_ball_variation, bowling_type, pace_buttons, leg_spin_buttons, off_spin_buttons, player_font, target_y, target_x, paused, total_runs_1, wickets_1

    running = True
    clock = pygame.time.Clock()
    show_bowler = True
    selected_ball_variation = ""

    def resume_game():
        global paused
        paused = False
        pause_menu.close()

    pause_menu = PauseMenu(screen, on_resume=resume_game)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
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
                        if selected_ball_variation != "":
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
                            show_bowler = False

                if pause_button_rect.collidepoint(mouse_pos):
                    screen.blit(blurred_pitch, (0, 0))

                    overlay = pygame.Surface((1450, 890))
                    overlay.set_alpha(100)
                    overlay.fill((0, 0, 0))
                    screen.blit(overlay, (0, 0))

                    paused = True
                    pause_menu.open()
                    handle_pause(pause_menu)

        screen.blit(pitch, (0, 0))
        screen.blit(pause_button, pause_button_rect)
        draw_scoreboard(screen, batter, total_runs, wickets)
        draw_target_circle(screen, target_x, target_y)

        mouse_pos = pygame.mouse.get_pos()

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

        if bowling_type == "pace":
            if selected_ball_variation == "Straight":
                pygame.draw.circle(screen, (235, 64, 52), (250, 500), 46, 4)
            elif selected_ball_variation == "In Swing":
                pygame.draw.circle(screen, (235, 64, 52), (250, 620), 46, 4)
            elif selected_ball_variation == "Out Swing":
                pygame.draw.circle(screen, (235, 64, 52), (100, 500), 46, 4)
            elif selected_ball_variation == "Slower":
                pygame.draw.circle(screen, (235, 64, 52), (100, 620), 46, 4)

        if bowling_type == "leg_spin":
            if selected_ball_variation == "Leg Spin":
                pygame.draw.circle(screen, (235, 64, 52), (250, 500), 46, 4)
            elif selected_ball_variation == "Googly":
                pygame.draw.circle(screen, (235, 64, 52), (250, 620), 46, 4)
            elif selected_ball_variation == "Top Spin":
                pygame.draw.circle(screen, (235, 64, 52), (100, 500), 46, 4)
            elif selected_ball_variation == "Slider":
                pygame.draw.circle(screen, (235, 64, 52), (100, 620), 46, 4)

        if bowling_type == "off_spin":
            if selected_ball_variation == "Off Spin":
                pygame.draw.circle(screen, (235, 64, 52), (250, 500), 46, 4)
            elif selected_ball_variation == "Doosra":
                pygame.draw.circle(screen, (235, 64, 52), (250, 620), 46, 4)
            elif selected_ball_variation == "Carrom":
                pygame.draw.circle(screen, (235, 64, 52), (100, 500), 46, 4)
            elif selected_ball_variation == "Arm Ball":
                pygame.draw.circle(screen, (235, 64, 52), (100, 620), 46, 4)

        if show_bowler:
            player_text = f"{bowler} bowling"
            player_surface = player_font.render(player_text, True, (255, 255, 255))
            screen.blit(player_surface, (0, 0))

            pause_menu.update_and_draw(events)
            pygame.display.update()
            clock.tick(38)
        else:
            pause_menu.update_and_draw(events)
            pygame.display.update()
            clock.tick(38)

            return

def batting(batter, screen, total_runs, wickets):
    global all_shots, chosen_shot, target_x, target_y, selected_ball_variation, player_font, paused
    running = True
    clock = pygame.time.Clock()
    show_batter = True

    def resume_game():
        global paused
        paused = False
        pause_menu.close()

    pause_menu = PauseMenu(screen, on_resume=resume_game)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for button in all_shots:
                    if button.is_clicked(mouse_pos):
                        chosen_shot = button.shot_id
                        running = False

                if pause_button_rect.collidepoint(mouse_pos):
                    screen.blit(blurred_pitch, (0, 0))

                    overlay = pygame.Surface((1450, 890))
                    overlay.set_alpha(100)
                    overlay.fill((0, 0, 0))
                    screen.blit(overlay, (0, 0))

                    paused = True
                    pause_menu.open()
                    handle_pause(pause_menu)

        screen.blit(pitch, (0, 0))
        screen.blit(pause_button, pause_button_rect)
        draw_scoreboard(screen, batter, total_runs, wickets)
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

        pause_menu.update_and_draw(events)
        pygame.display.update()
        clock.tick(38)

def show_error(screen):
    global wide
    video_playing = True
    clock = pygame.time.Clock()
    fps = wide.get(cv2.CAP_PROP_FPS)
    wide.set(cv2.CAP_PROP_POS_FRAMES, 0)

    while video_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        success, frame = wide.read()
        if not success:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.rotate(frame_surface, -90)

        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        clock.tick(fps)

def get_outcome_table(bowl_type, is_good, length):
    """
    bowling_type: 'pace', 'leg_spin', 'off_spin'
    shot_quality: 'good' or 'bad'
    length: 'yorker', 'full', 'good', 'short'
    """

    if is_good:
        return GOOD_TABLES[bowl_type]
    else:
        return BAD_TABLES[bowl_type][length]

def pick_outcome(probabilities):
    outcomes = list(probabilities.keys())
    weights = list(probabilities.values())
    return random.choices(outcomes, weights=weights, k=1)[0]

def record_ball(result):
    global ball_log
    if result == "dot":
        result = "0"
    if result == "lbw" or result == "bowled" or result == "run_out" or result == "caught":
        result = "W"
    ball_log.append(result)
    if len(ball_log) > 6:
        ball_log.pop(0)

def draw_scoreboard(screen, batter, total_runs, wickets):
    # Bottom strip background
    pygame.draw.rect(screen, (20, 20, 20), (0, 800, 1450, 90))

    font_big = pygame.font.SysFont(None, 42)
    font_small = pygame.font.SysFont(None, 36)

    # Score & overs
    score_text = f"{batter.upper()}  {total_runs}/{wickets}"
    overs_text = f"Overs {balls_bowled // 6}.{balls_bowled % 6}"

    screen.blit(font_big.render(score_text, True, (255, 255, 255)), (40, 825))
    screen.blit(font_small.render(overs_text, True, (200, 200, 200)), (40, 860))

    # Ball-by-ball display
    x = 750
    y = 825

    for ball in ball_log:
        if ball == "W":
            color = (235, 64, 52)
        elif ball in ["4", "6"]:
            color = (0, 200, 0)
        else:
            color = (255, 255, 255)

        text = font_big.render(ball, True, color)
        screen.blit(text, (x, y))
        x += 55

def show_outcome(screen, outcome):
    global outcome_videos

    video_playing = True
    clock = pygame.time.Clock()

    video = outcome_videos[outcome]
    fps = video.get(cv2.CAP_PROP_FPS)
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    while video_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        success, frame = video.read()
        if not success:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.rotate(frame_surface, -90)

        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        clock.tick(fps)

def first_innings(screen):
    global title_font, total_runs_1, wickets_1, continue_button
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if continue_button.is_clicked(mouse_pos):
                    return

        mouse_pos = pygame.mouse.get_pos()

        player_1_score = f"Player 1 scored: {total_runs_1}/{wickets_1}"
        player_1_score_surface = title_font.render(player_1_score, True, (255, 255, 255))
        player_1_score_rect = player_1_score_surface.get_rect(center=(725, 148))

        runs_needed = f"Player 2 needs {total_runs_1 + 1} runs to win."
        runs_needed_surface = title_font.render(runs_needed, True, (255, 255, 255))
        runs_needed_rect = runs_needed_surface.get_rect(center=(725, 275))

        screen.blit(blurred_pitch, (0, 0))
        screen.blit(player_1_score_surface, player_1_score_rect)
        screen.blit(runs_needed_surface, runs_needed_rect)

        hovered = continue_button.is_clicked(mouse_pos)
        continue_button.draw(screen, hovered)

        pygame.display.update()
        clock.tick(38)

def end_game(screen, batter, bowler):
    global title_font, total_runs_1, wickets_1, total_runs_2, wickets_2, main_menu_button
    clock = pygame.time.Clock()
    winner = ""
    score = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if main_menu_button.is_clicked(mouse_pos):
                    return

        mouse_pos = pygame.mouse.get_pos()

        if total_runs_1 > total_runs_2:
            winner = bowler
            score = f"{total_runs_1 - total_runs_2} runs."
        elif total_runs_2 > total_runs_1:
            winner = batter
            score = f"{10 - wickets_2} wickets."
        else:
            winner = "Tie"

        if winner != "Tie":
            show_winner = f"{winner} won by {score}"
        else:
            show_winner = f"The game ended in a tie!"

        show_winner_surface = title_font.render(show_winner, True, (255, 255, 255))
        show_winner_rect = show_winner_surface.get_rect(center=(725, 148))

        screen.blit(blurred_pitch, (0, 0))
        screen.blit(show_winner_surface, show_winner_rect)

        hovered = main_menu_button.is_clicked(mouse_pos)
        main_menu_button.draw(screen, hovered)

        pygame.display.update()
        clock.tick(38)

def double_one(screen, toss_result):
    global final_line, final_length, selected_ball_variation
    global chosen_shot, bowling_type
    global run_outcome_values, total_runs_1
    global wicket_outcomes, wickets_1
    global balls_bowled, paused
    global length_index, line_index
    global total_runs_2, wickets_2, ball_log

    paused = False
    total_runs_1 = 0
    wickets_1 = 0
    balls_bowled = 0
    total_runs_2 = 0
    wickets_2 = 0

    ball_log = []

    def resume_game():
        global paused
        paused = False

    pause_menu = PauseMenu(screen, resume_game)

    length_index = 2
    line_index = 1

    pygame.display.set_caption("Super Over! - Double Player Mode")

    handle_pause(pause_menu)
    if toss_result == "bowl":
        batter = "Player 2"
        bowler = "Player 1"

        user_choose_ball_type(bowler, screen)

        balls = 0

        while balls < 6:
            handle_pause(pause_menu)
            user_choose_line_length(bowler, batter, screen, total_runs_1, wickets_1)
            user_choose_ball_variation(bowler, batter, screen, total_runs_1, wickets_1)

            batting(batter, screen, total_runs_1, wickets_1)

            error = check_bowling_error_chances(final_line, final_length)

            if error == "wide":
                show_error(screen)
                total_runs_1 += 1
                record_ball("Wd")
                continue

            table = get_outcome_table(bowling_type, is_good_shot(chosen_shot, final_length, final_line), final_length)

            outcome = pick_outcome(table[chosen_shot])

            if outcome in run_outcome_values:
                total_runs_1 += run_outcome_values[outcome]

            if outcome in wicket_outcomes:
                wickets_1 += 1

            balls += 1
            balls_bowled += 1

            record_ball(outcome)
            show_outcome(screen, outcome)
            draw_scoreboard(screen, batter, total_runs_1, wickets_1)

    else:
        batter = "Player 1"
        bowler = "Player 2"

        handle_pause(pause_menu)
        user_choose_ball_type(bowler, screen)

        balls = 0

        while balls < 6:
            handle_pause(pause_menu)
            user_choose_line_length(bowler, batter, screen, total_runs_1, wickets_1)
            user_choose_ball_variation(bowler, batter, screen, total_runs_1, wickets_1)

            batting(batter, screen, total_runs_1, wickets_1)

            error = check_bowling_error_chances(final_line, final_length)

            if error == "wide":
                show_error(screen)
                total_runs_1 += 1
                record_ball("Wd")
                continue

            table = get_outcome_table(bowling_type, is_good_shot(chosen_shot, final_length, final_line), final_length)

            outcome = pick_outcome(table[chosen_shot])

            if outcome in run_outcome_values:
                total_runs_1 += run_outcome_values[outcome]

            if outcome in wicket_outcomes:
                wickets_1 += 1

            balls += 1
            balls_bowled += 1

            record_ball(outcome)
            show_outcome(screen, outcome)
            draw_scoreboard(screen, batter, total_runs_1, wickets_1)

    first_innings(screen)

    batter2 = bowler
    bowler2 = batter

    total_runs_2 = 0
    wickets_2 = 0
    ball_log = []

    handle_pause(pause_menu)
    user_choose_ball_type(bowler2, screen)

    balls = 0
    balls_bowled = 0

    while balls < 6:
        handle_pause(pause_menu)
        user_choose_line_length(bowler2, batter2, screen, total_runs_2, wickets_2)
        user_choose_ball_variation(bowler2, batter2, screen, total_runs_2, wickets_2)

        batting(batter2, screen, total_runs_2, wickets_2)

        error = check_bowling_error_chances(final_line, final_length)

        if error == "wide":
            show_error(screen)
            total_runs_2 += 1
            record_ball("Wd")
            continue

        table = get_outcome_table(bowling_type, is_good_shot(chosen_shot, final_length, final_line), final_length)

        outcome = pick_outcome(table[chosen_shot])

        if outcome in run_outcome_values:
            total_runs_2 += run_outcome_values[outcome]

        if outcome in wicket_outcomes:
            wickets_2 += 1

        balls += 2
        balls_bowled += 2

        record_ball(outcome)
        show_outcome(screen, outcome)
        draw_scoreboard(screen, batter2, total_runs_2, wickets_2)

        if total_runs_2 > total_runs_1:
            break

    end_game(screen, batter2, bowler2)
    return