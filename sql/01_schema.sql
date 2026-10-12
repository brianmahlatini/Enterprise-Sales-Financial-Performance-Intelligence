create schema if not exists enterprise_sales;
set search_path to enterprise_sales;

drop table if exists fact_sales cascade;
drop table if exists fact_targets cascade;
drop table if exists dim_customer cascade;
drop table if exists dim_product cascade;
drop table if exists dim_region cascade;
drop table if exists dim_date cascade;

create table dim_date (
  date_key date primary key,
  year int not null,
  quarter int not null,
  quarter_name text not null,
  month int not null,
  month_name text not null,
  day int not null,
  weekday_number int not null,
  weekday_name text not null,
  is_quarter_end boolean not null
);

create table dim_region (
  region_id int primary key,
  region text not null,
  country text not null,
  territory text not null,
  regional_manager text not null
);

create table dim_product (
  product_id int primary key,
  category text not null,
  product_name text not null,
  standard_unit_cost numeric(12,2) not null,
  list_price numeric(12,2) not null,
  portfolio text not null
);

create table dim_customer (
  customer_id int primary key,
  customer_name text not null,
  segment text not null,
  industry text not null,
  region_id int not null references dim_region(region_id),
  account_status text not null
);

create table fact_sales (
  sale_id bigint primary key,
  order_date date not null references dim_date(date_key),
  customer_id int not null references dim_customer(customer_id),
  product_id int not null references dim_product(product_id),
  region_id int not null references dim_region(region_id),
  channel text not null,
  quantity int not null check (quantity > 0),
  unit_price numeric(12,2) not null,
  unit_cost numeric(12,2) not null,
  discount_rate numeric(5,4) not null,
  revenue numeric(14,2) not null,
  cost numeric(14,2) not null
);

create table fact_targets (
  year int not null,
  month int not null,
  region_id int not null references dim_region(region_id),
  target_revenue numeric(14,2) not null,
  primary key (year, month, region_id)
);

create index ix_fact_sales_order_date on fact_sales(order_date);
create index ix_fact_sales_region_date on fact_sales(region_id, order_date);
create index ix_fact_sales_customer on fact_sales(customer_id);
create index ix_fact_sales_product on fact_sales(product_id);
