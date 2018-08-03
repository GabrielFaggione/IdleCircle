 # -*- coding: latin-1 -*-
''' README
Bom... o jogo é muito simples.
ele é um jogo IDLE, logo sua jogabilidade é o mais simples possível.
compre novos circulos e melhores os já comprados clicando nos menus.
não tem nenhuma sprite por tentar ser o mais simples possível, logo apenas usei .draw do pygame
o jogo não possui som por ser apenas um jogo visual.
possui um auto save a cada 10 segundos, gravando em uma db o seu progresso.
'''
import pygame, sqlite3, time
from pygame.locals import *

class Circles:
    def __init__(self, color, max_radius, grown, gold): # --- criação dos circulos
        self.color = color
        self.max_radius = max_radius
        self.radius = 1
        self.size = 0
        self.sizeGrowth = grown
        self.gold = float(gold)
        self.inScreen = False
    def update(self, player):   # --- verifica se o circulo está no tamanho máximo, e volta ao seu tamanho original
        self.radius += self.sizeGrowth
        self.circleReference = pygame.draw.circle(screen, self.color, (500,300), self.max_radius, 1)
        self.circle = pygame.draw.circle(screen, self.color, (500,300), int(self.radius), self.size)
        if self.radius >= (self.max_radius - 1):
            self.radius = 1
            player.gold += self.gold
    def upgrade(self):  # --- quando o jogador compra um upgrade é realizado a soma da velocidade que ele aumenta e do dinheiro ganho
        self.sizeGrowth += 0.01
        self.gold += self.gold/5

class MenuButton:
    def __init__(self, color, targetCircle, pos, cost):
        self.target = targetCircle
        self.color = targetCircle.color
        self.pos = pos
        self.cost = cost
        self.text = ""
        self.size = None
        self.box = None
        
    def update(self):
        if self.target.inScreen:
            self.text = "Upgrade " + str(self.target.color) + "circle"
        else:
            self.text = "Upgrade " + str(self.target.color) + "circle"
        self.text_surface = font.render(self.text, 1, button.color)
        self.size = (self.text_surface.get_width(), self.text_surface.get_height())
        self.box = Rect( self.pos, self.size )

    def checkClick(self, player, xClick, yClick):
        if (self.box.collidepoint( (xClick, yClick) )):
            if player.gold >= self.cost and self.target.inScreen == False:
                self.target.inScreen = True
                player.gold -= self.cost
            elif player.gold >= self.cost and self.target.inScreen == True:
                self.target.upgrade()
                player.gold -= self.cost
                self.cost += (self.cost / 10)        
        
class Player:
    def __init__(self): # --- apenas para contabilizar o dinheiro do player
        self.gold = 0

