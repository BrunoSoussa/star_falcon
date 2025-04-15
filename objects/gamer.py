
import pygame
import objects.config
import random
# Configuração da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
class Jogador:
    def __init__(self):
        # Base da nave
        tamanho_base = 50
        self.tamanho_original = tamanho_base
        self.img_original = pygame.Surface((tamanho_base, 30))
        self.img_original.fill(VERDE)
        # Desenha uma nave triangular
        pygame.draw.polygon(self.img_original, BRANCO, [(0, 30), (tamanho_base//2, 0), (tamanho_base, 30)])
        # Adiciona detalhes à nave
        pygame.draw.polygon(self.img_original, AZUL, [(10, 30), (tamanho_base//2, 10), (tamanho_base-10, 30)])
        pygame.draw.rect(self.img_original, VERMELHO, (tamanho_base//2-2, 15, 4, 15))
        self.img_original.set_colorkey(VERDE)  # Torna o verde transparente
        
        self.img = self.img_original.copy()
        self.rect = self.img.get_rect()
        self.x = largura // 2 - tamanho_base//2
        self.y = altura - 100
        self.rotacao = 0
        self.rotacao_alvo = 0
        self.velocidade = 5
        self.velocidade_rotacao = 5
        self.fator_escala = 1.0
        self.pulso = 0
        self.direcao_pulso = 0.02
        self.vidas = 3
        self.pontuacao = 0
        self.imune = False
        self.tempo_imune = 0

    def desenhar(self):
        # Aplica rotação à imagem
        img_rotacionada = pygame.transform.rotate(self.img, self.rotacao)
        # Aplica escalonamento (pulso visual quando está imune)
        if self.imune:
            self.pulso += self.direcao_pulso
            if self.pulso > 0.2 or self.pulso < 0:
                self.direcao_pulso *= -1
            fator_escala = 1.0 + self.pulso
        else:
            fator_escala = self.fator_escala
            self.pulso = 0
            
        if fator_escala != 1.0:
            tamanho = img_rotacionada.get_width(), img_rotacionada.get_height()
            novo_tamanho = int(tamanho[0] * fator_escala), int(tamanho[1] * fator_escala)
            img_rotacionada = pygame.transform.scale(img_rotacionada, novo_tamanho)
        
        # Obtém o retângulo centralizado na posição original
        rect = img_rotacionada.get_rect(center=(self.x + self.tamanho_original//2, self.y + 15))
        
        # Desenha com efeito piscante se imune
        if self.imune:
            if pygame.time.get_ticks() % 200 < 100:
                tela.blit(img_rotacionada, rect.topleft)
        else:
            tela.blit(img_rotacionada, rect.topleft)

    def mover(self, direcao):
        if direcao == 'esquerda' and self.x > 0:
            self.x -= self.velocidade
            self.rotacao_alvo = 20  # Inclina para esquerda
        if direcao == 'direita' and self.x < largura - 50:
            self.x += self.velocidade
            self.rotacao_alvo = -20  # Inclina para direita
        if direcao == 'cima' and self.y > 0:
            self.y -= self.velocidade
            self.fator_escala = 1.1  # Aumenta o tamanho ligeiramente quando vai para frente
        if direcao == 'baixo' and self.y < altura - 30:
            self.y += self.velocidade
            self.fator_escala = 0.9  # Diminui o tamanho ligeiramente quando vai para trás

    def atualizar(self):
        # Atualiza rotação gradualmente para dar um efeito suave
        if self.rotacao < self.rotacao_alvo:
            self.rotacao += self.velocidade_rotacao
        elif self.rotacao > self.rotacao_alvo:
            self.rotacao -= self.velocidade_rotacao
            
        # Retorna gradualmente à rotação neutra
        if not pygame.key.get_pressed()[pygame.K_LEFT] and not pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rotacao_alvo = 0
            
        # Retorna gradualmente ao tamanho normal
        if not pygame.key.get_pressed()[pygame.K_UP] and not pygame.key.get_pressed()[pygame.K_DOWN]:
            self.fator_escala = 1.0
            
        # Atualiza estado de imunidade
        if self.imune:
            if pygame.time.get_ticks() - self.tempo_imune > 2000:  # 2 segundos de imunidade
                self.imune = False

    def colidir(self):
        if not self.imune:
            self.vidas -= 1
            self.imune = True
            self.tempo_imune = pygame.time.get_ticks()
            # Efeito visual de impacto: rotação aleatória
            self.rotacao = random.randint(-30, 30)
