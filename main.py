import pygame #adding pygame library
import os
import random #adding random generator library
pygame.init() #initializing pygame

# Global Constants of the Game Window
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #ойын терезесәне мән беру

#ойынға қажетті суреттерді байланыстыру
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur: #создаем класс для Динозавра и даем координаты
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self): #создаем функцию для стартового положения динозавра
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.duck_img = DUCKING

        self.dino_duck = False #значения 3-х движений
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel=self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput): #создаем функцию, которая будет отвественна для
                                 #реакции динозавра на те или иные нажатия клавитуры
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump: #даем условие: если нажимается кнопка "ВВЕРХ",
                                                          #то динозавр прыгает
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True

        elif userInput[pygame.K_DOWN] and not self.dino_jump: #даем условие иначе: если нажимается кнопка "Вниз",
                                                              #то динозавр нагибается
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False

        elif not (self.dino_jump or userInput[pygame.K_DOWN]): #даем условие иначе не ровно: если нажимается кнопка "Вниз",
                                                              #то динозавр продолжает бегать
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self): #создаем фунцию для времени когда динозавр нагибается
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self): #создаем фунцию для времени когда динозавр бежит
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self): #создаем фунцию для времени когда динозавр прыгает и даем условии,
                    # чтобы не позволить динозавру провалиться за рамки экрана во время прыжка
        self.image=self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel<-self.JUMP_VEL:
            self.dino_jump=False
            self.jump_vel=self.JUMP_VEL


    def draw(self, SCREEN): #создаем фунцию для иллюстрации анимации
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud: #создаем класс для Облака
    def __init__(self): #создаем фунцию для стартового положения координаты облаки
        self.x=SCREEN_WIDTH+random.randint(800, 1000)
        self.y=random.randint(50, 100)
        self.image=CLOUD
        self.width=self.image.get_width()

    def update(self): #создаем фунцию для того, чтобы облако обновлял свой выход
        #и используем для этого библиотеку генерацию рандома
        self.x-=game_speed
        if self.x<-self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)


    def draw(self, SCREEN): #создаем функию для иллюстрации
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle: #создаем класс для объектов которые будут взаимодействовать с дино
    def __init__(self, image, type): #создаем фунцию для стартового положения и объявляем
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self): #создаем фунцию для обновления выхода фигур и увелечения их скорости со временем
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN): #создаем фунцию для иллюстрации
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle): #создаем отдельный класс для Маленького Кактуса
    def __init__(self, image): #создаем фунцию для стартового положения и объявляем
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle): #создаем отдельный класс для Большого Кактуса
    def __init__(self, image): #создаем фунцию для стартового положения и объявляем
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y=300

class Bird(Obstacle): #создаем отдельный класс для Птицы
    def __init__(self, image): #создаем фунцию для стартового положения и объявляем
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 260
        self.index = 0

    def draw(self, SCREEN): #создаем фунцию для иллюстрации и анимации
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def main(): #создаем функцию для основного цикла игры и меню
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles #даем значения
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud=Cloud()
    game_speed=14
    x_pos_bg=0 #бэкграундтың координаталары
    y_pos_bg=380
    points=0 #ұпай санына алғашқы 0 деген мән береміз
    font=pygame.font.Font('freesansbold.ttf', 20) #стиль и шрифт текста
    obstacles=[]
    death_count=0 #ұтылыс санына алғашқы 0 деген мән береміз

    def score(): #создаем функию для баллов
        global points, game_speed
        points+=1
        if points %100==0: #баллдар артқан сайын жылдамдық та артады
            game_speed+=1

        text=font.render("Points: "+str(points), True, (0,0,0)) #тексттің шрифті, стилі және тұрақты тұ  ратын орнының координаталары
        textRect=text.get_rect()
        textRect.center=(1000, 40)
        SCREEN.blit(text, textRect)

    def background(): #создаем функию для бэкграунда
        global x_pos_bg, y_pos_bg
        image_width=BG.get_width() #даем значение
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg)) #иллюстрируем
        SCREEN.blit(BG, (image_width+x_pos_bg, y_pos_bg)) # и тут тоже
        if x_pos_bg<=-image_width: #даем условие движения
            SCREEN.blit(BG, (image_width+x_pos_bg, y_pos_bg))
            x_pos_bg=0
        x_pos_bg-=game_speed


    while run: #цикл для бега Динозавра
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN) #взаимодействие с игроком при итераций с клавиаратурой и усвоить значение
        player.update(userInput)

        if len(obstacles) == 0: #даем условие и действие для рандомного выходы объектов
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect (obstacle.rect): #даем условие при столкновения какого-либо объекта и дино
                #и если условие выполняетя, то останавливаем игру на 2 секунды, чтобы игрок смог увидеть
                #плюс прибавляем 1 к счетчику проигрышей
                pygame.time.delay(2000)
                death_count+=1
                menu(death_count)



        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count): #дополнительная функция для меню
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0: #стартовая иллюстрация экрана где будут выявлены такие данные и интрукция
            text = font.render("Press any Key to Start", True, (0, 0, 0)) #это для самого начала, где счетсик проигрыша равен 0
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0)) # а тут уже счетчик не равен 0, поэтому выводится РЭСТАРТ
            score = font.render("Your Score: " + str(points), True, (0, 0, 0)) #и баллы, которые игрок набрал
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #  condition when game stopd
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)









