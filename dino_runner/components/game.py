import pygame  

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosaur  
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

FONT_STYLE = "freesansbold.ttf"  


class Game:
    def __init__(self):
        pygame.init()  
        pygame.display.set_caption(TITLE) 
        pygame.display.set_icon(ICON)  
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()  
        self.playing = False  
        self.running = False  
        self.game_speed = 20  
        self.player = Dinosaur()
        self.x_pos_bg = 0  
        self.y_pos_bg = 380 
        self.score = 0 
        self.death_count = 0  
        self.obstacle_manager = ObstacleManager()  

    def execute(self):
        self.running = True  
        while self.running:  
            if not self.playing:
                self.show_menu()  

        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True  
        self.score = 0  # Reinicia a pontuação
        self.game_speed = 20  # Reinicia a velocidade do jogo
        while self.playing:  
            self.events()  
            self.update() 
            self.draw()  

    def events(self):
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                self.playing = False  
                self.running = False  

    def update(self):
        user_input = pygame.key.get_pressed()  
        self.player.update(user_input)  
        self.obstacle_manager.update(self) 
        self.update_score()  

    def update_score(self):
        self.score += 1  
        if self.score % 100 == 0:  
            self.game_speed += 3  

    def draw_text(self, texto, x_pos, y_pos):  # draw_text
        font = pygame.font.Font(FONT_STYLE, 22) # Cria um objeto de fonte
        text = font.render(texto, True, (0, 0, 0))  
        text_rect = text.get_rect() 
        text_rect.center = (x_pos, y_pos)  
        self.screen.blit(text, text_rect) 

    def draw(self):
        self.clock.tick(FPS)  
        self.screen.fill((255, 255, 255))#'#FFFFFF' 
        self.draw_background()  
        self.player.draw(self.screen)  
        self.obstacle_manager.draw(self.screen)  
        self.draw_text(f"Score: {self.score}", 1000, 50)  # Desenha a pontuação na tela
        self.draw_text(f"Deaths: {self.death_count}", 850, 50)  # Desenha a contagem de mortes na tela
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

    def handle_events_on_menu(self):
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                self.playing = False 
                self.running = False  
            elif event.type == pygame.KEYDOWN:  
                self.run()  

    def show_menu(self):
        self.screen.fill((255, 255, 255)) 
        half_screen_height = SCREEN_HEIGHT // 2  # Calcula a metade da altura da tela
        half_screen_width = SCREEN_WIDTH // 2   # Calcula a metade da largura da tela

        if self.death_count == 0:  # Verifica se não houve mortes anteriores
            self.draw_text("Press any key to start", half_screen_width, half_screen_height)  # Desenha o texto do menu
        else:
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))  # Desenha o ícone do jogo no menu
            self.draw_text("Press any key to reset", half_screen_width, half_screen_height)  # Desenha o texto do menu
            self.draw_text(f"Score: {self.score}", 1000, 50)  # Desenha a pontuação no menu
            self.draw_text(f"Deaths: {self.death_count}", 850, 50)  # Desenha a contagem de mortes no menu

        pygame.display.flip()  

        self.handle_events_on_menu()  