# Enterprise Sales & Financial Performance Intelligence

Executive BI and analytics platform for revenue, profitability, growth, target variance, regional performance and customer/product sales intelligence.

This project turns a Power BI-style financial performance brief into a portfolio-ready analytics product with:

- PostgreSQL star schema and reproducible SQL reporting layer
- FastAPI backend exposing executive KPI, trend, breakdown and customer endpoints
- React dashboard for revenue, profitability and regional performance exploration
- Deterministic synthetic enterprise sales dataset
- Power BI-ready DAX measures, Power Query steps and row-level security design
- Docker Compose environment for one-command local execution

## Tech Stack

| Layer | Technologies |
|---|---|
| Business Intelligence | Power BI, DAX, Power Query, star schema modelling, row-level security |
| Backend API | Python, FastAPI, Pandas |
| Frontend | React, Vite, Recharts, Lucide React, CSS |
| Database | PostgreSQL, SQL views, indexed fact tables |
| Analytics | Revenue analysis, gross profit, margin, YoY growth, target variance |
| Data Engineering | Synthetic data generation, CSV ingestion, repeatable SQL loading |
| DevOps | Docker, Docker Compose, Nginx |
| Documentation | Markdown, KPI business logic, data dictionary, DAX and Power Query references |

## Architecture

```text
Power BI / React Executive Dashboard
              |
              v
      FastAPI Analytics API
              |
              v
 PostgreSQL Star Schema Warehouse
              |
              v
 SQL, DAX, Power Query and CSV assets
```

## Project Structure

```text
.
|-- backend/
|   |-- Dockerfile
|   |-- main.py
|   `-- requirements.txt
|-- data/
|   |-- dim_customer.csv
|   |-- dim_date.csv
|   |-- dim_product.csv
|   |-- dim_region.csv
|   |-- fact_sales.csv
|   `-- fact_targets.csv
|-- docs/
|   |-- BUSINESS_LOGIC.md
|   |-- DATA_DICTIONARY.md
|   |-- DAX_MEASURES.md
|   |-- POWER_QUERY_STEPS.md
|   `-- RECOMMENDATIONS.md
|-- frontend/
|   |-- src/
|   |   |-- App.jsx
|   |   `-- styles.css
|   |-- Dockerfile
|   |-- index.html
|   |-- nginx.conf
|   |-- package-lock.json
|   `-- package.json
|-- sql/
|   |-- 01_schema.sql
|   |-- 02_reporting_views.sql
|   |-- 03_rls.sql
|   `-- 04_load_csv.sql
|-- .dockerignore
|-- .gitignore
|-- docker-compose.yml
|-- generate_data.py
`-- README.md
```

## Business Questions Answered

- How much revenue and gross profit did the business generate?
- Which regions, segments, channels and product categories are driving performance?
- Are margins improving, or is profitability being eroded by cost and discount pressure?
- How is revenue trending month by month?
- Is the business ahead of or behind revenue targets?
- Which customers should executives drill into for growth or margin action?
- How can regional access be secured with row-level security?

## Metrics

| Metric | Definition |
|---|---|
| Revenue | Sum of sales value after discount, calculated as `quantity * unit_price` |
| Cost | Sum of direct product/service cost, calculated as `quantity * unit_cost` |
| Gross Profit | Revenue minus cost |
| Gross Margin % | Gross profit divided by revenue |
| YoY Revenue Growth % | Current selected-period revenue compared with the same period in the prior year |
| Target Revenue | Monthly revenue target by year, month and region |
| Target Variance | Actual revenue minus target revenue |
| Average Order Value | Revenue divided by distinct sales orders |

## Star Schema

Facts:

- `fact_sales`: order-level revenue, cost, quantity, discount, customer, product, date and region keys.
- `fact_targets`: monthly revenue target by year, month and region.

Dimensions:

- `dim_date`: calendar attributes for time intelligence.
- `dim_product`: product, category, list price, unit cost and portfolio.
- `dim_customer`: account, segment, industry, account status and region.
- `dim_region`: region, country, territory and regional manager ownership.

## Run With Docker

Requirements:

- Docker Desktop
- Docker Compose

Start the full stack:

```bash
docker compose up --build
```

Services:

| Service | URL |
|---|---|
| React dashboard | `http://127.0.0.1:5173` |
| FastAPI docs | `http://127.0.0.1:8000/docs` |
| PostgreSQL | `localhost:5432` |

Database credentials for local development:

```text
Database: enterprise_sales
User: analyst
Password: analyst_password
```

Stop the stack:

```bash
docker compose down
```

Reset the database and reload CSV data:

```bash
docker compose down -v
docker compose up --build
```

## Run Locally Without Docker

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

