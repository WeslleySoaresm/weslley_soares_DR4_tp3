import pandas as pd
from sqlalchemy import create_engine, text
#Exercício 1 Importação de arquivos Excel/CSV com Pandas

# Carregar o arquivo CSV
df20 = pd.read_csv("players_20.csv")
df21 = pd.read_csv("players_21.csv")

# Mostrar as 5 primeiras linhas
print("=== Cinco primeiras linhas ===")
print(df20.head())

# Exibir as colunas disponíveis
print("\n=== Colunas disponíveis ===")
print(df20.columns.tolist())

# Mostrar o número total de registros
print("\n=== Número total de registros ===")
print(len(df20))

"""
Exercício 2 Selecionar 20 jogadores âncora em um único DataFrame 
Contexto:
Modders precisam isolar um conjunto fixo de jogadores para manter comparações consistentes entre anos. A fonte é o arquivo players_20.csv. O artefato é um programa Python que filtra os 20 jogadores âncora. O impacto esperado é preparar uma base enxuta para análises posteriores.
Enunciado:
Carregue players_20.csv e filtre apenas os jogadores da lista âncora.
Crie um DataFrame chamado df20_anchor_20.
Exiba o tamanho final da tabela.
"""


#lista de jogadores âncora 
anchor_players = [
    "Cristiano Ronaldo",
    "Lionel Messi",
    "Neymar Jr",
    "Kylian Mbappé",
    "Kevin De Bruyne",
    "Mohamed Salah",
    "Robert Lewandowski",
    "Sergio Ramos",
    "Virgil van Dijk",
    "Luka Modric",
    "Toni Kroos",
    "Eden Hazard",
    "Luis Suárez",
    "Manuel Neuer",
    "Harry Kane",
    "Paulo Dybala",
    "Giorgio Chiellini",
    "Karim Benzema",
    "Antoine Griezmann",
    "Marc-André ter Stegen"
]

#filtrando apenas od jogadores âncora
df20_anchor_20 = df20[df20["long_name"].isin(anchor_players)]


# Exibir o tamanho final da tabela
print("Número de registros no df20_anchor_20:", len(df20_anchor_20))

# Mostrar as primeiras linhas para validar
print(df20_anchor_20.head())

"""Exercício 3 Combinar dados de anos diferentes
Contexto:
Analistas de atributos precisam estudar a evolução de overall e potencial de um jogador ao longo dos anos. Os dados vêm dos arquivos players_20.csv e players_21.csv. O artefato é um programa Python que combina tabelas utilizando merge. O impacto esperado é permitir comparações históricas.
Enunciado:
Carregue players_20.csv e players_21.csv.
Filtre apenas os jogadores âncora em ambos os DataFrames.
Realize um merge pelos campos short_name e long_name.
Crie um DataFrame consolidado contendo overall e potential para cada ano.
"""

# Filtrar apenas jogadores âncora
df20_anchor = df20[df20["long_name"].isin(anchor_players)]
df21_anchor = df21[df21["long_name"].isin(anchor_players)]

# Selecionar colunas relevantes
df20_anchor = df20_anchor[["short_name", "long_name", "overall", "potential"]].copy()
df21_anchor = df21_anchor[["short_name", "long_name", "overall", "potential"]].copy()

# Renomear colunas para diferenciar os anos
df20_anchor.rename(columns={"overall": "overall_20", "potential": "potential_20"}, inplace=True)
df21_anchor.rename(columns={"overall": "overall_21", "potential": "potential_21"}, inplace=True)

# Merge pelos campos short_name e long_name
df_anchor_merge = pd.merge(
    df20_anchor,
    df21_anchor,
    on=["short_name", "long_name"],
    how="inner"
)

# Exibir resultado
print("Número de registros no DataFrame consolidado:", len(df_anchor_merge))
print(df_anchor_merge.head())


"""
Exercício 4 Encontrar jogadores que aparecem em todos os anos disponíveis
Contexto:
A comunidade FIFA exige criar análises contínuas com jogadores presentes em todos os anos. A fonte são arquivos de vários anos da franquia. O artefato é um script que cruza registros entre anos para encontrar interseções. O impacto esperado é maior consistência nos comparativos.
Enunciado:
Carregue players_20.csv e players_21.csv.
Crie dois conjuntos contendo os nomes dos jogadores.
Encontre a interseção e salve-a em uma lista chamada jogadores_comuns.
Exiba os dez primeiros nomes comuns.
    """
    
    
