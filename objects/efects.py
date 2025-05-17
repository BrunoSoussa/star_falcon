
import pygame
import math
import random
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
class Explosao:
    def __init__(self, x, y, tamanho):
        self.x = x
        self.y = y
        self.tamanho = tamanho
        self.tempo = 0
        self.duracao = 30  # Duração aumentada
        self.ativo = True
        
        # Partículas da explosão
        self.particulas = []
        num_particulas = random.randint(8, 16)
        for _ in range(num_particulas):
            # Velocidade e direção aleatórias para as partículas
            angulo = random.uniform(0, math.pi * 2)
            velocidade = random.uniform(1, 3)
            vx = math.cos(angulo) * velocidade
            vy = math.sin(angulo) * velocidade
            
            # Cria variações de cores para as partículas (tons de laranja, vermelho, amarelo)
            r = min(255, random.randint(200, 255))
            g = min(255, random.randint(50, 200))
            b = min(255, random.randint(0, 50))
            cor = (r, g, b)
            
            # Garantindo que o tamanho máximo seja pelo menos igual ao mínimo
            tamanho_min = 2
            tamanho_max = max(tamanho_min + 1, tamanho // 4)
            tamanho_particula = random.randint(tamanho_min, tamanho_max)
            self.particulas.append({
                'x': x, 'y': y,
                'vx': vx, 'vy': vy,
                'raio': tamanho_particula,
                'cor': cor,
                'alpha': 255
            })
            
        # Onda de expansão circular
        self.ondas = [
            {'raio': 0, 'largura': 3, 'alpha': 180, 'cor': BRANCO},
            {'raio': 0, 'largura': 2, 'alpha': 150, 'cor': VERMELHO}
        ]
        
    def desenhar(self):
        # Desenha as ondas de choque
        for onda in self.ondas:
            if onda['alpha'] > 0:
                s = pygame.Surface((onda['raio']*2, onda['raio']*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*onda['cor'], onda['alpha']), 
                                (onda['raio'], onda['raio']), onda['raio'], onda['largura'])
                tela.blit(s, (self.x - onda['raio'], self.y - onda['raio']))
        
        # Desenha as partículas da explosão
        for particula in self.particulas:
            if particula['alpha'] > 0:
                s = pygame.Surface((particula['raio']*2, particula['raio']*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*particula['cor'], particula['alpha']), 
                                (particula['raio'], particula['raio']), particula['raio'])
                tela.blit(s, (particula['x'] - particula['raio'], particula['y'] - particula['raio']))
        
    def atualizar(self):
        # Incremeta o tempo
        self.tempo += 1
        
        # Atualiza as partículas
        for particula in self.particulas:
            # Movimento (translação)
            particula['x'] += particula['vx']
            particula['y'] += particula['vy']
            # Desaceleração gradual
            particula['vx'] *= 0.95
            particula['vy'] *= 0.95
            # Diminui o tamanho (escalonamento)
            particula['raio'] = max(0, particula['raio'] - 0.1)
            # Desaparece gradualmente
            particula['alpha'] = max(0, int(particula['alpha'] - 255 / self.duracao * 1.5))
            
        # Atualiza as ondas de choque
        for onda in self.ondas:
            # Expande o raio (escalonamento)
            onda['raio'] += self.tamanho / 10
            # Desaparece gradualmente
            onda['alpha'] = max(0, int(onda['alpha'] - 180 / (self.duracao * 0.7)))
        
        # Verifica se a explosão terminou
        if self.tempo >= self.duracao:
            self.ativo = False



class PowerUp:
    def __init__(self, x=None, y=None, tipo=None):
        # Cria imagem base do powerup
        tamanho = 30
        self.tamanho = tamanho
        self.img_original = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        self.img_original.fill((0, 0, 0, 0))  # Transparente
        self.velocid = 2
        
        # Define o tipo de powerup - apenas 'laser' (azul) e 'vida' (verde)
        # Se o tipo não for passado, escolhe aleatoriamente
        if tipo is None or tipo not in ['vida', 'laser']:
            self.tipo = random.choice(['vida', 'laser'])
        else:
            self.tipo = tipo
        
        # Cria visual baseado no tipo
        if self.tipo == 'vida':
            # Cor de base verde para vida
            pygame.draw.circle(self.img_original, VERDE, (tamanho//2, tamanho//2), tamanho//2)
            # Desenha um símbolo de cruz de vida
            largura_cruz = tamanho//3
            altura_cruz = tamanho//3
            pygame.draw.rect(self.img_original, BRANCO, 
                           (tamanho//2 - largura_cruz//6, tamanho//2 - altura_cruz//2, 
                            largura_cruz//3, altura_cruz))
            pygame.draw.rect(self.img_original, BRANCO, 
                           (tamanho//2 - largura_cruz//2, tamanho//2 - altura_cruz//6, 
                            largura_cruz, altura_cruz//3))
        else:  # Laser (azul)
            # Cor de base azul para laser
            pygame.draw.circle(self.img_original, AZUL, (tamanho//2, tamanho//2), tamanho//2)
            # Desenha um símbolo de raio laser
            pygame.draw.rect(self.img_original, (150, 200, 255), 
                           (tamanho//3, tamanho//4, tamanho//3, tamanho//2))
            # Desenha dois raios divergentes
            pontos1 = [
                (tamanho//3, tamanho//4),
                (tamanho//6, tamanho//8),
                (tamanho//3, tamanho//2)
            ]
            pontos2 = [
                (2*tamanho//3, tamanho//4),
                (5*tamanho//6, tamanho//8),
                (2*tamanho//3, tamanho//2)
            ]
            pygame.draw.polygon(self.img_original, (200, 230, 255), pontos1)
            pygame.draw.polygon(self.img_original, (200, 230, 255), pontos2)
        
        # Adiciona brilho/glow
        for i in range(3):
            raio = tamanho//2 - i
            alpha = 100 - i * 30
            s = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.cor_por_tipo(), alpha), (tamanho//2, tamanho//2), raio)
            self.img_original.blit(s, (0, 0))
        
        # Configurações de rotação e escala
        self.rotacao = random.randint(0, 360)
        self.velocid
        ade_rotacao = random.choice([-1, 1]) * random.uniform(1, 3)
        
        self.escala = 1.0
        self.direcao_escala = random.choice([-0.005, 0.005])  # Pulsação da escala
        
        # Aplica rotação inicial
        self.img = pygame.transform.rotate(self.img_original, self.rotacao)
        
        # Configurações de movimento
        if x is None:
            self.x = random.randint(0, largura - tamanho)
        else:
            self.x = x
            
        if y is None:
            self.y = -tamanho
        else:
            self.y = y
        self.velocidade_y = random.uniform(1, 2)
        self.velocidade_x = random.uniform(-0.5, 0.5)  # Movimento suave para os lados
        self.amplitude_oscilacao = random.randint(10, 30)
        self.frequencia_oscilacao = random.uniform(0.02, 0.05)
        self.velocidade_rotacao = 2
        self.tempo = 0
        
        # Partículas de brilho
        self.particulas = []
        
        self.ativo = True

    def cor_por_tipo(self):
        if self.tipo == 'vida':
            return (0, 220, 0)  # Verde
        else:  # laser
            return (0, 100, 220)  # Azul
    
    def desenhar(self):
        # Desenha as partículas de brilho
        for particula in self.particulas:
            if particula['alpha'] > 0:
                s = pygame.Surface((particula['raio']*2, particula['raio']*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*particula['cor'], particula['alpha']), 
                               (particula['raio'], particula['raio']), particula['raio'])
                tela.blit(s, (particula['x'] - particula['raio'], particula['y'] - particula['raio']))
        
        # Centraliza a imagem rotacionada na posição 
        rect = self.img.get_rect(center=(self.x + self.tamanho//2, self.y + self.tamanho//2))
        tela.blit(self.img, rect.topleft)

    def atualizar(self):
        # Atualiza o tempo para oscilação
        self.tempo += 1
        
        # Movimento vertical
        self.y += self.velocidade_y
        
        # Movimento horizontal com oscilação senoidal
        self.x += self.velocidade_x + math.sin(self.tempo * self.frequencia_oscilacao) * 0.5
        
        # Mantém dentro dos limites horizontais
        if self.x < 0:
            self.x = 0
            self.velocidade_x *= -1
        elif self.x > largura - self.tamanho:
            self.x = largura - self.tamanho
            self.velocidade_x *= -1
            
        # Atualiza rotação
        self.rotacao += self.velocidade_rotacao
        if self.rotacao >= 360:
            self.rotacao -= 360
            
        # Atualiza escala (pulsação)
        self.escala += self.direcao_escala
        if self.escala < 0.8 or self.escala > 1.2:
            self.direcao_escala *= -1
            
        # Aplica transformações
        # Primeiro escala, depois rotaciona
        img_escalada = pygame.transform.scale(
            self.img_original,
            (int(self.tamanho * self.escala), int(self.tamanho * self.escala))
        )
        self.img = pygame.transform.rotate(img_escalada, self.rotacao)
        
        # Gera partículas ocasionalmente
        if random.random() < 0.1:
            cor = self.cor_por_tipo()
            raio = random.randint(2, 4)
            angulo = random.uniform(0, math.pi * 2)
            distancia = random.randint(5, 15)
            px = self.x + self.tamanho//2 + math.cos(angulo) * distancia
            py = self.y + self.tamanho//2 + math.sin(angulo) * distancia
            
            self.particulas.append({
                'x': px, 'y': py,
                'vx': random.uniform(-0.2, 0.2),
                'vy': random.uniform(-0.2, 0.2),
                'raio': raio,
                'cor': cor,
                'alpha': 150
            })
        
        # Atualiza partículas
        for particula in self.particulas[:]:
            particula['x'] += particula['vx']
            particula['y'] += particula['vy']
            particula['alpha'] -= 5
            if particula['alpha'] <= 0:
                self.particulas.remove(particula)
        
        # Verifica se saiu da tela
        if self.y > altura:
            self.ativo = False



class Tiro:
    def __init__(self, x, y, rotacao=0, melhorado=False):
        # Cria imagem original do tiro
        self.melhorado = melhorado
        
        if melhorado:
            self.largura = 10  # Tiro mais largo
            self.altura = 30  # Tiro mais longo
        else:
            self.largura = 5
            self.altura = 20
            
        self.img_original = pygame.Surface((self.largura, self.altura))
        self.img_original.fill(PRETO)
        
        # Desenha um laser mais interessante
        if melhorado:
            # Tiro azul mais brilhante e com efeito de pulsação
            pygame.draw.rect(self.img_original, (50, 100, 255), (0, 0, self.largura, self.altura))
            pygame.draw.rect(self.img_original, (150, 220, 255), (2, 2, self.largura-4, self.altura-4))
            # Adiciona efeito de brilho no centro
            pygame.draw.rect(self.img_original, (200, 230, 255), (self.largura//2-1, 0, 2, self.altura))
        else:
            # Tiro padrão
            pygame.draw.rect(self.img_original, AZUL, (0, 0, self.largura, self.altura))
            pygame.draw.rect(self.img_original, (100, 200, 255), (1, 1, self.largura-2, self.altura-2))
            
        self.img_original.set_colorkey(PRETO)
        
        # Aplica rotação inicial baseada na rotação da nave
        self.rotacao = rotacao
        self.img = pygame.transform.rotate(self.img_original, self.rotacao)
        
        # Posição inicial ajustada para sair da ponta da nave
        self.x = x + 23  # Centraliza com a nave
        self.y = y
        
        # Ajusta velocidade baseada na rotação (para seguir a direção da nave)
        self.velocidade_base = 10
        angulo_radianos = math.radians(self.rotacao)
        self.velocidade_x = math.sin(angulo_radianos) * -self.velocidade_base * 0.3  # Fator para compensar a rotação
        self.velocidade_y = math.cos(angulo_radianos) * self.velocidade_base
        
        # Efeitos visuais
        self.escala = 1.0
        self.escala_dir = -0.03  # Tiro diminui de tamanho gradualmente
        self.alpha = 255  # Opacidade inicial
        
        self.ativo = True
        
        # Rastro de partículas
        self.particulas = []

    def desenhar(self):
        # Desenha rastro de partículas
        for particula in self.particulas:
            pos_x, pos_y, tamanho, alpha = particula
            s = pygame.Surface((tamanho, tamanho))
            s.fill(PRETO)
            s.set_colorkey(PRETO)
            s.set_alpha(alpha)
            pygame.draw.circle(s, (100, 150, 255), (tamanho//2, tamanho//2), tamanho//2)
            tela.blit(s, (pos_x, pos_y))
        
        # Desenha o tiro com transformações aplicadas
        tela.blit(self.img, (self.x, self.y))

    def atualizar(self):
        # Movimento do tiro
        self.y -= self.velocidade_y
        self.x += self.velocidade_x
        
        # Cria partículas para o rastro
        if random.random() < 0.3:  # 30% de chance por frame
            tamanho = random.randint(2, 4)
            # Centraliza a partícula no meio do tiro
            pos_x = self.x + self.img.get_width()//2 - tamanho//2
            pos_y = self.y + self.img.get_height()//2 - tamanho//2 + random.randint(0, 5)
            self.particulas.append([pos_x, pos_y, tamanho, 150])  # x, y, tamanho, alpha
        
        # Atualiza partículas
        for particula in self.particulas[:]:
            particula[3] -= 10  # Diminui a transparência
            if particula[3] <= 0:
                self.particulas.remove(particula)
        
        # Aplicar transformações
        if self.escala > 0.6:
            self.escala += self.escala_dir
            # Re-escala a imagem
            img_escala = pygame.transform.scale(
                self.img_original, 
                (int(self.largura * self.escala), int(self.altura * self.escala))
            )
            # Re-aplica rotação após o escalonamento
            self.img = pygame.transform.rotate(img_escala, self.rotacao)
        
        # Verifica se saiu da tela
        if self.y < 0 or self.x < 0 or self.x > largura:
            self.ativo = False
