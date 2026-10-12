# KPI Business Logic

- Revenue: recognised sales value after discount, calculated as `quantity * unit_price`.
- Gross Profit: revenue less direct product or service cost.
- Gross Margin %: gross profit divided by revenue; used to compare profitability across product mixes.
- YoY Growth %: current selected-period revenue compared with the same period in the prior year.
- Target Variance: actual revenue less assigned target revenue for the same region and month.
- Target Variance %: target variance divided by target revenue.
- Average Order Value: revenue divided by unique sales orders.

Dashboard pages:

1. Executive Overview: revenue, gross profit, margin, YoY growth and target variance.
2. Sales Performance: trend by month, region, segment, category and channel.
3. Profitability: margin analysis by product category, customer and region.
4. Drill-through: customer profile with revenue, margin, order count and product mix.
5. RLS Validation: region manager access matrix.

Row-level security:

- Power BI role: `Regional Manager`.
- Filter: `dim_region[regional_manager_email] = USERPRINCIPALNAME()` when using email-enabled access mapping.
- SQL equivalent is provided in `sql/03_rls.sql`.
