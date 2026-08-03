-- fact_orders
-- Grão: um pedido. Agrega os itens do pedido em métricas de nível de
-- cabeçalho (receita bruta, receita líquida, quantidade de itens).
-- Pedidos cancelados/devolvidos entram na fato mas com flag própria,
-- para que quem consumir a tabela decida se inclui ou não na receita.

DROP TABLE IF EXISTS fact_orders;

CREATE TABLE fact_orders AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.channel,
    CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END AS is_completed,
    COUNT(oi.order_item_id)                             AS item_count,
    SUM(oi.quantity)                                     AS unit_count,
    ROUND(SUM(oi.unit_price * oi.quantity), 2)           AS gross_amount,
    ROUND(SUM(oi.net_amount), 2)                         AS net_amount
FROM stg_orders o
JOIN stg_order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, o.customer_id, o.order_date, o.status, o.channel;

CREATE UNIQUE INDEX idx_fact_orders_id ON fact_orders(order_id);
CREATE INDEX idx_fact_orders_customer ON fact_orders(customer_id);
CREATE INDEX idx_fact_orders_date ON fact_orders(order_date);
