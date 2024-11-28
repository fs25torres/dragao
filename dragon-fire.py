import pygame as pg
import sys
import os

pg.init()

# mouse oculto
pg.mouse.set_visible(False)

# Parâmetros de tela
largura = 1366
altura = 768
# largura = 800
# altura = 600

# largura = 800
# altura = 600

# Fonte
fonte = pg.font.Font(None, 70)

# Cor da tela
preto = (0, 0, 0)
branco = (255, 255, 255)

# Carrega e define o ícone
icone = pg.image.load(os.path.join('assets/menu/dragon-icon.png'))
pg.display.set_icon(icone)

# Tela do jogo
tela = pg.display.set_mode((largura, altura))
pg.display.set_caption("Dragon-fire")

# Imagens da tela de menu
menu_bg = pg.image.load('assets/menu/menu dragão.png').convert_alpha()
menu_bg = pg.transform.scale(menu_bg, (largura, altura))

# Imagens da tela do jogo
fundo = pg.image.load('assets/background/skylua.png').convert_alpha()
fundo = pg.transform.scale(fundo, (largura, altura))

# Função para desenhar texto na tela
def desenha_texto(texto, fonte, cor, x, y):
    imagem_texto = fonte.render(texto, True, cor)
    tela.blit(imagem_texto, (x, y))

