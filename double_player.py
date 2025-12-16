# Imports
from sys import exit
import pygame

pygame.init()
pygame.font.init()

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

# Chosen bowling type
bowling_type = "pace"

# Buttons for selecting line and length
up_button = CircleButton(200, 500, 40, "^")
down_button = CircleButton(200, 620, 40, "v")
left_button = CircleButton(140, 560, 40, "<")
right_button = CircleButton(260, 560, 40, ">")
ok_button = CircleButton(1200, 560, 40, "OK")

# Buttons for selecting type of pace ball
straight = CircleButton(250, 500, 40, "STRAIGHT")
in_swing = CircleButton(250, 620, 40, "IN SWING")
out_swing = CircleButton(100, 500, 40, "OUT SWING")
slower = CircleButton(100, 620, 40, "SLOWER")

# Buttons for selecting type of leg spin ball
leg_spin = CircleButton(250, 500, 40, "LEG SPIN")
googly = CircleButton(250, 620, 40, "GOOGLY")
top_spin = CircleButton(100, 500, 40, "TOP SPIN")
slider = CircleButton(100, 620, 40, "SLIDER")

# Buttons for selecting type of off spin ball
off_spin = CircleButton(250, 500, 40, "OFF SPIN")
doosra = CircleButton(250, 620, 40, "DOOSRA")
carrom = CircleButton(100, 500, 40, "CARROM")
arm_ball = CircleButton(100, 620, 40, "ARM BALL")

# Game states
choose_length_line = True
choose_ball_type = False

line_length_buttons = [up_button, down_button, left_button, right_button, ok_button]
pace_buttons = [straight, in_swing, out_swing, slower, ok_button]
leg_spin_buttons = [leg_spin, googly, top_spin, slider, ok_button]
off_spin_buttons = [off_spin, doosra, carrom, arm_ball, ok_button]

# Different types of shots
front_foot_shots = ["forward defense", "sweep", "reverse sweep", "scoop", "cover drive", "straight drive", "flick shot"]
back_foot_shots = ["backward defense", "pull shot", "backfoot punch", "square cut", "upper cut"]
shot = "leave"

# Final choices of the user
final_length = ""
final_line = ""
selected_ball_type = ""

# Background image
pitch = pygame.image.load("pitch_background.png")

# Different types of balls
pace_balls = ["straight ball", "inswing", "outswing"]
leg_spin_balls = ["leg spin", "googly", "arm ball"]
off_spin_balls = ["off spin", "doosra", "arm ball"]

# Different types of length and line
lengths = ["yorker", "full", "good", "short"]
lines = ["outside_leg", "stumps", "outside_off"]

length_index = 2
line_index = 1

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
    "outside_leg": 850
}

# Different types of outcomes
outcomes = ["Dot Ball", "1 run", "2 runs", "3 runs", "4 runs", "6 runs", "Bowled out", "Caught out", "LBW", "Run out", "Wide", "No ball"]

def batting_first(screen):
    global line_index, length_index, final_line, final_length, choose_length_line, choose_ball_type, selected_ball_type, bowling_type
    running = True
    clock = pygame.time.Clock()

    while running:
        print("Player 2 bowling")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and choose_length_line:
                mouse_pos = pygame.mouse.get_pos()

                if up_button.is_clicked(mouse_pos):
                    length_index = max(0, length_index - 1)

                elif down_button.is_clicked(mouse_pos):
                    length_index = min(3, length_index + 1)

                elif left_button.is_clicked(mouse_pos):
                    line_index = min(2, line_index + 1)

                elif right_button.is_clicked(mouse_pos):
                    line_index = max(0, line_index - 1)

                elif ok_button.is_clicked(mouse_pos) and choose_length_line:
                    final_length = lengths[length_index]
                    final_line = lines[line_index]
                    choose_length_line = False
                    choose_ball_type = True

            if event.type == pygame.MOUSEBUTTONDOWN and choose_ball_type and bowling_type == "pace":
                mouse_pos = pygame.mouse.get_pos()

                if straight.is_clicked(mouse_pos):
                    selected_ball_type = "straight"
                elif in_swing.is_clicked(mouse_pos):
                    selected_ball_type = "in_swing"
                elif out_swing.is_clicked(mouse_pos):
                    selected_ball_type = "out_swing"
                elif slower.is_clicked(mouse_pos):
                    selected_ball_type = "slower"
                elif ok_button.is_clicked(mouse_pos):
                    chosen_ball_type = False
                    print(selected_ball_type)

        current_length = lengths[length_index]
        current_line = lines[line_index]

        target_x = line_positions[current_line]
        target_y = length_positions[current_length]

        screen.blit(pitch, (0, 0))
        draw_target_circle(screen, target_x, target_y)
        mouse_pos = pygame.mouse.get_pos()

        if choose_length_line:
            for button in line_length_buttons:
                hovered = button.is_clicked(mouse_pos)
                button.draw(screen, hovered)

        if choose_ball_type:
            for button in pace_buttons:
                hovered = button.is_clicked(mouse_pos)
                button.draw(screen, hovered)

        if choose_ball_type and bowling_type == "pace":
            if selected_ball_type == "straight":
                pygame.draw.circle(screen, (235, 64, 52), (250, 500), 46, 4)
            elif selected_ball_type == "in_swing":
                pygame.draw.circle(screen, (235, 64, 52), (250, 620), 46, 4)
            elif selected_ball_type == "out_swing":
                pygame.draw.circle(screen, (235, 64, 52), (100, 500), 46, 4)
            elif selected_ball_type == "slower":
                pygame.draw.circle(screen, (235, 64, 52), (100, 620), 46, 4)

        pygame.display.update()
        clock.tick(38)

