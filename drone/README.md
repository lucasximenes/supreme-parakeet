# Trabalho 4 - IA

O nosso drone utilizou uma máquina de estados para percorrer o mapa, pegar itens e reagir aos inimigos.

Nossa máquina de estado tem 5 estados:

- Inimigo na reta: quando tem um inimigo na frente do bot ele começa a atirar

- Levando dano, porém sem ter inimigo na frente: nesse caso o nosso bot faz uma curva a direita para fugir

- Pegar itens: quando encontra uma luz azul ele usa os comandos para se pegar um anel/ouro e quando encontra uma luz vermelha ele pega o power up se não está com 100% de vida

- Percorrer mapa: percorre mapa dando prioridade a locais desconhecidos e a retas onde ele tem conhecimento que há um tesouro



## Percorrendo mapa:

Ao percorrer o mapa, o bot faz uso de uma matriz que criamos chamada botCompass que mapeia tiles adjacentes que encontram-se obstruídos(podendo ser por paredes, buracos, teleportes, ...). Ao ter o botCompass bloqueado para frente ele faz uma decisão randomica se vai dar prioridade a girar para a esquerda ou para direita. Se ambas as direções também estiverem ocupadas, o bot anda para trás.

O mapa do jogo é anotado em uma matriz que começa povoada de caracteres "?" que representam tiles desconhecidos e que vão sendo substituídos por caracteres que tem significados atribuídos:
- "X": buraco
- "H": powerup
- "W": parede
- "T": tesouro
- ".": tile vazio, porem conhecido

Ao estar prestes a entrar em um tile conhecido e vazio, porém com um tile desconhecido na lateral, o bot opta por conhecer esse tile desconhecido.

Ao estar rodeado por tiles conhecidos, o bot checa se tem algum tesouro ou powerup(caso sua vida não esteja completa) na sua horizontal e vertical.

## Reagindo ao inimigo:

Ao ouvir passos o nosso bot fica girando para a direita para tentar encontrar o inimigo. Depois de 10 giros ele desiste e anda para a frente.

Se tiver algum inimigo na frente ele atira, mas depois de 30 tiros ele para de atirar e se move.



### O que tentamos fazer, mas sem êxito:

Tentamos colocar o algoritmo de busca A* para buscar itens conhecidos no mapa, entretanto tivemos dificuldades. A implementação do A* se encontra no arquivo ```astar.py```. A ideia era manter uma lista com os tesouros conhecidos disponíveis e usar o algoritmo para encontrar o menor caminho até eles em momento de ócio, considerando até o tempo de respawn deles.