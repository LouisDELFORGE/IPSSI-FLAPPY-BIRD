import pygame
from random import randint

pygame.init()
screen = pygame.display.set_mode((500,850))
clock = pygame.time.Clock()
running = True
paused = False
dt = 0

font = pygame.font.init()
used_font = pygame.font.SysFont('Comic Sans',60)
text_sf = used_font.render('0',True, (255,255,255))


playerObject = None
pipeElements = []

class pipes:
    # screen.get_width() - 50
    position = 0
    upPipeSize = 0
    gapSize = 0
    speed = 0
    hasCloned = None
    removing = False
    rect = pygame.Rect(0,0,0,0)
    rect1 = pygame.Rect(0,0,0,0)

    def pipeDraw(self):
        self.rect = pygame.Rect(self.position,0,40,self.upPipeSize)
        self.rect1 = pygame.Rect(self.position,self.upPipeSize + self.gapSize,40,screen.get_height())
        pygame.draw.rect(screen,(0,255,0),(self.position,0,40,self.upPipeSize))
        pygame.draw.rect(screen,(0,255,0),(self.position,self.upPipeSize + self.gapSize,40,screen.get_height()))

    def __init__(self):
        self.position = screen.get_width()
        self.gapSize = 175
        self.upPipeSize = randint(0,screen.get_height() - self.gapSize)
        self.speed = 150
        self.hasCloned = False
        

        pipeElements.append(self)

    def pipeLogic(self):
        global paused
        if paused:
            return
        self.position -= self.speed * dt
        if (self.position <= 0 - 40):
            removing = True
        if (self.position <= screen.get_width() / 4 and self.hasCloned == False):
            self.hasCloned = True
            pipes()
        if self.rect.colliderect(playerObject.rect) or self.rect1.colliderect(playerObject.rect):
            paused = True

class player:
    #size = [0,0]
    position = {"x" : 0, "y" : 0}
    velocity = {"x" : 0, "y" : 0}
    rect = pygame.Rect(0,0,0,0)
    def playerDraw(self):
        self.rect = pygame.Rect(self.position["x"],self.position["y"],30,30)
        pygame.draw.rect(screen,(255,0,0),(self.position["x"],self.position["y"],30,30))
    def physics(self):
        if paused:
            self.velocity["x"] = 0
            self.velocity["y"] = 0
            return
        if self.position["y"] > screen.get_height():
            self.position["y"] = 0
        elif self.position["y"] < -10:
                self.position["y"] = screen.get_height()
        self.position["x"] -= self.velocity["x"]
        self.position["y"] -= self.velocity["y"]
    def __init__(self):
        self.rect = pygame.Rect(self.position["x"],self.position["y"],30,30)
        self.position["x"] = 20
        self.position["y"] = screen.get_height() / 2


def updateText(text):
    global text_sf
    text_sf = used_font.render(str(text),True, (255,255,255))

def inputHandler():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playerObject.velocity["y"] = 8
                if paused:
                    startGame()
        elif event.type == pygame.QUIT:
            global running
            running = False

def gameLogic():
    playerObject.velocity["y"] -= 25 * dt
    if playerObject.velocity["y"] <= -13:
        playerObject.velocity["y"] = -13
    inputHandler()
    playerObject.physics()

    for pipe in pipeElements:
        pipe.pipeLogic()
        pipe.pipeDraw()
        if pipe.removing:
            pipeElements.remove(pipe)
            updateText("dsada")

    playerObject.playerDraw()

def startGame():
    global playerObject
    global paused
    pipeElements.clear()
    playerObject = player()
    pipes()
    paused = False


startGame()
while running:
    dt = clock.tick(60) / 1000
    screen.fill((0,0,0))
    gameLogic()
    screen.blit(text_sf,(screen.get_width() - 35,20))
    pygame.display.flip()