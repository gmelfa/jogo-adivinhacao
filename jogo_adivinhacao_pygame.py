import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (50, 50, 50)
VERDE_ESCURO = (0, 100, 0)
AZUL_ESCURO = (0, 0, 128)

# Configurações da tela
LARGURA = 640
ALTURA = 480
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Adivinhação Retrô")

# Fontes
fonte_grande = pygame.font.Font(None, 48)
fonte_media = pygame.font.Font(None, 36)
fonte_pequena = pygame.font.Font(None, 24)

class BotaoRetro:
    def __init__(self, x, y, largura, altura, texto, cor=VERDE_ESCURO, cor_texto=BRANCO):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_texto = cor_texto
        self.cor_hover = (min(cor[0]+30, 255), min(cor[1]+30, 255), min(cor[2]+30, 255))
        
    def desenhar(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        cor_atual = self.cor_hover if self.rect.collidepoint(mouse_pos) else self.cor
        
        # Desenhar botão com borda 3D
        pygame.draw.rect(tela, cor_atual, self.rect)
        pygame.draw.rect(tela, BRANCO, self.rect, 2)
        pygame.draw.line(tela, (200, 200, 200), self.rect.topleft, self.rect.topright, 2)
        pygame.draw.line(tela, (200, 200, 200), self.rect.topleft, self.rect.bottomleft, 2)
        pygame.draw.line(tela, (100, 100, 100), self.rect.bottomleft, self.rect.bottomright, 2)
        pygame.draw.line(tela, (100, 100, 100), self.rect.topright, self.rect.bottomright, 2)
        
        # Texto do botão
        texto_surface = fonte_pequena.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        tela.blit(texto_surface, texto_rect)
        
    def foi_clicado(self, pos):
        return self.rect.collidepoint(pos)

class JogoAdivinhacao:
    def __init__(self):
        self.estado = "menu"
        self.numero_secreto = 0
        self.tentativas = 0
        self.max_tentativas = 0
        self.mensagem = "Escolha a dificuldade!"
        self.entrada = ""
        self.historico = []
        
        # Botões do menu
        self.btn_facil = BotaoRetro(LARGURA//2-150, 200, 100, 50, "FÁCIL", VERDE)
        self.btn_medio = BotaoRetro(LARGURA//2-50, 200, 100, 50, "MÉDIO", AZUL)
        self.btn_dificil = BotaoRetro(LARGURA//2+50, 200, 100, 50, "DIFÍCIL", VERMELHO)
        
        # Botões numéricos
        self.botoes_num = []
        for i in range(10):
            x = LARGURA//2 - 125 + (i % 5) * 50
            y = 300 + (i // 5) * 50
            self.botoes_num.append(BotaoRetro(x, y, 45, 45, str(i), CINZA))
            
        # Botões de controle
        self.btn_apagar = BotaoRetro(LARGURA//2-125, 400, 100, 45, "APAGAR", VERMELHO)
        self.btn_enviar = BotaoRetro(LARGURA//2+25, 400, 100, 45, "ENVIAR", VERDE)
        
    def iniciar_jogo(self, dificuldade):
        self.estado = "jogando"
        self.numero_secreto = random.randint(1, 100)
        
        if dificuldade == "facil":
            self.max_tentativas = 20
        elif dificuldade == "medio":
            self.max_tentativas = 10
        else:
            self.max_tentativas = 5
            
        self.tentativas = 0
        self.mensagem = f"Adivinhe o número entre 1 e 100!"
        self.entrada = ""
        self.historico = []
        
    def verificar_palpite(self):
        if not self.entrada:
            return
            
        try:
            palpite = int(self.entrada)
            
            if palpite < 1 or palpite > 100:
                self.mensagem = "Digite um número entre 1 e 100!"
                self.entrada = ""
                return
                
            self.tentativas += 1
            tentativas_restantes = self.max_tentativas - self.tentativas
            
            if palpite < self.numero_secreto:
                resultado = "MAIOR"
                self.mensagem = f"Tente um número MAIOR! Restam {tentativas_restantes} tentativas."
            elif palpite > self.numero_secreto:
                resultado = "MENOR"
                self.mensagem = f"Tente um número MENOR! Restam {tentativas_restantes} tentativas."
            else:
                resultado = "ACERTOU!"
                self.mensagem = f"PARABÉNS! Você acertou em {self.tentativas} tentativas!"
                self.estado = "fim_jogo"
                
            # Adicionar ao histórico
            self.historico.append((palpite, resultado))
            
            if self.tentativas >= self.max_tentativas and self.estado != "fim_jogo":
                self.mensagem = f"GAME OVER! O número era {self.numero_secreto}."
                self.estado = "fim_jogo"
                
            self.entrada = ""
            
        except ValueError:
            self.mensagem = "Entrada inválida!"
            self.entrada = ""
        
    def desenhar(self):
        # Fundo
        tela.fill(PRETO)
        
        # Desenhar borda da tela estilo retrô
        pygame.draw.rect(tela, CINZA, (10, 10, LARGURA-20, ALTURA-20), 4)
        pygame.draw.rect(tela, AZUL_ESCURO, (20, 20, LARGURA-40, 100))
        
        # Título
        titulo = fonte_grande.render("JOGO DE ADIVINHAÇÃO", True, BRANCO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 40))
        
        # Mensagem
        linhas_mensagem = [self.mensagem[i:i+40] for i in range(0, len(self.mensagem), 40)]
        for i, linha in enumerate(linhas_mensagem):
            mensagem_surface = fonte_media.render(linha, True, BRANCO)
            tela.blit(mensagem_surface, (LARGURA//2 - mensagem_surface.get_width()//2, 140 + i*30))
        
        if self.estado == "menu":
            self.btn_facil.desenhar(tela)
            self.btn_medio.desenhar(tela)
            self.btn_dificil.desenhar(tela)
            
        elif self.estado in ["jogando", "fim_jogo"]:
            # Desenhar display da entrada
            pygame.draw.rect(tela, VERDE_ESCURO, (LARGURA//2 - 100, 200, 200, 50))
            pygame.draw.rect(tela, BRANCO, (LARGURA//2 - 100, 200, 200, 50), 2)
            
            entrada_text = fonte_media.render(self.entrada, True, BRANCO)
            tela.blit(entrada_text, (LARGURA//2 - entrada_text.get_width()//2, 215))
            
            # Desenhar histórico de palpites
            if self.historico:
                pygame.draw.rect(tela, CINZA, (20, 260, 150, min(180, len(self.historico) * 25 + 10)))
                titulo_historico = fonte_pequena.render("HISTÓRICO", True, BRANCO)
                tela.blit(titulo_historico, (30, 265))
                
                for i, (palpite, resultado) in enumerate(self.historico[-7:]):  # Mostrar apenas os últimos 7
                    cor_resultado = VERDE if resultado == "ACERTOU!" else VERMELHO
                    texto = f"{palpite}: {resultado}"
                    historico_surface = fonte_pequena.render(texto, True, cor_resultado)
                    tela.blit(historico_surface, (30, 290 + i*25))
            
            # Desenhar botões numéricos e de controle
            if self.estado == "jogando":
                for btn in self.botoes_num:
                    btn.desenhar(tela)
                self.btn_apagar.desenhar(tela)
                self.btn_enviar.desenhar(tela)
            else:
                # Botão para voltar ao menu
                voltar = BotaoRetro(LARGURA//2-75, 350, 150, 50, "NOVO JOGO", VERDE)
                voltar.desenhar(tela)
        
        pygame.display.flip()
        
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if self.estado == "menu":
                    if self.btn_facil.foi_clicado(pos):
                        self.iniciar_jogo("facil")
                    elif self.btn_medio.foi_clicado(pos):
                        self.iniciar_jogo("medio")
                    elif self.btn_dificil.foi_clicado(pos):
                        self.iniciar_jogo("dificil")
                        
                elif self.estado == "jogando":
                    # Verificar cliques nos botões numéricos
                    for i, btn in enumerate(self.botoes_num):
                        if btn.foi_clicado(pos) and len(self.entrada) < 3:
                            self.entrada += str(i)
                            
                    # Verificar cliques nos botões de controle
                    if self.btn_apagar.foi_clicado(pos) and self.entrada:
                        self.entrada = self.entrada[:-1]
                    elif self.btn_enviar.foi_clicado(pos):
                        self.verificar_palpite()
                        
                elif self.estado == "fim_jogo":
                    # Verificar clique no botão de novo jogo
                    voltar_rect = pygame.Rect(LARGURA//2-75, 350, 150, 50)
                    if voltar_rect.collidepoint(pos):
                        self.estado = "menu"
                        
            elif evento.type == pygame.KEYDOWN and self.estado == "jogando":
                if evento.key == pygame.K_RETURN:
                    self.verificar_palpite()
                elif evento.key == pygame.K_BACKSPACE:
                    self.entrada = self.entrada[:-1]
                elif evento.unicode.isdigit() and len(self.entrada) < 3:
                    self.entrada += evento.unicode
                    
        return True

# Loop principal
def main():
    jogo = JogoAdivinhacao()
    clock = pygame.time.Clock()
    rodando = True
    
    while rodando:
        rodando = jogo.processar_eventos()
        jogo.desenhar()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
