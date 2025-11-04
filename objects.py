import pygame
from utils import *
import math
import random

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

class Ball:
    def __init__(self, x, y, speed=ball_speed, size=ball_size):
        self.x = x
        self.y = y
        self.radius = size
        self.color = (255, 215, 0)
        angle = random.uniform(-math.pi/4, math.pi/4)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        if random.random() < 0.5:
            self.vx *= -1
    
    def handle_input(self, screen, player1:raquette, player2:raquette):

        self.x += self.vx
        self.y += self.vy
    
        self.check_collide()  
        self.check_collide(player1)  
        self.check_collide(player2)  
        
        self.draw(screen)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, center=(self.x, self.y), radius=self.radius)

    def check_collide(self, player:raquette=None):
        # Collision avec les murs haut et bas
        if self.y > game_height + HUD_HEIGHT - self.radius:
            self.y = game_height + HUD_HEIGHT - self.radius
            self.vy *= -1  # Inversion de la vitesse verticale
        if self.y < HUD_HEIGHT + self.radius:
            self.y = HUD_HEIGHT + self.radius
            self.vy *= -1
        
        # Collision avec les raquettes
        if player is not None:
            # Vérifier si la balle est dans la zone de la raquette
            if (self.x - self.radius <= player.x + player.width and 
                self.x + self.radius >= player.x and
                self.y + self.radius >= player.y and 
                self.y - self.radius <= player.y + player.height):
                
                # Position de collision sur la raquette (de -1 à 1)
                relative_intersect_y = (player.y + player.height/2) - self.y
                normalized_intersect = relative_intersect_y / (player.height/2)
                
                # Angle de rebond basé sur la position d'impact (-60° à +60°)
                bounce_angle = normalized_intersect * (math.pi / 3)  # 60 degrés max
                
                # Direction horizontale selon le joueur
                direction = -1 if player.player == 1 else 1
                
                # Calcul des nouvelles vitesses
                speed_magnitude = math.sqrt(self.vx**2 + self.vy**2)
                self.vx = direction * speed_magnitude * math.cos(bounce_angle)
                self.vy = -speed_magnitude * math.sin(bounce_angle)
                
                # Repositionner la balle pour éviter qu'elle reste coincée
                if player.player == 2:  # Joueur gauche
                    self.x = player.x + player.width + self.radius
                else:  # Joueur droit
                    self.x = player.x - self.radius
                
                # Légère augmentation de vitesse à chaque rebond
                self.vx *= 1.05
                self.vy *= 1.05
                
                return True
        
        return False

    def check_goal(self) -> int:
        if self.x > game_width - self.radius:
            return 1  
        if self.x < 0 + self.radius:
            return 2  
        return 0


    