# 📊 Portfólio de Dados — Vinicius Domingues Ribeiro

Projetos de análise, ciência e engenharia de dados, cobrindo o ciclo
completo que aparece no dia a dia da área: extração de dados via API,
modelagem em SQL, e machine learning (classificação, regressão,
clustering) com Python e scikit-learn.

Sou profissional de dados com experiência em Python (pandas, PySpark),
SQL, Databricks/ambientes de nuvem e dados de Open Finance. Busco
oportunidades como **analytics engineer** ou **cientista de dados**, no
Brasil (remoto) ou internacionalmente.

**Contato:** [LinkedIn](#) · [E-mail](#)
*(atualize os links acima com suas URLs antes de publicar)*

---

## Projetos

### 1. Open Finance Brasil — extração e análise de consentimentos
📁 `open_finance_brasil/`

Engenharia de dados sobre o ecossistema de Open Finance brasileiro:
engenharia reversa das APIs do dashboard público do cidadão
(`dashboard.openfinancebrasil.org.br`), consumo de mais de 130 instituições
participantes, e consolidação de uma série histórica (2023–2025) de
consentimentos ativos e únicos por instituição.

**Stack:** Python, pandas, requests, matplotlib.
**Destaque:** trabalho de descoberta de API não documentada (engenharia
reversa via DevTools do navegador) — habilidade que aparece pouco em
portfólio, mas é comum no dia a dia de quem integra com sistemas
legados/institucionais.

### 2. Previsão de churn — case de ciência de dados (Data Master)
📁 `previsao_churn_streaming/` *(hoje em repositório privado — publicar
ou copiar o notebook antes de linkar aqui)*

Modelo de predição de cancelamento (churn) para uma empresa de streaming
de música, desenvolvido como case avaliativo do programa Data Master, com
avaliação por especialistas de ciência de dados do Santander.

**Stack:** PySpark, pandas, matplotlib/seaborn.
**Destaque:** EDA criteriosa sobre uma base real com outliers extremos
(idade variando de -7000 a 2015 anos — tratamento explícito documentado
no notebook) e decisão justificada de descartar a variável de gênero por
ela estar ausente em quase metade da base.

### 3. Modelagem dimensional e pipeline analítico (SQL)
📁 `novo_projeto_03_analytics_engineering/`

Pipeline de dados de ponta a ponta simulando a rotina de um analytics
engineer: tabelas brutas com inconsistências propositais → camada de
staging em SQL → modelagem dimensional (star schema) → testes de
qualidade automatizados, no estilo do que o dbt oferece nativamente.

**Stack:** SQL, SQLite, Python (orquestração).
**Destaque:** 9 testes de qualidade de dados (unique, not_null,
relationships, accepted_values) reimplementados em SQL puro, e uma
dimensão de calendário gerada via CTE recursiva. Roda com um único
comando (`python build_warehouse.py`) e imprime um resumo de negócio ao
final.

### 4. Machine Learning com Kaggle (classificação, regressão, clustering)
📁 `novo_projeto_04_kaggle_sklearn/`

Três notebooks, três datasets famosos do Kaggle, três tipos de problema:

- **Titanic** — classificação binária (sobrevivência), com
  `ColumnTransformer` + `Pipeline`, comparação Logistic Regression x
  Random Forest, `GridSearchCV` e curva ROC.
- **House Prices** — regressão (preço de imóvel), com tratamento de
  nulos categóricos, regressão em log e comparação Linear/Ridge x Random
  Forest.
- **Mall Customer Segmentation** — clustering (K-Means), com método do
  cotovelo, silhouette score e tradução dos clusters em segmentos de
  negócio nomeados.

**Stack:** pandas, numpy, matplotlib/seaborn, scikit-learn, Jupyter
Notebook.

---

## Estrutura do repositório

```
.
├── open_finance_brasil/
├── previsao_churn_streaming/
├── novo_projeto_03_analytics_engineering/
│   ├── models/staging/       (views SQL de limpeza)
│   ├── models/marts/         (star schema + métricas)
│   ├── tests/                (testes de qualidade de dados)
│   └── build_warehouse.py
└── novo_projeto_04_kaggle_sklearn/
    ├── data/                 (datasets)
    ├── 01_titanic_classificacao.ipynb
    ├── 02_house_prices_regressao.ipynb
    └── 03_segmentacao_clientes_kmeans.ipynb
```

Cada pasta tem seu próprio `README.md` com objetivo, decisões técnicas e
instruções de execução.

## Como usar este README

1. Ajuste os nomes de pasta acima para bater com a organização real do seu
   repositório (renomeie `open_finance_brasil.ipynb` para dentro de uma
   pasta própria se quiser seguir esse padrão, ou ajuste o link).
2. Decida se o notebook de churn (`datamaster`) vai virar público ou se
   você prefere copiar só o notebook para dentro deste repositório.
3. Rode os notebooks do projeto 4 uma vez localmente (`pip install -r
   requirements.txt` dentro da pasta, depois `jupyter notebook`, `Run
   All`) para que os gráficos e resultados fiquem salvos e visíveis
   direto no GitHub.
