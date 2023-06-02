import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, SHIELD_TYPE, HAMMER_TYPE, HEART_TYPE


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
    
    def update(self, game):
        if len(self.obstacles) == 0:
            if random.random() < 0.6:
                self.obstacles.append(Cactus((SMALL_CACTUS + LARGE_CACTUS)))
            else:
                self.obstacles.append(Bird())

        self.handle_colliderect(game) # Chama a função para verificar colisões

    def handle_colliderect(self, game):
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):  # Verifica se houve colisão entre o jogador e o obstáculo
                if not game.player.has_power_up:
                    game.sounds[3].play()  # Reproduz o som de colisão
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    self.obstacles.pop()
                    break
                elif game.player.type == HAMMER_TYPE:
                    self.obstacles.remove(obstacle) # remove os obtaculos
                    game.sounds[1].play() # Reproduz o som correspondent
                elif game.player.type == SHIELD_TYPE:
                    return
                elif game.player.type == HEART_TYPE: # Se o jogador tiver o power-up HEART_TYPE
                    game.death_count -= 1 # Diminui o contador de mortes
                    self.obstacles.pop() # Remove o obstáculo da lista
                    game.player.power_up_time = 0 # Redefine o tempo de duração do power-up 

    def reset_obstacles(self):
        self.obstacles = []  # Redefine a lista de obstáculos como vazia

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)