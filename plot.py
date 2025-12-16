import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid", font_scale=1.2)

# ===============================
# Leitura
# ===============================
v1 = pd.read_csv("saxpy_v1.csv")
v2 = pd.read_csv("saxpy_v2.csv")
v3 = pd.read_csv("saxpy_v3.csv")

# ===============================
# Conversão para microssegundos
# ===============================
for df in [v1, v2, v3]:
    df["tempo_us"] = df["tempo"] * 1e6

# ===============================
# Estatísticas
# ===============================
def stats(df, group_cols):
    return (
        df.groupby(group_cols)["tempo_us"]
        .agg(["mean", "std"])
        .reset_index()
        .rename(columns={
            "mean": "media_us",
            "std": "desvio_padrao_us"
        })
    )

stats_v1 = stats(v1, ["N"])
stats_v2 = stats(v2, ["N"])
stats_v3 = stats(v3, ["N", "T"])

print("\n=== V1 (µs) ===")
print(stats_v1)
print("\n=== V2 (µs) ===")
print(stats_v2)
print("\n=== V3 (µs) ===")
print(stats_v3)

# ===============================
# Funções de plot
# ===============================
def scatter_plot(df, x, y, hue, title, filename):
    plt.figure(figsize=(9, 6))
    sns.scatterplot(
        data=df, x=x, y=y, hue=hue,
        s=80, alpha=0.8
    )
    plt.ylabel("Tempo (µs)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

def box_plot(df, x, y, hue, title, filename):
    plt.figure(figsize=(9, 6))
    sns.boxplot(data=df, x=x, y=y, hue=hue)
    plt.ylabel("Tempo (µs)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

# ===============================
# V1 – Sequencial
# ===============================
scatter_plot(
    v1, "N", "tempo_us", None,
    "SAXPY v1 – Tempo por N (µs)",
    "v1_scatter_us.png"
)

box_plot(
    v1, "N", "tempo_us", None,
    "SAXPY v1 – Boxplot (µs)",
    "v1_boxplot_us.png"
)

# ===============================
# V2 – SIMD
# ===============================
scatter_plot(
    v2, "N", "tempo_us", None,
    "SAXPY v2 (SIMD) – Tempo por N (µs)",
    "v2_scatter_us.png"
)

box_plot(
    v2, "N", "tempo_us", None,
    "SAXPY v2 (SIMD) – Boxplot (µs)",
    "v2_boxplot_us.png"
)

# ===============================
# V3 – OpenMP + SIMD
# ===============================
scatter_plot(
    v3, "N", "tempo_us", "T",
    "SAXPY v3 (OMP + SIMD) – Tempo por N e Threads (µs)",
    "v3_scatter_us.png"
)

box_plot(
    v3, "N", "tempo_us", "T",
    "SAXPY v3 (OMP + SIMD) – Boxplot (µs)",
    "v3_boxplot_us.png"
)

print("\nGráficos em microssegundos gerados com sucesso.")
