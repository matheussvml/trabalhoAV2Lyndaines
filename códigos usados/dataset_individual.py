import numpy as np
import pandas as pd
import statsmodels.api as sm

nome = "Matheus Vasconcelos de Macena Lima"
seed = sum([ord(c) for c in nome])
np.random.seed(seed)

n = 12
max_tentativas = 50
tentativa = 0

while tentativa < max_tentativas:
    tentativa += 1

    threads, memoria, tempo = [], [], []

    for t in [-1, 1]:
        for m in [-1, 1]:
            for _ in range(n):
                base = 200
                efeito_t = -35 * t
                efeito_m = -28 * m
                inter = -15 * t * m

                ruido = np.random.normal(0, 6)

                y = base + efeito_t + efeito_m + inter + ruido

                threads.append(t)
                memoria.append(m)
                tempo.append(y)

    df = pd.DataFrame({
        "threads": threads,
        "memoria": memoria,
        "tempo_execucao": tempo
    })

    # regressão
    X = df[['threads', 'memoria']].copy()
    X['interacao'] = df['threads'] * df['memoria']
    X = sm.add_constant(X)

    model = sm.OLS(df['tempo_execucao'], X).fit()

    if (
            model.params['threads'] < 0 and
            model.params['memoria'] < 0 and
            model.params['interacao'] < 0 and
            model.pvalues['threads'] < 0.05 and
            model.pvalues['memoria'] < 0.05
    ):
        print(f"Dataset válido gerado na tentativa {tentativa}")
        break

else:
    raise ValueError(
        "Não foi possível gerar um dataset válido após várias tentativas. "
        "Tente mudar a seed (nome) ou os parâmetros do modelo."
    )

df.to_csv("dataset.csv", index=False)