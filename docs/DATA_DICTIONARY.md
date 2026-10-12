# Data Dictionary

## fact_sales

| Column | Definition |
|---|---|
| sale_id | Unique transaction identifier. |
| order_date | Date key linked to `dim_date`. |
| customer_id | Customer dimension foreign key. |
| product_id | Product dimension foreign key. |
| region_id | Region dimension foreign key used for RLS. |
| channel | Sales route: Direct, Partner or Marketplace. |
| quantity | Units sold. |
| unit_price | Discounted selling price. |
| unit_cost | Cost per unit. |
| discount_rate | Commercial discount applied. |
| revenue | Quantity multiplied by unit price. |
| cost | Quantity multiplied by unit cost. |

## fact_targets

Monthly revenue target by year, month and region.

## Dimensions

- `dim_date`: calendar attributes for time intelligence.
- `dim_product`: category, product, pricing and portfolio grouping.
- `dim_customer`: account, segment, industry and customer status.
- `dim_region`: region, country, territory and regional manager.
