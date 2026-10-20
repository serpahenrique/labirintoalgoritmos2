# Labirinto 10 × 10 — DFS, BFS e Busca Gulosa

Compara três algoritmos de busca para ir do início (`I`) à saída (`F`) de um labirinto 10 × 10. Para executar: `python labirinto.py`.

| Algoritmo | Caminho (casas) | Casas visitadas |
|---|---:|---:|
| DFS | 23 | 23 |
| BFS | **19** | 59 |
| Busca Gulosa | 23 | 23 |

## BFS × DFS

A BFS explora por camadas de distância, então a primeira vez que alcança a saída é pelo menor caminho. A DFS testa "direita" antes de "baixo", entra no corredor da linha 0 e segue por ele até a saída sem nunca testar a rota mais curta.

## Onde a parede enganou a Gulosa

Em (0, 2), descer e ir para a direita tinham a mesma heurística, e o empate levou a Gulosa pela linha 0. Em (2, 8), a parede `###` da linha 3 bloqueou a descida e a obrigou a contornar 2 casas para a esquerda e 2 de volta: são as 4 casas a mais em relação à BFS.

## Conclusão

A BFS garante o menor caminho, mas explora muito mais. A DFS e a Gulosa visitam menos casas, mas não garantem o caminho mais curto.
