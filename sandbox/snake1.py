import turtle
import time
import random

# --- Configurações Iniciais ---
delay = 0.1  # Atraso para controlar a velocidade do jogo
score = 0
high_score = 0

# Configuração da Tela
tela = turtle.Screen()
tela.title("O Jogo da Cobrinha em Python")
tela.bgcolor("green")
tela.setup(width=600, height=600)
tela.tracer(0)  # Desliga a atualização automática da tela

# Cabeça da Cobrinha
cabeca = turtle.Turtle()
cabeca.speed(0)  # Velocidade de animação (máxima)
cabeca.shape("circle")
cabeca.color("black")
cabeca.penup()
cabeca.goto(0, 0)
cabeca.direction = "stop"

# Comida (Food)
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup()
comida.goto(0, 100)

# Placar (Scoreboard)
placar = turtle.Turtle()
placar.speed(0)
placar.shape("square")
placar.color("white")
placar.penup()
placar.hideturtle()
placar.goto(0, 260)
placar.write("Pontuação: 0  Recorde: 0", align="center", font=("Courier", 24, "normal"))

# Lista de Segmentos do Corpo
segmentos = []

# --- Funções de Movimento ---
def ir_cima():
    if cabeca.direction != "down":
        cabeca.direction = "up"

def ir_baixo():
    if cabeca.direction != "up":
        cabeca.direction = "down"

def ir_esquerda():
    if cabeca.direction != "right":
        cabeca.direction = "left"

def ir_direita():
    if cabeca.direction != "left":
        cabeca.direction = "right"

def mover():
    if cabeca.direction == "up":
        y = cabeca.ycor()
        cabeca.sety(y + 20)
    if cabeca.direction == "down":
        y = cabeca.ycor()
        cabeca.sety(y - 20)
    if cabeca.direction == "left":
        x = cabeca.xcor()
        cabeca.setx(x - 20)
    if cabeca.direction == "right":
        x = cabeca.xcor()
        cabeca.setx(x + 20)

# --- Funções de Controle de Teclas ---
tela.listen()
tela.onkeypress(ir_cima, "Up")      # Seta para cima
tela.onkeypress(ir_baixo, "Down")    # Seta para baixo
tela.onkeypress(ir_esquerda, "Left")  # Seta para esquerda
tela.onkeypress(ir_direita, "Right") # Seta para direita

# --- Loop Principal do Jogo ---
while True:
    tela.update()  # Atualiza a tela

    # 1. Checa Colisão com a Borda
    if cabeca.xcor() > 290 or cabeca.xcor() < -290 or cabeca.ycor() > 290 or cabeca.ycor() < -290:
        time.sleep(1)  # Pausa
        cabeca.goto(0, 0)
        cabeca.direction = "stop"

        # Esconde os segmentos
        for segmento in segmentos:
            segmento.goto(1000, 1000) # Move para fora da tela

        # Limpa a lista de segmentos
        segmentos.clear()
        
        # Reseta a pontuação
        score = 0
        delay = 0.1
        placar.clear()
        placar.write(f"Pontuação: {score}  Recorde: {high_score}", align="center", font=("Courier", 24, "normal"))

    # 2. Checa Colisão com a Comida
    if cabeca.distance(comida) < 20:
        # Move a comida para um lugar aleatório
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        comida.goto(x, y)

        # Adiciona um novo segmento ao corpo
        novo_segmento = turtle.Turtle()
        novo_segmento.speed(0)
        novo_segmento.shape("square")
        novo_segmento.color("gray")
        novo_segmento.penup()
        segmentos.append(novo_segmento)

        # Acelera o jogo e aumenta a pontuação
        delay -= 0.001
        score += 10

        if score > high_score:
            high_score = score
        
        placar.clear()
        placar.write(f"Pontuação: {score}  Recorde: {high_score}", align="center", font=("Courier", 24, "normal"))

    # 3. Move os Segmentos do Corpo
    # Move os segmentos na ordem reversa, do final para o início
    for index in range(len(segmentos) - 1, 0, -1):
        x = segmentos[index-1].xcor()
        y = segmentos[index-1].ycor()
        segmentos[index].goto(x, y)

    # Move o segmento 0 (o mais próximo da cabeça) para a posição da cabeça
    if len(segmentos) > 0:
        x = cabeca.xcor()
        y = cabeca.ycor()
        segmentos[0].goto(x, y)

    mover()

    # 4. Checa Colisão com o Próprio Corpo
    for segmento in segmentos:
        if segmento.distance(cabeca) < 20:
            time.sleep(1)
            cabeca.goto(0, 0)
            cabeca.direction = "stop"

            # Esconde os segmentos
            for seg in segmentos:
                seg.goto(1000, 1000)
            
            # Limpa a lista de segmentos
            segmentos.clear()
            
            # Reseta a pontuação
            score = 0
            delay = 0.1
            placar.clear()
            placar.write(f"Pontuação: {score}  Recorde: {high_score}", align="center", font=("Courier", 24, "normal"))

    time.sleep(delay) # Controla a velocidade do jogo

# Mantém a janela aberta
tela.mainloop()