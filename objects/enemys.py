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
        
        # Controle de disparo para inimigos que atiram (tipo 1)
        self.ultimo_disparo = 0
        self.intervalo_disparo = 2000  # 2 segundos entre disparos
        self.raio_visao = 300  # Distância em que o jogador é detectado
        
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

    def pode_atirar(self, jogador_x, jogador_y):
        # Todos os inimigos tipo 1 podem atirar, independentemente da distância
        return self.tipo == 1  # Apenas inimigos tipo 1 atiram
    
    def disparar(self, jogador_x, jogador_y):
        # Retorna um projétil se for hora de atirar
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_disparo > self.intervalo_disparo:
            self.ultimo_disparo = tempo_atual
            return Projetil(self.x + self.tamanho//2, self.y + self.tamanho, jogador_x, jogador_y)
        return None
    
    def atualizar(self, jogador_x=None, jogador_y=None):
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


class Projetil:
    def __init__(self, x, y, alvo_x, alvo_y):
        self.tamanho = 20  # Aumentando o tamanho para melhor visibilidade
        self.img = pygame.Surface((self.tamanho, self.tamanho), pygame.SRCALPHA)  # Superfície com transparência
        
        # Desenha um círculo vermelho com borda laranja
        pygame.draw.circle(self.img, (255, 100, 0), (self.tamanho//2, self.tamanho//2), self.tamanho//2)
        pygame.draw.circle(self.img, (255, 200, 0), (self.tamanho//2, self.tamanho//2), self.tamanho//2, 2)
        
        # Adiciona um brilho no centro
        pygame.draw.circle(self.img, (255, 255, 200), (self.tamanho//2, self.tamanho//2), self.tamanho//4)
        
        self.x = x
        self.y = y
        
        # Calcula a direção para o alvo
        dx = alvo_x - x
        dy = alvo_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist == 0:  # Evita divisão por zero
            self.velocidade_x = 0
            self.velocidade_y = 3
        else:
            self.velocidade_x = (dx / dist) * 5  # Velocidade ajustável
            self.velocidade_y = (dy / dist) * 5
            
        self.rotacao = 0
        self.velocidade_rotacao = random.uniform(3, 8)
        self.ativo = True
        self.raio = self.tamanho // 2
    
    def desenhar(self):
        rotated = pygame.transform.rotate(self.img, self.rotacao)
        rect = rotated.get_rect(center=(self.x + self.tamanho//2, self.y + self.tamanho//2))
        tela.blit(rotated, rect.topleft)
    
    def atualizar(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y
        self.rotacao += self.velocidade_rotacao
        
        # Remove se sair da tela
        if (self.x < -self.tamanho or 
            self.x > largura + self.tamanho or 
            self.y < -self.tamanho or 
            self.y > altura + self.tamanho):
            self.ativo = False


class Boss:
    def __init__(self):
        self.tamanho = 100
        self.img_original = pygame.Surface((self.tamanho, self.tamanho))
        self.img_original.fill(PRETO)
        
        # Desenha o boss (uma nave maior e mais ameaçadora)
        pygame.draw.polygon(self.img_original, (150, 0, 0), [
            (self.tamanho//2, 0),  # Ponta
            (0, self.tamanho),  # Canto inferior esquerdo
            (self.tamanho//3, self.tamanho//1.5),  # Recorte esquerdo
            (2*self.tamanho//3, self.tamanho//1.5),  # Recorte direito
            (self.tamanho, self.tamanho)  # Canto inferior direito
        ])
        pygame.draw.circle(self.img_original, AZUL, (self.tamanho//2, self.tamanho//2), self.tamanho//4)
        pygame.draw.circle(self.img_original, (255, 0, 0), (self.tamanho//2, self.tamanho//2), self.tamanho//6)
        
        # Adiciona detalhes
        for _ in range(5):
            pos_x = random.randint(self.tamanho//4, 3*self.tamanho//4)
            pos_y = random.randint(self.tamanho//4, 3*self.tamanho//4)
            raio = random.randint(3, 8)
            pygame.draw.circle(self.img_original, VERMELHO, (pos_x, pos_y), raio)
        
        self.img_original.set_colorkey(PRETO)
        self.img = self.img_original
        
        # Posição inicial (centralizado no topo)
        self.x = largura // 2 - self.tamanho // 2
        self.y = -self.tamanho
        
        # Movimento
        self.velocidade_base = 2
        self.velocidade_x = 0
        self.velocidade_y = self.velocidade_base
        self.destino_y = 100  # Posição vertical final
        self.movimento_lateral = True
        
        # Status
        self.ativo = True
        self.hp_maximo = 20
        self.hp = self.hp_maximo
        self.dano_visual = False
        self.tempo_dano = 0
        self.raio = self.tamanho // 2
        
        # Controle de disparo
        self.ultimo_disparo = 0
        self.intervalo_disparo = 1000  # Milissegundos
        self.padrao_disparo = "alternado"  # Pode ser alternado, circular, mirando
        self.contador_padroes = 0
    
    def desenhar(self):
        # Aplica efeito visual se sofreu dano recentemente
        if self.dano_visual and pygame.time.get_ticks() % 200 < 100:
            # Cria versão avermelhada
            img_dano = self.img.copy()
            brilho = pygame.Surface(img_dano.get_size())
            brilho.fill((255, 0, 0))
            brilho.set_alpha(100)
            rect = img_dano.get_rect(topleft=(self.x, self.y))
            tela.blit(img_dano, rect.topleft)
            tela.blit(brilho, rect.topleft)
        else:
            tela.blit(self.img, (self.x, self.y))
        
        # Desenha barra de vida
        barra_largura = self.tamanho
        barra_altura = 8
        borda = 1
        x_barra = self.x
        y_barra = self.y - 15
        
        # Borda
        pygame.draw.rect(tela, BRANCO, (x_barra-borda, y_barra-borda, barra_largura+2*borda, barra_altura+2*borda))
        # Fundo vermelho
        pygame.draw.rect(tela, VERMELHO, (x_barra, y_barra, barra_largura, barra_altura))
        # Vida atual (verde)
        vida_percentual = max(0, self.hp / self.hp_maximo)
        pygame.draw.rect(tela, VERDE, (x_barra, y_barra, int(barra_largura * vida_percentual), barra_altura))
    
    def atualizar(self, jogador_x, jogador_y):
        # Movimento inicial até posição de batalha
        if self.y < self.destino_y:
            self.y += self.velocidade_y
        elif self.movimento_lateral:
            # Movimento lateral quando está na posição de batalha
            if not hasattr(self, 'direcao') or self.direcao is None:
                self.direcao = 1  # Começa indo para a direita
            
            self.x += self.velocidade_base * self.direcao
            
            # Muda de direção nas bordas
            if self.x <= 0:
                self.direcao = 1
            elif self.x + self.tamanho >= largura:
                self.direcao = -1
        
        # Atualiza efeito visual de dano
        if self.dano_visual:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_dano > 300:
                self.dano_visual = False
    
    def disparar(self, jogador_x, jogador_y):
        """Verifica se pode disparar e retorna uma lista de projéteis criados"""
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_disparo < self.intervalo_disparo:
            return []  # Ainda não é hora de disparar
            
        self.ultimo_disparo = tempo_atual
        projeteis = []
        
        # Centro do boss para os disparos
        centro_x = self.x + self.tamanho // 2
        centro_y = self.y + self.tamanho // 2
        
        # A cada 3 disparos, muda o padrão
        self.contador_padroes += 1
        if self.contador_padroes >= 3:
            self.contador_padroes = 0
            padroes = ["alternado", "circular", "mirando"]
            self.padrao_disparo = padroes[random.randint(0, len(padroes)-1)]
        
        # Padrões de disparo
        if self.padrao_disparo == "alternado":  # Dispara 3 projéteis alternados
            projeteis.append(Projetil(centro_x, centro_y, jogador_x, jogador_y))  # Centro
            projeteis.append(Projetil(centro_x - 20, centro_y + 10, jogador_x - 30, jogador_y))  # Esquerda
            projeteis.append(Projetil(centro_x + 20, centro_y + 10, jogador_x + 30, jogador_y))  # Direita
            
        elif self.padrao_disparo == "circular":  # Dispara em padrão circular
            num_projeteis = 8
            for i in range(num_projeteis):
                angulo = i * (2 * math.pi / num_projeteis)
                destino_x = centro_x + math.cos(angulo) * 100
                destino_y = centro_y + math.sin(angulo) * 100
                projeteis.append(Projetil(centro_x, centro_y, destino_x, destino_y))
                
        elif self.padrao_disparo == "mirando":  # Dispara vários projéteis mirando o jogador
            for _ in range(5):
                offset_x = random.randint(-30, 30)
                offset_y = random.randint(-30, 30)
                projeteis.append(Projetil(centro_x, centro_y, jogador_x + offset_x, jogador_y + offset_y))
        
        return projeteis
    
    def dano(self):
        self.hp -= 1
        self.dano_visual = True
        self.tempo_dano = pygame.time.get_ticks()
        
        # Aumenta velocidade e muda padrão de ataque quando perde vida
        if self.hp <= self.hp_maximo // 2:
            self.intervalo_disparo = 800  # Disparo mais rápido
            self.velocidade_base = 3  # Movimento mais rápido
            
        if self.hp <= 0:
            self.ativo = False