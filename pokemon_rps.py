import pygame, sys
import random
from pathlib import Path

from pygame.constants import KEYDOWN

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "assets" / "images"
AUDIO_DIR = BASE_DIR / "assets" / "audio"

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()
 
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

DISPLAYSURF = pygame.display.set_mode((400,500))
bg = pygame.image.load(IMAGES_DIR / "grass.png")
bg = pygame.transform.scale(bg, (400, 500))
DISPLAYSURF.blit(bg, (0,0))

pygame.display.set_caption("Pokemon Rock Paper Scissors")
 
class Text_Overlay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #convert_alpha gets rid of the black background of the image
        self.player_win = pygame.image.load(IMAGES_DIR / "win.png").convert_alpha()
        self.player_win = pygame.transform.scale(self.player_win, (250, 100))

        self.ai_win = pygame.image.load(IMAGES_DIR / "AI_win.png").convert_alpha()
        self.ai_win = pygame.transform.scale(self.ai_win, (250, 100))

        self.start = pygame.image.load(IMAGES_DIR / "start.png").convert_alpha()
        self.start = pygame.transform.scale(self.start, (250, 100))

        self.draw = pygame.image.load(IMAGES_DIR / "draw.png").convert_alpha()
        self.draw = pygame.transform.scale(self.draw, (250, 100))

        self.restart = pygame.image.load(IMAGES_DIR / "restart.png").convert_alpha()
        self.restart = pygame.transform.scale(self.restart, (370, 85))
        
        self.player_win_rect = self.player_win.get_rect(topleft =(75, 180))
        self.ai_win_rect = self.ai_win.get_rect(topleft =(75,180))
        self.start_rect = self.start.get_rect(topleft =(75, 180))
        self.draw_rect = self.draw.get_rect(topleft=(75, 180))
        self.restart_rect = self.restart.get_rect(topleft =(15, 180))

    def draw_player_win(self, surface):
        surface.blit(self.player_win, self.player_win_rect)

    def draw_AI_win(self, surface):
        surface.blit(self.ai_win, self.ai_win_rect)

    def draw_start(self, surface):
        surface.blit(self.start, self.start_rect)

    def draw_draw(self, surface):
        surface.blit(self.draw, self.draw_rect)

    def remove_start(self):
        self.start.fill(TRANSPARENT)
    
    def remove_p_win(self):
        self.player_win.fill(TRANSPARENT)

    def remove_ai_win(self):
        self.ai_win.fill(TRANSPARENT)

    def remove_draw(self):
        self.draw.fill(TRANSPARENT)

    def draw_restart(self, surface):
        surface.blit(self.restart, self.restart_rect)                    
           

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        #load character sprites
        #Blatt
        self.image1 = pygame.image.load(IMAGES_DIR / "bulbasaur_front.png").convert()
        #Feuer
        self.image2 = pygame.image.load(IMAGES_DIR / "charmander_front.png").convert()
        #Wasser
        self.image3 = pygame.image.load(IMAGES_DIR / "squirtle_front.png").convert()  
        #trainer
        self.trainer = pygame.image.load(IMAGES_DIR / "bugsy.png").convert()
        #set inital positions 
        self.rect1 = self.image1.get_rect(topleft=(210, 50))
        self.rect2 = self.image2.get_rect(topleft=(240, 50))
        self.rect3 = self.image3.get_rect(topleft=(270, 50))
        self.rect_trainer = self.trainer.get_rect(topleft=(250, 30))
        
      #show the Pokemon on screen
      def draw(self, surface):
        surface.blit(self.trainer, self.rect_trainer)
        surface.blit(self.image1, self.rect1) 
        surface.blit(self.image2, self.rect2) 
        surface.blit(self.image3, self.rect3) 
        
    # move Grass Pokemon
      def move1(self, surface):  
          self.rect1 = self.image1.get_rect(topleft=(200, 150))
          surface.blit(self.image1, (200, 150))
    # move Fire Pokemon
      def move2(self, surface):
          self.rect2 = self.image2.get_rect(topleft=(200, 150))
          surface.blit(self.image2, (200, 150))
    # move Water Pokemon
      def move3(self, surface):
          self.rect3 = self.image3.get_rect(topleft=(200, 150))
          surface.blit(self.image3, (200, 150))

     # Enemy play method    
      def enemy_play(self, surface, enemy_choice):
         if enemy_choice == 1:
            self.move1(surface)
         elif enemy_choice == 2:
            self.move2(surface)
         else:
            self.move3(surface)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        #Blatt
        self.image1 = pygame.image.load(IMAGES_DIR / "bulbasaur_back.png").convert()
        #Feuer
        self.image2 = pygame.image.load(IMAGES_DIR / "charmander_back.png").convert()
        #Wasser
        self.image3 = pygame.image.load(IMAGES_DIR / "squirtle_back.png").convert()
        #set inital positions 
        self.rect1 = self.image1.get_rect()
        self.rect1.center = (75, 370)

        self.rect2 = self.image2.get_rect()
        self.rect2.center = (135, 370)

        self.rect3 = self.image3.get_rect()
        self.rect3.center = (195, 370)
        
    #show the Pokemon on screen
    def draw(self, surface):
        surface.blit(self.image1, self.rect1) 
        surface.blit(self.image2, self.rect2) 
        surface.blit(self.image3, self.rect3) 
    # move Grass Pokemon
    def move1(self):
          self.rect1 = self.image1.get_rect(bottomright=(180, 340))
    # move Fire Pokemon    
    def move2(self):
          self.rect2 = self.image2.get_rect(bottomright=(180, 340))
    # move Water Pokemon
    def move3(self):
          self.rect3 = self.image3.get_rect(bottomright=(180, 340))

