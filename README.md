# 📊 Relatórios Longitudinais FIFA (TP3/TP4)

Este repositório contém uma sequência de exercícios práticos em **Python + Pandas + SQLAlchemy**, simulando pipelines analíticos sobre datasets do FIFA (edições 2015 a 2021).  
O objetivo é consolidar técnicas de **ETL, SQL em memória, análise longitudinal e visualização de dados** para uso em modding, dashboards e estudos estatísticos.

---

## 🚀 Estrutura dos Exercícios

### Exercício 1 – Carregar CSV e explorar
- Carregar `players_20.csv` com Pandas.
- Exibir primeiras linhas, colunas disponíveis e número total de registros.

### Exercício 2 – Selecionar jogadores âncora
- Filtrar os 20 jogadores âncora definidos no início do TP.
- Criar `df_anchor_20` e mostrar tamanho final da tabela.

### Exercício 3 – Combinar dados de anos diferentes
- Carregar `players_20.csv` e `players_21.csv`.
- Filtrar jogadores âncora.
- Realizar `merge` pelos campos `short_name` e `long_name`.
- Consolidar `overall` e `potential` de cada ano.

### Exercício 4 – Encontrar jogadores comuns
- Criar conjuntos de nomes de jogadores de 2020 e 2021.
- Calcular interseção (`jogadores_comuns`).
- Exibir os 10 primeiros nomes.

### Exercício 5 – Banco SQL em memória
- Criar banco SQLite em memória com SQLAlchemy.
- Gravar `df_anchor_20` na tabela `jogadores_20`.
- Consultar com SQL e exibir 5 registros.

### Exercício 6 – Consultar atributos específicos
- Usar SQL para retornar `short_name`, `pace`, `shooting`, `defending`.
- Converter resultado para DataFrame Pandas.

### Exercício 7 – Médias por posição
- Agrupar `players_20.csv` por `player_positions`.
- Calcular médias de `overall`, `potential` e `age`.
- Ordenar pelo `overall` médio.

### Exercício 8 – Comparar distribuições entre anos
- Calcular médias globais de `overall`, `potential` e `age` em 2020 e 2021.
- Consolidar em `df_comparacao_anos`.

### Exercício 9 – Exportar DataFrame para SQL
- Gravar `players_21.csv` em tabela `jogadores_21`.
- Consultar jogadores com `overall > 88`.

### Exercício 10 – Banco SQL com múltiplas tabelas
- Criar banco em memória com `jogadores_20` e `jogadores_21`.
- Usar `INNER JOIN` para retornar 100 jogadores presentes nos dois anos.

### Exercício 11 – Consolidar atributos âncora
- Filtrar jogadores âncora em 2020 e 2021.
- Criar DataFrame com `overall_20`, `overall_21`, `potential_20`, `potential_21`.

### Exercício 12 – Relatório longitudinal FIFA 15–21
- Carregar `players_15.csv` até `players_21.csv`.
- Filtrar jogadores âncora.
- Consolidar atributos `overall`, `potential`, `age` e posição principal.
- Calcular evolução (`evolucao_overall_15_21`, `evolucao_potential_15_21`).
- Criar coluna categórica `tendencia_overall` (`subiu`, `caiu`, `estavel`).
- Exportar para `relatorio_fifa_15_21_sj90.csv`.

---

## 🛠️ Tecnologias utilizadas
- **Python 3.13**
- **Pandas** para manipulação de dados
- **SQLAlchemy** para integração SQL
- **SQLite em memória** para consultas rápidas
- **Jupyter/VS Code (#%%)** para execução modular

---

## 📌 Exemplos de uso

### Carregar e filtrar jogadores âncora
```python
import pandas as pd

anchor_players = ["Cristiano Ronaldo", "Lionel Messi", "Neymar Jr", "Kylian Mbappé", ...]
df = pd.read_csv("players_20.csv")
df_anchor_20 = df[df["long_name"].isin(anchor_players)]
print(df_anchor_20.head())
