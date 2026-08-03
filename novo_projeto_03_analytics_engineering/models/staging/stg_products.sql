-- stg_products
-- Apenas padroniza tipos e remove eventuais preços negativos/zerados
-- (não deveriam existir, mas é boa prática validar na camada de staging).

DROP VIEW IF EXISTS stg_products;

CREATE VIEW stg_products AS
SELECT
    product_id,
    TRIM(product_name) AS product_name,
    category,
    subcategory,
    ROUND(price, 2)     AS price
FROM raw_products
WHERE price > 0;
