import pygame
from pygame.locals import *
import random
from pygame import mixer


pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy birb")

#define font
font = pygame.font.SysFont("arialblack", 50)
font1 = pygame.font.SysFont("arialblack", 30)

#define colours
white = (255, 255, 255)
cyan = (0, 255, 255)
black = (0, 0, 0)


#gamw variables
scroll = 0
scroll_rate = 4
flying  = False
game_over = False
pipe_gap = 160
pipe_frequency = 1500  #miliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pipe_passed = False
# C:\Users\Navneet\Desktop\Master\VSCODE\python\flappy_bird_game_files\assets\images

#load images
back = pygame.image.load("C:\\Users\\Navneet\\Desktop\\Master\\VSCODE\\python\\flappy_bird_game_files\\assets\\images\\vapor.jpg")
ground = pygame.image.load("C:\\Users\\Navneet\\Desktop\\Master\\VSCODE\\python\\flappy_bird_game_files\\assets\\images\\ground.png")
restart = pygame.image.load("C:\\Users\\Navneet\\Desktop\\Master\\VSCODE\\python\\flappy_bird_game_files\\assets\\images\\restart.png")
restart = pygame.transform.scale(restart, (250, 100))

#load sounds
mixer.music.load("C:\\Users\\Navneet\\Desktop\\Master\\VSCODE\\python\\flappy_bird_game_files\\assets\\sounds\\Aqua Braincell Bgm.wav")
mixer.music.set_volume(0.7)
mixer.music.play(-1, 0.0, 5000)

jumping = pygame.mixer.Sound("C:\\Users\\Navneet\\Desktop\\Master\\VSCODE\\python\\flappy_bird_game_files\\assets\\sounds\\fireInTheHole.wav")
jumping.set_volume(0.5)
death = pygame.mixer.Sound("C:\\Users\\Navneet\\Desktop\\Master\\VSCODE\\python\\flappy_bird_game_files\\assets\\sounds\\death3.wav")
death.set_volume(0.2)


#text on display
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    bird.rect.x = 100
    bird.rect.y = int(screen_height / 2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self , x , y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f"C:\\Users\\Navneet\\Desktop\\Master\\VSCODE\\python\\flappy_bird_game_files\\assets\\images\\bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.jumped = False
        self.mid_air = False
        self.clicked = False


    def update(self):

        if flying == True:
        #acceleration and gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom  < 650:
                self.rect.y += int(self.vel)

        if game_over == False:    
            #jump
            self.mid_air = True
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.mid_air == True:  #so that the character dossnt keep jumping up on holding space
                    jumping.play()
                    self.vel = -10
                    self.jumped = True
            if key[pygame.K_SPACE] == False:
                    self.jumped = False
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False   


            #handle animation
            self.counter += 1
            wings_cooldown = 5

            if self.counter > wings_cooldown:
                self.counter = 0
                self.index += 1
                self.index = self.index % len(self.images)
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        #position = 1 from the top ; position = -1 from the bottom
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\Navneet\\Desktop\\Master\\VSCODE\\python\\flappy_bird_game_files\\assets\\images\\redpipe1.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap // 2)]
        if position == -1:       
            self.rect.topleft = [x , y + int(pipe_gap // 2)]

    def update(self):
        self.rect.x -= scroll_rate
        if self.rect.right < 0:  #kills the memory taken up  by the pipes that go all the way to left 
            self.kill()

class Button:
    def __init__(self, x, y, image):
        self.image = image
        # image = pygame.transform.scale(self.image, (screen_width // 2 // 2 , screen_height // 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def draw(self):

        action = False 

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is on button or not
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draws the restart button
        draw_text(f"YOU DIED! SCORE: {score}", font1, cyan, (screen_width / 2 / 2) + 30, 400)
        #play sound here#
        screen.blit(self.image , (self.rect.x, self.rect.y))

        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


bird = Bird(100, int(screen_height // 2))

bird_group.add(bird)

button = Button(screen_width // 2 - 130, screen_height // 2 - 100, restart)

################################################################ MAIN WHILE LOOP ##########################################################################
run = True
while run:

     clock.tick(fps)
     
     #backgorund
     screen.blit(back, (0,-115))

     bird_group.draw(screen)
     bird_group.update()
     pipe_group.draw(screen)
    

     #create ground
     screen.blit(ground, (scroll , 650))

     #checking score 
     #first we check if there is something in the pipe group
     if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
           and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pipe_passed == False:
             #we are trying to check whether the bird is inside the central zone of the pipe or not
           pipe_passed = True
        if pipe_passed == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:  #the bird has exited the pipe
                score += 1
                pipe_passed = False
                

     draw_text(f"{score}", font, white, (screen_width / 2) - 20, 20)

     
     #check for collision
     if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird.rect.top < 0:
        game_over = True

     #check if bird has hit the ground
     if bird.rect.bottom > 650:
        #play sound here#
        game_over = True
        flying = False
    

     #scrolling the ground
     if game_over == False and flying == True:
        #generate more pipes
        time_now = pygame.time.get_ticks() 
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(screen_width, int(screen_height // 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height // 2) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now



        scroll -= scroll_rate
        if abs(scroll) > 30:
            scroll = 0

        pipe_group.update()

    #check for game over and resets
     if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()


     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying  == False and game_over == False:
            flying = True
        
     pygame.display.update()

pygame.quit()

