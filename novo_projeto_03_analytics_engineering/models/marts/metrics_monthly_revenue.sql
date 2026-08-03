-- metrics_monthly_revenue
-- Mart de negócio: receita líquida mensal, número de pedidos e ticket médio,
-- considerando apenas pedidos concluídos. É a tabela que alimentaria um
-- dashboard de receita.

DROP TABLE IF EXISTS metrics_monthly_revenue;

CREATE TABLE metrics_monthly_revenue AS
SELECT
    d.year_month,
    COUNT(DISTINCT f.order_id)               AS completed_orders,
    ROUND(SUM(f.net_amount), 2)              AS net_revenue,
    ROUND(SUM(f.net_amount) * 1.0 / COUNT(DISTINCT f.order_id), 2) AS avg_ticket
FROM fact_orders f
JOIN dim_date d ON d.date_day = f.order_date
WHERE f.status = 'completed'
GROUP BY d.year_month
ORDER BY d.year_month;
