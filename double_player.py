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
            pygame.draw.circle(screen, (0, 135, 245), (self.x, self.y), self.radius + 6, 4)

        label = self.font.render(self.text, True, (255, 255, 255))
        rect = label.get_rect(center=(self.x, self.y))
        screen.blit(label, rect)

    def is_clicked(self, mouse_pos):
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        return dx * dx + dy * dy <= self.radius * self.radius

up_button = CircleButton(200, 500, 40, "^")
down_button = CircleButton(200, 620, 40, "v")
left_button = CircleButton(140, 560, 40, "<")
right_button = CircleButton(260, 560, 40, ">")
ok_button = CircleButton(1200, 560, 40, "OK")

buttons = [up_button, down_button, left_button, right_button, ok_button]

# Different types of shots
front_foot_shots = ["forward defense", "sweep", "reverse sweep", "scoop", "cover drive", "straight drive", "flick shot"]
back_foot_shots = ["backward defense", "pull shot", "backfoot punch", "square cut", "upper cut"]
shot = "leave"

# Background image
pitch = pygame.image.load("pitch_background.png")

# Different types of balls
pace_balls = ["straight ball", "inswing", "outswing"]
leg_spin_balls = ["leg spin", "googly", "arm ball"]
off_spin_balls = ["off spin", "doosra", "arm ball"]

# Different types of length and line
lengths = ["yorker", "full", "good", "short"]
lines = ["outside_off", "stumps", "outside_leg"]

length_index = 2
line_index = 1

# Draw circle to show where user is bowling
def draw_target_circle(screen, x, y):
    # Outer glow
    pygame.draw.circle(screen, (0, 135, 245), (x, y), 80, 10)

length_positions = {
    "yorker": 620,
    "full": 540,
    "good": 450,
    "short": 300
}

line_positions = {
    "outside_leg": 550,
    "stumps": 715,
    "outside_off": 850
}

# Different types of outcomes
outcomes = ["Dot Ball", "1 run", "2 runs", "3 runs", "4 runs", "6 runs", "Bowled out", "Caught out", "LBW", "Run out", "Wide", "No ball"]

def batting_first():
    pass

def bowling_first():
    pass

def double_one(screen, toss_result):
    global line_index, length_index
    # Setting up the new screen
    pygame.display.set_caption("Double Player - One Over")
    clock = pygame.time.Clock()
    running = True

    while running:
        if toss_result == "bowl":
            bowling_first()
        elif toss_result == "bat":
            batting_first()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if up_button.is_clicked(mouse_pos):
                    length_index = min(3, length_index + 1)

                elif down_button.is_clicked(mouse_pos):
                    length_index = max(0, length_index - 1)

                elif left_button.is_clicked(mouse_pos):
                    line_index = min(2, line_index + 1)

                elif right_button.is_clicked(mouse_pos):
                    line_index = max(0, line_index - 1)

        current_length = lengths[length_index]
        current_line = lines[line_index]

        target_x = line_positions[current_line]
        target_y = length_positions[current_length]

        screen.blit(pitch, (0, 0))
        draw_target_circle(screen, target_x, target_y)
        mouse_pos = pygame.mouse.get_pos()

        for btn in buttons:
            hovered = btn.is_clicked(mouse_pos)
            btn.draw(screen, hovered)

        pygame.display.update()
        clock.tick(38)

def double_two(screen, toss_result):
    pass
def double_five(screen, toss_result):
    pass