def bowling_first(screen):
    global line_index, length_index, final_line, final_length, choose_length_line, choose_ball_type, selected_ball_type, bowling_type
    running = True
    clock = pygame.time.Clock()

    while running:
        print("Player 1 bowling")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and choose_length_line:
                mouse_pos = pygame.mouse.get_pos()

                if up_button.is_clicked(mouse_pos):
                    length_index = max(0, length_index - 1)

                elif down_button.is_clicked(mouse_pos):
                    length_index = min(3, length_index + 1)

                elif left_button.is_clicked(mouse_pos):
                    line_index = min(2, line_index + 1)

                elif right_button.is_clicked(mouse_pos):
                    line_index = max(0, line_index - 1)

                elif ok_button.is_clicked(mouse_pos):
                    final_length = lengths[length_index]
                    final_line = lines[line_index]
                    choose_length_line = False
                    choose_ball_type = True

            if event.type == pygame.MOUSEBUTTONDOWN and choose_ball_type and bowling_type == "pace":
                mouse_pos = pygame.mouse.get_pos()

                if straight.is_clicked(mouse_pos):
                    selected_ball_type = "straight"
                elif in_swing.is_clicked(mouse_pos):
                    selected_ball_type = "in_swing"
                elif out_swing.is_clicked(mouse_pos):
                    selected_ball_type = "out_swing"
                elif slower.is_clicked(mouse_pos):
                    selected_ball_type = "slower"
                elif ok_button.is_clicked(mouse_pos):
                    chosen_ball_type = False
                    print(selected_ball_type)

        current_length = lengths[length_index]
        current_line = lines[line_index]

        target_x = line_positions[current_line]
        target_y = length_positions[current_length]

        screen.blit(pitch, (0, 0))
        draw_target_circle(screen, target_x, target_y)
        mouse_pos = pygame.mouse.get_pos()

        if choose_length_line:
            for button in line_length_buttons:
                hovered = button.is_clicked(mouse_pos)
                button.draw(screen, hovered)

        if choose_ball_type:
            for button in pace_buttons:
                hovered = button.is_clicked(mouse_pos)
                button.draw(screen, hovered)

        if choose_ball_type and bowling_type == "pace":
            if selected_ball_type == "straight":
                pygame.draw.circle(screen, (235, 64, 52), (250, 500), 46, 4)
            elif selected_ball_type == "in_swing":
                pygame.draw.circle(screen, (235, 64, 52), (250, 620), 46, 4)
            elif selected_ball_type == "out_swing":
                pygame.draw.circle(screen, (235, 64, 52), (100, 500), 46, 4)
            elif selected_ball_type == "slower":
                pygame.draw.circle(screen, (235, 64, 52), (100, 620), 46, 4)

        pygame.display.update()
        clock.tick(38)

def double_one(screen, toss_result):
    # Setting up the new screen
    pygame.display.set_caption("Double Player - One Over")

    if toss_result == "bowl":
        bowling_first(screen)
    elif toss_result == "bat":
        batting_first(screen)

def double_two(screen, toss_result):
    pass
def double_five(screen, toss_result):
    pass