import pygame
import random
import math
import os
from pygame import mixer
from objects.efects import Explosao, PowerUp, Tiro
from objects.enemys import Asteroide, Inimigo, Boss, Projetil
from objects.gamer import Jogador
import pygame.freetype

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Inicializar o Pygame
pygame.init()
mixer.init()    
sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')
shoot_sound = mixer.Sound(os.path.join(sound_dir, 'buster_tiro.wav'))
explosion_sound = mixer.Sound(os.path.join(sound_dir, 'explosion.wav'))
opening_sound = mixer.Sound(os.path.join(sound_dir, 'star_wars_tema.wav'))


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
# Criar três camadas de estrelas para efeito 3D
for i in range(150):
    x = random.randint(0, largura)
    y = random.randint(0, altura)
    camada = random.randint(1, 3)
    
    if camada == 1:  # Camada distante
        tamanho = 1
        velocidade = 0.3
        brilho = 150  # Estrelas distantes têm menos brilho
    elif camada == 2:  # Camada média
        tamanho = 2
        velocidade = 1.0
        brilho = 200
    else:  # Camada próxima
        tamanho = 3
        velocidade = 2.5
        brilho = 255  # Estrelas próximas têm brilho total
        
    estrelas.append([x, y, tamanho, velocidade, camada, brilho])

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
    
    # Indicador de tiro melhorado
    if jogador.tiro_melhorado:
        tempo_atual = pygame.time.get_ticks()
        tempo_restante = max(0, jogador.duracao_tiro_melhorado - (tempo_atual - jogador.tempo_tiro_melhorado))
        porcentagem = tempo_restante / jogador.duracao_tiro_melhorado
        
        # Texto do indicador
        desenhar_texto('LASER+', 24, 10, 70, AZUL)
        
        # Barra de tempo
        largura_total = 100
        altura = 10
        pygame.draw.rect(tela, (100, 100, 100), (70, 75, largura_total, altura))
        pygame.draw.rect(tela, AZUL, (70, 75, int(largura_total * porcentagem), altura))

# Estados do jogo
MENU = 0
HISTORIA = 1
JOGANDO = 2
GAME_OVER = 3
VITORIA = 4  # Novo estado para quando o jogador vence (derrota o boss)

