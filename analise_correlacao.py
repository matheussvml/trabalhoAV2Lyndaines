"""
Análise de Correlação de Pearson
Dataset: threads, memoria, tempo_execucao
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from numpy.linalg import inv, det, lstsq
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

# ── 1. Carregamento ────────────────────────────────────────────────────────────
df = pd.read_csv(BASE_DIR / 'dataset.csv')
print("=== Visão geral do dataset ===")
print(f"Shape: {df.shape}")
print(df.describe().round(4))

# ── 2. Matriz de Correlação de Pearson ────────────────────────────────────────
corr = df.corr(method='pearson')
print("\n=== Matriz de Correlação de Pearson ===")
print(corr.round(6))

# Correlação apenas entre independentes
indep = ['threads', 'memoria']
corr_indep = df[indep].corr()
corr_threads_memoria = corr_indep.loc['threads', 'memoria']
print(f"\nCorrelação entre variáveis independentes (threads <-> memoria): {corr_threads_memoria:.2e}")
print(f"-> Essencialmente ZERO (aprox. {corr_threads_memoria:.4f})")

# ── 3. VIF (Variance Inflation Factor) ────────────────────────────────────────
X = df[indep].values

def calc_vif(X, j):
    """VIF da j-ésima variável: 1 / (1 - R²_j)"""
    cols = list(range(X.shape[1]))
    y_j = X[:, j]
    X_resto = X[:, [c for c in cols if c != j]]
    X_aug = np.column_stack([np.ones(len(X_resto)), X_resto])
    coef, _, _, _ = lstsq(X_aug, y_j, rcond=None)
    pred = X_aug @ coef
    ss_res = np.sum((y_j - pred)**2)
    ss_tot = np.sum((y_j - y_j.mean())**2)
    r2 = 1 - ss_res / ss_tot
    return 1 / (1 - r2) if r2 < 1 else np.inf

vif_results = {var: calc_vif(X, i) for i, var in enumerate(indep)}
print("\n=== VIF (Variance Inflation Factor) ===")
for var, vif in vif_results.items():
    flag = "OK - Sem multicolinearidade" if vif < 5 else ("Moderado" if vif < 10 else "Alta multicolinearidade")
    print(f"  {var}: VIF = {vif:.4f}  ->  {flag}")

# ── 4. Determinante da matriz de correlação ───────────────────────────────────
det_val = det(corr_indep.values)
print(f"\nDeterminante da matriz de correlação (independentes): {det_val:.6f}")
print("-> Det próximo de 1.0 = variáveis ORTOGONAIS (design balanceado fatorial)")

# ── 5. Regressão OLS manual ───────────────────────────────────────────────────
y = df['tempo_execucao'].values
Xc = np.column_stack([np.ones(len(X)), X])
beta = inv(Xc.T @ Xc) @ Xc.T @ y
y_pred = Xc @ beta
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res / ss_tot
n, k = Xc.shape
s2 = ss_res / (n - k)
se = np.sqrt(np.diag(s2 * inv(Xc.T @ Xc)))
t_stats = beta / se

print("\n=== Regressão Linear Múltipla (OLS) ===")
labels = ['Intercepto', 'threads', 'memoria']
for lbl, b, s, t in zip(labels, beta, se, t_stats):
    print(f"  {lbl:12s}: coef={b:10.4f}  SE={s:.4f}  t={t:.4f}")
print(f"  R² = {r2:.4f}  |  R²_ajustado = {1 - (1-r2)*(n-1)/(n-k):.4f}")

# ── 6. Visualizações ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Análise de Correlação de Pearson — threads, memoria, tempo_execucao',
             fontsize=13, fontweight='bold')

# 6a. Heatmap completo
sns.heatmap(corr, annot=True, fmt='.4f', cmap='coolwarm', center=0,
            vmin=-1, vmax=1, ax=axes[0], square=True, linewidths=0.8,
            annot_kws={'size': 12, 'weight': 'bold'})
axes[0].set_title('Matriz de Correlação\n(Pearson)', fontsize=11)
axes[0].tick_params(axis='x', rotation=25)

# 6b. Barras – correlação com variável dependente
dep_corr = corr['tempo_execucao'].drop('tempo_execucao').sort_values()
colors = ['#d62728' if v < 0 else '#2ca02c' for v in dep_corr.values]
bars = axes[1].barh(dep_corr.index, dep_corr.values, color=colors,
                    edgecolor='black', height=0.4)
axes[1].axvline(0, color='black', linewidth=0.8)
for bar, val in zip(bars, dep_corr.values):
    offset = -0.02 if val < 0 else 0.02
    ha = 'right' if val < 0 else 'left'
    axes[1].text(val + offset, bar.get_y() + bar.get_height()/2,
                 f'{val:.4f}', va='center', ha=ha, fontsize=12, fontweight='bold')
axes[1].set_xlim(-1, 0.3)
axes[1].set_title('Correlação com tempo_execucao\n(variável dependente)', fontsize=11)
axes[1].set_xlabel('Coeficiente de Pearson')

# 6c. VIF bars
vif_vals = list(vif_results.values())
vif_vars = list(vif_results.keys())
bar_colors = ['#2ca02c' if v < 5 else '#d62728' for v in vif_vals]
axes[2].bar(vif_vars, vif_vals, color=bar_colors, edgecolor='black', width=0.4)
axes[2].axhline(5, color='orange', linestyle='--', label='Limiar moderado (VIF=5)')
axes[2].axhline(10, color='red', linestyle='--', label='Limiar crítico (VIF=10)')
for i, (v, val) in enumerate(zip(vif_vars, vif_vals)):
    axes[2].text(i, val + 0.03, f'{val:.2f}', ha='center', fontsize=12, fontweight='bold')
axes[2].set_ylim(0, 12)
axes[2].set_title('VIF por variável independente', fontsize=11)
axes[2].set_ylabel('VIF')
axes[2].legend(fontsize=9)

plt.tight_layout()
saida = BASE_DIR / 'correlacao_pearson.png'
plt.savefig(saida, dpi=150, bbox_inches='tight')
print(f"\nOK - Gráfico salvo em: {saida}")
