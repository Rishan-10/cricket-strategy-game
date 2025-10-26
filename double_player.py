# Imports
from sys import exit
import pygame

# Different types of shots
front_foot_shots = ["forward defense", "sweep", "reverse sweep", "scoop", "cover drive", "straight drive", "flick shot"]
back_foot_shots = ["backward defense", "pull shot", "backfoot punch", "square cut", "upper cut"]
shot = "leave"

# Different types of balls
pace_balls = ["straight ball", "inswing", "outswing"]
leg_spin_balls = ["leg spin", "googly", "arm ball"]
off_spin_balls = ["off spin", "doosra", "arm ball"]

# Different types of length and line
length = ["yorker", "full", "good", "short"]
line = ["outside off stump", "on the stumps", "outside leg stumps"]

# Different types of outcomes
outcomes = ["Dot Ball", "1 run", "2 runs", "3 runs", "4 runs", "6 runs", "Bowled out", "Caught out", "LBW", "Run out", "Wide", "No ball"]

def double_one(screen, toss_result):
    # Setting up the new screen
    pygame.display.set_caption("Double Player - One Over")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
                running = False

        screen.fill((0, 0, 0))

        pygame.display.update()
        clock.tick(38)

def double_two(screen, toss_result):
    pass
def double_five(screen, toss_result):
    pass