# Criar conjuntos com os nomes dos jogadores
jogadores_20 = set(df20["long_name"])
jogadores_21 = set(df21["long_name"])

# Encontrar a interseção
jogadores_comuns = list(jogadores_20.intersection(jogadores_21))

# Exibir os 10 primeiros nomes comuns
print("Jogadores comuns entre 2020 e 2021 (primeiros 10):")
print(jogadores_comuns[:10])



"""Exercício 5 Criar banco SQL em memória e armazenar jogadores âncora 
Contexto:
Modders com conhecimento avançado criam pequenos bancos internos para consultas rápidas. Os dados vêm de players_20.csv. O artefato é um banco SQLite em memória conectado via SQLAlchemy. O impacto esperado é permitir consultas SQL sem arquivos externos.
Enunciado:
Carregue players_20.csv.
Filtre apenas jogadores âncora.
Crie um banco em memória com SQLAlchemy.
Grave o DataFrame na tabela jogadores_20.
Leia novamente com SQL e exiba cinco registros."""

# 2. Filtrar apenas jogadores âncora
df_anchor_20 = df20[df20["long_name"].isin(anchor_players)]

# 3. Criar banco SQLite em memória
engine = create_engine("sqlite:///:memory:")

# 4. Gravar DataFrame na tabela jogadores_20
df_anchor_20.to_sql("jogadores_20", engine, index=False, if_exists="replace")

# 5. Ler novamente com SQL e exibir cinco registros
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jogadores_20 LIMIT 5"))
    rows = result.fetchall()

# Exibir resultado
for row in rows:
    print(row)

"""Exercício 6 Consultar atributos específicos via SQL 
Contexto:
A análise técnica exige que os modders obtenham rapidamente atributos como pace, shooting e defense. O banco SQL criado no exercício anterior será usado. O artefato é uma consulta SQL. O impacto esperado é reforçar a habilidade de acessar bases tabulares via SQL.
Enunciado:Utilize o banco criado no exercício anterior. 
Execute uma consulta que retorne short_name, pace, shooting e defending dos jogadores âncora.
Converta a resposta para DataFrame e imprima o resultado."""

# Consulta SQL para atributos específicos
sql = text("""
    SELECT short_name, pace, shooting, defending
    FROM jogadores_20
""")

# Executar consulta e converter para DataFrame
with engine.connect() as conn:
    result = conn.execute(sql)
    df_atributos = pd.DataFrame(result.fetchall(), columns=result.keys())

# Exibir resultado
print("=== Atributos dos jogadores âncora ===")
print(df_atributos.head())


"""Exercício 7 Gerar uma tabela consolidada de médias por posição 
Contexto:
Estatísticos amadores procuram identificar como as posições evoluem no jogo. A fonte é players_20.csv. O artefato é um DataFrame agrupado pela coluna player_positions. O impacto esperado é servir como base para discussões em fóruns de modding.
Enunciado:
Carregue players_20.csv.
Agrupe por player_positions.
Calcule média de overall, potential e age.
Exiba o DataFrame final ordenado pelo overall médio."""

# 2. Agrupar por player_positions e calcular médias
df_grouped = (
    df20.groupby("player_positions")[["overall", "potential", "age"]]
    .mean()
    .reset_index()
)

# 3. Ordenar pelo overall médio (coluna "overall")
df_grouped = df_grouped.sort_values(by="overall", ascending=False)

# 4. Exibir resultado
print("=== Médias por posição (ordenado por overall) ===")
print(df_grouped.head(10))  # mostra as 10 primeiras posições





"""Exercício 8 Comparar distribuições entre anos
Contexto:
Criadores de conteúdo de análise tática fazem vídeos comparando médias globais entre anos do FIFA. A fonte são players_20.csv e players_21.csv. O artefato é um DataFrame final contendo médias das principais estatísticas por ano. O impacto esperado é permitir visualização clara das mudanças anuais.
Enunciado:
Carregue players_20.csv e players_21.csv.
Calcule as médias globais de overall, potential e age em cada ano.
Crie um DataFrame resumo chamado df_comparacao_anos.
Imprima o resultado."""


