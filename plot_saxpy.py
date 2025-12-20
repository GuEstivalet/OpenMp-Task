import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações de estilo
sns.set_theme(style="whitegrid")

# 1. Carregamento dos dados
try:
    df1 = pd.read_csv('csv/saxpy_v1.csv')
    df2 = pd.read_csv('csv/saxpy_v2.csv')
    df3 = pd.read_csv('csv/saxpy_v3.csv')
except FileNotFoundError as e:
    print(f"Erro: Arquivos CSV não encontrados. Rode o run.sh primeiro. {e}")
    exit()

# --- CONVERSÃO DE SEGUNDOS PARA MILISSEGUNDOS ---
for df in [df1, df2, df3]:
    df['tempo'] = df['tempo'] * 1000

# Adicionando identificadores de versão
df1['Versao'] = 'v1 (Sequencial)'
df1['T'] = 1
df2['Versao'] = 'v2 (SIMD)'
df2['T'] = 1
df3['Versao'] = 'v3 (OMP+SIMD)'

# Unificando para cálculos globais
df_total = pd.concat([df1, df2, df3], ignore_index=True)

# 2. GERAÇÃO DAS ESTATÍSTICAS (Define stats_final)
stats_final = df_total.groupby(['N', 'Versao', 'T'])['tempo'].agg(['mean', 'std']).reset_index()
stats_final.to_csv('csv/estatisticas_ms.csv', index=False)

# =========================================================
# 3. CÁLCULO E GRÁFICO DE SPEEDUP
# =========================================================
# Extrai apenas a v1 para servir de baseline (T=1)
base_seq = stats_final[stats_final['Versao'] == 'v1 (Sequencial)'][['N', 'mean']].rename(columns={'mean': 'tempo_seq'})

# Mescla com a tabela geral para calcular a razão
speedup_df = pd.merge(stats_final, base_seq, on='N')
speedup_df['speedup'] = speedup_df['tempo_seq'] / speedup_df['mean']
speedup_df.to_csv('csv/tabela_speedup.csv', index=False)

# Gráfico de Speedup
plt.figure(figsize=(10, 6))
v3_speedup = speedup_df[speedup_df['Versao'] == 'v3 (OMP+SIMD)']
for n in sorted(v3_speedup['N'].unique()):
    subset = v3_speedup[v3_speedup['N'] == n]
    plt.plot(subset['T'], subset['speedup'], marker='s', label=f'N={n}')

# Linha de Speedup Ideal (S = T) limitada ao máximo de cores lógicos (8)
plt.plot([1, 8], [1, 8], color='black', linestyle='--', alpha=0.5, label='Speedup Ideal (Linear)')

plt.title('Speedup da Versão v3 sobre a Sequencial v1')
plt.xlabel('Threads (T)')
plt.ylabel('Fator de Speedup (x)')
plt.legend()
plt.savefig('png/grafico_speedup.png')
plt.close()

# =========================================================
# 4. BOXPLOTS INDIVIDUALIZADOS (Correção de Warning)
# =========================================================
# Boxplot v1
plt.figure(figsize=(8, 6))
sns.boxplot(data=df1, x='N', y='tempo', hue='N', palette='Blues', legend=False)
plt.title('V1 (Sequencial): Tempo por N')
plt.ylabel('Tempo (ms)')
plt.savefig('png/boxplot_v1.png')
plt.close()

# Boxplot v2
plt.figure(figsize=(8, 6))
sns.boxplot(data=df2, x='N', y='tempo', hue='N', palette='Greens', legend=False)
plt.title('V2 (SIMD): Tempo por N')
plt.ylabel('Tempo (ms)')
plt.savefig('png/boxplot_v2.png')
plt.close()

# Boxplot v3 (Facetado)
g = sns.catplot(data=df3, x='T', y='tempo', col='N', hue='T', kind='box', 
                palette='Oranges', sharey=False, height=5, aspect=0.8, legend=False)
g.fig.suptitle('V3 (OMP+SIMD): Distribuição por Threads/N', y=1.05)
g.set_axis_labels("Threads (T)", "Tempo (ms)")
plt.savefig('png/boxplot_v3.png')
plt.close()

# =========================================================
# 5. NUVEM E ESCALABILIDADE
# =========================================================
# Nuvem de Pontos
plt.figure(figsize=(10, 6))
sns.stripplot(data=df_total, x='N', y='tempo', hue='Versao', dodge=True, alpha=0.5)
plt.yscale('log')
plt.title('Variabilidade Global (ms)')
plt.savefig('png/nuvem_pontos.png')
plt.close()

# Escalabilidade
plt.figure(figsize=(10, 6))
for n in sorted(v3_speedup['N'].unique()):
    subset = stats_final[(stats_final['Versao'] == 'v3 (OMP+SIMD)') & (stats_final['N'] == n)]
    plt.plot(subset['T'], subset['mean'], marker='o', label=f'N={n}')
plt.title('Escalabilidade (Média ms)')
plt.xlabel('Threads')
plt.ylabel('Tempo (ms)')
plt.legend()
plt.savefig('png/escalabilidade.png')
plt.close()

print("Processamento concluído. Verifique os arquivos CSV e PNG gerados.")