Open the dashboard at `http://127.0.0.1:5173`.

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/filters` | Available dashboard filters and date range |
| `GET /api/kpis` | Revenue, gross profit, margin, YoY growth, target variance and order count |
| `GET /api/trends` | Monthly revenue and gross profit trend |
| `GET /api/breakdown?by=region` | Revenue and gross profit by region, category, segment or channel |
| `GET /api/customers/top` | Top customers by revenue with segment, region, gross profit and margin |

Example KPI response:

```json
{
  "revenue": 124221129.31,
  "grossProfit": 55889956.27,
  "margin": 0.4499,
  "yoyGrowth": 0.0497,
  "targetRevenue": 111625871.93,
  "targetVariance": 12595257.38,
  "orders": 9500
}
```

## React Dashboard

The dashboard includes:

- Executive KPI cards for revenue, gross profit, YoY growth and target variance.
- Date, region and customer segment filters.
- Monthly revenue and gross profit trend.
- Regional revenue and profitability comparison.
- Top customer drill-through table.
- RLS-ready regional ownership design.

The frontend reads from the FastAPI backend at `http://127.0.0.1:8000/api`.

## PostgreSQL Reporting Layer

Create the schema manually:

```bash
psql -d your_database -f sql/01_schema.sql
```

Load the CSV files from `data/` using `COPY` or use the Docker init script:

```bash
psql -d your_database -f sql/04_load_csv.sql
```

Create reporting views and RLS objects:

```bash
psql -d your_database -f sql/02_reporting_views.sql
psql -d your_database -f sql/03_rls.sql
```

Reporting views:

- `vw_sales_enriched`
- `vw_monthly_financial_performance`
- `vw_customer_profitability`

When using Docker, the SQL files run automatically on first database startup and load all CSV data into PostgreSQL.

## Generate Synthetic Data

The dataset is deterministic, so the same command creates the same demo data each time:

```bash
python generate_data.py
```

Generated outputs:

- `data/dim_date.csv`
- `data/dim_region.csv`
- `data/dim_product.csv`
- `data/dim_customer.csv`
- `data/fact_sales.csv`
- `data/fact_targets.csv`

To refresh Docker PostgreSQL after regenerating data:

```bash
docker compose down -v
python generate_data.py
docker compose up --build
```

## Power BI Build Guide

1. Open Power BI Desktop.
2. Select Get Data > PostgreSQL database, or import the CSV files from `data/`.
3. Connect to `localhost:5432`.
4. Database: `enterprise_sales`.
5. Import the dimension and fact tables, or use the reporting views.
6. Create relationships:
   - `dim_date[date_key]` to `fact_sales[order_date]`
   - `dim_product[product_id]` to `fact_sales[product_id]`
   - `dim_customer[customer_id]` to `fact_sales[customer_id]`
   - `dim_region[region_id]` to `fact_sales[region_id]`
   - `dim_region[region_id]` to `fact_targets[region_id]`
7. Mark `dim_date` as the date table.
8. Apply the Power Query steps in `docs/POWER_QUERY_STEPS.md`.
9. Add the DAX measures in `docs/DAX_MEASURES.md`.
10. Configure row-level security using the regional access design in `docs/BUSINESS_LOGIC.md` and `sql/03_rls.sql`.

Suggested report pages:

- Executive Overview
- Sales Performance
- Profitability Analysis
- Regional Target Performance
- Customer Drill-Through
- RLS Validation

Suggested visuals:

- KPI cards for revenue, gross profit, margin, YoY growth and target variance.
- Line chart for monthly revenue and gross profit.
- Bar charts for region, category, channel and segment performance.
- Matrix visual for target variance by month and region.
- Table visual for customer-level revenue, gross profit and margin.
- Slicers for date, region, segment, category and channel.

## Portfolio Narrative

Recommended CV wording:

Built a Dockerized Enterprise Sales & Financial Performance Intelligence platform using PostgreSQL, FastAPI, React, Python, SQL, DAX and Power BI. Developed a star-schema sales model, documented KPI logic, created SQL reporting views, implemented regional row-level security design and delivered an executive dashboard for revenue, profitability, YoY growth and target-variance analysis.

Evidence to include:

- Screenshot of React executive dashboard.
- Screenshot of Power BI executive overview.
- Screenshot of Power BI customer drill-through page.
- Link to FastAPI `/docs` page.
- SQL schema and reporting views.
- DAX measure catalogue.
- Power Query transformation documentation.
- Data dictionary and business recommendations.

## Senior-Level Design Notes

- The model uses a clean star schema with conformed dimensions and separate sales and target facts.
- KPI logic is documented consistently across SQL, API, React and Power BI.
- SQL reporting views provide a tested semantic layer for BI consumption.
- Fact tables include indexes for date, region, product and customer filters.
- Docker Compose initialises PostgreSQL automatically from versioned SQL scripts.
- The API exposes stable analytics endpoints that can support both React and BI QA workflows.
- The frontend is API-driven and can be deployed independently from the backend.
- RLS is designed around regional ownership and can be implemented in both SQL and Power BI.

## Next Enhancements

- Add pytest coverage for API endpoints and KPI calculations.
- Add dbt models for transformation lineage and data quality tests.
- Add GitHub Actions for automated backend and frontend validation.
- Add authentication for executive and regional manager roles.
- Add a published `.pbix` file after Power BI visuals are finalised.
- Add screenshots to a `screenshots/` folder for the final portfolio presentation.