# 2. Calcular médias globais de cada ano
media_20 = {
    "ano": 2020,
    "overall": df20["overall"].mean(),
    "potential": df20["potential"].mean(),
    "age": df20["age"].mean()
}

media_21 = {
    "ano": 2021,
    "overall": df21["overall"].mean(),
    "potential": df21["potential"].mean(),
    "age": df21["age"].mean()
}

# 3. Criar DataFrame resumo
df_comparacao_anos = pd.DataFrame([media_20, media_21])

# 4. Exibir resultado
print("=== Comparação de médias globais entre anos ===")
print(df_comparacao_anos)


"""Exercício 9 Exportar DataFrame para SQL e recuperar com outra consulta 
Contexto:
Modders que criam ferramentas externas precisam exportar bases temporárias para SQL para uso posterior. A fonte é players_21.csv. O artefato é a gravação de uma tabela e sua leitura com filtros. O impacto esperado é ensinar persistência em SQL no fluxo de dados.
Enunciado:
Carregue players_21.csv.
Grave no banco em memória com o nome jogadores_21.
Leia apenas jogadores com overall acima de 88 via SQL.
Mostre os resultados."""

# 3. Gravar DataFrame na tabela jogadores_21
df21.to_sql("jogadores_21", engine, index=False, if_exists="replace")

# 4. Consulta SQL: jogadores com overall acima de 88
sql = text("""
    SELECT short_name, long_name, overall, potential, age
    FROM jogadores_21
    WHERE overall > 88
    ORDER BY overall DESC
""")

# 5. Executar consulta e converter para DataFrame
with engine.connect() as conn:
    result = conn.execute(sql)
    df_top_players = pd.DataFrame(result.fetchall(), columns=result.keys())

# 6. Mostrar resultados
print("=== Jogadores com overall acima de 88 ===")
print(df_top_players)


"""Exercício 10 Criar um banco SQL com múltiplas tabelas 
Contexto:
Alguns membros da comunidade criam bancos complexos para armazenar ratings de diferentes anos. A fonte são players_20.csv e players_21.csv. O artefato é um banco SQL em memória contendo duas tabelas. O impacto esperado é simular organização profissional.
Enunciado:
Carregue players_20.csv e players_21.csv.
Armazene cada um em uma tabela separada no banco.
Use SQL para retornar 100 jogadores que aparecem nos dois anos.
Exiba o resultado."""



# 3. Gravar cada DataFrame em uma tabela separada
df20.to_sql("jogadores_20", engine, index=False, if_exists="replace")
df21.to_sql("jogadores_21", engine, index=False, if_exists="replace")

# 4. Consulta SQL: jogadores que aparecem nos dois anos
sql = text("""
    SELECT j20.short_name, j20.long_name, j20.overall AS overall_20, j21.overall AS overall_21
    FROM jogadores_20 j20
    INNER JOIN jogadores_21 j21
        ON j20.long_name = j21.long_name
    LIMIT 100;
""")

# 5. Executar consulta e converter para DataFrame
with engine.connect() as conn:
    result = conn.execute(sql)
    df_comuns = pd.DataFrame(result.fetchall(), columns=result.keys())

# 6. Exibir resultado
print("=== 100 jogadores que aparecem nos dois anos ===")
print(df_comuns.head(100))  # mostra os primeiros 20 para validar

"""Exercício 11 Consolidar atributos de 20 jogadores âncora entre anos diferentes
Contexto:
A comunidade costuma publicar comparativos de evolução anual focados em jogadores famosos. A fonte são players_20.csv e players_21.csv. O artefato é um DataFrame que unifica atributos essenciais. O impacto esperado é fornecer uma base visual para vídeos e análises.
Enunciado:
Carregue os dois CSV.
Filtre os 20 jogadores âncora em cada arquivo.
Crie um DataFrame consolidado com as colunas short_name, overall_20, overall_21, potential_20 e potential_21.
Mostre o resultado final.
"""

# 2. Filtrar apenas jogadores âncora
df20_anchor = df20[df20["long_name"].isin(anchor_players)][["short_name", "long_name", "overall", "potential"]]
df21_anchor = df21[df21["long_name"].isin(anchor_players)][["short_name", "long_name", "overall", "potential"]]

# 3. Renomear colunas para diferenciar os anos
df20_anchor = df20_anchor.rename(columns={"overall": "overall_20", "potential": "potential_20"})
df21_anchor = df21_anchor.rename(columns={"overall": "overall_21", "potential": "potential_21"})

