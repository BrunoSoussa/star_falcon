import pygame
import random
import math
import os
from pygame import mixer
from objects.efects import Explosao, PowerUp, Tiro
from objects.enemys import Asteroide, Inimigo   
from objects.gamer import Jogador

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Inicializar o Pygame
pygame.init()

# Configuração da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Star Falcon')



# Imagens
icone = pygame.Surface((32, 32))
icone.fill(AZUL)
pygame.display.set_icon(icone)

# Fundo
fundo = pygame.Surface((largura, altura))
fundo.fill(PRETO)
estrelas = []
for i in range(100):
    x = random.randint(0, largura)
    y = random.randint(0, altura)
    tamanho = random.randint(1, 3)
    estrelas.append([x, y, tamanho])

# Classes de objetos do jogo




# Função para verificar colisão entre dois objetos (círculos)
def verificar_colisao(x1, y1, r1, x2, y2, r2):
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distancia < (r1 + r2)

# Função para desenhar texto
def desenhar_texto(texto, tamanho, x, y, cor=BRANCO):
    fonte = pygame.font.SysFont(None, tamanho)
    superficie = fonte.render(texto, True, cor)
    rect = superficie.get_rect(topleft=(x, y))
    tela.blit(superficie, rect)

# Função para desenhar barras laterais HUD
def desenhar_hud(jogador):
    # Desenha barra de vida
    desenhar_texto(f'Vidas: {jogador.vidas}', 24, 10, 10)
    desenhar_texto(f'Pontuação: {jogador.pontuacao}', 24, 10, 40)

# Estados do jogo
MENU = 0
JOGANDO = 1
GAME_OVER = 2

