"""
Testes de qualidade de dados, no espírito dos testes genéricos do dbt
(unique, not_null, relationships, accepted_values), implementados aqui
diretamente em SQL/Python por não haver dbt disponível no ambiente de
execução deste projeto.

Cada função de teste retorna a quantidade de linhas que violam a regra.
0 = passou. Qualquer valor > 0 = falhou, e a run é interrompida com
código de saída != 0 (o mesmo comportamento que um `dbt test` teria
num pipeline de CI).
"""


def _count(conn, sql):
    return conn.execute(sql).fetchone()[0]


def test_unique(conn, table, column):
    sql = f"""
        SELECT COUNT(*) FROM (
            SELECT {column}, COUNT(*) c FROM {table}
            GROUP BY {column} HAVING c > 1
        )
    """
    return _count(conn, sql)


def test_not_null(conn, table, column):
    return _count(conn, f"SELECT COUNT(*) FROM {table} WHERE {column} IS NULL")


def test_relationship(conn, table, column, ref_table, ref_column):
    sql = f"""
        SELECT COUNT(*) FROM {table} t
        WHERE t.{column} IS NOT NULL
          AND t.{column} NOT IN (SELECT {ref_column} FROM {ref_table})
    """
    return _count(conn, sql)


def test_accepted_values(conn, table, column, values):
    values_sql = ", ".join(f"'{v}'" for v in values)
    sql = f"SELECT COUNT(*) FROM {table} WHERE {column} NOT IN ({values_sql})"
    return _count(conn, sql)


def test_non_negative(conn, table, column):
    return _count(conn, f"SELECT COUNT(*) FROM {table} WHERE {column} < 0")


CHECKS = [
    ("unique: dim_customer.customer_id", lambda c: test_unique(c, "dim_customer", "customer_id")),
    ("unique: dim_product.product_id", lambda c: test_unique(c, "dim_product", "product_id")),
    ("unique: fact_orders.order_id", lambda c: test_unique(c, "fact_orders", "order_id")),
    ("not_null: fact_orders.customer_id", lambda c: test_not_null(c, "fact_orders", "customer_id")),
    ("not_null: fact_orders.net_amount", lambda c: test_not_null(c, "fact_orders", "net_amount")),
    ("relationship: fact_orders.customer_id -> dim_customer",
     lambda c: test_relationship(c, "fact_orders", "customer_id", "dim_customer", "customer_id")),
    ("accepted_values: fact_orders.status",
     lambda c: test_accepted_values(c, "fact_orders", "status", ["completed", "cancelled", "returned"])),
    ("non_negative: fact_orders.net_amount", lambda c: test_non_negative(c, "fact_orders", "net_amount")),
    ("non_negative: metrics_customer_ltv.lifetime_value",
     lambda c: test_non_negative(c, "metrics_customer_ltv", "lifetime_value")),
]


def run_all_tests(conn):
    failures = 0
    for name, check in CHECKS:
        violations = check(conn)
        status = "PASS" if violations == 0 else "FAIL"
        if violations != 0:
            failures += 1
        print(f"  [{status}] {name} ({violations} violação(ões))")
    return failures
