# AV2 — Modelagem e Avaliação de Desempenho

Este repositório contém o dataset individual, os scripts utilizados nas análises e o relatório final do trabalho da AV2.

## Estrutura dos Arquivos

| Arquivo/Pasta | Finalidade |
|---|---|
| `dataset.csv` | Dataset individual usado nas respostas. |
| `Respostas.md` | Relatório em Markdown com as respostas das 12 questões. |
| `Template - Trabalho - 26.1.docx` | Template original do trabalho. |
| `Template - Trabalho - 26.1 copia.docx` | Documento Word gerado com as respostas. |
| `códigos usados/` | Pasta com os scripts Python usados para gerar dataset, gráficos e análises. |
| `grafico_q1_interacao.png` | Gráfico de interação usado nas questões 1, 3 e 11. |
| `q7_matriz_correlacao.png` | Gráfico da matriz de correlação da questão 7. |
| `q9_residuos.png` | Gráfico de diagnóstico dos resíduos da questão 9. |
| `correlacao_pearson.png` | Gráfico complementar da análise de correlação/VIF. |

## Bibliotecas Necessárias

Os scripts usam as seguintes bibliotecas Python:

```text
numpy
pandas
matplotlib
seaborn
statsmodels
python-docx
```

Instale todas com:

```powershell
python -m pip install numpy pandas matplotlib seaborn statsmodels python-docx
```

## Como Rodar Usando a `.venv`

Se a pasta `.venv` já existir no projeto, use o Python dela diretamente.

### Ativar a venv

No PowerShell, dentro da pasta do projeto:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação por política de execução, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Depois de ativar, instale as dependências:

```powershell
python -m pip install numpy pandas matplotlib seaborn statsmodels python-docx
```

### Rodar scripts com a venv ativada

Execute os comandos a partir da raiz do projeto:

```powershell
python ".\códigos usados\dataset_individual.py"
python ".\códigos usados\grafico_q1_interacao.py"
python ".\códigos usados\q7_correlacao.py"
python ".\códigos usados\q7_analise_correlacao.py"
python ".\códigos usados\q9_residuos.py"
python ".\códigos usados\gerar_docx_respostas.py"
```

### Rodar sem ativar a venv

Também é possível chamar diretamente o Python da `.venv`:

```powershell
.\.venv\Scripts\python.exe ".\códigos usados\dataset_individual.py"
.\.venv\Scripts\python.exe ".\códigos usados\grafico_q1_interacao.py"
.\.venv\Scripts\python.exe ".\códigos usados\q7_correlacao.py"
.\.venv\Scripts\python.exe ".\códigos usados\q7_analise_correlacao.py"
.\.venv\Scripts\python.exe ".\códigos usados\q9_residuos.py"
.\.venv\Scripts\python.exe ".\códigos usados\gerar_docx_respostas.py"
```

## Como Rodar Fora da `.venv`

Caso não queira usar ambiente virtual, instale as dependências no Python global:

```powershell
python -m pip install numpy pandas matplotlib seaborn statsmodels python-docx
```

Depois execute os scripts normalmente, sempre a partir da raiz do projeto:

```powershell
python ".\códigos usados\dataset_individual.py"
python ".\códigos usados\grafico_q1_interacao.py"
python ".\códigos usados\q7_correlacao.py"
python ".\códigos usados\q7_analise_correlacao.py"
python ".\códigos usados\q9_residuos.py"
python ".\códigos usados\gerar_docx_respostas.py"
```

## Ordem Recomendada de Execução

Para reproduzir o trabalho inteiro do início:

1. Gerar ou atualizar o dataset individual:

```powershell
python ".\códigos usados\dataset_individual.py"
```

2. Gerar o gráfico de interação:

```powershell
python ".\códigos usados\grafico_q1_interacao.py"
```

3. Gerar a matriz de correlação da questão 7:

```powershell
python ".\códigos usados\q7_correlacao.py"
```

4. Rodar a análise complementar de correlação e VIF:

```powershell
python ".\códigos usados\q7_analise_correlacao.py"
```

5. Gerar o diagnóstico dos resíduos:

```powershell
python ".\códigos usados\q9_residuos.py"
```

6. Gerar o documento Word a partir do Markdown:

```powershell
python ".\códigos usados\gerar_docx_respostas.py"
```

## Saídas Geradas

Ao executar os scripts, os principais arquivos gerados/atualizados são:

| Script | Saída |
|---|---|
| `dataset_individual.py` | `dataset.csv` |
| `grafico_q1_interacao.py` | `grafico_q1_interacao.png` |
| `q7_correlacao.py` | `q7_matriz_correlacao.png` |
| `q7_analise_correlacao.py` | `correlacao_pearson.png` |
| `q9_residuos.py` | `q9_residuos.png` |
| `gerar_docx_respostas.py` | `Template - Trabalho - 26.1 copia.docx` |

## Observações Importantes

- Execute os comandos a partir da raiz do projeto: `D:\FACULDADE\Lyndaines`.
- Os caminhos têm espaço e acento, então use aspas ao chamar scripts dentro de `códigos usados`.
- Antes de regenerar o `.docx`, feche o arquivo `Template - Trabalho - 26.1 copia.docx` no Word/LibreOffice para evitar erro de permissão.
- O relatório principal é o `Respostas.md`; o `.docx` é gerado a partir dele.
- Se mudar o `Respostas.md`, rode novamente `gerar_docx_respostas.py` para atualizar o Word.

