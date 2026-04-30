import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("dataset.csv")
df["interacao"] = df["threads"] * df["memoria"]

colunas = ["threads", "memoria", "interacao", "tempo_execucao"]
matriz = df[colunas].corr(method="pearson")

print("Matriz de correlacao de Pearson:")
print(matriz.round(6))

print("\nMatriz apenas das variaveis independentes:")
print(df[["threads", "memoria", "interacao"]].corr(method="pearson").round(6))

fig, ax = plt.subplots(figsize=(8, 6))
imagem = ax.imshow(matriz, cmap="coolwarm", vmin=-1, vmax=1)

ax.set_xticks(range(len(colunas)))
ax.set_yticks(range(len(colunas)))
ax.set_xticklabels(["Threads", "Memoria", "Interacao", "Tempo"])
ax.set_yticklabels(["Threads", "Memoria", "Interacao", "Tempo"])

for i in range(len(colunas)):
    for j in range(len(colunas)):
        ax.text(j, i, f"{matriz.iloc[i, j]:.2e}", ha="center", va="center", color="black")

ax.set_title("Matriz de Correlacao de Pearson")
fig.colorbar(imagem, ax=ax, label="Correlacao")
plt.tight_layout()
plt.savefig("q7_matriz_correlacao.png", dpi=200)
plt.close()
