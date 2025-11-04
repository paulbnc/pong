import pygame
from utils import *

class raquette:
    def __init__(self, x, y, player:int, height=player_height, width=player_width, speed=player_speed):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.player = player
        self.speed = speed
        self.color = (255, 215, 0)

    def handle_input(self, screen):
        keys = pygame.key.get_pressed()

        if self.player == 1:
            if keys[pygame.K_UP]:
                self.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.y += self.speed

        if self.player == 2:
            if keys[pygame.K_z]:
                self.y -= self.speed
            if keys[pygame.K_s]:
                self.y += self.speed

        self.check_coords()
        self.draw(screen)
    
    def check_coords(self):
        if self.y < HUD_HEIGHT:
            self.y = HUD_HEIGHT
        if self.y > game_height - self.height + HUD_HEIGHT:
            self.y = game_height - self.height + HUD_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


import math
import pygame
from utils import *

class Ball:
    def __init__(self, x, y, speed=ball_speed, size=ball_size):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = size
        self.color = (255, 215, 0)

        angle = math.radians(45)
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, center=(self.x, self.y), radius=self.radius)

    def handle_input(self, screen, player1, player2):
        self.x += self.vx
        self.y += self.vy

        self.check_collide(player1)
        self.check_collide(player2)

        self.draw(screen)

    def check_collide(self, player=None):
        """Vérifie les collisions avec les murs et les raquettes."""

        if self.y - self.radius < HUD_HEIGHT: 
            self.y = HUD_HEIGHT + self.radius
            self.vy *= -1

        if self.y + self.radius > game_height + HUD_HEIGHT:  
            self.y = game_height + HUD_HEIGHT - self.radius
            self.vy *= -1

        if player is not None:
            rect = pygame.Rect(player.x, player.y, player.width, player.height)

            if rect.collidepoint(self.x, self.y):
                self.vx *= -1

                # Calcul du point d'impact relatif à la raquette
                # (plus on frappe loin du centre, plus l'angle est fort)
                offset = (self.y - (player.y + player.height / 2)) / (player.height / 2)
                max_angle = math.radians(45)  # angle maximal du rebond

                angle = offset * max_angle
                direction = 1 if self.vx > 0 else -1  # direction du mouvement après rebond

                # Mise à jour des composantes de vitesse selon l'angle de rebond
                self.vx = direction * self.speed * math.cos(angle)
                self.vy = self.speed * math.sin(angle)

                # Correction pour éviter qu’elle reste collée à la raquette
                if player.player == 1:
                    self.x = player.x + player.width + self.radius
                else:
                    self.x = player.x - self.radius

    def check_goal(self) -> int:
        if self.x > game_width - self.radius:
            return 1 
        if self.x < 0 + self.radius:
            return 2 
        return 0


    