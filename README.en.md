# 📊 Data Portfolio — Vinicius Domingues Ribeiro

Data analysis, data science and analytics engineering projects, covering
the full cycle that shows up in day-to-day data work: API-based data
extraction, SQL modeling, and machine learning (classification,
regression, clustering) with Python and scikit-learn.

I'm a data professional with experience in Python (pandas, PySpark), SQL,
Databricks/cloud environments and Open Finance data. Looking for
**analytics engineer** or **data scientist** roles, remote in Brazil or
internationally.

**Contact:**[LinkedIn](https://www.linkedin.com/in/vinicius-domingues-ribeiro/) · [E-mail](mailto:vinicius.domingues.ribeiro@gmail.com)

---

## Projects

### 1. Open Finance Brasil — consent data extraction and analysis
📁 `open_finance_brasil/`

Data engineering work on Brazil's Open Finance ecosystem: reverse
engineering the public citizen dashboard's APIs
(`dashboard.openfinancebrasil.org.br`), pulling data for 130+ participating
institutions, and consolidating a 2023–2025 time series of active and
unique consents per institution.

**Stack:** Python, pandas, requests, matplotlib.
**Highlight:** undocumented API discovery work (reverse-engineered via
browser DevTools) — a skill that rarely shows up in portfolios but is
common when integrating with legacy/institutional systems.

### 2. Churn prediction — data science case study (Data Master)
📁 `previsao_churn_streaming/`

Churn prediction model for a music streaming subscription business,
built as an evaluated case study for the Data Master program, reviewed
by Santander's data science team.

**Stack:** PySpark, pandas, matplotlib/seaborn.
**Highlight:** careful EDA on a real dataset with extreme outliers (age
ranging from -7000 to 2015 — explicit treatment documented in the
notebook) and a justified decision to drop the gender variable given it
was missing for nearly half the base.

### 3. Dimensional modeling and analytics pipeline (SQL)
📁 `novo_projeto_03_analytics_engineering/`

End-to-end data pipeline mimicking an analytics engineer's typical
workflow: raw tables with deliberate messiness → SQL staging layer →
dimensional modeling (star schema) → automated data quality tests, in the
same spirit as what dbt provides natively.

**Stack:** SQL, SQLite, Python (orchestration).
**Highlight:** 9 data quality tests (unique, not_null, relationships,
accepted_values) reimplemented in plain SQL, plus a calendar dimension
generated via a recursive CTE. Runs with a single command
(`python build_warehouse.py`) and prints a business summary at the end.

### 4. Machine learning with Kaggle (classification, regression, clustering)
📁 `novo_projeto_04_kaggle_sklearn/`

Three notebooks, three famous Kaggle datasets, three problem types:

**Titanic** — binary classification (survival), with `ColumnTransformer` + `Pipeline`, Logistic Regression vs. Random Forest comparison, `GridSearchCV` and ROC curve.

**House Prices** — regression (sale price), with categorical null handling, log-scale regression, and Linear/Ridge vs. Random Forest comparison.

**Mall Customer Segmentation** — clustering (K-Means), with the elbow method, silhouette score, and translation of clusters into named business segments.

**Stack:** pandas, numpy, matplotlib/seaborn, scikit-learn, Jupyter Notebook.

---

## Repository structure

```
.
├── open_finance_brasil/
├── previsao_churn_streaming/
├── novo_projeto_03_analytics_engineering/
│   ├── models/staging/       (SQL cleaning views)
│   ├── models/marts/         (star schema + metrics)
│   ├── tests/                (data quality tests)
│   └── build_warehouse.py
└── novo_projeto_04_kaggle_sklearn/
    ├── data/                 (datasets)
    ├── 01_titanic_classificacao.ipynb
    ├── 02_house_prices_regressao.ipynb
    └── 03_segmentacao_clientes_kmeans.ipynb
```

Each folder has its own `README.md` with objective, technical decisions
and run instructions.

## How to use this README

Adjust the folder names above to match your repository's actual layout (move `open_finance_brasil.ipynb` into its own folder if you want to follow this pattern, or update the link). Run the project 4 notebooks once locally (`pip install -r requirements.txt` inside the folder, then `jupyter notebook`, `Run All`) so charts and results are saved and visible directly on GitHub.