pygame.mixer.init()
file_start = AUDIO_DIR / 'battle_start.mp3'
music_start = pygame.mixer.music.load(file_start)
def start_music():
    music_start
    pygame.mixer.music.play(-1)

def stop():
    pygame.mixer.music.stop()

def unload():
    pygame.mixer.music.unload()



def main():
    P1 = Player()
    E1 = Enemy()
    T1 = Text_Overlay()
    enemy_choice = random.randint(1, 3)
    player_choice = 0
    start_screen = True
    end_screen = False
    restart_screen = False
    WAIT_TIME = 3.5
    timer = 0
    elapsed = FramePerSec.tick(FPS)
    start_music()
    while True:     
        for event in pygame.event.get(): 
            #Player choice
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and P1.rect1.collidepoint(event.pos):
                    P1.move1()
                    player_choice = 1
                    E1.enemy_play(DISPLAYSURF, enemy_choice)  
                    end_screen = True
                elif event.button == 1 and P1.rect2.collidepoint(event.pos):
                    P1.move2()
                    player_choice = 2
                    E1.enemy_play(DISPLAYSURF, enemy_choice)
                    end_screen = True
                elif event.button == 1 and P1.rect3.collidepoint(event.pos):
                    P1.move3() 
                    player_choice = 3
                    E1.enemy_play(DISPLAYSURF, enemy_choice)  
                    end_screen = True       
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #restart the game
            if event.type == KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
    
        DISPLAYSURF.blit(bg, (0, 0))
        P1.draw(DISPLAYSURF)
        E1.draw(DISPLAYSURF)
        #shows the game start image in the beginning, for a specific amount of time
        if start_screen:
                T1.draw_start(DISPLAYSURF)
                timer = timer + elapsed/1000
                elapsed = FramePerSec.tick(FPS)
                if timer > 2:
                    start_screen = False
                    

        if end_screen:
            timer = timer + elapsed/1000
            elapsed = FramePerSec.tick(FPS)
            if timer > 2.5:
                if player_choice == 1:
                    if enemy_choice == 1:
                        T1.draw_draw(DISPLAYSURF)
                        timer = timer + elapsed/1000
                        elapsed = FramePerSec.tick(FPS)
                        if timer > WAIT_TIME:
                            T1.remove_draw()
                            restart_screen = True
                    elif enemy_choice == 2:
                        T1.draw_AI_win(DISPLAYSURF)
                        timer = timer + elapsed/1000
                        elapsed = FramePerSec.tick(FPS)
                        if timer > WAIT_TIME:
                            T1.remove_ai_win()
                            restart_screen = True
                    elif enemy_choice == 3:
                        T1.draw_player_win(DISPLAYSURF)
                        timer = timer + elapsed/1000
                        elapsed = FramePerSec.tick(FPS)
                        if timer > WAIT_TIME:
                            T1.remove_p_win()
                            restart_screen = True

                elif player_choice == 2:
                    if enemy_choice == 1:
                        T1.draw_player_win(DISPLAYSURF)
                        timer = timer + elapsed/1000
                        elapsed = FramePerSec.tick(FPS)
                        if timer > WAIT_TIME:
                            T1.remove_p_win()
                            restart_screen = True
                    elif enemy_choice == 2:
                        T1.draw_draw(DISPLAYSURF)
                        timer = timer + elapsed/1000
                        elapsed = FramePerSec.tick(FPS)
                        if timer > WAIT_TIME:
                            T1.remove_draw()
                            restart_screen = True
                    elif enemy_choice == 3:
                        T1.draw_AI_win(DISPLAYSURF)
                        timer = timer + elapsed/1000
                        elapsed = FramePerSec.tick(FPS)
                        if timer > WAIT_TIME:
                            T1.remove_ai_win()
                            restart_screen = True

                elif player_choice == 3:
                    if enemy_choice == 1:
                        T1.draw_AI_win(DISPLAYSURF)
                        timer = timer + elapsed/1000
                        elapsed = FramePerSec.tick(FPS)
                        if timer > WAIT_TIME:
                            T1.remove_ai_win()
                            restart_screen = True
                    elif enemy_choice == 2:
                        T1.draw_player_win(DISPLAYSURF)
                        timer = timer + elapsed/1000
                        elapsed = FramePerSec.tick(FPS)
                        if timer > WAIT_TIME:
                            T1.remove_p_win()
                            restart_screen = True
                    elif enemy_choice == 3:
                        T1.draw_draw(DISPLAYSURF)
                        timer = timer + elapsed/1000
                        elapsed = FramePerSec.tick(FPS)
                        if timer > WAIT_TIME:
                            T1.remove_draw()
                            restart_screen = True

        if restart_screen:
            timer = timer + elapsed/1000
            elapsed = FramePerSec.tick(FPS)
            if timer > 5:
                T1.draw_restart(DISPLAYSURF)
            
        pygame.display.flip()
        FramePerSec.tick(FPS)

main()