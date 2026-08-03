-- metrics_customer_ltv
-- Mart de negócio: valor total gasto por cliente (pedidos concluídos),
-- número de pedidos e ticket médio. Base para a análise de segmentação
-- do projeto seguinte do portfólio (RFM + clustering).

DROP TABLE IF EXISTS metrics_customer_ltv;

CREATE TABLE metrics_customer_ltv AS
SELECT
    c.customer_id,
    c.segment,
    c.acquisition_channel,
    c.signup_date,
    COUNT(f.order_id)                                            AS completed_orders,
    ROUND(COALESCE(SUM(f.net_amount), 0), 2)                     AS lifetime_value,
    MAX(f.order_date)                                            AS last_order_date
FROM dim_customer c
LEFT JOIN fact_orders f
    ON f.customer_id = c.customer_id AND f.status = 'completed'
GROUP BY c.customer_id, c.segment, c.acquisition_channel, c.signup_date;
