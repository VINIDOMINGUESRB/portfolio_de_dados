-- stg_order_items
-- Calcula o valor líquido do item (preço x quantidade x (1 - desconto)),
-- métrica que os marts vão reaproveitar em vários lugares.

DROP VIEW IF EXISTS stg_order_items;

CREATE VIEW stg_order_items AS
SELECT
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.discount_pct,
    ROUND(oi.unit_price * oi.quantity * (1 - oi.discount_pct), 2) AS net_amount
FROM raw_order_items oi
WHERE oi.quantity > 0;