# 4. Consolidar com merge
df_consolidado = pd.merge(
    df20_anchor,
    df21_anchor,
    on=["short_name", "long_name"],
    how="inner"
)[["short_name", "overall_20", "overall_21", "potential_20", "potential_21"]]

# 5. Exibir resultado final
print("=== DataFrame consolidado de jogadores âncora ===")
print(df_consolidado)

"""Exercício 12 Relatório longitudinal de atributos FIFA 15 a FIFA 21
Contexto:
A comunidade de modders e estatísticos amadores deseja publicar um relatório completo mostrando a evolução dos principais jogadores ao longo de várias edições do FIFA, da versão 2015 até a 2021. Os analistas querem comparar como ratings, potencial e idade mudam ao longo do tempo para um grupo fixo de atletas famosos. A fonte de dados são os arquivos players_15.csv, players_16.csv, players_17.csv, players_18.csv, players_19.csv, players_20.csv e players_21.csv, além da lista de jogadores âncora definida no início do TP. O artefato de destino é um DataFrame final consolidado, pronto para exportação e uso em dashboards ou análises externas. O impacto esperado é simular o fluxo completo de uma pipeline analítica longitudinal, permitindo que a comunidade discuta de forma objetiva como cada jogador evoluiu em sete edições consecutivas do jogo.
Enunciado:
Carregue com Pandas os arquivos players_15.csv, players_16.csv, players_17.csv, players_18.csv, players_19.csv, players_20.csv e players_21.csv em DataFrames separados.
Em cada DataFrame, filtre apenas os jogadores presentes na lista de jogadores âncora definida no início do TP, usando o campo apropriado de identificação de nome (por exemplo short_name).
Para cada ano, crie colunas renomeadas para os atributos principais, como overall_15, potential_15, overall_16, potential_16 e assim sucessivamente até overall_21 e potential_21, preservando também a posição principal e uma informação de idade representativa, como age_21.
Construa um DataFrame consolidado em que cada linha represente um jogador âncora e cada coluna traga as métricas desses sete anos, incluindo pelo menos overall, potential e uma coluna com a posição principal escolhida para análise.
Calcule, para cada jogador, a evolução de overall e de potential entre FIFA 15 e FIFA 21, criando colunas como evolucao_overall_15_21 e evolucao_potential_15_21, que representem a diferença entre os valores finais e iniciais.
Adicione uma coluna categórica chamada tendencia_overall que receba o valor "subiu" quando a evolução de overall for positiva, "caiu" quando for negativa e "estavel" quando a diferença estiver dentro de um intervalo pequeno de variação definido por você no código.
Salve o DataFrame consolidado em um arquivo chamado relatorio_fifa_15_21_sj90.csv.
Imprima na tela o DataFrame final ou um recorte com os principais jogadores e colunas, de forma legível, para que seja possível validar visualmente os resultados da consolidação."""
 
#1) Lista de jogadores âncora 
ANCHOR_PLAYERS = [
    "Cristiano Ronaldo", "Lionel Messi", "Neymar Jr", "Kylian Mbappé",
    "Kevin De Bruyne", "Mohamed Salah", "Robert Lewandowski", "Sergio Ramos",
    "Virgil van Dijk", "Luka Modric", "Toni Kroos", "Eden Hazard",
    "Luis Suárez", "Manuel Neuer", "Harry Kane", "Paulo Dybala",
    "Giorgio Chiellini", "Karim Benzema", "Antoine Griezmann", "Marc-André ter Stegen"
]
# 2) Configurar anos e caminhos
YEARS = [15, 16, 17, 18, 19, 20, 21]
FILE_BY_YEAR = {year: f"players_{year}.csv" for year in YEARS}

# 3) Função para carregar e filtrar por âncora (usando long_name como chave primária; opcional: incluir short_name)
def load_anchor_df(year: int) -> pd.DataFrame:
    path = FILE_BY_YEAR[year]
    df = pd.read_csv(path)

    # Seleção mínima de colunas relevantes por ano
    cols_needed = ["short_name", "long_name", "overall", "potential", "age", "player_positions"]
    existing_cols = [c for c in cols_needed if c in df.columns]
    df = df[existing_cols].copy()

    # Filtrar âncora pelo long_name
    df_anchor = df[df["long_name"].isin(ANCHOR_PLAYERS)].copy()

    # Renomear colunas de atributos por ano
    rename_map = {}
    if "overall" in df_anchor.columns:
        rename_map["overall"] = f"overall_{year}"
    if "potential" in df_anchor.columns:
        rename_map["potential"] = f"potential_{year}"
    df_anchor = df_anchor.rename(columns=rename_map)

    # Padronizar chave de merge (usaremos both: short_name + long_name quando possível)
    return df_anchor

