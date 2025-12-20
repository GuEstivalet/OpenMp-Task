import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ===============================
# Configurações Estéticas
# ===============================
sns.set(style="whitegrid", context="talk", font_scale=1.0)
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

# ===============================
# 1. Carregar Dados
# ===============================
FILE_NAME = "csv/resultados_tarefa_a.csv"

if not os.path.exists(FILE_NAME):
    print(f"ERRO: Arquivo '{FILE_NAME}' não encontrado.")
    print("Execute o script 'run.sh' antes de plotar.")
    exit()

df = pd.read_csv(FILE_NAME)

# Verificar se temos os dados esperados (N=1M, K=28, Threads=16)
# Filtramos apenas para garantir, caso o CSV tenha "sujeira" de testes anteriores
df = df[
    (df['N'] == 500000) & 
    (df['K'] == 28) & 
    (df['Threads'] == 4)
]

if df.empty:
    print("ERRO: O CSV existe mas não contém dados para N=1M, K=28, Threads=16.")
    exit()

# ===============================
# 2. Processamento
# ===============================

# Calcular a média do STATIC (Linha de Base)
# O Static tem Chunk=0 no nosso CSV
static_mean = df[df['Variante'] == 'static']['Tempo'].mean()

# Filtrar apenas Dynamic e Guided para o Eixo X (Chunks variáveis)
df_variavel = df[df['Variante'].isin(['dynamic', 'guided'])].copy()

# ===============================
# 3. Plotagem
# ===============================
plt.figure()

# Plot de Linha com Marcadores (Melhor para ver tendências de granularidade)
# Usamos 'dashes=False' para linhas sólidas, diferenciando apenas por cor/marcador
sns.lineplot(
    data=df_variavel, 
    x='Chunk', 
    y='Tempo', 
    hue='Variante', 
    style='Variante', 
    markers=True, 
    dashes=False,
    markersize=9,
    linewidth=2.5
)

# Adicionar Linha de Referência do Static
label_static = 'Static'
plt.axhline(y=static_mean, color='tab:red', linestyle='--', linewidth=2, label=label_static)

# ===============================
# 4. Ajustes dos Eixos
# ===============================
# Como os chunks são potências (1, 4, 16, 64), escala logarítmica no X fica melhor
plt.xscale('log')
plt.xticks([1, 4, 16, 64], ['1', '4', '16', '64']) # Força labels inteiros
plt.minorticks_off() # Remove ticks menores logarítmicos que poluem

plt.title("Impacto do Escalonamento (Schedule) no Desempenho\n(N=1M, K=28, Threads=16)", fontsize=14, pad=15)
plt.ylabel("Tempo de Execução (s)", fontsize=12)
plt.xlabel("Tamanho do Chunk", fontsize=12)

# Legenda
plt.legend(title="Política", loc='best', frameon=True)

# ===============================
# 5. Salvar
# ===============================
OUTPUT_FILE = "png/tarefa_a_grafico_comparativo_schedule.png"
plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=300)
print(f"Gráfico gerado com sucesso: {OUTPUT_FILE}")
#plt.show()
