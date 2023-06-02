import pygame
from enum import Enum

class FontEnum(Enum): # Define uma enumeração para as diferentes fontes de texto
    DEFAULT_FONT = ("freesansbold.ttf", 22) # Fonte padrão
    JURASSIC_FONT = ("./jurassic_park.ttf", 60)  # Fonte personalizada


def draw_text(game, texto, x_pos, y_pos, font: FontEnum = FontEnum.DEFAULT_FONT):
        font = pygame.font.Font(font.value[0], font.value[1]) # Cria um objeto de fonte com base na fonte especificada
        text = font.render(texto, True, (0, 0, 0)) # Renderiza o texto usando a fonte especificada e a cor preta
        text_rect = text.get_rect()
        text_rect.center = (x_pos, y_pos)
        game.screen.blit (text, text_rect)  # Desenha o texto renderizado na tela do jogo