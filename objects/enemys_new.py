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

class Asteroide:
    def __init__(self):
        # Carrega as imagens dos asteroides uma vez (se ainda não foram carregadas)
        if not hasattr(Asteroide, 'imagens'):
            Asteroide.imagens = []
            for i in range(1, 5):
                try:
                    # Tenta carregar as imagens na ordem asteroid1.png, asteroid2.png, etc.
                    img_path = f'img/asteroids/asteroid{i}.png' if i < 4 else 'img/asteroids/asteroide1.png'
                    img = pygame.image.load(img_path).convert_alpha()
                    Asteroide.imagens.append(img)
                except:
                    # Se não conseguir carregar a imagem, cria uma superfície de fallback
                    img = pygame.Surface((50, 50), pygame.SRCALPHA)
                    pygame.draw.circle(img, (150, 150, 150), (25, 25), 25)
                    pygame.draw.circle(img, (100, 100, 100), (15, 15), 5)
                    pygame.draw.circle(img, (100, 100, 100), (35, 20), 3)
                    pygame.draw.circle(img, (100, 100, 100), (25, 35), 4)
                    Asteroide.imagens.append(img)
        
        # Escolhe uma imagem aleatória
        self.img_original = random.choice(Asteroide.imagens)
        
        # Define tamanho aleatório e redimensiona a imagem
        self.tamanho = random.randint(30, 80)
        self.img_original = pygame.transform.scale(self.img_original, 
                                                (self.tamanho, self.tamanho))
        
        # Define posição e velocidade
        self.x = random.randint(0, largura - self.tamanho)
        self.y = random.randint(-300, -self.tamanho)
        self.velocidade_x = random.choice([-1, 1]) * random.uniform(0.2, 1.0)
        self.velocidade_y = random.uniform(2, 4)
        self.rotacao = 0
        self.velocidade_rotacao = random.choice([-1, 1]) * random.uniform(0.5, 3)
        self.ativo = True
        self.raio = self.tamanho // 2

    def desenhar(self):
        # Aplica rotação na imagem original para evitar perda de qualidade
        rotated = pygame.transform.rotate(self.img_original, self.rotacao)
        # Obtém o retângulo da imagem rotacionada e centraliza
        rect = rotated.get_rect(center=(self.x + self.tamanho//2, 
                                      self.y + self.tamanho//2))
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
        self.velocidade_x = random.choice([-1, 1]) * random.uniform(0.2, 1.0)
        self.velocidade_y = random.uniform(2, 4)
        self.rotacao = 0
