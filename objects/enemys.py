import pygame
import random
import math
largura = 800
altura = 600
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
tela = pygame.display.set_mode((largura, altura))
class Inimigo:
    def __init__(self):
        # Cria nave inimiga com formato diferente da nave do jogador
        tamanho = 40
        self.tamanho = tamanho
        self.img_original = pygame.Surface((tamanho, tamanho))
        self.img_original.fill(PRETO)
        
        # Define o tipo de inimigo (visual diferente)
        self.tipo = random.randint(1, 3)
        if self.tipo == 1:  # Inimigo circular
            pygame.draw.circle(self.img_original, VERMELHO, (tamanho//2, tamanho//2), tamanho//2)
            pygame.draw.circle(self.img_original, (255, 100, 100), (tamanho//2, tamanho//2), tamanho//4)
        elif self.tipo == 2:  # Inimigo triangular
            pygame.draw.polygon(self.img_original, VERMELHO, [(tamanho//2, 0), (tamanho, tamanho), (0, tamanho)])
            pygame.draw.polygon(self.img_original, (255, 100, 100), [(tamanho//2, tamanho//4), (3*tamanho//4, 3*tamanho//4), (tamanho//4, 3*tamanho//4)])
        else:  # Inimigo quadrado
            pygame.draw.rect(self.img_original, VERMELHO, (0, 0, tamanho, tamanho))
            pygame.draw.rect(self.img_original, (255, 100, 100), (tamanho//4, tamanho//4, tamanho//2, tamanho//2))
        
        self.img_original.set_colorkey(PRETO)
        self.img = self.img_original
        
        # Posição e movimento
        self.x = random.randint(0, largura - tamanho)
        self.y = random.randint(-100, -tamanho)
        self.velocidade_x = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.velocidade_y = random.uniform(1, 3)
        
        # Rotação e escala
        self.rotacao = random.randint(0, 360)
        self.velocidade_rotacao = random.choice([-1, 1]) * random.uniform(0.5, 3)
        self.escala = 1.0
        self.direcao_escala = random.choice([-0.01, 0.01])  # Pulsação da escala
        
        # Padrão de movimento
        self.padrao_movimento = random.choice(['linear', 'zigzag', 'circular'])
        self.angulo_movimento = 0
        self.centro_circular_x = self.x
        self.amplitude_zigzag = random.randint(20, 100)
        
        self.ativo = True
        self.hp = 1 + self.tipo  # HP baseado no tipo de inimigo
        self.dano_visual = False
        self.tempo_dano = 0

    def desenhar(self):
        # Aplica rotação
        img_rotacionada = pygame.transform.rotate(self.img, self.rotacao)
        
        # Aplica escalonamento
        if self.escala != 1.0:
            tamanho_atual = img_rotacionada.get_width(), img_rotacionada.get_height()
            nova_escala = (int(tamanho_atual[0] * self.escala), int(tamanho_atual[1] * self.escala))
            img_rotacionada = pygame.transform.scale(img_rotacionada, nova_escala)
        
        # Centraliza a imagem rotacionada/escalonada na posição original
        rect = img_rotacionada.get_rect(center=(self.x + self.tamanho//2, self.y + self.tamanho//2))
        
        # Aplica efeito visual se sofreu dano recentemente
        if self.dano_visual and pygame.time.get_ticks() % 200 < 100:
            # Cria efeito de dano (vermelho mais claro)
            brilho = pygame.Surface(img_rotacionada.get_size())
            brilho.fill((255, 0, 0))
            brilho.set_alpha(100)  # Transparência
            tela.blit(img_rotacionada, rect.topleft)
            tela.blit(brilho, rect.topleft)
        else:
            tela.blit(img_rotacionada, rect.topleft)

    def atualizar(self):
        # Atualiza rotação
        self.rotacao += self.velocidade_rotacao
        if self.rotacao >= 360:
            self.rotacao -= 360
        elif self.rotacao < 0:
            self.rotacao += 360
            
        # Atualiza escala (efeito de pulsação)
        self.escala += self.direcao_escala
        if self.escala > 1.2 or self.escala < 0.8:
            self.direcao_escala *= -1
        
        # Aplica diferentes padrões de movimento
        if self.padrao_movimento == 'linear':
            # Movimento linear padrão
            self.x += self.velocidade_x
            self.y += self.velocidade_y
        elif self.padrao_movimento == 'zigzag':
            # Movimento em zigzag (onda senoidal no eixo X)
            self.angulo_movimento += 0.05
            self.y += self.velocidade_y
            self.x = self.x + self.velocidade_x + math.sin(self.angulo_movimento) * 2
        elif self.padrao_movimento == 'circular':
            # Movimento circular + descida
            self.angulo_movimento += 0.03
            raio = 50
            self.x = self.centro_circular_x + math.sin(self.angulo_movimento) * raio
            self.y += self.velocidade_y * 0.7  # Movimento mais lento para baixo
        
        # Rebate nas paredes laterais
        if self.x <= 0 or self.x >= largura - self.tamanho:
            self.velocidade_x *= -1
            if self.padrao_movimento == 'circular':
                self.centro_circular_x = max(50, min(largura - 50, self.x))
            
        # Se sair da tela por baixo, reposiciona no topo
        if self.y > altura:
            self.reposicionar()
            
        # Atualiza efeito visual de dano
        if self.dano_visual:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_dano > 300:
                self.dano_visual = False
    
    def reposicionar(self):
        self.x = random.randint(0, largura - self.tamanho)
        self.y = random.randint(-100, -self.tamanho)
        self.velocidade_x = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.velocidade_y = random.uniform(1, 3)
        self.padrao_movimento = random.choice(['linear', 'zigzag', 'circular'])
        self.centro_circular_x = self.x
        self.hp = 1 + self.tipo

    def dano(self):
        self.hp -= 1
        self.dano_visual = True
        self.tempo_dano = pygame.time.get_ticks()
        # Aplica um "empurrão" aleatório quando leva dano
        self.velocidade_x += random.uniform(-0.5, 0.5)
        self.velocidade_y += random.uniform(-0.3, 0.3)
        if self.hp <= 0:
            self.ativo = False



class Asteroide:
    def __init__(self):
        tamanho = random.randint(20, 60)
        self.img = pygame.Surface((tamanho, tamanho))
        self.img.fill(PRETO)
        pygame.draw.circle(self.img, (150, 150, 150), (tamanho//2, tamanho//2), tamanho//2)
        # Adiciona crateras
        for _ in range(5):
            pos_x = random.randint(5, tamanho-5)
            pos_y = random.randint(5, tamanho-5)
            raio = random.randint(2, 5)
            pygame.draw.circle(self.img, (100, 100, 100), (pos_x, pos_y), raio)
        
        self.tamanho = tamanho
        self.x = random.randint(0, largura - tamanho)
        self.y = random.randint(-300, -tamanho)
        self.velocidade_x = random.choice([-1, 1]) * random.uniform(0.2, 1.0)
        self.velocidade_y = random.uniform(2, 4)
        self.rotacao = 0
        self.velocidade_rotacao = random.choice([-1, 1]) * random.uniform(0.5, 3)
        self.ativo = True
        self.raio = tamanho // 2

    def desenhar(self):
        rotated = pygame.transform.rotate(self.img, self.rotacao)
        rect = rotated.get_rect(center=(self.x + self.tamanho//2, self.y + self.tamanho//2))
        tela.blit(rotated, rect.topleft)

    def atualizar(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y
        self.rotacao += self.velocidade_rotacao
        
        # Rebate nas paredes laterais
        if self.x <= 0 or self.x >= largura - self.tamanho:
            self.velocidade_x *= -1
            
        # Se sair da tela por baixo, reposiciona no topo
        if self.y > altura:
            self.reposicionar()
    
    def reposicionar(self):
        self.x = random.randint(0, largura - self.tamanho)
        self.y = random.randint(-300, -self.tamanho)