# DAX Measures

```DAX
Revenue = SUM ( fact_sales[revenue] )

Cost = SUM ( fact_sales[cost] )

Gross Profit = [Revenue] - [Cost]

Gross Margin % = DIVIDE ( [Gross Profit], [Revenue] )

Revenue PY =
CALCULATE ( [Revenue], SAMEPERIODLASTYEAR ( dim_date[date_key] ) )

YoY Revenue Growth % =
DIVIDE ( [Revenue] - [Revenue PY], [Revenue PY] )

Target Revenue = SUM ( fact_targets[target_revenue] )

Target Variance = [Revenue] - [Target Revenue]

Target Variance % = DIVIDE ( [Target Variance], [Target Revenue] )

Average Order Value =
DIVIDE ( [Revenue], DISTINCTCOUNT ( fact_sales[sale_id] ) )

Dynamic KPI Value =
SWITCH (
    SELECTEDVALUE ( 'KPI Selector'[KPI] ),
    "Revenue", [Revenue],
    "Gross Profit", [Gross Profit],
    "Gross Margin %", [Gross Margin %],
    "YoY Growth %", [YoY Revenue Growth %],
    "Target Variance", [Target Variance],
    [Revenue]
)
```

Recommended format strings:

- Revenue, Cost, Gross Profit, Target Revenue, Target Variance: currency, zero decimals.
- Gross Margin %, YoY Revenue Growth %, Target Variance %: percentage, one decimal.
- Average Order Value: currency, zero decimals.
