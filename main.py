import pygame
from utils import width, height, draw_popup, fps, piece_size, shape_piece_map, HUD_HEIGHT, pacman_health
from objects import Pacman, Piecesmap, horde
from session_status import best, total
import time
import numpy as np

def main():
    pygame.init()
    pygame.font.init()

    # Polices "retro gaming"
    vic_font = pygame.font.SysFont("Courier", 64, bold=True)
    btn_font = pygame.font.SysFont("Courier", 28, bold=True)
    hud_font = pygame.font.SysFont("Courier", 20, bold=True)

    screen = pygame.display.set_mode((width, height + HUD_HEIGHT))
    pygame.display.set_caption("Pacman Prototype")
    clock = pygame.time.Clock()

    pacman = Pacman(width // 2, height // 2 + HUD_HEIGHT)
    pieces = Piecesmap()
    enemies = horde(nb=5)  # 👈 Horde d’ennemis
    victory_mode = False
    nb_pieces_partie = np.sum(pieces.map)

    scanlines = [y for y in range(HUD_HEIGHT, height + HUD_HEIGHT, 4)]
    restart_rect = pygame.Rect(width//2 - 100, height//2 + HUD_HEIGHT + 60, 200, 60)

    # Timer de partie
    start_time = time.time()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        screen.fill("black")

        if victory_mode:
            # Affichage popup
            draw_popup(screen, victory=True, font=vic_font)

            # Bouton RESTART
            if restart_rect.collidepoint(mouse_pos):
                color = (255, 220, 120)
                if click:
                    pacman = Pacman(width // 2, height // 2 + HUD_HEIGHT)
                    pieces = Piecesmap()
                    enemies = horde(nb=5)
                    nb_pieces_partie = np.sum(pieces.map)
                    victory_mode = False
                    start_time = time.time()
            else:
                color = (180, 180, 180)

            pygame.draw.rect(screen, color, restart_rect, border_radius=8)
            restart_text = btn_font.render("RESTART", True, (0, 0, 0))
            text_rect = restart_text.get_rect(center=restart_rect.center)
            screen.blit(restart_text, text_rect)

            # Scanlines pour effet retro
            for y in scanlines:
                pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y), 1)

        else:
            # Gestion du joueur et des pièces
            pacman.handle_input()
            pieces.handle_input(pacman)
            pacman.clean_bullets()

            # Gestion des ennemis
            enemies.update_enemies()
            enemies.handle_input(pacman)

            # Mise à jour du total de pièces mangées
            total['pieces'] += pieces.cpt_pieces

            # Dessin
            pieces.draw(screen)
            enemies.draw(screen)
            pacman.draw(screen)
            pacman.update_bullets(screen)
            
            # Vérifie si Pacman est mort
            if not pacman.alive:
                victory_mode = True  # On termine la partie sur défaite

            # Victoire
            if pieces.victory():
                victory_mode = True
                elapsed_time = time.time() - start_time
                if (nb_pieces_partie > best['pieces'] or 
                    (nb_pieces_partie == best['pieces'] and elapsed_time < best['time'])):
                    best['pieces'] = nb_pieces_partie
                    best['time'] = elapsed_time

# === HUD ===
        pygame.draw.rect(screen, 'black', (0, 0, width, HUD_HEIGHT))

        # COLONNE GAUCHE - Statistiques
        left_x = 10
        total_pieces_text = hud_font.render(f"Total: {total['pieces']}", True, (255, 215, 0))
        screen.blit(total_pieces_text, (left_x, 10))

        remaining = np.sum(pieces.map)
        proportion_text = hud_font.render(f"Remaining: {remaining}", True, (255, 215, 0))
        screen.blit(proportion_text, (left_x, 35))

        # Timer partie en cours
        if not victory_mode:
            elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        tenths = int((elapsed_time * 10) % 10)
        timer_text = hud_font.render(f"Time: {minutes:02}:{seconds:02}.{tenths}", True, (255, 215, 0))
        screen.blit(timer_text, (left_x, 60))

        # CENTRE - BARRE DE VIE DE PACMAN
        bar_width = 180
        bar_height = 20
        bar_x = width//2 - bar_width//2
        bar_y = 15
        
        health_ratio = pacman.health / pacman_health
        health_width = int(bar_width * health_ratio)

        # Couleur selon niveau de vie
        if health_ratio > 0.6:
            color = (0, 255, 0)     # Vert
        elif health_ratio > 0.3:
            color = (255, 165, 0)   # Orange
        else:
            color = (255, 0, 0)     # Rouge

        # Label HP au-dessus de la barre
        hp_label = hud_font.render("HEALTH", True, (255, 215, 0))
        screen.blit(hp_label, (width//2 - hp_label.get_width()//2, bar_y - 15))
        
        # Fond et barre
        pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y + 10, bar_width, bar_height))
        pygame.draw.rect(screen, color, (bar_x, bar_y + 10, health_width, bar_height))
        pygame.draw.rect(screen, (255, 215, 0), (bar_x, bar_y + 10, bar_width, bar_height), 2)

        # COLONNE DROITE - Stats meilleure partie
        best_time = best['time']
        if best_time == float('inf'):
            best_time = 0
        best_minutes = int(best_time // 60)
        best_seconds = int(best_time % 60)
        best_tenths = int((best_time * 10) % 10)
        
        best_label = hud_font.render("BEST RUN:", True, (255, 215, 0))
        screen.blit(best_label, (width - 200, 10))
        
        best_pieces = hud_font.render(f"{best['pieces']} pieces", True, (255, 215, 0))
        screen.blit(best_pieces, (width - 200, 35))
        
        best_time_text = hud_font.render(f"{best_minutes:02}:{best_seconds:02}.{best_tenths}", True, (255, 215, 0))
        screen.blit(best_time_text, (width - 200, 60))

        pygame.display.flip()
        clock.tick(fps) 

if __name__ == "__main__":
    main()