def tela_menu():
    tela.fill(PRETO)
    # Desenha estrelas com diferentes brilhos conforme a camada
    for estrela in estrelas:
        cor_estrela = (estrela[5], estrela[5], estrela[5])  # Usar o valor do brilho para RGB
        pygame.draw.circle(tela, cor_estrela, (estrela[0], estrela[1]), estrela[2])
    
    desenhar_texto('STAR FALCON', 72, largura//2 - 180, altura//2 - 100)
    desenhar_texto('Pressione ESPAÇO para jogar', 36, largura//2 - 180, altura//2)
    desenhar_texto('Setas para mover, ESPAÇO para atirar', 24, largura//2 - 180, altura//2 + 50)
    desenhar_texto('ESC para sair', 24, largura//2 - 180, altura//2 + 80)
    
    pygame.display.update()


def tela_historia():
    # Configurações da animação
    textos = [
        'STAR FALCON',
        '',
        'Episódio I',
        'A AMEAÇA ESPACIAL',
        '',
        'Há muito tempo, em uma galáxia',
        'muito, muito distante...',
        '',
        'As forças da Rebelião lutam contra',
        'o tirânico Império Galáctico.',
        '',
        'Uma nova esperança surge entre as estrelas...',
        '',
        'Você é o piloto do lendário STAR FALCON,',
        'a última esperança da Rebelião.',
        '',
        'Sua missão é navegar pelo perigoso',
        'campo de asteroides e derrotar as',
        'forças imperiais.',
        '',
        'Que a Força esteja com você...'
    ]
    
    # Altura total do texto para animação
    tamanho_fonte = 26
    espaco_linhas = 10
    altura_total = len(textos) * (tamanho_fonte + espaco_linhas)
    
    # Posição inicial (começa abaixo da tela)
    posicao_y = altura
    
    # Cor amarela estilo Star Wars
    cor_texto = (255, 232, 31)
    
    # Ângulo de perspectiva (texto inclinado)
    angulo = 60
    
    # Velocidade da animação
    velocidade = 1.2
    # Pré-renderizar superfícies de texto (fonte em dobro) para smooth scaling
    big_font = pygame.font.SysFont(None, tamanho_fonte * 2)
    base_surfaces = [big_font.render(linha, True, cor_texto).convert_alpha() for linha in textos]
    
    relogio = pygame.time.Clock()
    rodando = True
    
    # Loop da animação
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if evento.key == pygame.K_SPACE:
                    return
        
        # Atualiza posição das estrelas
        for estrela in estrelas:
            # Mover a estrela para baixo com base na sua velocidade
            estrela[1] += estrela[3]
            
            # Se a estrela sair da tela, reposicioná-la no topo
            if estrela[1] > altura:
                estrela[1] = 0
                estrela[0] = random.randint(0, largura)
        
        # Limpa a tela e desenha as estrelas
        tela.fill(PRETO)
        for estrela in estrelas:
            cor_estrela = (estrela[5], estrela[5], estrela[5])  # Usar o valor do brilho para RGB
            pygame.draw.circle(tela, cor_estrela, (estrela[0], estrela[1]), estrela[2])
        
        # Desenha cada linha do texto com efeito de perspectiva
        for i, linha in enumerate(textos):
            # Cálculo da posição Y ajustada com a perspectiva
            linha_y = posicao_y + i * (tamanho_fonte + espaco_linhas)
            
            # Só desenha se estiver na área visível
            if 0 < linha_y < altura:
                # Escalonamento contínuo usando smoothscale das superfícies pré-renderizadas
                base_surface = base_surfaces[i]
                progress = linha_y / altura  # 0 (base) -> 1 (topo)
                scale = 0.5 + 0.5 * progress  # mapeia entre 0.5 e 1.0
                new_w = int(base_surface.get_width() * scale)
                new_h = int(base_surface.get_height() * scale)
                surface_scaled = pygame.transform.smoothscale(base_surface, (new_w, new_h))
                rect = surface_scaled.get_rect(center=(largura//2, linha_y))
                tela.blit(surface_scaled, rect)
        
        # Atualiza a posição Y para movimento ascendente
        posicao_y -= velocidade
        
        # Se o texto inteiro já passou para além do topo da tela, encerra a animação
        if posicao_y + altura_total < 0:
            return
        
        pygame.display.update()
        relogio.tick(60)  # 60 FPS


def tela_game_over(pontuacao):
    tela.fill(PRETO)
    # Desenha estrelas
    for estrela in estrelas:
        cor_estrela = (estrela[5], estrela[5], estrela[5])  # Usar o valor do brilho para RGB
        pygame.draw.circle(tela, cor_estrela, (estrela[0], estrela[1]), estrela[2])
    
    desenhar_texto('GAME OVER', 72, largura//2 - 180, altura//2 - 100)
    desenhar_texto(f'Pontuação: {pontuacao}', 48, largura//2 - 120, altura//2)
    desenhar_texto('Pressione ESPAÇO para jogar novamente', 30, largura//2 - 240, altura//2 + 80)
    desenhar_texto('ESC para sair', 24, largura//2 - 80, altura//2 + 120)
    
    pygame.display.update()


def tela_vitoria(pontuacao):
    tela.fill(PRETO)
    # Desenha estrelas com efeito mais rápido para celebração
    for estrela in estrelas:
        cor_estrela = (estrela[5], estrela[5], estrela[5])  # Usar o valor do brilho para RGB
        pygame.draw.circle(tela, cor_estrela, (estrela[0], estrela[1]), estrela[2])
        # Move as estrelas mais rápido para efeito festivo
        estrela[1] += estrela[3] * 2
        if estrela[1] > altura:
            estrela[1] = 0
            estrela[0] = random.randint(0, largura)
    
    # Texto piscando para efeito de celebração
    if pygame.time.get_ticks() % 1000 < 800:
        desenhar_texto('VOCÊ VENCEU!', 72, largura//2 - 200, altura//2 - 150, (255, 215, 0))  # Cor dourada
    
    desenhar_texto('Missão Cumprida!', 48, largura//2 - 160, altura//2 - 50, (50, 255, 50))
    desenhar_texto(f'Pontuação Final: {pontuacao}', 36, largura//2 - 140, altura//2 + 20)
    desenhar_texto('A galáxia está segura novamente!', 30, largura//2 - 210, altura//2 + 70, (100, 200, 255))
    desenhar_texto('Pressione ESPAÇO para voltar ao menu', 30, largura//2 - 220, altura//2 + 150)
    
    pygame.display.update()

def jogo_principal():
    estado_jogo = MENU
    relogio = pygame.time.Clock()
    
    # Criação de objetos
    jogador = Jogador()
    inimigos = []
    asteroides = []
    tiros = []
    explosoes = []
    powerups = []
    
    # Boss e seus projéteis
    boss = None
    boss_projeteis = []
    pontuacao_boss = 1000  # Pontuação necessária para o boss aparecer
    boss_derrotado = False
    
    # Função para atualizar a posição das estrelas
    def atualizar_estrelas():
        for estrela in estrelas:
            # Mover a estrela para baixo com base na sua velocidade
            # A velocidade é proporcional à camada (proximidade)
            estrela[1] += estrela[3]
            
            # Se a estrela sair da tela, reposicioná-la no topo
            if estrela[1] > altura:
                estrela[1] = 0
                estrela[0] = random.randint(0, largura)
    
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
                        # Ao pressionar ESPAÇO no menu, vai para a tela de história
                        estado_jogo = HISTORIA
                
                elif estado_jogo == GAME_OVER or estado_jogo == VITORIA:
                    if evento.key == pygame.K_SPACE:
                        # Se estiver na tela de vitória, volta para o menu inicial
                        # Se estiver na tela de game over, recomeça o jogo
                        if estado_jogo == VITORIA:
                            estado_jogo = MENU
                        else:  # GAME_OVER
                            estado_jogo = JOGANDO
                            
                        # Reinicia todos os objetos do jogo
                        jogador = Jogador()
                        tiros = []
                        inimigos = []
                        asteroides = []
                        explosoes = []
                        powerups = []
                        
                        # Reinicia o boss e seus objetos relacionados
                        boss = None
                        boss_projeteis = []
                        boss_derrotado = False
                        
                        # Cria inimigos iniciais
                        for _ in range(5):
                            inimigos.append(Inimigo())
                        
                        # Cria asteroides iniciais
                        for _ in range(3):
                            asteroides.append(Asteroide())
        
        # Verifica estado do jogo
        if estado_jogo == MENU:
            # Atualiza posição das estrelas mesmo no menu
            atualizar_estrelas()
            tela_menu()
            continue
        
        elif estado_jogo == HISTORIA:
            # Mostra a tela de história com animação estilo Star Wars
            opening_sound.play()
            tela_historia()
            # Após a tela de história, passa para o estado de jogo
            estado_jogo = JOGANDO
            continue
            
        elif estado_jogo == JOGANDO:
            # Atualiza posição das estrelas durante o jogo
            opening_sound.stop()
            atualizar_estrelas()
        
        elif estado_jogo == GAME_OVER:
            # Atualiza posição das estrelas na tela de game over
            atualizar_estrelas()
            tela_game_over(jogador.pontuacao)
            continue
        
        elif estado_jogo == VITORIA:
            # A tela de vitória já tem seu próprio efeito de estrelas
            tela_vitoria(jogador.pontuacao)
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
        if teclas[pygame.K_SPACE]:
            # Intervalo entre tiros - menor para tiros melhorados
            intervalo_tiro = 150 if jogador.tiro_melhorado else 300  # 150ms ou 300ms entre tiros
            if tempo_atual - tempo_ultimo_tiro > intervalo_tiro:
                # Cria o tiro com a mesma rotação da nave para seguir a direção apontada
                if jogador.tiro_melhorado:
                    # Tiro melhorado (maior e mais poderoso)
                    tiros.append(Tiro(jogador.x, jogador.y, jogador.rotacao, melhorado=True))
                    # Adiciona um efeito visual para o tiro melhorado
                    if random.random() < 0.3:  # 30% de chance por tiro
                        explosoes.append(Explosao(jogador.x + 25, jogador.y, 15))
                else:
                    # Tiro normal
                    tiros.append(Tiro(jogador.x, jogador.y, jogador.rotacao))
                
                shoot_sound.play()
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
                explosion_sound.play()
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
                    # Tiros melhorados causam dano duplo
                    if hasattr(tiro, 'melhorado') and tiro.melhorado:
                        inimigo.dano()  # Aplica dano uma primeira vez
                        inimigo.dano()  # Aplica dano uma segunda vez (dano duplo)
                    else:
                        inimigo.dano()  # Dano normal
                        
                    if tiro in tiros:  # Verifica se o tiro ainda está na lista
                        tiros.remove(tiro)
                    break
        
        # Verifica colisões jogador-inimigo
        for inimigo in inimigos[:]:
            if verificar_colisao(jogador.x + 25, jogador.y + 15, 15, inimigo.x + 20, inimigo.y + 20, 20):
                jogador.colidir()
                inimigo.ativo = False
                explosoes.append(Explosao(inimigo.x + 20, inimigo.y + 20, 40))
                explosion_sound.play()
        
        # Verifica colisões jogador-asteroide
        for asteroide in asteroides[:]:
            if verificar_colisao(jogador.x + 25, jogador.y + 15, 15, 
                               asteroide.x + asteroide.tamanho//2, 
                               asteroide.y + asteroide.tamanho//2, 
                               asteroide.raio):
                jogador.colidir()
                explosoes.append(Explosao(asteroide.x + asteroide.tamanho//2, 
                                       asteroide.y + asteroide.tamanho//2, 30))
                explosion_sound.play()
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
                    explosion_sound.play()
                    asteroide.reposicionar()
                    break
        
        # Verifica colisões jogador-powerup
        for powerup in powerups[:]:
            if verificar_colisao(jogador.x + 25, jogador.y + 15, 15, powerup.x + 15, powerup.y + 15, 15):
                if powerup.tipo == 'vida' and jogador.vidas < 5:
                    # Booster verde: aumenta vida
                    jogador.vidas += 1
                    desenhar_texto('+ VIDA!', 30, jogador.x - 10, jogador.y - 30, VERDE)
                elif powerup.tipo == 'laser':
                    # Booster azul: ativa tiro melhorado
                    jogador.tiro_melhorado = True
                    jogador.tempo_tiro_melhorado = pygame.time.get_ticks()
                    desenhar_texto('TIRO MELHORADO!', 30, jogador.x - 60, jogador.y - 30, AZUL)
                powerups.remove(powerup)
        
        # Verifica para spawnar boss
        if jogador.pontuacao >= pontuacao_boss and boss is None and not boss_derrotado:
            boss = Boss()
        
        # Atualiza o boss e seus projéteis
        if boss is not None and boss.ativo:
            boss.atualizar(jogador.x, jogador.y)
            novos_projeteis = boss.disparar(jogador.x, jogador.y)
            if novos_projeteis:
                boss_projeteis.extend(novos_projeteis)
                
            # Atualiza projéteis do boss
            for projetil in boss_projeteis[:]:
                projetil.atualizar()
                if not projetil.ativo:
                    boss_projeteis.remove(projetil)
            
            # Verifica colisões jogador-projétil
            for projetil in boss_projeteis[:]:
                if verificar_colisao(jogador.x + 25, jogador.y + 15, 15, 
                                     projetil.x + projetil.tamanho//2, 
                                     projetil.y + projetil.tamanho//2, 
                                     projetil.raio):
                    jogador.colidir()
                    projetil.ativo = False
                    boss_projeteis.remove(projetil)
                    explosoes.append(Explosao(projetil.x, projetil.y, 15))
                    explosion_sound.play()
            
            # Verifica colisões tiro-boss
            for tiro in tiros[:]:
                if verificar_colisao(tiro.x + 2, tiro.y + 7, 2, 
                                     boss.x + boss.tamanho//2, 
                                     boss.y + boss.tamanho//2, 
                                     boss.raio):
                    boss.dano()
                    if boss.hp <= 0:
                        boss_derrotado = True
                        jogador.pontuacao += 500  # Bônus por derrotar o boss
                        explosoes.append(Explosao(boss.x + boss.tamanho//2, 
                                                boss.y + boss.tamanho//2, 80))
                        explosion_sound.play()
                        
                        # Aguarda um momento antes de ir para a tela de vitória
                        # (para mostrar a explosão do boss)
                        pygame.time.delay(1000)  # Pausa por 1 segundo
                        
                        # Muda para a tela de vitória
                        estado_jogo = VITORIA
                    
                    explosoes.append(Explosao(tiro.x, tiro.y, 10))
                    if tiro in tiros:  # Verifica se o tiro ainda está na lista
                        tiros.remove(tiro)
                    
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
        
        # Desenha boss e seus projéteis
        if boss is not None and boss.ativo:
            boss.desenhar()
            
            for projetil in boss_projeteis:
                projetil.desenhar()
            
        jogador.desenhar()
        
        # Indicador quando o boss vai aparecer ou está presente
        if jogador.pontuacao >= pontuacao_boss * 0.7 and boss is None and not boss_derrotado:
            progresso = min(1.0, (jogador.pontuacao - pontuacao_boss * 0.7) / (pontuacao_boss * 0.3))
            mensagem = 'ALERTA: BOSS SE APROXIMANDO!'
            tamanho_fonte = 36
            cor = (255, 50, 50)
            if pygame.time.get_ticks() % 1000 < 500:  # Faz piscar
                desenhar_texto(mensagem, tamanho_fonte, largura//2 - 220, 100, cor)
        
        # Mensagem quando o boss é derrotado
        if boss_derrotado and pygame.time.get_ticks() % 2000 < 1000:
            desenhar_texto('BOSS DERROTADO!', 36, largura//2 - 140, 100, (50, 255, 50))
            
        desenhar_hud(jogador)
        
        
        # Atualiza a tela
        pygame.display.update()
        relogio.tick(60)  # 60 FPS
    
    # Finaliza o jogo
    pygame.quit()

# Inicia o jogo
if __name__ == '__main__':
    jogo_principal()
