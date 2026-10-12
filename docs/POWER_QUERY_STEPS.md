# Power Query Transformation Plan

1. Load CSV extracts from `data/` or connect Power BI directly to PostgreSQL views.
2. Promote headers and enforce data types for dates, whole numbers, decimal currency fields and text dimensions.
3. Trim and clean all text columns in customer, product and region dimensions.
4. Remove duplicates from dimension primary keys: `customer_id`, `product_id`, `region_id`, `date_key`.
5. Validate fact keys by merging `fact_sales` to each dimension using inner joins during QA.
6. Add `gross_profit = revenue - cost` only in SQL/reporting views or DAX, not as duplicated business logic in multiple places.
7. Disable load for staging queries and load only curated dimensions, facts and reporting views.
8. Mark `dim_date` as the date table in Power BI.

Model relationships:

- `dim_date[date_key]` 1:* `fact_sales[order_date]`
- `dim_product[product_id]` 1:* `fact_sales[product_id]`
- `dim_customer[customer_id]` 1:* `fact_sales[customer_id]`
- `dim_region[region_id]` 1:* `fact_sales[region_id]`
- `dim_region[region_id]` 1:* `fact_targets[region_id]`