# 4) Carregar e preparar DataFrames por ano
dfs_year = {year: load_anchor_df(year) for year in YEARS}

# 5) Consolidar em um único DataFrame via merges progressivos
# Começa pelo primeiro ano e vai dando merge pelos campos-chave
# Para robustez, usamos ["long_name", "short_name"] quando ambas existem; senão, apenas "long_name".
def merge_keys(df):
    keys = []
    if "long_name" in df.columns:
        keys.append("long_name")
    if "short_name" in df.columns:
        keys.append("short_name")
    return keys or ["long_name"]  # fallback

years_iter = iter(YEARS)
base_year = next(years_iter)
df_consolidado = dfs_year[base_year]

for year in years_iter:
    left_keys = merge_keys(df_consolidado)
    right_keys = merge_keys(dfs_year[year])
    # Garantir mesmas chaves (se faltar, usa interseção viável)
    common_keys = [k for k in left_keys if k in right_keys]
    if not common_keys:
        common_keys = ["long_name"]
    df_consolidado = pd.merge(
        df_consolidado,
        dfs_year[year],
        on=common_keys,
        how="outer",# outer para manter todos âncora e diagnosticar faltas de algum ano
        suffixes=("", f"_{year}")    
    )

# 6) Manter colunas essenciais: nomes, posição principal, idade representativa (do ano 21)
# player_positions pode ter múltiplas posições; aqui mantemos a string original do ano 21 se disponível
# age_21 representativa
if "age" in dfs_year[21].columns:
    df_consolidado = pd.merge(
        df_consolidado,
        dfs_year[21][["long_name", "age"]].rename(columns={"age": "age_21"}),
        on="long_name",
        how="left"
    )

if "player_positions" in dfs_year[21].columns:
    df_consolidado = pd.merge(
        df_consolidado,
        dfs_year[21][["long_name", "player_positions"]].rename(columns={"player_positions": "player_positions_21"}),
        on="long_name",
        how="left"
    )

# 7) Calcular evolução entre 2015 e 2021
# Se algum valor estiver ausente, o resultado pode ser NaN; isso ajuda a diagnosticar jogadores faltantes em algum ano.
df_consolidado["evolucao_overall_15_21"] = df_consolidado.get("overall_21") - df_consolidado.get("overall_15")
df_consolidado["evolucao_potential_15_21"] = df_consolidado.get("potential_21") - df_consolidado.get("potential_15")

# 8) Tendência categórica de overall (limiar de estabilidade: variação absoluta <= 2)
def tendencia_from_delta(delta):
    if pd.isna(delta):
        return "indisponivel"
    if delta > 2:
        return "subiu"
    elif delta < -2:
        return "caiu"
    else:
        return "estavel"

df_consolidado["tendencia_overall"] = df_consolidado["evolucao_overall_15_21"].apply(tendencia_from_delta)

# 9) Ordenar para visualização (por exemplo, pelo overall_21 desc, depois long_name)
sort_cols = [c for c in ["overall_21", "long_name"] if c in df_consolidado.columns]
if sort_cols:
    df_consolidado = df_consolidado.sort_values(by=sort_cols, ascending=[False, True])

# 10) Salvar CSV final
output_file = "relatorio_fifa_15_21_sj90.csv"
df_consolidado.to_csv(output_file, index=False)

# 11) Imprimir recorte legível com principais colunas
principal_cols = [
    "short_name", "long_name",
    "player_positions_21", "age_21",
    "overall_15", "overall_21",
    "potential_15", "potential_21",
    "evolucao_overall_15_21", "evolucao_potential_15_21",
    "tendencia_overall"
]
existing_principal_cols = [c for c in principal_cols if c in df_consolidado.columns]
print("=== Relatório longitudinal: principais colunas ===")
print(df_consolidado[existing_principal_cols].head(20))