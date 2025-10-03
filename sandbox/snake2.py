import pygame
import random
import time

pygame.init()

# --- Configurações da Tela ---
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Cobrinha")

# --- Cores ---
preto = (0, 0, 0)
branco = (255, 255, 255)
verde = (0, 255, 0)
vermelho = (255, 0, 0)

# --- Jogo ---
tamanho_bloco = 20
velocidade_cobra = 15

fonte = pygame.font.SysFont("comicsansms", 35)

def mostrar_mensagem(msg, cor):
    texto = fonte.render(msg, True, cor)
    tela.blit(texto, [largura / 6, altura / 3])

def desenhar_cobra(tamanho_bloco, lista_cobra):
    for x in lista_cobra:
        pygame.draw.rect(tela, verde, [x[0], x[1], tamanho_bloco, tamanho_bloco])

def loop_jogo():
    jogo_finalizado = False
    fim_de_jogo = False

    # Posição inicial da cobra
    x1 = largura / 2
    y1 = altura / 2
    
    # Mudança de posição
    x1_muda = 0
    y1_muda = 0

    lista_cobra = []
    tamanho_cobra = 1

    # Posição inicial da comida
    comida_x = round(random.randrange(0, largura - tamanho_bloco) / 20.0) * 20.0
    comida_y = round(random.randrange(0, altura - tamanho_bloco) / 20.0) * 20.0

    relogio = pygame.time.Clock()

    while not jogo_finalizado:
        
        while fim_de_jogo == True:
            tela.fill(preto)
            mostrar_mensagem("Você perdeu! Pressione C para jogar de novo ou Q para sair.", vermelho)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        jogo_finalizado = True
                        fim_de_jogo = False
                    if evento.key == pygame.K_c:
                        loop_jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_finalizado = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x1_muda = -tamanho_bloco
                    y1_muda = 0
                elif evento.key == pygame.K_RIGHT:
                    x1_muda = tamanho_bloco
                    y1_muda = 0
                elif evento.key == pygame.K_UP:
                    y1_muda = -tamanho_bloco
                    x1_muda = 0
                elif evento.key == pygame.K_DOWN:
                    y1_muda = tamanho_bloco
                    x1_muda = 0

        # Verifica colisão com as bordas
        if x1 >= largura or x1 < 0 or y1 >= altura or y1 < 0:
            fim_de_jogo = True
        
        x1 += x1_muda
        y1 += y1_muda
        tela.fill(preto)
        
        # Desenha a comida
        pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])
        
        # Lógica para o corpo da cobra
        cabeca_cobra = []
        cabeca_cobra.append(x1)
        cabeca_cobra.append(y1)
        lista_cobra.append(cabeca_cobra)

        if len(lista_cobra) > tamanho_cobra:
            del lista_cobra[0]

        # Verifica colisão da cobra com ela mesma
        for segmento in lista_cobra[:-1]:
            if segmento == cabeca_cobra:
                fim_de_jogo = True
        
        desenhar_cobra(tamanho_bloco, lista_cobra)
        
        pygame.display.flip()

        # Lógica de crescimento da cobra
        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, largura - tamanho_bloco) / 20.0) * 20.0
            comida_y = round(random.randrange(0, altura - tamanho_bloco) / 20.0) * 20.0
            tamanho_cobra += 1

        relogio.tick(velocidade_cobra)

    pygame.quit()
    quit()

loop_jogo()