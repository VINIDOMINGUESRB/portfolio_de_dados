-- stg_orders
-- Só considera pedidos com status válido e cliente existente
-- (defesa contra órfãos, mesmo que nesta base sintética não devam ocorrer).

DROP VIEW IF EXISTS stg_orders;

CREATE VIEW stg_orders AS
SELECT
    o.order_id,
    o.customer_id,
    DATE(o.order_date) AS order_date,
    o.status,
    o.channel
FROM raw_orders o
WHERE o.status IN ('completed', 'cancelled', 'returned')
  AND o.customer_id IN (SELECT customer_id FROM raw_customers);
