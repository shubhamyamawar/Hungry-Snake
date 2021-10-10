import pygame
from pygame.locals import *
import time
import random
SIZE=40

class Apple:
    def __init__(self,parent_screen):
        self.parent_screen=parent_screen
        self.block = pygame.image.load("resorces/apple.jpg").convert()
        self.x=SIZE*3
        self.y=SIZE*3
    def draw(self):
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 20) * SIZE
        self.y = random.randint(1, 19) * SIZE


class Snake:
    def __init__(self, parent_screen,length):
        self.parent_screen=parent_screen
        self.block = pygame.image.load("resorces/block.jpg").convert()
        self.length=length
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction="down"

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
          self.direction="left"
    def move_right(self):
          self.direction="right"
    def move_up(self):
          self.direction="up"
    def move_down(self):
          self.direction="down"

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction=="left":
            self.x[0]-=SIZE
        elif self.direction=="right":
            self.x[0]+= SIZE
        elif self.direction=="up":
            self.y[0]-=SIZE
        elif self.direction=="down":
            self.y[0]+=SIZE
        self.draw()
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 800))  # create game window
        self.Snake=Snake(self.surface,1)
        self.Snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()

    def render_background(self):
        bg = pygame.image.load("resorces/background.jpg")
        self.surface.blit(bg,(0, 0))
    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2+SIZE:
            if y1 >= y2 and y1 <y2 + SIZE:
                return True
        return False


    def reset(self):
        self.Snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
    def play_background_music(self):
        pygame.mixer.music.load("resorces/bg_music_1.mp3")
        pygame.mixer.music.play(-1,0)

    def play_sound(self,Sound):
        if Sound=="ding":
            Sound = pygame.mixer.Sound("resorces/1_snake_game_resources_ding.mp3")
        elif Sound=="crash":
            Sound = pygame.mixer.Sound("resorces/1_snake_game_resources_crash.mp3")


        pygame.mixer.Sound.play(Sound)
    def play(self):
        self.render_background()
        self.Snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        #Snake colliding with apple
        if self.is_collision(self.Snake.x[0],self.Snake.y[0],self.apple.x,self.apple.y):
                self.play_sound("ding")
                self.Snake.increase_length()
                self.apple.move()
        #Snake colliding with itself
        for i in range(2,self.Snake.length):
            if self.is_collision(self.Snake.x[0], self.Snake.y[0], self.Snake.x[i], self.Snake.y[i]):
                self.play_sound("crash")

                raise "Game Over"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.Snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (850, 10))
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your Score is {self.Snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter .To Exit Press Escape", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()
        pygame.mixer.music.pause()
    def run(self):

        running = True
        pause=False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: # when escape
                        running = False
                    if event.key==K_RETURN:
                        pygame.mixer.music.unpause()
                        pause=False
                    if not pause:
                        if event.key == K_LEFT:
                            self.Snake.move_left()
                        if event.key == K_RIGHT:
                            self.Snake.move_right()
                        if event.key == K_UP:
                            self.Snake.move_up()
                        if event.key == K_DOWN:
                            self.Snake.move_down()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()

                pause=True
                self.reset()


            time.sleep(0.2)
if __name__=="__main__":
    game= Game()
    game.run()

