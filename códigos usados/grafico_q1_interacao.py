"""
Questao 01 - Grafico de Interacao (Planejamento Fatorial 2^2)
Disciplina: Modelagem e Avaliacao de Desempenho - AV2 2026.1
Aluno: Matheus Vasconcelos de Macena Lima
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR if (SCRIPT_DIR / "Respostas.md").exists() else SCRIPT_DIR.parent

# Reproduzir o dataset individual
nome = "Matheus Vasconcelos de Macena Lima"
seed = sum([ord(c) for c in nome])
np.random.seed(seed)

n = 12
max_tentativas = 50

for tentativa in range(1, max_tentativas + 1):
    threads, memoria, tempo = [], [], []
    for t in [-1, 1]:
        for m in [-1, 1]:
            for _ in range(n):
                base     = 200
                efeito_t = -35 * t
                efeito_m = -28 * m
                inter    = -15 * t * m
                ruido    = np.random.normal(0, 6)
                y        = base + efeito_t + efeito_m + inter + ruido
                threads.append(t)
                memoria.append(m)
                tempo.append(y)

    df = pd.DataFrame({"threads": threads, "memoria": memoria, "tempo_execucao": tempo})

    X = df[["threads", "memoria"]].copy()
    X["interacao"] = df["threads"] * df["memoria"]
    X = sm.add_constant(X)
    model = sm.OLS(df["tempo_execucao"], X).fit()

    if (
        model.params["threads"]   < 0 and
        model.params["memoria"]   < 0 and
        model.params["interacao"] < 0 and
        model.pvalues["threads"]  < 0.05 and
        model.pvalues["memoria"]  < 0.05
    ):
        break

# Calcular medias por combinacao
medias = df.groupby(["threads", "memoria"])["tempo_execucao"].mean().reset_index()

y_nn = medias.query("threads==-1 and memoria==-1")["tempo_execucao"].values[0]
y_np = medias.query("threads==-1 and memoria== 1")["tempo_execucao"].values[0]
y_pn = medias.query("threads== 1 and memoria==-1")["tempo_execucao"].values[0]
y_pp = medias.query("threads== 1 and memoria== 1")["tempo_execucao"].values[0]

print("Medias por combinacao:")
print(f"  threads=-1, memoria=-1 -> {y_nn:.4f} ms")
print(f"  threads=-1, memoria=+1 -> {y_np:.4f} ms")
print(f"  threads=+1, memoria=-1 -> {y_pn:.4f} ms")
print(f"  threads=+1, memoria=+1 -> {y_pp:.4f} ms")

# Grafico de interacao
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Grafico de Interacao - Tempo de Execucao (ms)", fontsize=14, fontweight="bold")

# Plot 1: eixo X = Threads, linhas por Memoria
for m_val, label, color, marker in [
    (-1, f"Memoria=-1 (pequena): T=-1:{y_nn:.1f}ms / T=+1:{y_pn:.1f}ms", "#e74c3c", "o"),
    ( 1, f"Memoria=+1 (grande):  T=-1:{y_np:.1f}ms / T=+1:{y_pp:.1f}ms",  "#2980b9", "s"),
]:
    sub = medias[medias["memoria"] == m_val]
    axes[0].plot(sub["threads"], sub["tempo_execucao"],
                 marker=marker, linewidth=2.5, markersize=9, label=label, color=color)
axes[0].set_title("Efeito de Threads por nivel de Memoria", fontsize=11)
axes[0].set_xlabel("Threads  (-1 = poucos, +1 = muitos)", fontsize=10)
axes[0].set_ylabel("Tempo medio de execucao (ms)", fontsize=10)
axes[0].set_xticks([-1, 1])
axes[0].legend(fontsize=8.5)
axes[0].grid(True, linestyle="--", alpha=0.6)

# Plot 2: eixo X = Memoria, linhas por Threads
for t_val, label, color, marker in [
    (-1, f"Threads=-1 (poucos): M=-1:{y_nn:.1f}ms / M=+1:{y_np:.1f}ms", "#e67e22", "o"),
    ( 1, f"Threads=+1 (muitos): M=-1:{y_pn:.1f}ms / M=+1:{y_pp:.1f}ms",  "#27ae60", "s"),
]:
    sub = medias[medias["threads"] == t_val]
    axes[1].plot(sub["memoria"], sub["tempo_execucao"],
                 marker=marker, linewidth=2.5, markersize=9, label=label, color=color)
axes[1].set_title("Efeito de Memoria por nivel de Threads", fontsize=11)
axes[1].set_xlabel("Memoria  (-1 = pequena, +1 = grande)", fontsize=10)
axes[1].set_ylabel("Tempo medio de execucao (ms)", fontsize=10)
axes[1].set_xticks([-1, 1])
axes[1].legend(fontsize=8.5)
axes[1].grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
saida = BASE_DIR / "grafico_q1_interacao.png"
plt.savefig(saida, dpi=150, bbox_inches="tight")
print(f"\nGrafico salvo em: {saida}")
