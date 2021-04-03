'''
TODO/Questionamentos:
Q: Será que precisa de uma lista de adjacências? A gente sabe que a partir de uma posição (i,j) só da pra ir
(i+1, j), (i, j+1), (i-1, j) e (i, j-1), talvez isso exclua a necessidade de representar um grafo e fazer tudo
pela matriz que guarda o "mapa".
1.
'''

class Game:
    def __init__(self):
        self.map = []
        self.bases = []
        self.pokemons = {'Pikachu': 1.5, 'Bulbassauro': 1.4, 'Rattata': 1.3,
        'Caterpie': 1.2, 'Weedle': 1.1}
        for i in range(12):
            if i < 10:
                self.bases.append(55 + i*5)
            else:
                self.bases.append(55 + (i+1)*5)
    
    def setPokeStrenght(self, pokemon: str, val: float):
        self.pokemons[pokemon] = val
    
    def setBaseDifficulty(self, base: int, difficulty: int):
        self.bases[base-1] = difficulty

    def read_map(self):
        path = input()
        f = open(path, "r")
        for line in f:
            self.mapa.append(line)
        f.close()



