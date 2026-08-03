-- dim_date
-- Dimensão de calendário gerada a partir do próprio intervalo de pedidos.
-- Evita hardcode de datas e cobre exatamente o período coberto pelos fatos.

DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date AS
WITH RECURSIVE calendar(date_day) AS (
    SELECT MIN(order_date) FROM stg_orders
    UNION ALL
    SELECT DATE(date_day, '+1 day') FROM calendar
    WHERE date_day < (SELECT MAX(order_date) FROM stg_orders)
)
SELECT
    date_day,
    CAST(STRFTIME('%Y', date_day) AS INTEGER)      AS year,
    CAST(STRFTIME('%m', date_day) AS INTEGER)      AS month,
    STRFTIME('%Y-%m', date_day)                    AS year_month,
    CAST(STRFTIME('%w', date_day) AS INTEGER)      AS weekday_num,
    CASE WHEN STRFTIME('%w', date_day) IN ('0', '6') THEN 1 ELSE 0 END AS is_weekend
FROM calendar;

CREATE UNIQUE INDEX idx_dim_date_day ON dim_date(date_day);
