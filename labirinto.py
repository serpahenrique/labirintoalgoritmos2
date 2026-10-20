import heapq
from collections import deque

# Labirinto usado nas buscas. Pode ser editado a vontade, desde que
# tenha um simbolo de entrada e um de saida.
LABIRINTO = """
E..#......
.#.#.####.
.#...#....
.###.#.##.
.....#..#.
##.####.#.
...#....#.
.#.#.##.##
.#...#....
...#.#.#.S
"""

SIMBOLO_ENTRADA = 'E'
SIMBOLO_SAIDA = 'S'
SIMBOLO_PAREDE = '#'
SIMBOLO_LIVRE = '.'
SIMBOLO_PERCURSO = 'o'

# cima, direita, baixo, esquerda
DIRECOES = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def carregar_labirinto(texto):
    labirinto = []
    for linha_texto in texto.strip().split('\n'):
        labirinto.append(list(linha_texto))

    posicoes_livres = set()
    posicao_entrada = None
    posicao_saida = None

    for numero_linha in range(len(labirinto)):
        for numero_coluna in range(len(labirinto[numero_linha])):
            simbolo = labirinto[numero_linha][numero_coluna]
            if simbolo == SIMBOLO_PAREDE:
                continue
            posicoes_livres.add((numero_linha, numero_coluna))
            if simbolo == SIMBOLO_ENTRADA:
                posicao_entrada = (numero_linha, numero_coluna)
            if simbolo == SIMBOLO_SAIDA:
                posicao_saida = (numero_linha, numero_coluna)

    return labirinto, posicoes_livres, posicao_entrada, posicao_saida


def buscar_vizinhos(posicao, posicoes_livres):
    numero_linha, numero_coluna = posicao
    vizinhos = []
    for deslocamento_linha, deslocamento_coluna in DIRECOES:
        vizinho = (numero_linha + deslocamento_linha, numero_coluna + deslocamento_coluna)
        if vizinho in posicoes_livres:
            vizinhos.append(vizinho)
    return vizinhos


def montar_percurso(veio_de, posicao_saida):
    if posicao_saida not in veio_de:
        return []
    percurso = []
    posicao_atual = posicao_saida
    while posicao_atual is not None:
        percurso.append(posicao_atual)
        posicao_atual = veio_de[posicao_atual]
    percurso.reverse()
    return percurso


def busca_em_profundidade(posicoes_livres, posicao_entrada, posicao_saida):
    pilha = [(posicao_entrada, None)]
    veio_de = {}

    while len(pilha) > 0:
        posicao_atual, posicao_anterior = pilha.pop()
        if posicao_atual in veio_de:
            continue
        veio_de[posicao_atual] = posicao_anterior

        if posicao_atual == posicao_saida:
            break

        for vizinho in buscar_vizinhos(posicao_atual, posicoes_livres):
            if vizinho not in veio_de:
                pilha.append((vizinho, posicao_atual))

    return montar_percurso(veio_de, posicao_saida), len(veio_de)


def busca_em_largura(posicoes_livres, posicao_entrada, posicao_saida):
    fila = deque()
    fila.append(posicao_entrada)
    veio_de = {posicao_entrada: None}

    while len(fila) > 0:
        posicao_atual = fila.popleft()
        if posicao_atual == posicao_saida:
            break

        for vizinho in buscar_vizinhos(posicao_atual, posicoes_livres):
            if vizinho not in veio_de:
                veio_de[vizinho] = posicao_atual
                fila.append(vizinho)

    return montar_percurso(veio_de, posicao_saida), len(veio_de)


def distancia_manhattan(posicao_origem, posicao_destino):
    distancia_linhas = abs(posicao_origem[0] - posicao_destino[0])
    distancia_colunas = abs(posicao_origem[1] - posicao_destino[1])
    return distancia_linhas + distancia_colunas


def busca_gulosa(posicoes_livres, posicao_entrada, posicao_saida):
    fila_prioridade = []
    heapq.heappush(fila_prioridade, (distancia_manhattan(posicao_entrada, posicao_saida), posicao_entrada))
    veio_de = {posicao_entrada: None}
    visitadas = set()

    while len(fila_prioridade) > 0:
        item_retirado = heapq.heappop(fila_prioridade)
        posicao_atual = item_retirado[1]
        if posicao_atual in visitadas:
            continue
        visitadas.add(posicao_atual)

        if posicao_atual == posicao_saida:
            break

        for vizinho in buscar_vizinhos(posicao_atual, posicoes_livres):
            if vizinho in visitadas:
                continue
            if vizinho not in veio_de:
                veio_de[vizinho] = posicao_atual
            distancia_vizinho = distancia_manhattan(vizinho, posicao_saida)
            heapq.heappush(fila_prioridade, (distancia_vizinho, vizinho))

    return montar_percurso(veio_de, posicao_saida), len(visitadas)


def desenhar_percurso(labirinto, percurso):
    desenho = []
    for linha in labirinto:
        desenho.append(linha.copy())

    for numero_linha, numero_coluna in percurso:
        if desenho[numero_linha][numero_coluna] == SIMBOLO_LIVRE:
            desenho[numero_linha][numero_coluna] = SIMBOLO_PERCURSO

    linhas_texto = []
    for linha in desenho:
        linhas_texto.append(''.join(linha))
    return '\n'.join(linhas_texto)


def main():
    labirinto, posicoes_livres, posicao_entrada, posicao_saida = carregar_labirinto(LABIRINTO)

    buscas = [
        ('Profundidade (DFS)', busca_em_profundidade),
        ('Largura (BFS)', busca_em_largura),
        ('Gulosa', busca_gulosa),
    ]

    resultados = []
    for nome_busca, funcao_busca in buscas:
        percurso, quantidade_visitadas = funcao_busca(posicoes_livres, posicao_entrada, posicao_saida)
        resultados.append((nome_busca, percurso, quantidade_visitadas))
        print('=== ' + nome_busca + ' ===')
        print(desenhar_percurso(labirinto, percurso))
        print()

    print('=== Comparacao entre as buscas ===')
    for nome_busca, percurso, quantidade_visitadas in resultados:
        print(nome_busca + ': tamanho do percurso = ' + str(len(percurso))
              + ', posicoes visitadas = ' + str(quantidade_visitadas))


if __name__ == '__main__':
    main()
