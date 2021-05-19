# INF1771
Repositório referente aos trabalhos da matéria INF1771 - Inteligência Artificial, composto pela nata da nata da PUC-Rio.


## Jornada Pokémon
![Image](https://github.com/lucasximenes/supreme-parakeet/blob/main/headers/kantoheader.jpg)

O vídeo de apresentação está disponível no Google Drive, [nesse link](https://drive.google.com/file/d/1MCet1EriEPcBvyISA1P5r0o4WjqkXB3k/view?usp=sharing).

[*(Queriamos agradecer essx designer pelos ótimos vetores os quais usamos nos slides! :D)*](https://www.vecteezy.com/members/originalme2)
## Conteúdo:
- ./main.py: script contém os algoritmos de A* (para os caminhos) e Branch and Bound (para as batalhas). Ele lê um arquivo de texto com informações sobre o mapa e cria um arquivo path.txt, com as coordernadas do caminho ótimo. Logo em seguida, ele executa o algoritmo de Branch and Bound para calcular a melhor combinação de times para as batalhas.
- ./genetic_algorithm.py: script contém a implementação de algoritmo genético que usamos para encontrar um bom resultado para o problema das batalhas
- ./src/: contém os arquivos da implementação da nossa interface, em JavaScript


## Instruções:
- **Scripts Python**: no caso do script principal, basta rodar e seguir as instruções do script. O script genético já tem as informações no código, então não precisa de entradas.

- **Interface**: a interface precisa ser acessada em um servidor. Recomendamos a extensão Live Server, do VSCode. Mas qualquer outra opção resolveria. Para usá-la, basta acessar o site e um prompt irá pedir as informações do mapa (as mesmas que passamos para o script principal) e, em seguida, pede o caminho (que está no arquivo path.txt, criado pelo script).

## Akinator

