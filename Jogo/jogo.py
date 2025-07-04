######################################################
##                                                  ##
##                PIG: A pig in HELL!               ##
##    Arthur Dondoni, Eduardo Paim, Pedro Adolfi    ##
##                                                  ##
######################################################

import pygame
import random
import sys

#Inicia o pygame e o mixer para as musicas
pygame.init()
pygame.mixer.init()

#Configurações da tela
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('PIG: A pig in HELL!')

### textos ###

#Texto intro
intro1 = 'You were living your peaceful and boring life on the farm as a pig, with nothing to'
intro2 = 'do but pig things. Then, suddenly, you hear a cracking sound behind you.'
intro3 = 'You turn your whole body around (pigs dont have great necks, unfortunately) and see something '
intro4 = 'that gives you goosebumps: a red, scary-looking, horned little guy with a trident — yes, a DEMON — '
intro5 ='crawling out of a big hole in the ground. He gives you no chance.He says, “You shall pay for'
intro6 = 'your pig sins, now” and strikes you right on the head. Everything goes black.'

#texto inferno
hell1 = 'Now, you wake up in chains, with red sand above you — it is hot as hell down here, you think...'
hell2 = 'Wait... is this hell? You look around and see hundreds of thousands of red, scary-looking, horned '
hell3 = 'little guys — demons — marching around and kicking the asses of humans, snakes, pigs...'
hell4 = 'you name it. Fear crawls up your spine, and somehow, you manage to break free from the chains' 
hell5 = 'and start running for your life. As you run, the demons try to stop you using whatever they can.' 
hell6 = 'You notice fragments of portals scattered around — collect them. You might need them.'

#Texto finais
endingEscape1 = 'You finally manage to escape from hell by opening a giant '
endingEscape2 = 'portal using the 50 fragments you collected. Running for your life '
endingEscape3 = 'through all those little monsters, you jump into the portal.'
endingEscape4 = 'And now... you are back to your boring pig life.'

endingDemon1 = 'You dash right through the demons fireballs, and they see that.'
endingDemon2 = 'They ask, “Are you a sadomasochist fire-and-evil worshiper too?”'
endingDemon3 = 'You answer, "Yes, I am just like you, hehe.” Maybe just to avoid death... '
endingDemon4 = 'but now you are one of them. You are a demon.'

endingDeath1 = 'So... this is how it ends. With a burning ass and'
endingDeath2 = 'the rest of eternity here, in hell.'

### Sprites, icones, sons, musicas, etc ###

#Cores
bgColor = (91, 180, 232)
white = (255, 255, 255)
grey = (30, 30, 30)
black = (0, 0, 0)
red = (200, 0, 0)
golden = (255, 215, 0)

#define o icone
icon = pygame.image.load('sprites/icon.png')
pygame.display.set_icon(icon)

#configuração dos sound effects
soundDammage = pygame.mixer.Sound('sounds/hurtSE.mp3')
soundDammage.set_volume(0.3)
soundCoin = pygame.mixer.Sound('sounds/coinSE.mp3')
soundCoin.set_volume(0.1)
soundCollect = pygame.mixer.Sound('sounds/collectSE.mp3')
soundCollect.set_volume(0.6)

#Fontes
smallFont = pygame.font.Font("fonts/Kirsty.otf", 16)
font = pygame.font.Font("fonts/Kirsty.otf", 32)
bigFont = pygame.font.Font("fonts/Kirsty.otf", 72)
evilFont = pygame.font.Font("fonts/oldevils.ttf", 36)
endingFont = pygame.font.Font("fonts/Kirsty.otf", 24)

#Imgens background
backgroundImg = pygame.image.load('sprites/hell.png')
bgImgMenu = pygame.image.load('sprites/BGMENU.png')
bgImgDif = pygame.image.load('sprites/BGMENU2.png')
bgEnding1 = pygame.image.load('sprites/hell.png')
bgEnding1 = pygame.transform.scale(bgEnding1, (width, height))
bgEnding2 = pygame.image.load('sprites/heaven.jpg')
bgY = 0

floorSprite = pygame.image.load("sprites/floor.png")

