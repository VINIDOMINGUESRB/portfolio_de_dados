-- stg_customers
-- Normaliza nomes de cidade (títulos), preenche canal de aquisição nulo
-- como 'desconhecido' e garante um customer_id único.

DROP VIEW IF EXISTS stg_customers;

CREATE VIEW stg_customers AS
SELECT
    customer_id,
    LOWER(TRIM(email))                                   AS email,
    -- normaliza capitalização (raw_customers tem cidades em UPPER por sujeira proposital)
    UPPER(SUBSTR(TRIM(city), 1, 1)) || LOWER(SUBSTR(TRIM(city), 2)) AS city,
    state,
    DATE(signup_date)                                    AS signup_date,
    segment,
    COALESCE(acquisition_channel, 'desconhecido')         AS acquisition_channel
FROM raw_customers
WHERE customer_id IS NOT NULL;
