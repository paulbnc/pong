import pygame
from utils import *
from objects import raquette, Ball
import time

def main():
    pygame.init()
    pygame.font.init()

    hud_font = pygame.font.SysFont("Courier", 20, bold=True)

    screen = pygame.display.set_mode((game_width, game_height + HUD_HEIGHT))
    pygame.display.set_caption("Pong Prototype")
    clock = pygame.time.Clock()
    score1 = score2 = 0
    running = True

    player1 = raquette(x=game_width-side_value-player_width, y=(game_height-HUD_HEIGHT)//2, player=1)

    player2 = raquette(x=side_value, y=(game_height-HUD_HEIGHT)//2, player=2)

    ball = Ball(x=game_width//2, y=(game_height+HUD_HEIGHT)//2)

    is_ball = True
    last_deletion = time.time()

    while running:

        goal = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        if is_ball:
            goal = ball.check_goal()
        
        if goal != 0:
            del ball
            last_deletion = time.time()
            if goal == 1:
                score1 += 1
            if goal == 2:
                score2 += 1
            is_ball = False
        if not(is_ball) and time.time() - last_deletion > 1. :
            ball = Ball(x=game_width//2, y=(game_height+HUD_HEIGHT)//2)
            is_ball = True
        player1.handle_input(screen)
        player2.handle_input(screen)
        if is_ball:
            ball.handle_input(screen, player1, player2)

        # === HUD ===
        pygame.draw.rect(screen, 'black', (0, 0, game_width, HUD_HEIGHT))
        pygame.draw.rect(screen, (255, 215, 0), (0, HUD_HEIGHT-5, game_width, 5))

        score_label = hud_font.render(f"{score1}:{score2}", True, (255, 215, 0))
        screen.blit(score_label, (game_width//2 - score_label.get_width()//2, HUD_HEIGHT//4))
        
        pygame.display.flip()
        clock.tick(fps) 

if __name__ == "__main__":
    main()
