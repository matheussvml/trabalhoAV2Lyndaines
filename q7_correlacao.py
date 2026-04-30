import pandas as pd


df = pd.read_csv("dataset.csv")
df["interacao"] = df["threads"] * df["memoria"]

colunas = ["threads", "memoria", "interacao", "tempo_execucao"]
matriz = df[colunas].corr(method="pearson")

print("Matriz de correlacao de Pearson:")
print(matriz.round(6))

print("\nMatriz apenas das variaveis independentes:")
print(df[["threads", "memoria", "interacao"]].corr(method="pearson").round(6))
