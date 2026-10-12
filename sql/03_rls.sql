set search_path to enterprise_sales;

alter table fact_sales enable row level security;

create table if not exists user_region_access (
  user_email text not null,
  region_id int not null references dim_region(region_id),
  primary key (user_email, region_id)
);

create policy region_sales_access on fact_sales
using (
  exists (
    select 1
    from user_region_access ura
    where ura.region_id = fact_sales.region_id
      and lower(ura.user_email) = lower(current_setting('app.current_user_email', true))
  )
);
