-- dim_product

DROP TABLE IF EXISTS dim_product;

CREATE TABLE dim_product AS
SELECT
    product_id,
    product_name,
    category,
    subcategory,
    price AS current_price
FROM stg_products;

CREATE UNIQUE INDEX idx_dim_product_id ON dim_product(product_id);
