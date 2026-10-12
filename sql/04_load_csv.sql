set search_path to enterprise_sales;

copy dim_date (
  date_key,
  year,
  quarter,
  quarter_name,
  month,
  month_name,
  day,
  weekday_number,
  weekday_name,
  is_quarter_end
)
from '/data/dim_date.csv'
with (format csv, header true);

copy dim_region (
  region_id,
  region,
  country,
  territory,
  regional_manager
)
from '/data/dim_region.csv'
with (format csv, header true);

copy dim_product (
  product_id,
  category,
  product_name,
  standard_unit_cost,
  list_price,
  portfolio
)
from '/data/dim_product.csv'
with (format csv, header true);

copy dim_customer (
  customer_id,
  customer_name,
  segment,
  industry,
  region_id,
  account_status
)
from '/data/dim_customer.csv'
with (format csv, header true);

copy fact_sales (
  sale_id,
  order_date,
  customer_id,
  product_id,
  region_id,
  channel,
  quantity,
  unit_price,
  unit_cost,
  discount_rate,
  revenue,
  cost
)
from '/data/fact_sales.csv'
with (format csv, header true);

copy fact_targets (
  year,
  month,
  region_id,
  target_revenue
)
from '/data/fact_targets.csv'
with (format csv, header true);