# ---------------------- banco de dados -----------------
conn = sqlite3.connect('playerStatus.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) # --- cria o arquivo.db
cursor = conn.cursor() # cria um objeto para controlar entrada, verificação e outros comandos relacionados a db
cursor.execute("""CREATE TABLE IF NOT EXISTS saves( 
                RedSizeGrowth, RedGold, RedInScreen, RedCost,
                BlueSizeGrowth, BlueGold, BlueInScreen, BlueCost,
                GreenSizeGrowth, GreenGold, GreenInScreen, GreenCost,
                YellowSizeGrowth, YellowGold, YellowInScreen, YellowCost,
                OrangeSizeGrowth, OrangeGold, OrangeInScreen, OrangeCost,
                PinkSizeGrowth, PinkGold, PinkInScreen, PinkCost,
                WhiteSizeGrowth, WhiteGold, WhiteInScreen, WhiteCost,
                PlayerGold) """) # --- cria no db uma pagina com as seguintes colunas caso não exista
# ------------------------ colors --------------------------
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,165,0)
pink = (255,20,147)
white = (255,255,255)
black = (0,0,0)
# ---------------------------------------------------
# ---------------------- criando os objetos ----------------------
player = Player()
red_circle = Circles(red, 10, 0.1, 1)
red_circle.inScreen = True
blue_circle = Circles(blue, 25, 0.1, 500)
green_circle = Circles(green, 50, 0.1, 50000)
yellow_circle = Circles(yellow, 100, 0.1, 5000000)
orange_circle = Circles(orange, 150, 0.1, 500000000)
pink_circle = Circles(pink, 200, 0.1, 50000000000)
white_circle = Circles(white, 250, 0.1, 5000000000000)
# ------------------------------------------------------------
# ----menu------------------------------------------------------
redCircleButton = MenuButton(red, red_circle, (20, 150), 10)
blueCircleButton = MenuButton(blue, blue_circle, (20, 200), 1000)
greenCircleButton = MenuButton(green, green_circle, (20, 250), 100000)
yellowCircleButton = MenuButton(yellow, yellow_circle, (20, 300), 10000000)
orangeCircleButton = MenuButton(orange, orange_circle, (20, 350), 1000000000)
pinkCircleButton = MenuButton(pink, pink_circle, (20, 400), 10000000000000)
whiteCircleButton = MenuButton(white, white_circle, (20, 450), 10000000000000)
menuButtons = [redCircleButton, blueCircleButton, greenCircleButton, yellowCircleButton,
               orangeCircleButton, pinkCircleButton, whiteCircleButton]

#---------------------------------------------------------------
#------------------------------------------defs -------------
def draw_menu(lista): # --- desenha o menu junto do retangulo em volta pra ficar mais chavoso --------
    for button in menuButtons:
        #text_surface = font.render(button.text, 1, button.color)
        #x['size'] = (text_surface.get_width(), text_surface.get_height())
        button.update()
        screen.blit(button.text_surface, button.pos)
        red_box = pygame.draw.rect(screen, red, [ (button.pos[0] - 10), (button.pos[1] - 5), (button.pos[0] + 300) , (button.pos[1], 2) ])
        
def click( evento, lista, player ): # --- verifica a pos do mouse com a pos dos itens do menu
    x, y = evento.pos
    for button in menuButtons:
        button.checkClick(player, x, y)
#---------------------------------------------------------------------------------          
#--------------- carrega o jogo salvo ----------------
"""
for row in cursor.execute('SELECT * FROM saves'):
    red_circle.sizeGrowth, red_circle.gold, red_circle.inScreen, menu[0]["cost"] = row[0], row[1], row[2], row[3]
    blue_circle.sizeGrowth, blue_circle.gold, blue_circle.inScreen, menu[1]["cost"] = row[4], row[5], row[6], row[7]
    if blue_circle.inScreen == True:
       new_text = menu[1]['text'].split(' ')
       menu[1]['text'] = "Upgrade "+ new_text[1] + ' '+ new_text[2]
    green_circle.sizeGrowth, green_circle.gold, green_circle.inScreen, menu[2]["cost"] = row[8], row[9], row[10], row[11]
    if green_circle.inScreen == True:
       new_text = menu[2]['text'].split(' ')
       menu[2]['text'] = "Upgrade "+ new_text[1] + ' '+ new_text[2]
    yellow_circle.sizeGrowth, yellow_circle.gold, yellow_circle.inScreen, menu[3]["cost"] = row[12], row[13], row[14], row[15]
    if yellow_circle.inScreen == True:
       new_text = menu[3]['text'].split(' ')
       menu[3]['text'] = "Upgrade "+ new_text[1] + ' '+ new_text[2]
    orange_circle.sizeGrowth, orange_circle.gold, orange_circle.inScreen, menu[4]["cost"] = row[16], row[17], row[18], row[19]
    if orange_circle.inScreen == True:
       new_text = menu[4]['text'].split(' ')
       menu[4]['text'] = "Upgrade "+ new_text[1] + ' '+ new_text[2]
    pink_circle.sizeGrowth, pink_circle.gold, pink_circle.inScreen, menu[5]["cost"] = row[20], row[21], row[22], row[23]
    if pink_circle.inScreen == True:
       new_text = menu[5]['text'].split(' ')
       menu[5]['text'] = "Upgrade "+ new_text[1] + ' '+ new_text[2]
    white_circle.sizeGrowth, white_circle.gold, white_circle.inScreen, menu[6]["cost"] = row[24], row[25], row[26], row[27]
    if white_circle.inScreen == True:
       new_text = menu[6]['text'].split(' ')
       menu[6]['text'] = "Upgrade "+ new_text[1] + ' '+ new_text[2]
    player.gold = row[28]
circleOrd = (white_circle, pink_circle, orange_circle, yellow_circle, green_circle, blue_circle, red_circle) # --- ordem de quem é desenhado primeiro
"""
# --------------------------------------------------------