#Sprites
spriteSheet = pygame.image.load("sprites/porco.png").convert_alpha()
frameNum = 4

# Ajuste dos quadros do personagem
frameWidth = spriteSheet.get_width() // frameNum
frameHeight = spriteSheet.get_height()

frames = [spriteSheet.subsurface((i * frameWidth, 0, frameWidth - 6, frameHeight)) for i in range(frameNum)]
frameRight = [pygame.transform.flip(frame, True, False) for frame in frames]
facingLeft = True

# Variáveis de animação
frameIndex = 0
animeTime = 200

# Posição inicial do personagem
posX = 10
posY = height - frameHeight - 20
movement = 0.35

coinSprite = pygame.image.load('sprites/portal.png')

#Função para criar o sprite da moeda
def createSprite(width, height, color):
    spriteCoin = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.circle(spriteCoin, color, (width // 2, height // 2), width // 2)
    return spriteCoin

coinSprites2 = createSprite(20, 20, golden)
fireSprite = pygame.image.load('sprites/fire.png')

### Variaveis, objetos, ticks, etc ###

#Ticks de tempo
lastTime = 0
lastTimeCoins = 0
lastSpawn = 0

#Objetos coletaveis/projéteis
fragments = []
coins = []
fires = []

#Variaveis de dificuldade
coinFallSpeed, maxCoins, spawnDelay = 0, 0, 0

#Pontuação e variaveis semelhantes
score = 0
score2 = 0
missedCoins = 0
maxMisses = 5
gameOver = False

### Funções ###

#Função para desenhar um botão na tela
def drawButton(screen, color, pos, size, text, fontT):
    pygame.draw.rect(screen, color, (pos[0], pos[1], size[0], size[1]))
    textSurface = fontT.render(text, True, white)
    textRect = textSurface.get_rect(center=(pos[0] + size[0] // 2, pos[1] + size[1] // 2))
    screen.blit(textSurface, textRect)

#Função para a escolha de dificuldades
def chooseDifficult(difficult):
    match(difficult):
        case 1:
            coinFallSpeed = 2
            maxCoins = 4
            spawnDelay = 1400
        case 2:
            coinFallSpeed = 3
            maxCoins = 5
            spawnDelay = 1000 
        case 3:
            coinFallSpeed = 6
            maxCoins = 15
            spawnDelay = 200
        case _:
            coinFallSpeed = 2
            maxCoins = 5
            spawnDelay = 1000 
    
    return coinFallSpeed, maxCoins, spawnDelay

#função para definir o poder
def setPower():
    global movement, animeTime, coinFallSpeed, spawnDelay
    num = random.randint(1, 3)
    match(num):
        case 1:
            movement = 1
            animeTime = 50
        case 2:
            coinFallSpeed = 1
        case 3:
            spawnDelay = 1500

#função para resetar o poder
def resetPower():
    global movement, animeTime, coinFallSpeed, maxCoins, spawnDelay
    movement = 0.35
    animeTime = 200
    coinFallSpeed, maxCoins, spawnDelay = chooseDifficult(setDif)

#Função para gerar nova moeda
def spawnFragment():
    x = random.randint(0, width - 20)
    y = -20
    fragments.append(pygame.Rect(x, y, 20, 20))

def spawnCoins():
    x = random.randint(0, width - 20)
    y = -20
    coins.append(pygame.Rect(x, y, 20, 20))
    
def spawnFire():
    x = random.randint(0, width - 20)
    y = -20
    fires.append(pygame.Rect(x, y, 20, 20))

def playHighway():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/highway.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

def playSuspense():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/suspense.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def playStarway():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/starway.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

def playWelcome():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/welcome.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

playHighway()

### Loopings ###

#Menu loop
running = True
control = True
while running:
    keys = pygame.key.get_pressed()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            control = False
            running = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if buttonMenu.collidepoint(evento.pos):
                running = False

    #Preenche o fundo de branco
    screen.fill(white)
    screen.blit(bgImgMenu, (0, 0))

    #Desenha o botão
    buttonMenu = pygame.Rect(240, 300, 320, 75)
    drawButton(screen, grey, (240, 300), buttonMenu.size, "Start Game", font)

    creditsText = font.render("Arthur Dondoni - Eduardo Paim - Pedro Adolfi", True, white)
    screen.blit(creditsText, (50, 540))

    #Atualiza a tela
    pygame.display.flip()

setDif = 0
if control:
    running = True

#Difficult loop
while running:
    keys = keys = pygame.key.get_pressed()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            control = False
            running = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if buttonDif1.collidepoint(evento.pos):
                setDif = 1
                coinFallSpeed, maxCoins, spawnDelay = chooseDifficult(setDif)
                running = False
            elif buttonDif2.collidepoint(evento.pos):
                setDif = 2
                coinFallSpeed, maxCoins, spawnDelay = chooseDifficult(setDif)
                running = False
            elif buttonDif3.collidepoint(evento.pos):
                setDif = 3
                coinFallSpeed, maxCoins, spawnDelay = chooseDifficult(setDif)
                running = False

    #Preenche o fundo de branco
    screen.fill(white)
    screen.blit(bgImgDif, (0, 0))

    #Desenha o botão
    buttonDif1 = pygame.Rect(240, 250, 320, 75)
    buttonDif2 = pygame.Rect(240, 350, 320, 75)
    buttonDif3 = pygame.Rect(240, 450, 320, 75)
    drawButton(screen, grey, (240, 250), buttonDif1.size, "I'm too young to die", font)
    drawButton(screen, grey, (240, 350), buttonDif2.size, "Hurt me plenty", font)
    drawButton(screen, grey, (240, 450), buttonDif3.size, "NIGHTMARE", evilFont)


    #Atualiza a tela
    pygame.display.flip()

playSuspense()

if control:
    running = True
textControl = 0

#Text loop
while running:
    keys = pygame.key.get_pressed()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            control = False
            running = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if buttonSkipText.collidepoint(evento.pos):
                textControl += 1

    screen.fill(black)
    #Eu sei... isso é feio... mas é a vida
    if textControl == 0:
        introText1 = smallFont.render(intro1, True, white)
        screen.blit(introText1, (width // 2 - introText1.get_width() // 2, 140))
        introText2 = smallFont.render(intro2, True, white)
        screen.blit(introText2, (width // 2 - introText2.get_width() // 2, 200))
        introText3 = smallFont.render(intro3, True, white)
        screen.blit(introText3, (width // 2 - introText3.get_width() // 2, 260))
        introText4 = smallFont.render(intro4, True, white)
        screen.blit(introText4, (width // 2 - introText4.get_width() // 2, 320))
        introText5 = smallFont.render(intro5, True, white)
        screen.blit(introText5, (width // 2 - introText5.get_width() // 2, 380))
        introText6 = smallFont.render(intro6, True, white)
        screen.blit(introText6, (width // 2 - introText6.get_width() // 2, 440))
    elif textControl == 1:
        hellText1 = smallFont.render(hell1, True, white)
        screen.blit(hellText1, (width // 2 - hellText1.get_width() // 2, 140))
        hellText2 = smallFont.render(hell2, True, white)
        screen.blit(hellText2, (width // 2 - hellText2.get_width() // 2, 200))
        hellText3 = smallFont.render(hell3, True, white)
        screen.blit(hellText3, (width // 2 - hellText3.get_width() // 2, 260))
        hellText4 = smallFont.render(hell4, True, white)
        screen.blit(hellText4, (width // 2 - hellText4.get_width() // 2, 320))
        hellText5 = smallFont.render(hell5, True, white)
        screen.blit(hellText5, (width // 2 - hellText5.get_width() // 2, 380))
        hellText6 = smallFont.render(hell6, True, white)
        screen.blit(hellText6, (width // 2 - hellText6.get_width() // 2, 440))
    else:
        running = False
    
    buttonSkipText = pygame.Rect(240, 500, 320, 75)
    drawButton(screen, grey, (240, 500), buttonSkipText.size, "Skip", font)

    pygame.display.flip()

playHighway()

endings = 0
cont = False

clock = pygame.time.Clock()
if control:
    running = True
    cont = True

#Game loop
while cont:
    while running:
        dt = clock.tick(60)
        keys = pygame.key.get_pressed()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                running = False
                cont = False
                control = False
            elif gameOver and keys[pygame.K_r]:
                cont = True
                score = 0
                score2 = 0
                missedCoins = 0
                movement = 0.35
                gameOver = False
                running = True
                fragments.clear()
                coins.clear()
                fires.clear()
                coinFallSpeed, maxCoins, spawnDelay = chooseDifficult(setDif)

        if not gameOver:
            #Movimento do personagem
            if keys[pygame.K_RIGHT]:
                posX += movement * dt
                facingLeft = False
            elif keys[pygame.K_LEFT]:
                posX -= movement * dt
                facingLeft = True

            if posX < 0:
                posX = 0
            elif posX > width - frameWidth:
                posX = width - frameWidth

            #Animação
            now = pygame.time.get_ticks()
            if now - lastTime > animeTime:
                frameIndex = (frameIndex + 1) % frameNum
                lastTime = now

            currentFrame = frames if facingLeft else frameRight

            #Spawn de fragmentos e fogo
            if now - lastSpawn > spawnDelay and len(fragments) < maxCoins:
                spawnFragment()
                spawnFire()
                lastSpawn = now

            #Spawn de moedas
            if score == score2 + 10 and len(coins) == 0:
                score2 = score
                spawnCoins()

            #Atualiza posições dos fragmentos
            for fragment in fragments[:]:
                fragment.y += coinFallSpeed

                #Retira se sair da tela
                if fragment.y > height:
                    fragments.remove(fragment)
                    missedCoins += 1
                    if missedCoins >= maxMisses:
                        gameOver = True

                #Verifica colisão com personagem
                pigRect = pygame.Rect(posX, posY, frameWidth, frameHeight)
                if pigRect.colliderect(fragment):
                    fragments.remove(fragment)
                    score += 1
                    soundCollect.play()

            #Atualiza posições do fogo
            for fire in fires[:]:
                fire.y += coinFallSpeed

                #Retira se sair da tela
                if fire.y > height:
                    fires.remove(fire)

                #Verifica colisão com personagem
                if pigRect.colliderect(fire):
                    fires.remove(fire)
                    score -= 1
                    soundDammage.play()

            #Atualiza posições das moedas
            for coin in coins[:]:
                coin.y += coinFallSpeed

                #Retira se sair da tela
                if coin.y > height:
                    coins.remove(coin)

                #Verifica colisão com personagem
                if pigRect.colliderect(coin):
                    coins.remove(coin)
                    setPower()
                    lastTimeCoins = now
                    soundCoin.play()

            if lastTimeCoins > 0 and now - lastTimeCoins >= 12000:
                resetPower()
                lastTimeCoins = 0
                
            #Move o fundo para cima
            bgY -= 1

            #Reinicia a posição quando o fundo sair da tela toda
            if bgY <= -backgroundImg.get_height():
                bgY = 0

        #Desenha
        screen.fill(bgColor)
        screen.blit(backgroundImg, (0, bgY))
        screen.blit(backgroundImg, (0, bgY + backgroundImg.get_height()))

        if score >= 50:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonEnd.collidepoint(evento.pos):
                    running = False
                    cont = False
                
            endText = bigFont.render("Congratulations", True, white)
            screen.blit(endText, (width // 2 - endText.get_width() // 2, height // 2 - 50))

            buttonEnd = pygame.Rect(240, 450, 320, 75)
            drawButton(screen, grey, (240, 450), buttonEnd.size, "Finish Story", font)

            gameOver = True
            endings = 2
        elif score <= -5:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonEnd.collidepoint(evento.pos):
                    running = False
                    cont = False
            endText = bigFont.render("SECRET!! Shhhhh...", True, white)
            screen.blit(endText, (width // 2 - endText.get_width() // 2, height // 2 - 50))

            buttonEnd = pygame.Rect(240, 450, 320, 75)
            drawButton(screen, grey, (240, 450), buttonEnd.size, "Finish Story", font)

            gameOver = True
            endings = 3
        elif not gameOver:
            screen.blit(floorSprite, (0, 500))
            screen.blit(currentFrame[frameIndex], (posX, posY))

            for coin in fragments:
                screen.blit(coinSprite, (coin.x, coin.y))

            for coin in coins:
                screen.blit(coinSprites2, (coin.x, coin.y)) 
            
            for fire in fires:
                screen.blit(fireSprite, (fire.x, fire.y)) 

            scoreText = font.render(f"Score: {score}/50", True, black)
            screen.blit(scoreText, (10, 10))

            missText = font.render(f"Misses: {missedCoins}/{maxMisses}", True, white)
            screen.blit(missText, (10, 40))
        else:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonGiveUp.collidepoint(evento.pos):
                    running = False
                    cont = False
                    endings = 1

            gameOverText = bigFont.render("GAME OVER", True, white)
            scoreText = font.render(f"Final Score: {score}", True, black)
            resetText = font.render("Press 'R' to restart.", True, black)
            closeText = font.render("Press 'Esc' to close the game.", True, black)

            screen.blit(gameOverText, (width // 2 - gameOverText.get_width() // 2, height // 2 - 70))
            screen.blit(scoreText, (width // 2 - scoreText.get_width() // 2, height // 2 + 20))
            screen.blit(resetText, (width // 2 - resetText.get_width() // 2, height // 2 + 100))
            screen.blit(closeText, (width // 2 - closeText.get_width() // 2, height // 2 + 150))

            buttonGiveUp = pygame.Rect(240, 500, 320, 75)
            drawButton(screen, grey, (240, 500), buttonGiveUp.size, "Give Up", font)

        pygame.display.flip()

if control:
    running = True
cont = True

#Ending loop
while running:
    keys = pygame.key.get_pressed()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
    
    if cont:
        match(endings):
            case 1:
                #Novamente...
                screen.blit(bgEnding1, (0, 0))
                endingText = bigFont.render("E1 - Highway to Hell", True, black)
                screen.blit(endingText, (width // 2 - endingText.get_width() // 2, 100))
                endingText1 = endingFont.render(endingDeath1, True, white)
                screen.blit(endingText1, (width // 2 - endingText1.get_width() // 2, 260))
                endingText2 = endingFont.render(endingDeath2, True, white)
                screen.blit(endingText2, (width // 2 - endingText2.get_width() // 2, 320))

            case 2:
                playStarway()
                screen.blit(bgEnding2, (-100, -200))
                endingText = bigFont.render("E2 - Starway to Heaven", True, black)
                screen.blit(endingText, (width // 2 - endingText.get_width() // 2, 100))
                endingText1 = endingFont.render(endingEscape1, True, white)
                screen.blit(endingText1, (width // 2 - endingText1.get_width() // 2, 260))
                endingText2 = endingFont.render(endingEscape2, True, white)
                screen.blit(endingText2, (width // 2 - endingText2.get_width() // 2, 320))
                endingText3 = endingFont.render(endingEscape3, True, white)
                screen.blit(endingText3, (width // 2 - endingText3.get_width() // 2, 380))
                endingText4 = endingFont.render(endingEscape4, True, white)
                screen.blit(endingText4, (width // 2 - endingText4.get_width() // 2, 440))
                cont = False
            case 3:
                playWelcome()
                screen.blit(bgEnding1, (0, 0))
                endingText = font.render("E3 - Welcome Princess of Hell", True, black)
                screen.blit(endingText, (width // 2 - endingText.get_width() // 2, 100))
                endingText1 = endingFont.render(endingDemon1, True, white)
                screen.blit(endingText1, (width // 2 - endingText1.get_width() // 2, 260))
                endingText2 = endingFont.render(endingDemon2, True, white)
                screen.blit(endingText2, (width // 2 - endingText2.get_width() // 2, 320))
                endingText3 = endingFont.render(endingDemon3, True, white)
                screen.blit(endingText3, (width // 2 - endingText3.get_width() // 2, 380))
                endingText4 = endingFont.render(endingDemon4, True, white)
                screen.blit(endingText4, (width // 2 - endingText4.get_width() // 2, 440))
                cont = False
    
    pygame.display.flip()

pygame.quit()
sys.exit()