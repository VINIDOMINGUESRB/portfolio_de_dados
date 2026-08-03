"""
Geração de dados brutos sintéticos para simular o banco transacional de um
e-commerce de médio porte no Brasil.

Por que dados sintéticos?
Este projeto tem como objetivo demonstrar modelagem dimensional e engenharia
analítica (staging -> marts, testes de qualidade), não a análise de um dataset
real específico. Gerar os próprios dados brutos permite controlar volume,
sazonalidade e "sujeira" propositalmente, e evita qualquer dependência de
fontes externas para reproduzir o projeto do zero.

As tabelas geradas imitam o que normalmente vem de um banco operacional
(Postgres/MySQL) antes de qualquer tratamento: nomes inconsistentes, nulos,
duplicidade ocasional e tipos "sujos" - exatamente o tipo de coisa que um
pipeline de staging precisa arrumar.
"""

import random
import sqlite3
from datetime import date, timedelta

random.seed(42)

DB_PATH = "warehouse.sqlite"

CITIES = [
    ("São Paulo", "SP"), ("Rio de Janeiro", "RJ"), ("Belo Horizonte", "MG"),
    ("Curitiba", "PR"), ("Porto Alegre", "RS"), ("Salvador", "BA"),
    ("Recife", "PE"), ("Fortaleza", "CE"), ("Brasília", "DF"),
    ("Campinas", "SP"), ("Goiânia", "GO"), ("Florianópolis", "SC"),
]

CHANNELS = ["organico", "google_ads", "meta_ads", "indicacao", "email", None]

CATEGORIES = {
    "Eletrônicos": ["Fones", "Carregadores", "Smartwatch", "Acessórios PC"],
    "Casa": ["Utensílios", "Decoração", "Organização", "Iluminação"],
    "Moda": ["Camisetas", "Calçados", "Acessórios", "Bolsas"],
    "Livros": ["Ficção", "Negócios", "Técnico", "Infantil"],
    "Esporte": ["Suplementos", "Roupas Esportivas", "Equipamentos", "Calçados Esportivos"],
}

START = date(2024, 1, 1)
END = date(2025, 12, 31)
N_DAYS = (END - START).days


def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def seasonality_weight(d: date) -> float:
    """Pico de vendas em novembro (Black Friday) e dezembro (Natal),
    leve queda em janeiro/fevereiro."""
    weight = 1.0
    if d.month == 11:
        weight = 2.6
    elif d.month == 12:
        weight = 1.9
    elif d.month in (1, 2):
        weight = 0.7
    # fim de semana vende um pouco menos (perfil B2C típico de semana)
    if d.weekday() >= 5:
        weight *= 0.85
    return weight


def gerar_customers(n=1500):
    rows = []
    for i in range(1, n + 1):
        city, state = random.choice(CITIES)
        signup = random_date(START, END - timedelta(days=1))
        segment = random.choices(["regular", "premium"], weights=[0.85, 0.15])[0]
        channel = random.choice(CHANNELS)
        # Sujeira proposital: alguns nomes de cidade com variação de grafia
        city_dirty = city if random.random() > 0.05 else city.upper()
        rows.append((i, f"cliente_{i}@exemplo.com", city_dirty, state,
                      signup.isoformat(), segment, channel))
    return rows


def gerar_products(n=150):
    rows = []
    pid = 1
    for category, subcats in CATEGORIES.items():
        per_cat = n // len(CATEGORIES)
        for _ in range(per_cat):
            subcat = random.choice(subcats)
            base_price = {
                "Eletrônicos": (80, 900),
                "Casa": (30, 400),
                "Moda": (40, 350),
                "Livros": (25, 120),
                "Esporte": (35, 500),
            }[category]
            price = round(random.uniform(*base_price), 2)
            rows.append((pid, f"{subcat} {pid}", category, subcat, price))
            pid += 1
    return rows


def gerar_orders_e_items(customers, products, n_orders=9000):
    orders = []
    items = []
    order_id = 1
    item_id = 1

    # peso de propensão de compra por dia, proporcional à sazonalidade
    days = [START + timedelta(days=x) for x in range(N_DAYS + 1)]
    weights = [seasonality_weight(d) for d in days]

    customer_ids = [c[0] for c in customers]
    customer_signup = {c[0]: date.fromisoformat(c[4]) for c in customers}
    product_ids_prices = [(p[0], p[4]) for p in products]

    for _ in range(n_orders):
        order_date = random.choices(days, weights=weights, k=1)[0]
        # só clientes que já existiam na data do pedido
        elig = [cid for cid in customer_ids if customer_signup[cid] <= order_date]
        if not elig:
            continue
        customer_id = random.choice(elig)

        status = random.choices(
            ["completed", "cancelled", "returned"], weights=[0.88, 0.07, 0.05]
        )[0]
        channel = random.choice(["site", "app", "marketplace"])

        orders.append((order_id, customer_id, order_date.isoformat(), status, channel))

        n_items = random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0]
        for _ in range(n_items):
            product_id, unit_price = random.choice(product_ids_prices)
            qty = random.choices([1, 2, 3], weights=[0.7, 0.22, 0.08])[0]
            discount = round(random.choices([0, 0.05, 0.1, 0.2], weights=[0.6, 0.2, 0.15, 0.05])[0], 2)
            items.append((item_id, order_id, product_id, qty, unit_price, discount))
            item_id += 1

        order_id += 1

    return orders, items


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript(
        """
        DROP TABLE IF EXISTS raw_customers;
        DROP TABLE IF EXISTS raw_products;
        DROP TABLE IF EXISTS raw_orders;
        DROP TABLE IF EXISTS raw_order_items;

        CREATE TABLE raw_customers (
            customer_id INTEGER,
            email TEXT,
            city TEXT,
            state TEXT,
            signup_date TEXT,
            segment TEXT,
            acquisition_channel TEXT
        );

        CREATE TABLE raw_products (
            product_id INTEGER,
            product_name TEXT,
            category TEXT,
            subcategory TEXT,
            price REAL
        );

        CREATE TABLE raw_orders (
            order_id INTEGER,
            customer_id INTEGER,
            order_date TEXT,
            status TEXT,
            channel TEXT
        );

        CREATE TABLE raw_order_items (
            order_item_id INTEGER,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            discount_pct REAL
        );
        """
    )

    customers = gerar_customers()
    products = gerar_products()
    orders, items = gerar_orders_e_items(customers, products)

    cur.executemany("INSERT INTO raw_customers VALUES (?,?,?,?,?,?,?)", customers)
    cur.executemany("INSERT INTO raw_products VALUES (?,?,?,?,?)", products)
    cur.executemany("INSERT INTO raw_orders VALUES (?,?,?,?,?)", orders)
    cur.executemany("INSERT INTO raw_order_items VALUES (?,?,?,?,?,?)", items)

    conn.commit()
    print(f"raw_customers: {len(customers)}")
    print(f"raw_products: {len(products)}")
    print(f"raw_orders: {len(orders)}")
    print(f"raw_order_items: {len(items)}")
    conn.close()


if __name__ == "__main__":
    main()
