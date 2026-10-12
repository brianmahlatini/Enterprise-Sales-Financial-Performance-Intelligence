# Enterprise Sales & Financial Performance Intelligence

Senior-level portfolio project for executive sales, profitability, growth and target-performance analysis using Power BI concepts, DAX, Power Query, SQL/PostgreSQL, FastAPI and React.

## Business Objective

The dashboard answers the questions executives ask every month:

- How much revenue and gross profit did we generate?
- Are margins improving or being eroded by discounts and product mix?
- Which regions, customer segments and product categories are driving growth?
- Are we ahead of or behind revenue targets?
- Where should leadership intervene?

## Project Architecture

```text
data/                 Synthetic enterprise star-schema CSV data
sql/                  PostgreSQL schema, reporting views and RLS policy
backend/              FastAPI analytics API over the generated model
frontend/             React executive dashboard
docs/                 Power BI model, DAX, Power Query and KPI documentation
generate_data.py      Deterministic synthetic data generator
```

## Star Schema

Facts:

- `fact_sales`: order-level revenue, cost, quantity, discounts and keys.
- `fact_targets`: monthly revenue target by region.

Dimensions:

- `dim_date`: marked date table for time intelligence.
- `dim_product`: category, product, list price, cost and portfolio.
- `dim_customer`: segment, industry, status and region.
- `dim_region`: geography and regional manager ownership.

## Run the Project

Generate the dataset:

```bash
python generate_data.py
```

Run the backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Run the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually `http://127.0.0.1:5173`.

## Run with Docker

The project includes Docker support for the full portfolio stack:

- PostgreSQL warehouse loaded with the generated star-schema CSVs.
- FastAPI analytics backend.
- React executive dashboard served through Nginx.

Build and start everything:

```bash
docker compose up --build
```

Then open:

- Dashboard: `http://127.0.0.1:5173`
- API docs: `http://127.0.0.1:8000/docs`
- PostgreSQL: `localhost:5432`

Default database credentials:

```text
Database: enterprise_sales
User: analyst
Password: analyst_password
```

Stop the stack:

```bash
docker compose down
```

Reset the database volume and reload CSV data from scratch:

```bash
docker compose down -v
docker compose up --build
```

## PostgreSQL Reporting Layer

Create the schema:

```bash
psql -d your_database -f sql/01_schema.sql
```

Load the CSV files from `data/` using `COPY` or your preferred ingestion process, then create reporting views:

```bash
psql -d your_database -f sql/02_reporting_views.sql
psql -d your_database -f sql/03_rls.sql
```

The reporting layer includes:

- `vw_sales_enriched`
- `vw_monthly_financial_performance`
- `vw_customer_profitability`

When using Docker, the files in `sql/` run automatically on the first database startup and `sql/04_load_csv.sql` loads the CSV files mounted from `data/`.

## Power BI Build Guide

1. Connect to PostgreSQL views or import the CSVs from `data/`.
2. Apply the Power Query cleaning steps in `docs/POWER_QUERY_STEPS.md`.
3. Build relationships exactly as described in the star schema section.
4. Add the DAX measures from `docs/DAX_MEASURES.md`.
5. Create report pages for executive overview, sales performance, profitability, customer drill-through and RLS validation.
6. Configure row-level security using `dim_region` ownership or the SQL access map.
7. Capture screenshots listed in `docs/RECOMMENDATIONS.md`.

## KPI Logic

The project centralises KPI definitions so SQL, API, React and Power BI tell the same story:

- Revenue = `quantity * unit_price`
- Gross Profit = `revenue - cost`
- Gross Margin % = `gross_profit / revenue`
- YoY Growth % = current-period revenue versus same period previous year
- Target Variance = actual revenue less assigned target revenue

Detailed definitions are in `docs/BUSINESS_LOGIC.md`.

## CV Evidence

This project demonstrates:

- Interactive executive dashboard with filters, KPIs, charts and customer drill-through table.
- Star schema design with sales fact, target fact and conformed dimensions.
- Documented DAX measures for revenue, gross profit, margin, YoY growth and target variance.
- Tested SQL reporting layer with indexed facts and curated views.
- Power Query transformation plan and data dictionary.
- Row-level security design for regional managers.
- Business recommendations grounded in sales and margin performance.

## Suggested Power BI Screenshots

Place final screenshots in a `screenshots/` folder:

- `01_executive_overview.png`
- `02_sales_trend.png`
- `03_profitability.png`
- `04_customer_drillthrough.png`
- `05_rls_validation.png`

## Quality Notes

- Data generation is deterministic for repeatable demos.
- API calculations intentionally mirror documented DAX measures.
- SQL indexes support common date, region, customer and product filters.
- The React dashboard is an auxiliary executive web interface; the Power BI artifacts remain fully documented for the BI deliverable.
