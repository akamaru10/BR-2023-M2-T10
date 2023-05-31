import random

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD


class Bird(Obstacle):
    def __init__(self):
        self.type = 0
        self.image = BIRD
        super().__init__(self.image, self.type)
        self.Y_POS = 250
        random_high = random.random()
        if random_high <= 0.2:
            self.Y_POS = 335
        elif random_high >= 0.9:
            self.Y_POS = 200
        self.rect.y = self.Y_POS
        self.step_index = 0

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()


        if self.step_index >= 10:
            self.step_index = 0

        self.type = 0 if self.step_index < 5 else 1
        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.image[self.type], (self.rect.x, self.rect.y))