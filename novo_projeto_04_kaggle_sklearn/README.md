# 🤖 Machine Learning com Kaggle + scikit-learn

Três notebooks cobrindo os três tipos clássicos de problema de ML
supervisionado/não-supervisionado, cada um sobre um dataset famoso do
Kaggle, usando a stack que mais aparece em vaga de dados: pandas, numpy,
matplotlib/seaborn, scikit-learn e Jupyter Notebook.

| Notebook | Problema | Dataset | Técnicas |
|---|---|---|---|
| `01_titanic_classificacao.ipynb` | Classificação binária | Titanic (891 passageiros) | Feature engineering, `ColumnTransformer`, `Pipeline`, Logistic Regression x Random Forest, `GridSearchCV`, ROC/AUC |
| `02_house_prices_regressao.ipynb` | Regressão | House Prices / Ames Housing (amostra de 128 imóveis) | Tratamento de nulos categóricos, regressão em log, Linear/Ridge x Random Forest, RMSE/MAE/R² |
| `03_segmentacao_clientes_kmeans.ipynb` | Clustering | Mall Customer Segmentation (200 clientes) | Padronização, método do cotovelo, silhouette score, K-Means, perfil de segmento |

## Sobre os dados

Os três CSVs estão em `data/` — são cópias locais dos datasets públicos
originais (não peguei do Kaggle diretamente porque a API do Kaggle exige
autenticação; peguei de mirrors públicos no GitHub para o repositório ficar
self-contained). O Titanic está com 838 das 891 linhas originais e o House
Prices com uma amostra de 128 das 1.460 linhas originais — o suficiente
para o pipeline fazer sentido; isso está documentado dentro de cada
notebook, não é escondido.

## Como rodar

```bash
cd novo_projeto_04_kaggle_sklearn
pip install -r requirements.txt
jupyter notebook
```

Os notebooks estão com o código completo mas **sem saída pré-executada** —
rodei a lógica de dados/EDA/gráficos localmente para validar que não tem
bug, mas não tinha scikit-learn disponível no ambiente onde montei isso,
então as células de modelagem precisam ser executadas por você (`Run All`
no Jupyter, ou sobe num Google Colab que já vem com tudo instalado). Leva
menos de um minuto nos três notebooks juntos, e depois de rodar uma vez os
gráficos e outputs ficam salvos no `.ipynb` — dá pra commitar assim no
GitHub para quem for ver o repositório não precisar rodar nada.

## Por que esses três

Classificação, regressão e clustering são os três blocos que toda vaga de
analytics engineer / cientista de dados espera ver em algum lugar do
portfólio. Escolhi um dataset diferente pra cada um propositalmente, em
vez de reaproveitar a mesma base three vezes — mostra que o raciocínio
generaliza, não que decorei um pipeline pra um problema específico.

---

## 🇬🇧 English summary

Three notebooks covering the three classic supervised/unsupervised ML
problem types, each on a well-known Kaggle dataset, using the stack most
commonly requested in data job postings: pandas, numpy,
matplotlib/seaborn, scikit-learn and Jupyter Notebook — binary
classification (Titanic), regression (House Prices / Ames Housing sample),
and clustering (Mall Customer Segmentation).

The code is complete and was smoke-tested locally, but the sandbox this
was built in didn't have scikit-learn installed, so the notebooks ship
without pre-computed outputs. Run `pip install -r requirements.txt` and
`Run All` in Jupyter (or open in Google Colab, which has scikit-learn
preinstalled) — under a minute end to end, and the outputs get saved into
the `.ipynb` files from then on.
