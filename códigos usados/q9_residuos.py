import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR if (SCRIPT_DIR / "dataset.csv").exists() else SCRIPT_DIR.parent

df = pd.read_csv(BASE_DIR / "dataset.csv")
df["interacao"] = df["threads"] * df["memoria"]

X = np.column_stack(
    [
        np.ones(len(df)),
        df["threads"],
        df["memoria"],
        df["interacao"],
    ]
)
y = df["tempo_execucao"].to_numpy()

beta = np.linalg.inv(X.T @ X) @ X.T @ y
df["ajustado"] = X @ beta
df["residuo"] = y - df["ajustado"]
df["configuracao"] = df.apply(
    lambda linha: f"T={int(linha['threads'])}, M={int(linha['memoria'])}",
    axis=1,
)

print("Coeficientes do modelo:")
print(f"beta0 = {beta[0]:.6f}")
print(f"beta1 = {beta[1]:.6f}")
print(f"beta2 = {beta[2]:.6f}")
print(f"beta3 = {beta[3]:.6f}")

print("\nResumo dos residuos:")
print(df["residuo"].agg(["mean", "std", "min", "max"]).to_string())

print("\nResumo dos residuos por configuracao:")
print(df.groupby(["threads", "memoria"])["residuo"].agg(["mean", "std", "min", "max"]))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].scatter(df["ajustado"], df["residuo"], color="#2f6f8f", edgecolor="black", alpha=0.85)
axes[0].axhline(0, color="black", linewidth=1)
axes[0].set_title("Residuos vs Valores Ajustados")
axes[0].set_xlabel("Valor ajustado")
axes[0].set_ylabel("Residuo")
axes[0].grid(alpha=0.25)

ordem = ["T=-1, M=-1", "T=-1, M=1", "T=1, M=-1", "T=1, M=1"]
dados_boxplot = [df.loc[df["configuracao"] == config, "residuo"] for config in ordem]
axes[1].boxplot(dados_boxplot, tick_labels=ordem, patch_artist=True)
axes[1].axhline(0, color="black", linewidth=1)
axes[1].set_title("Distribuicao dos Residuos por Configuracao")
axes[1].set_xlabel("Configuracao")
axes[1].set_ylabel("Residuo")
axes[1].tick_params(axis="x", rotation=25)
axes[1].grid(axis="y", alpha=0.25)

plt.tight_layout()
plt.savefig(BASE_DIR / "q9_residuos.png", dpi=200, bbox_inches="tight")
plt.close()
