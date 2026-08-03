-- dim_customer
-- Dimensão de cliente. Guarda o atributo "segment" (regular/premium) como
-- SCD tipo 1 (sobrescreve) já que, para este caso de uso, não há necessidade
-- de reter histórico de mudança de segmento.

DROP TABLE IF EXISTS dim_customer;

CREATE TABLE dim_customer AS
SELECT
    customer_id,
    email,
    city,
    state,
    signup_date,
    segment,
    acquisition_channel
FROM stg_customers;

CREATE UNIQUE INDEX idx_dim_customer_id ON dim_customer(customer_id);