pygame.init()
pygame.display.set_caption('Circle')
font = pygame.font.SysFont('Comic Sans MS', 25, bold=1, italic=0) # --- font padrão para os textos do jogo
title = font.render("Circle", 1, red) # --- objeto que será criado na screen
gold = font.render("Gold:", 1, red) # --- objeto que será criado na screen
fps = pygame.time.Clock()
screen = pygame.display.set_mode((800,600), 0, 32)
last_time = time.time()
running = True
try:
    while running == True:
        now_time = time.time()
        screen.fill((0, 0, 0))
        for circle in circleOrd:
            if circle.inScreen == True:
                circle.update(player)  # --- desenha os circulos
        draw_menu(menu) #--- desenha o menu
        screen.blit(title, (350, 50)) #--- blit no nome do jogo
        screen.blit(gold, (30, 100)) # ---- blit no texto "Gold"
        playerGold = font.render(str(int(player.gold)), 1, red) # --- atualiza o valor do gold do jogador
        screen.blit(playerGold, (100, 100)) # --- mostra o valor do gold
        fps.tick(60)
"""
        if now_time - last_time >= 10: # ---- save do jogo - joga tudo para uma lista, pois é mais seguro na hora de jogar pro db, método abaixo
            listValues = [red_circle.sizeGrowth, red_circle.gold, red_circle.inScreen, menu[0]["cost"],
                          blue_circle.sizeGrowth, blue_circle.gold, blue_circle.inScreen, menu[1]["cost"],
                          green_circle.sizeGrowth, green_circle.gold, green_circle.inScreen, menu[2]["cost"],
                          yellow_circle.sizeGrowth, yellow_circle.gold, yellow_circle.inScreen, menu[3]["cost"],
                          orange_circle.sizeGrowth, orange_circle.gold, orange_circle.inScreen, menu[4]["cost"],
                          pink_circle.sizeGrowth, pink_circle.gold, pink_circle.inScreen, menu[5]["cost"],
                          white_circle.sizeGrowth, white_circle.gold, white_circle.inScreen, menu[6]["cost"],
                          player.gold] # ----- inserção dos dados na tabela atráves de uma lista -------
            cursor.execute("""INSERT INTO saves (RedSizeGrowth, RedGold, RedInScreen, RedCost, BlueSizeGrowth, BlueGold, BlueInScreen, BlueCost,
                    GreenSizeGrowth, GreenGold, GreenInScreen, GreenCost, YellowSizeGrowth, YellowGold, YellowInScreen, YellowCost,
                    OrangeSizeGrowth, OrangeGold, OrangeInScreen, OrangeCost, PinkSizeGrowth, PinkGold, PinkInScreen, PinkCost,
                    WhiteSizeGrowth, WhiteGold, WhiteInScreen, WhiteCost, PlayerGold)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", listValues)
            conn.commit() # --- salva a db
            # ------ save do jogo -----------------------------------------------------------
            last_time = now_time
"""
        for event in pygame.event.get():
            if (event.type == MOUSEBUTTONDOWN):
                click(event, menu, player )
            elif event.type == QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
except SystemExit:
    pygame.quit()