# classes do jogador, inimigos e projéteis
class DragaoPlayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Carregar as imagens do dragão e redimensionar para um único tamanho
        self.images = [
            pg.image.load('assets/classes game/sprites/dragon_play/dragonplay1.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/dragon_play/dragonplay2.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/dragon_play/dragonplay3.png').convert_alpha()
        ]
        self.images = [pg.transform.scale(img, (200, 200)) for img in self.images]
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(largura // 2, altura - 100))
        self.index = 0
        self.health = 20
        self.velocidade = 5
        self.tempo_animacao = 200
        self.ultimo_tempo_animacao = pg.time.get_ticks()
        self.projeteis = pg.sprite.Group()
        self.contador_tiros = 0  # Contador de tiros

    def update(self):
        agora = pg.time.get_ticks()
        if agora - self.ultimo_tempo_animacao > self.tempo_animacao:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.ultimo_tempo_animacao = agora

        # Movimento do dragão
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if keys[pg.K_DOWN] and self.rect.bottom < altura:
            self.rect.y += self.velocidade
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if keys[pg.K_RIGHT] and self.rect.right < largura:
            self.rect.x += self.velocidade

        self.projeteis.update()

    def atirar(self):
        # Ajustar o ponto de disparo para a cabeça do dragão
        pos_projetil_x = self.rect.centerx
        pos_projetil_y = self.rect.top + 70
        novo_projetil = ProjetilPlayer(pos_projetil_x, pos_projetil_y)
        self.projeteis.add(novo_projetil)

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [
            pg.image.load('assets/classes game/sprites/inidrag/enedrag1.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/inidrag/enedrag2.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/inidrag/enedrag3.png').convert_alpha()
        ]
        self.images = [pg.transform.scale(img, (600, 600)) for img in self.images]
        self.index = 0
        self.health = 50
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(largura // 2, 200))
        self.velocidade_x = 3
        self.tempo_animacao = 200
        self.ultimo_tempo_animacao = pg.time.get_ticks()
        self.direcao = 1
        self.ultimo_tempo_tiro = pg.time.get_ticks()
        self.tempo_tiro = 2000
        self.projeteis = pg.sprite.Group()
        self.contador_tiros = 0  # Contador de tiros

    def update(self):
        agora = pg.time.get_ticks()
        if agora - self.ultimo_tempo_animacao > self.tempo_animacao:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.ultimo_tempo_animacao = agora

        self.rect.x += self.velocidade_x * self.direcao
        if self.rect.left <= 0 or self.rect.right >= largura:
            self.direcao *= -1  

        self.projeteis.update()

    def atirar(self):
        pos_projetil_inimigo_x = self.rect.centerx
        pos_projetil_inimigo_y = self.rect.top + 300
        agora = pg.time.get_ticks()
        if agora - self.ultimo_tempo_tiro > self.tempo_tiro:
            novo_projetil = ProjetilEnemy(pos_projetil_inimigo_x, pos_projetil_inimigo_y)
            self.projeteis.add(novo_projetil)
            self.ultimo_tempo_tiro = agora

class ProjetilEnemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [
            pg.image.load('assets/classes game/sprites/proj.inimigo/proj_enemy1.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/proj.inimigo/proj_enemy2.png').convert_alpha()
        ]
        self.images = [pg.transform.scale(img, (350, 350)) for img in self.images]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 10
        self.tempo_animacao = 100
        self.ultimo_tempo_animacao = pg.time.get_ticks()

        self.som_tiro = pg.mixer.Sound('assets/sons/fireball-whoosh-5.mp3')
        self.som_tiro.play()

    def update(self):
        agora = pg.time.get_ticks()
        if agora - self.ultimo_tempo_animacao > self.tempo_animacao:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.ultimo_tempo_animacao = agora

        # Movimento do projétil
        self.rect.y += self.velocidade
        if self.rect.top > altura:
            self.kill()

class ProjetilPlayer(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carregar as imagens da animação do projétil e redimensionar
        self.images = [
            pg.image.load('assets/classes game/sprites/proj.player/fire_play1.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/proj.player/fire_play2.png').convert_alpha()
        ]
        self.images = [pg.transform.scale(img, (200, 200)) for img in self.images]  
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = -10  
        self.tempo_animacao = 300
        self.ultimo_tempo_animacao = pg.time.get_ticks()

        self.som_tiro = pg.mixer.Sound('assets/sons/fireball-whoosh-2.mp3')
        self.som_tiro.play()

    def update(self):
        agora = pg.time.get_ticks()
        if agora - self.ultimo_tempo_animacao > self.tempo_animacao:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.ultimo_tempo_animacao = agora

        # Movimento do projétil para cima
        self.rect.y += self.velocidade
        if self.rect.bottom < 0:
            self.kill()

# Verificar colisões
def desenha_health(health, x, y, cor):
    largura_barra = 200
    altura_barra = 20
    comprimento_health = int((health / 20) * largura_barra)
    pg.draw.rect(tela, cor, (x, y, comprimento_health, altura_barra))

# Definir o limite y para os projéteis
LIMITE_Y = 400 # Altere esse valor conforme necessário para corresponder ao limite da área visível na tela
LIMITE_CENTER = 400 # Altere esse valor conforme necessário para corresponder ao limite da área visível na tela

def verificar_colisoes(dragao, inimigo):
    # Verificar colisão dos projéteis do dragão com o inimigo
    for projetil in dragao.projeteis:
        if projetil.rect.colliderect(inimigo.rect):
            # Verifica se o projétil passou pelo centro do rect do inimigo
            if inimigo.rect.collidepoint(projetil.rect.center):
                dragao.contador_tiros += 1  # Aumenta o contador de tiros

                # Simula dano: a cada 10 tiros, o inimigo perde 1 de vida
                if dragao.contador_tiros >= 50:
                    inimigo.health -= 1
                    dragao.contador_tiros = 0  # Reseta o contador de tiros
                    
                # Limite para o projétil do dragão, impedindo que ele ultrapasse a linha
                if projetil.rect.top >= LIMITE_Y:
                    dragao.projeteis.remove(projetil)  # Remover projétil que ultrapassou o limite
                elif projetil.rect.top >= LIMITE_CENTER:
                    dragao.projeteis.remove(projetil)

    # Verificar colisão dos projéteis do inimigo com o dragão
    for projetil in inimigo.projeteis:
        if projetil.rect.colliderect(dragao.rect):
            # Verifica se o projétil passou pelo centro do rect do dragão
            if dragao.rect.collidepoint(projetil.rect.center):
                inimigo.contador_tiros += 1  # Aumenta o contador de tiros

                # Simula dano: a cada 10 tiros, o dragão perde 1 de vida
                if inimigo.contador_tiros >= 5:
                    dragao.health -= 1
                    inimigo.contador_tiros = 0  # Reseta o contador de tiros

                # Limite para o projétil do inimigo, impedindo que ele ultrapasse a linha
                if projetil.rect.top >= LIMITE_Y:
                    inimigo.projeteis.remove(projetil)  # Remover projétil que ultrapassou o limite
                elif projetil.rect.top >= LIMITE_CENTER:
                    dragao.projeteis.remove(projetil)

# Definição do menu
def menu():
    # tocar musica
    pg.mixer.music.load('assets/sons/musica/Skyrim - The Dragonborn Comes cover by Grissini Pr(MP3_160K).mp3')
    pg.mixer.music.play(-1)  # Tocar em loop infinito
    
    menu = True
    while menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                   pg.quit()
                   sys.exit()

        # Desenha o fundo do menu
        tela.blit(menu_bg, (0, 0))
        desenha_texto('Pressione Enter para começar', fonte, branco, largura // 2 - 200, altura // 2 - 100)
        desenha_texto('Pressione Esc para sair', fonte, branco, largura // 2 - 200, altura // 2 - 15)

        pg.display.flip()
        # Aguarda pressionar a tecla Enter
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            jogo()

# Função principal do jogo 
def jogo():
    # tocar musica
    pg.mixer.music.load('assets/sons/musica/Skyrim - The Dragonborn Comes cover by Grissini Pr(MP3_160K).mp3')
    pg.mixer.music.play(0)  # Tocar em loop infinito
    
    # variaves de elementos do jogo
    clock = pg.time.Clock()
    dragao = DragaoPlayer()
    inimigo = Enemy()
    todos_sprites = pg.sprite.Group(dragao, inimigo)

    rodando = True
    while rodando:
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_SPACE:
                    dragao.atirar()
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    menu()

         # Condições de fim de jogo
        if dragao.health <= 0:
            desenha_texto('Game Over!', fonte, branco, 400, 300)
            pg.display.flip()
            pg.time.wait(3000)
            menu()
        elif inimigo.health <= 0:
            desenha_texto('Você Venceu!', fonte, branco, 400, 300)
            pg.display.flip()
            pg.time.wait(3000)
            menu()

        # Renderizar
        tela.blit(fundo, (0, 0))
        todos_sprites.draw(tela)
        dragao.projeteis.draw(tela)
        inimigo.projeteis.draw(tela)

        desenha_health(dragao.health, 100, 50, (0, 0, 255))
        desenha_health(inimigo.health, largura - 300, 50, (255, 0, 0))
        verificar_colisoes(dragao, inimigo)
        pg.display.flip()

         # Atualizar o jogo
        todos_sprites.update()
        inimigo.atirar()

        # Atualizar a tela
        pg.display.flip()
        clock.tick(30)  # 60 quadros por segundo

# Executar o jogo
menu()
jogo()
