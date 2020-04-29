## Bomberman

Descrição: Jogo de classe de bomberman com single/multi player. Testando em Python 3.8.1

Instruções: Para executar o jogo, digite o seguinte comando

python main.py

# Multijogador
Para executar isso, é um pouco mais complicado. Atualmente, está definido para ser executado no host local.
Essa configuração pode ser modificada no arquivo config.py. Para executá-lo no seu servidor,
altere LOCALHOST = True para LOCALHOST = False. O server, admin e o game estão atualmente
definido como localhost. Esses valores teriam que ser alterados também.

Supondo que estamos no localhost. Você precisará executar duas instâncias separadas do jogo.

# Execute o servidor
python server.py

# Inicie as duas instâncias dos jogos, entre no multiplayer
python bomberman/main.py
python bomberman2/main.py

# Execute o admin para iniciar o jogo multiplayer
python bomberman/admin.py

Pressione 8 para iniciar o jogo

-----------------------------------------------

# Teclas
Teclas de seta para mover
Barra de espaço para colocar bomba
G é um cheat/secreto. Adiciona 1 bomba e 1 poder

# Tela principal
- Single Player
  = Um jogador, atualmente definido para ter 2 estágios com 6 níveis por estágio.

- Multi Player
  = Bomberman multiplayer que suporta até 4 jogadores através de uma conexão TCP. este
    pode ser jogado via local

- Instruções
  = Não implementado

- Pontos
  = Isso exibe todas as pontuações mais altas para um jogador.

- Exit/Sair
  = Encerra o aplicativo.

-----------------------------------------------

BUGS

- Explosão não mata quando você fica em uma bomba
- A bomba não aparece quando você pressiona a barra de espaço
- Atraso na animação quando a bomba explode/o jogador se move
- Quando você se depara com um inimigo, ele não redesenha
- O temporizador acaba, sem cálculos
- Cálculos de estágio, após 2-6, ele trava
- Pressionar as teclas não gira se o jogador não puder se mover para essa posição
- Multiplayer, sem game over?


## Menu
![Main](/images/menu.png)

## Game
![Main](/images/game.png)
