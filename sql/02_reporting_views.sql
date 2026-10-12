set search_path to enterprise_sales;

create or replace view vw_sales_enriched as
select
  fs.sale_id,
  fs.order_date,
  dd.year,
  dd.quarter_name,
  dd.month,
  dd.month_name,
  dc.customer_name,
  dc.segment,
  dc.industry,
  dc.account_status,
  dp.category,
  dp.product_name,
  dp.portfolio,
  dr.region,
  dr.country,
  dr.territory,
  dr.regional_manager,
  fs.channel,
  fs.quantity,
  fs.revenue,
  fs.cost,
  fs.revenue - fs.cost as gross_profit,
  case when fs.revenue = 0 then 0 else (fs.revenue - fs.cost) / fs.revenue end as gross_margin
from fact_sales fs
join dim_date dd on dd.date_key = fs.order_date
join dim_customer dc on dc.customer_id = fs.customer_id
join dim_product dp on dp.product_id = fs.product_id
join dim_region dr on dr.region_id = fs.region_id;

create or replace view vw_monthly_financial_performance as
with monthly_sales as (
  select
    s.year,
    s.month,
    r.region_id,
    s.region,
    sum(s.revenue) as revenue,
    sum(s.cost) as cost,
    sum(s.gross_profit) as gross_profit
  from vw_sales_enriched s
  join dim_region r on r.region = s.region
  group by s.year, s.month, r.region_id, s.region
)
select
  ms.year,
  ms.month,
  ms.region,
  ms.revenue,
  ms.cost,
  ms.gross_profit,
  case when ms.revenue = 0 then 0 else ms.gross_profit / ms.revenue end as gross_margin,
  coalesce(t.target_revenue, 0) as target_revenue,
  ms.revenue - coalesce(t.target_revenue, 0) as target_variance
from monthly_sales ms
left join fact_targets t on t.year = ms.year and t.month = ms.month and t.region_id = ms.region_id;

create or replace view vw_customer_profitability as
select
  customer_name,
  segment,
  region,
  count(distinct sale_id) as order_count,
  sum(revenue) as revenue,
  sum(gross_profit) as gross_profit,
  case when sum(revenue) = 0 then 0 else sum(gross_profit) / sum(revenue) end as gross_margin
from vw_sales_enriched
group by customer_name, segment, region;
