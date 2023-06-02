
import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, RESET
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.cloud import Cloud # Importa a classe Cloud do arquivo cloud.py
from dino_runner.utils.text import FontEnum, draw_text # Importa o enum FontEnum e a função draw_text do arquivo text.py
sound_files = ['jump_sound.mp3', 'cutting_wood_sound.mp3', 'life_sound.mp3', "damage_sound.mp3"] # Lista de nomes de arquivos de som


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.sounds = [] # Lista para armazenar objetos Sound dos arquivos de som
        self.load_sounds() # Carrega os sons na lista
        self.cloud = Cloud() # Cria um objeto da classe Cloud
        self.best_score = 0 # Melhor pontuação do jogador

    def execute(self):  # Método que executa o menu do jogo
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):  # Método que executa o jogo
        self.playing = True
        self.power_up_manager.reset_power_ups()
        self.score = 0
        self.game_speed = 20 # Reinicia a pontuação
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def load_sounds(self): # Método para carregar os sons do jogo
        for file in sound_files:  # Percorre a lista de nomes de arquivo de som
            sound = pygame.mixer.Sound(file) # Carrega o som do arquivo
            sound.set_volume(0.2) # Define o volume do som
            self.sounds.append(sound)  # Adiciona o som à lista de sons

    def events(self): # Método para tratar os eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input, self)
        self.obstacle_manager.update(self) # Atualiza o estado dos obstáculos
        self.update_score()
        self.power_up_manager.update(self)  # Atualiza o estado dos power-ups
        self.cloud.update(self.game_speed) # Atualiza o estado das nuvens

    def best_score(self):  # Método para reiniciar a melhor pontuação
        return self.best_score # Reinicia a melhor pontuação
    
    def update_score(self):  # Método para atualizar a pontuação
        self.score += 1
        if self.score > self.best_score:
            self.best_score = self.score
        if self.score % 100 == 0:
            self.game_speed += 3
    
    def draw_power_up_time(self):  # Método para desenhar o tempo restante do power-up
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2) # Calcula o tempo restante em segundos

            if time_to_show >= 0: # Se o tempo restante for maior ou igual a 0
                draw_text(
                    self,f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",500, 40)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE  # Retorna ao tipo padrão

    def draw(self): # Método para desenhar os elementos na tela
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))  #FFFFFF
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        draw_text(self, f"Score: {self.score}", 1000, 50) # Desenha a pontuação na tela
        draw_text(self, f"Deaths: {self.death_count}", 850, 50)  # Desenha a contagem de mortes na tela
        draw_text(self, f"Best Score: {self.best_score}", 700, 50)  # Desenha a melhor pontuação na tela
        self.draw_power_up_time() # Desenha o tempo restante do power-up na tela
        self.cloud.draw(self.screen)  # Desenha as nuvens na tela
        self.power_up_manager.draw(self.screen) # Desenha os power-ups na tela
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def handle_events_on_menu(self):  # Método para tratar os eventos no menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self): # Método para exibir o menu
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))
            draw_text(self, "PRESS  ANY  KEY  TO  START", half_screen_width, half_screen_height, FontEnum.JURASSIC_FONT)
        else:
            self.screen.blit(RESET, (half_screen_width - 20, half_screen_height - 140))
            draw_text(self, "PRESS  ANY  KEY  TO  RESTART", half_screen_width, half_screen_height, FontEnum.JURASSIC_FONT)
            draw_text(self, f"Score: {self.score}", 1000, 50)
            draw_text(self, f"Deaths: {self.death_count}", 850, 50)
            draw_text(self, f"Best Score: {self.best_score}", 700, 50)

        pygame.display.flip()  

        self.handle_events_on_menu()