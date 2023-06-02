import random

from dino_runner.utils.constants import  CLOUD, SCREEN_WIDTH


class Cloud:
    def __init__(self):
        self.image = CLOUD
        self.image_whidth = self.image.get_width() # Largura da imagem da nuvem
        self.x_pos_cloud = SCREEN_WIDTH + random.randint(800, 1000)  # Posição horizontal inicial da nuvem
        self.y_pos_cloud = random.randint(50, 100)  # Posição vertical inicial da nuvem

    def update(self, game_speed):
        self.x_pos_cloud -= game_speed  # Atualiza a posição horizontal da nuvem com base na velocidade do jogo
        if self.x_pos_cloud < -self.image_whidth: # Verifica se a nuvem passou completamente para fora da tela
            self.x_pos_cloud = SCREEN_WIDTH + random.randint(250, 300) # Reinicia a posição horizontal da nuvem para uma nova posição aleatória
            self.y_pos_cloud = random.randint(50,100) # Reinicia a posição vertical da nuvem para uma nova posição aleatória

    def draw(self, screen):
        screen.blit(self.image,(self.x_pos_cloud,self.y_pos_cloud))  # Desenha a nuvem na tela