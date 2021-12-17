import pygame
import math
import sys
import random
pygame.init()

def blit_rotate_centre(win, image, top_left, angle):
    """Функция, которая отвечаем за поворот машин"""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center = image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)

background = pygame.image.load("background2.png")
font = pygame.font.Font("NFS_by_JLTV.ttf",30)
font1 = pygame.font.Font("NFS_by_JLTV.ttf",50)
pygame.mixer.music.load('kaito-shoma-gaz.mp3')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
menuwin=pygame.image.load("menu.png")
win_font = font.render('PRESS SPACE TO RESTART ',1,(0,0,0))
restart_font1 = font1.render('GAME PAUSED ',1,(0,0,0))
restart_font2 = font.render('PRESS ENTER to continue',1,(0,0,0))
restart_font3 = font.render('PRESS space to restart',1,(0,0,0))
pausegame = font.render('PAUSE ',1,(0,0,0))
boardroad = pygame.image.load("boardroad2.png")
boardroad_mask = pygame.mask.from_surface(boardroad)
finish = pygame.image.load("finish2.png")
finish_mask = pygame.mask.from_surface(finish)
finish_pos = (26,446)
greencar = pygame.image.load("car2.png")
bluecar = pygame.image.load("car1.png")
speed1 = random.randint(1,5)
speed2 = random.randint(1,5)
width, height = boardroad.get_width(), boardroad.get_height()
win = pygame.display.set_mode((width , height))
pygame.display.set_caption("nfs")
FPS = 60

def pausegame():
    """Функция, которая ставит паузу."""
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            win.blit(restart_font1, (455, 350))
            win.blit(restart_font2, (840, 650))
            win.blit(restart_font3, (830, 680))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        if keys[pygame.K_SPACE]:
            paused = False
            player_car.reset()
            player_car2.reset()
        pygame.display.update()
        clock.tick(15)
def finishgame():
    """Функция, которая перезапускает игру на финише."""
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            win.blit(win_font, (830, 680))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                paused = False
            pygame.display.update()
            clock.tick(15)
class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.img
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.start
        self.acceleration = 0.1
    def rotate(self, left=False, right=False):
        """Функция, которая отвечает за поворот машин"""
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
    def draw(self, win):
        """Функция, которая рисует машины"""
        blit_rotate_centre(win, self.img, (self.x, self.y), self.angle)
    def move_forward(self):
        """Функция, которая движение вперед"""
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    def move_backward(self):
        """Функция, которая движение назад"""
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    def move(self):

        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal
    def collide(self,mask , x=0, y=0 ):
        """Функция, которая отвечает за коллизию"""
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x),int( self.y - y))
        poi = mask.overlap(car_mask,offset)
        return poi
    def reset(self):
        """Функция, которая отвечает за перезапуск"""
        self.x, self.y = self.start
        self.angle = 0
        self.vel = 0
class PlayerCar1(AbstractCar):

    img = bluecar
    start = (35,400)

    def reduce_speed(self):
        """Функция, которая задмедляет скорость при остановке"""
        self.vel = max(self.vel - self.acceleration / 1.5, 0)
        self.move()
    def bounce(self):
        """Функция, которая отвечает за отталкивание от бортов"""
        self.vel = -self.vel
        self.move()
class PlayerCar2(AbstractCar):
    img = greencar
    start =(60,400)
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 1.5, 0)
        self.move()
    def bounce(self):
        self.vel = -self.vel
        self.move()

def draw(win, images, player_car,player_car2):
    """Функция, которая рисует машины на экране"""
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    player_car2.draw(win)
    pygame.display.update()
def move_player(player_car):
    """Функция, которая отвечаем за передвижение  первого игрока"""
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

def move_player2(player_car2):
    """Функция, которая отвечаем за передвежение  второго игрока"""
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        player_car2.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car2.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_car2.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car2.move_backward()
    if not moved:
        player_car2.reduce_speed()

def menu():
    """Функция, которая создает меню перед игрой"""
    pygame.mixer.music.play()
    run_menu = True
    while run_menu:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)

        win.blit(menuwin, (0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            gamestart()
            sys.exit(1)
        else:
            if keys[pygame.K_ESCAPE]:
                sys.exit(1)
        pygame.display.update()
        clock.tick(60)

run = True
clock = pygame.time.Clock()
images = [(background, (0, 0)),(finish,finish_pos)]
player_car = PlayerCar1(speed1, speed1)
player_car2 = PlayerCar2(speed2, speed2)
def gamestart():
    """Функция, которая запускает игру"""
    run = True
    while run:
        clock.tick(FPS)
        draw(win, images, player_car,player_car2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =False
        pygame.display.update()
        move_player(player_car)
        move_player2(player_car2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pausegame()
        if player_car.collide(boardroad_mask) != None:
            player_car.bounce()
        finish_poi_collide = player_car.collide(finish_mask, *finish_pos)
        if finish_poi_collide !=None:
            if finish_poi_collide[1]==0:
                player_car.bounce()
            else:
                finishgame()
                player_car.reset()
                player_car2.reset()
        if player_car2.collide(boardroad_mask) != None:
            player_car2.bounce()
        finish_poi_collide = player_car2.collide(finish_mask, *finish_pos)
        if finish_poi_collide !=None:
            if finish_poi_collide[1]==0:
                player_car2.bounce()
            else:
                finishgame()
                player_car.reset()
                player_car2.reset()
if __name__ == "__main__":
    menu()
    pygame.QUIT()