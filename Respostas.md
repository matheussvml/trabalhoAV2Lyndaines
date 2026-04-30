# Respostas — AV2 1ª Chamada 2026.1
**Aluno:** Matheus Vasconcelos de Macena Lima

---

## Questão 01 — Planejamento Fatorial 2²

O experimento avalia o efeito de dois fatores no **tempo de execução (ms)**:
- **Fator A (Threads):** −1 = poucos threads | +1 = muitos threads
- **Fator B (Memória):** −1 = memória pequena | +1 = memória grande

Cada combinação possui **n = 12 réplicas**, totalizando **48 observações**.

---

### a) Tabela de Médias por Combinação

| Threads (x₁) | Memória (x₂) | Média do Tempo de Execução (ms) |
|:---:|:---:|:---:|
| −1 (poucos) | −1 (pequena) | **248,62** |
| −1 (poucos) | +1 (grande)  | **219,69** |
| +1 (muitos) | −1 (pequena) | **208,87** |
| +1 (muitos) | +1 (grande)  | **124,45** |

---

### b) Efeito Principal de Threads

O efeito principal de Threads mede a variação média no tempo de execução ao mudar threads de −1 para +1, calculado como a média das diferenças em cada nível de Memória:

$$E_{Threads} = \frac{(\bar{y}_{+1,-1} - \bar{y}_{-1,-1}) + (\bar{y}_{+1,+1} - \bar{y}_{-1,+1})}{2}$$

$$E_{Threads} = \frac{(208{,}87 - 248{,}62) + (124{,}45 - 219{,}69)}{2} = \frac{-39{,}75 + (-95{,}24)}{2}$$

$$\boxed{E_{Threads} \approx -67{,}50 \text{ ms}}$$

**Interpretação:** Aumentar o número de threads reduz o tempo de execução em média **67,50 ms**, indicando que mais paralelismo acelera o processamento.

---

### c) Efeito Principal de Memória

O efeito principal de Memória mede a variação média ao mudar memória de −1 para +1:

$$E_{Memoria} = \frac{(\bar{y}_{-1,+1} - \bar{y}_{-1,-1}) + (\bar{y}_{+1,+1} - \bar{y}_{+1,-1})}{2}$$

$$E_{Memoria} = \frac{(219{,}69 - 248{,}62) + (124{,}45 - 208{,}87)}{2} = \frac{-28{,}93 + (-84{,}42)}{2}$$

$$\boxed{E_{Memoria} \approx -56{,}67 \text{ ms}}$$

**Interpretação:** Aumentar a memória reduz o tempo de execução em média **56,67 ms**, o que faz sentido dado que mais memória reduz a necessidade de acesso a disco e swapping.

---

### d) Efeito de Interação Threads × Memória

A interação mede se o efeito de um fator depende do nível do outro:

$$E_{T \times M} = \frac{(\bar{y}_{-1,-1} - \bar{y}_{-1,+1}) - (\bar{y}_{+1,-1} - \bar{y}_{+1,+1})}{2}$$

$$E_{T \times M} = \frac{(248{,}62 - 219{,}69) - (208{,}87 - 124{,}45)}{2} = \frac{28{,}93 - 84{,}42}{2}$$

$$\boxed{E_{T \times M} \approx -27{,}74 \text{ ms}}$$

**Interpretação:** O efeito de interação negativo indica que o ganho ao usar mais threads **é amplificado quando a memória também está no nível alto**. Os fatores se potencializam mutuamente.

---

### e) Gráfico de Interação

> Script: `grafico_q1_interacao.py`

![Grafico de Interacao](grafico_q1_interacao.png)

---

### f) Existe interação entre Threads e Memória?

**Sim, existe interação significativa entre os fatores.**

Analisando o gráfico:
- As linhas **não são paralelas** — isso é a evidência visual de que há interação.
- Com **Memória = −1** (pequena): aumentar threads reduz o tempo em ~**39,75 ms**
- Com **Memória = +1** (grande): aumentar threads reduz o tempo em ~**95,25 ms**

A diferença de comportamento (39,75 ms vs 95,25 ms) confirma que o efeito dos threads depende do nível de memória — definição de interação.

Estatisticamente, confirmada pela regressão OLS:
- **Coeficiente de interação:** −13,87
- **p-valor da interação:** < 0,001 (altamente significativo)

**Conclusão:** Os dois fatores **não agem de forma independente**. Para obter o melhor desempenho, é preciso combinar **mais threads com mais memória** simultaneamente — a combinação T=+1, M=+1 obteve o menor tempo médio de execução: **124,45 ms**.

---
