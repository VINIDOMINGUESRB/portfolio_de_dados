"""
Orquestra o pipeline completo: gera dados brutos -> aplica staging ->
constrói os marts -> roda os testes de qualidade -> imprime um resumo.

Uso:
    python build_warehouse.py

Isso simula, em escala pequena e num único arquivo SQLite, o que uma
ferramenta como dbt faz: materializar modelos em camadas (staging, marts)
a partir de SQL versionado, com testes automatizados ao final do run.
"""

import glob
import sqlite3

import data_generation
from tests.data_quality_tests import run_all_tests

DB_PATH = "warehouse.sqlite"


def run_sql_file(cur, path):
    with open(path, encoding="utf-8") as f:
        cur.executescript(f.read())


def main():
    print("== 1. Gerando dados brutos ==")
    data_generation.main()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("\n== 2. Rodando camada de staging ==")
    for path in sorted(glob.glob("models/staging/*.sql")):
        print(f"  -> {path}")
        run_sql_file(cur, path)

    print("\n== 3. Rodando camada de marts ==")
    # ordem importa: dimensões antes dos fatos, fatos antes das métricas
    mart_order = [
        "models/marts/dim_customer.sql",
        "models/marts/dim_product.sql",
        "models/marts/dim_date.sql",
        "models/marts/fact_orders.sql",
        "models/marts/metrics_monthly_revenue.sql",
        "models/marts/metrics_customer_ltv.sql",
    ]
    for path in mart_order:
        print(f"  -> {path}")
        run_sql_file(cur, path)

    conn.commit()

    print("\n== 4. Testes de qualidade ==")
    failures = run_all_tests(conn)

    print("\n== 5. Resumo de negócio ==")
    total_revenue = cur.execute(
        "SELECT ROUND(SUM(net_revenue), 2) FROM metrics_monthly_revenue"
    ).fetchone()[0]
    total_customers = cur.execute("SELECT COUNT(*) FROM dim_customer").fetchone()[0]
    active_customers = cur.execute(
        "SELECT COUNT(*) FROM metrics_customer_ltv WHERE completed_orders > 0"
    ).fetchone()[0]
    print(f"  Receita líquida total (2024-2025): R$ {total_revenue:,.2f}")
    print(f"  Clientes cadastrados: {total_customers}")
    print(f"  Clientes com pelo menos 1 pedido concluído: {active_customers}")

    conn.close()

    if failures:
        raise SystemExit(f"\nPipeline concluído com {failures} teste(s) falhando.")
    print("\nPipeline concluído com sucesso, todos os testes passaram.")


if __name__ == "__main__":
    main()
