import pygame
import time
import random
import sys
import asyncio

SCREEN_WIDTH: int = 260 * 3   # 780
SCREEN_HEIGHT: int = 260 * 2  # 520
IMAGES_PATH_BG = 'images/background/'
IMAGES_PATH_MENU = 'images/menu/'
FONT_PATH = 'fonts/'
FPS: int = 60
IMAGES_PATH = 'images/'
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Bullet:
    bullet = None

    def __init__(self, x: int, y: int):
        self.bullet = pygame.Surface((3, 5))
        self.bullet.fill((0, 0, 50))
        self.rect = self.bullet.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.speed = 3

    def move(self):
        self.rect.y -= self.speed

    def draw(self):
        screen.blit(self.bullet,self.rect)
class Bullets:
    bullet_list: list = []

    def add(self, x: int, y: int):
        self.bullet_list.append(Bullet(x, y))

    def move(self):
        for b in self.bullet_list:
            b.move()
            if b.rect.y < 0:
                self.bullet_list.remove(b)
            b.draw()

class Player:
    moving: list = []
    dt = 1
    bullets = None

    def __init__(self):
        n = random.randint(1, 8)
        self.image = pygame.image.load(IMAGES_PATH + f'Ship{n}.png')
        self.x = int(SCREEN_WIDTH / 2)
        self.y = SCREEN_HEIGHT - (self.image.get_height() + 10)
        self.speed = 7

        self.bullets = Bullets()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if len(self.moving) > 0:
            if self.moving[0] == pygame.K_LEFT:
                self.move_left()
            elif self.moving[0] == pygame.K_RIGHT:
                self.move_right()

        self.bullets.move()

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
        else:
            self.x = 0

    def move_right(self):
        if self.x < SCREEN_WIDTH - self.image.get_width():
            self.x += self.speed
        else:
            self.x = SCREEN_WIDTH - self.image.get_width()

    def shoot(self):
        self.bullets.add(self.x, self.y)

class AnimationExplosion:
    def __init__(self, x, y):
        self.index = 0
        self.frames = []
        img = pygame.image.load(IMAGES_PATH + 'explosion.png')
        for i in range(-10, 10):
            k = 5 * (10 - abs(i) + 1)
            im = pygame.transform.scale(img, (k, k))
            self.frames.append(im)

        self.x = x
        self.y = y
        self.end_animation = False

    def animation(self):
        self.index += 1
        if self.index >= len(self.frames):
            self.end_animation = True
            self.index = 0

        screen.blit(self.frames[self.index], (self.x, self.y))
class Background:
     image = None

     def __init__(self):
         self.bg_x: int = 0
         self.bg_y: int = -SCREEN_HEIGHT
         self.bg_y_speed: float = 0.2
         self.bg_y_pos = self.bg_y
         self.bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 2))
         self.interval = time.time()
         self.dt = 1

         self.add()

     def add(self):
         self.image = pygame.image.load(IMAGES_PATH_BG + 'bg02.png')

         nx = int(SCREEN_WIDTH / self.image.get_width())
         ny = int(SCREEN_HEIGHT / self.image.get_height())
         w = self.image.get_width()
         h = self.image.get_height()

         for x in range(nx):
             for y in range(ny * 2):
                 self.bg_surface.blit(self.image, (w * x, h * y))

     def draw(self):
         self.bg_y_pos += self.bg_y_speed
         self.bg_y = int(self.bg_y_pos)

         if self.bg_y >= 0:
             self.bg_y = -SCREEN_HEIGHT
             self.bg_y_pos = self.bg_y

         screen.blit(self.bg_surface, (self.bg_x, self.bg_y))


class Menu:
    def __init__(self):
        bg_img = pygame.image.load(IMAGES_PATH_MENU + 'bg-02.jpg')
        self.bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        box_img = pygame.image.load(IMAGES_PATH_MENU + 'm_01.png')
        self.box_img = pygame.transform.scale(box_img, (300, 300))
    def start_btn(self):
        color = (0,0,0)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if self.start_pos():
            color = (255,255,255)
        font = pygame.font.SysFont(FONT_PATH + 'Calibri', 40)
        text = font.render('START', True, color)
        screen.blit(text, (130, 100))

    def draw(self):
        screen.blit(self.bg_img, (0, 0))
        screen.blit(self.box_img, (20, 20))
        self.start_btn()

    def start_pos(self):
        pos = pygame.mouse.get_pos()  # (x, y)
        print(pos)
        if ((pos[0] > 130 and pos[0] < 220) and (pos[1] > 100 and pos[1] < 130)):
            return True

        return False

    def click_mouse(self):
        btn = pygame.mouse.get_pressed()  # (False, False, False)

        if btn[0] and self.start_pos():
            return 'run'

        return None

# class Enemy:
#     x: int = 0
#     y: int = 0
#     speed: int = 0
#     image = None
#
#     def add(self):
#         pass
#
#     def move(self):
#         pass
#
#     def fire(self):
#         pass

enemies_group = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        n = random.randint(1,7)
        self.image = pygame.image.load(IMAGES_PATH + f'Ship{n}.png')
        self.image = pygame.transform.rotate(self.image, 180)
        x, y = random.randint(50, SCREEN_WIDTH-50), random.randint(-100, -50)
        self.rect =self.image.get_rect(center=(x,y))

        self.speed = random.randint(50,120)
    def update(self, dt):
        self.rect.centery += 2  # self.speed * dt

        if self.rect.centery > SCREEN_HEIGHT - 100:
            self.kill()
class Game:
    bg_game = None
    game_run: bool = False

    def __init__(self):
        self.interval = time.time()
        self.dt = 1
        self.menu = Menu()
        self.bg = Background()
        self.player = Player()

        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, random.randint(1500, 3000))

        self.collisions_explosion = []
    def delta_time(self):
        clock.tick(FPS)
        self.dt = time.time() - self.interval
        self.interval = time.time()

        self.player.dt = self.dt

    def collisions(self):
        for b in self.player.bullets.bullet_list:
            for e in enemies_group:
                if pygame.sprite.collide_rect(b, e):
                    self.collisions_explosion.append(AnimationExplosion(e.rect.x, e.rect.y))
                    self.player.bullets.bullet_list.remove(b)
                    e.kill()

        for e in self.collisions_explosion:
            e.animation()
            if e.end_animation:
                self.collisions_explosion.remove(e)

    async def init(self):
        while True:
            if self.game_run:
                self.run()
            else:
                self.main_menu()

            pygame.display.update()
            await asyncio.sleep(0)
    def main_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.game_run = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu.click_mouse() == 'run':
                    self.run()

        self.menu.draw()

    def run(self):
        self.delta_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if event.key not in self.player.moving:
                        self.player.moving.append(event.key)
                elif event.key == pygame.K_SPACE:
                    self.player.shoot()
                elif event.key == pygame.K_q:
                    self.game_run = False
                    break
            elif event.type == pygame.KEYUP:
                if event.key in self.player.moving:
                    self.player.moving.remove(event.key)
            elif event.type == self.enemy_event:
                Enemy(enemies_group)
        # ---
        if self.game_run:
            self.bg.draw()
            self.player.move()
            self.player.draw()
            self.delta_time()
            enemies_group.update(self.dt)
            self.collisions()
            enemies_group.draw(screen)

if __name__ == '__main__':
    game = Game()
    asyncio.run(game.init())