def tela_menu():
    tela.fill(PRETO)
    # Desenha estrelas
    for estrela in estrelas:
        pygame.draw.circle(tela, BRANCO, (estrela[0], estrela[1]), estrela[2])
    
    desenhar_texto('STAR FALCON', 72, largura//2 - 180, altura//2 - 100)
    desenhar_texto('Pressione ESPAÇO para jogar', 36, largura//2 - 180, altura//2)
    desenhar_texto('Setas para mover, ESPAÇO para atirar', 24, largura//2 - 180, altura//2 + 50)
    desenhar_texto('ESC para sair', 24, largura//2 - 180, altura//2 + 80)
    
    pygame.display.update()

def tela_game_over(pontuacao):
    tela.fill(PRETO)
    # Desenha estrelas
    for estrela in estrelas:
        pygame.draw.circle(tela, BRANCO, (estrela[0], estrela[1]), estrela[2])
    
    desenhar_texto('GAME OVER', 72, largura//2 - 180, altura//2 - 100)
    desenhar_texto(f'Pontuação: {pontuacao}', 48, largura//2 - 120, altura//2)
    desenhar_texto('Pressione ESPAÇO para jogar novamente', 30, largura//2 - 240, altura//2 + 80)
    desenhar_texto('ESC para sair', 24, largura//2 - 80, altura//2 + 120)
    
    pygame.display.update()

def jogo_principal():
    # Cria objetos do jogo
    jogador = Jogador()
    tiros = []
    inimigos = []
    asteroides = []
    explosoes = []
    powerups = []
    
    # Cria inimigos iniciais
    for _ in range(5):
        inimigos.append(Inimigo())
    
    # Cria asteroides iniciais
    for _ in range(3):
        asteroides.append(Asteroide())
    
    # Configurações do jogo
    relogio = pygame.time.Clock()
    tempo_ultimo_tiro = 0
    estado_jogo = MENU
    
    # Loop principal
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            # Eventos de teclado
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                    
                if estado_jogo == MENU:
                    if evento.key == pygame.K_SPACE:
                        estado_jogo = JOGANDO
                
                elif estado_jogo == GAME_OVER:
                    if evento.key == pygame.K_SPACE:
                        estado_jogo = JOGANDO
                        jogador = Jogador()
                        tiros = []
                        inimigos = []
                        asteroides = []
                        explosoes = []
                        powerups = []
                        
                        # Cria inimigos iniciais
                        for _ in range(5):
                            inimigos.append(Inimigo())
                        
                        # Cria asteroides iniciais
                        for _ in range(3):
                            asteroides.append(Asteroide())
        
        # Verifica estado do jogo
        if estado_jogo == MENU:
            tela_menu()
            continue
        
        elif estado_jogo == GAME_OVER:
            tela_game_over(jogador.pontuacao)
            continue
        
        # Obtém teclas pressionadas
        teclas = pygame.key.get_pressed()
        
        # Movimento do jogador
        if teclas[pygame.K_LEFT]:
            jogador.mover('esquerda')
        if teclas[pygame.K_RIGHT]:
            jogador.mover('direita')
        if teclas[pygame.K_UP]:
            jogador.mover('cima')
        if teclas[pygame.K_DOWN]:
            jogador.mover('baixo')
            
        # Tiro
        tempo_atual = pygame.time.get_ticks()
        if teclas[pygame.K_SPACE] and tempo_atual - tempo_ultimo_tiro > 300:  # 300ms entre tiros
            # Cria o tiro com a mesma rotação da nave para seguir a direção apontada
            tiros.append(Tiro(jogador.x, jogador.y, jogador.rotacao))
            tempo_ultimo_tiro = tempo_atual
        
        # Atualiza tiros
        for tiro in tiros[:]:
            tiro.atualizar()
            if not tiro.ativo:
                tiros.remove(tiro)
        
        # Atualiza inimigos
        for inimigo in inimigos[:]:
            inimigo.atualizar()
            if not inimigo.ativo:
                explosoes.append(Explosao(inimigo.x + 20, inimigo.y + 20, 40))
                jogador.pontuacao += 100
                if jogador.pontuacao > 200:
                    desenhar_texto('GAME OVER', 72, largura//2 - 180, altura//2 - 100)
                inimigos.remove(inimigo)
                if random.random() < 0.2:  # 20% de chance de gerar power-up
                    powerup = PowerUp()
                    powerup.x = inimigo.x
                    powerup.y = inimigo.y
                    powerups.append(powerup)
        
        # Gera novos inimigos periodicamente
        if len(inimigos) < 5 + jogador.pontuacao // 1000:  # Aumenta quantidade com a pontuação
            inimigos.append(Inimigo())
        
        # Atualiza asteroides
        for asteroide in asteroides[:]:
            asteroide.atualizar()
        
        # Gera novos asteroides periodicamente
        if len(asteroides) < 3 + jogador.pontuacao // 2000:  # Aumenta quantidade com a pontuação
            asteroides.append(Asteroide())
        
        # Atualiza explosões
        for explosao in explosoes[:]:
            explosao.atualizar()
            if not explosao.ativo:
                explosoes.remove(explosao)
        
        # Atualiza power-ups
        for powerup in powerups[:]:
            powerup.atualizar()
            if not powerup.ativo:
                powerups.remove(powerup)
        
        # Atualiza jogador
        jogador.atualizar()
        
        # Verifica colisões tiro-inimigo
        for tiro in tiros[:]:
            for inimigo in inimigos[:]:
                if verificar_colisao(tiro.x + 2, tiro.y + 7, 2, inimigo.x + 20, inimigo.y + 20, 20):
                    inimigo.dano()
                    if tiro in tiros:  # Verifica se o tiro ainda está na lista
                        tiros.remove(tiro)
                    break
        
        # Verifica colisões jogador-inimigo
        for inimigo in inimigos[:]:
            if verificar_colisao(jogador.x + 25, jogador.y + 15, 15, inimigo.x + 20, inimigo.y + 20, 20):
                jogador.colidir()
                inimigo.ativo = False
                explosoes.append(Explosao(inimigo.x + 20, inimigo.y + 20, 40))
        
        # Verifica colisões jogador-asteroide
        for asteroide in asteroides[:]:
            if verificar_colisao(jogador.x + 25, jogador.y + 15, 15, 
                               asteroide.x + asteroide.tamanho//2, 
                               asteroide.y + asteroide.tamanho//2, 
                               asteroide.raio):
                jogador.colidir()
                explosoes.append(Explosao(asteroide.x + asteroide.tamanho//2, 
                                       asteroide.y + asteroide.tamanho//2, 30))
                asteroide.reposicionar()
        
        # Verifica colisões tiro-asteroide
        for tiro in tiros[:]:
            for asteroide in asteroides[:]:
                if verificar_colisao(tiro.x + 2, tiro.y + 7, 2, 
                                   asteroide.x + asteroide.tamanho//2, 
                                   asteroide.y + asteroide.tamanho//2, 
                                   asteroide.raio):
                    if tiro in tiros:  # Verifica se o tiro ainda está na lista
                        tiros.remove(tiro)
                    jogador.pontuacao += 50
                    explosoes.append(Explosao(asteroide.x + asteroide.tamanho//2, 
                                           asteroide.y + asteroide.tamanho//2, 20))
                    asteroide.reposicionar()
                    break
        
        # Verifica colisões jogador-powerup
        for powerup in powerups[:]:
            if verificar_colisao(jogador.x + 25, jogador.y + 15, 15, powerup.x + 15, powerup.y + 15, 15):
                if powerup.tipo == 'vida' and jogador.vidas < 5:
                    jogador.vidas += 1
                elif powerup.tipo == 'escudo':
                    jogador.imune = True
                    jogador.tempo_imune = pygame.time.get_ticks()
                powerups.remove(powerup)
        
        # Verifica game over
        if jogador.vidas <= 0:
            estado_jogo = GAME_OVER
        
        # Desenha o jogo
        tela.fill(PRETO)
        
        # Desenha estrelas
        for estrela in estrelas:
            pygame.draw.circle(tela, BRANCO, (estrela[0], estrela[1]), estrela[2])
            # Move as estrelas para criar efeito de movimento
            estrela[1] += 0.5
            if estrela[1] > altura:
                estrela[1] = 0
                estrela[0] = random.randint(0, largura)
        
        # Desenha objetos
        for tiro in tiros:
            tiro.desenhar()
            
        for inimigo in inimigos:
            inimigo.desenhar()
            
        for asteroide in asteroides:
            asteroide.desenhar()
            
        for explosao in explosoes:
            explosao.desenhar()
            
        for powerup in powerups:
            powerup.desenhar()
            
        jogador.desenhar()
        
        # Desenha HUD
        desenhar_hud(jogador)
        desenhar_texto(f'OOOOOOOOOOOOOOOOOOOOO: {jogador.vidas}', 24, 10, 10)
        
        # Atualiza a tela
        pygame.display.update()
        relogio.tick(60)  # 60 FPS
    
    # Finaliza o jogo
    pygame.quit()

# Inicia o jogo
if __name__ == '__main__':
    jogo_principal()
