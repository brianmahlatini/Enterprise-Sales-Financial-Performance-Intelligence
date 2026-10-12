from functools import lru_cache
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

app = FastAPI(title="Enterprise Sales & Financial Performance Intelligence API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache
def model():
    sales = pd.read_csv(DATA / "fact_sales.csv", parse_dates=["order_date"])
    products = pd.read_csv(DATA / "dim_product.csv")
    customers = pd.read_csv(DATA / "dim_customer.csv")
    regions = pd.read_csv(DATA / "dim_region.csv")
    targets = pd.read_csv(DATA / "fact_targets.csv")
    df = sales.merge(products, on="product_id").merge(customers, on="customer_id", suffixes=("", "_customer")).merge(regions, on="region_id")
    df["gross_profit"] = df["revenue"] - df["cost"]
    df["margin"] = df["gross_profit"] / df["revenue"]
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    return df, targets


def filtered(df, start=None, end=None, region=None, segment=None):
    out = df.copy()
    if start:
        out = out[out["order_date"] >= pd.to_datetime(start)]
    if end:
        out = out[out["order_date"] <= pd.to_datetime(end)]
    if region and region != "All":
        out = out[out["region"] == region]
    if segment and segment != "All":
        out = out[out["segment"] == segment]
    return out


@app.get("/api/filters")
def filters():
    df, _ = model()
    return {
        "regions": ["All"] + sorted(df["region"].unique().tolist()),
        "segments": ["All"] + sorted(df["segment"].unique().tolist()),
        "minDate": df["order_date"].min().date().isoformat(),
        "maxDate": df["order_date"].max().date().isoformat(),
    }


@app.get("/api/kpis")
def kpis(start: str | None = None, end: str | None = None, region: str = "All", segment: str = "All"):
    df, targets = model()
    view = filtered(df, start, end, region, segment)
    revenue = float(view["revenue"].sum())
    cost = float(view["cost"].sum())
    gp = revenue - cost
    margin = gp / revenue if revenue else 0
    current_year = int(view["year"].max()) if len(view) else int(df["year"].max())
    cy = float(view[view["year"] == current_year]["revenue"].sum())
    py = float(view[view["year"] == current_year - 1]["revenue"].sum())
    yoy = (cy - py) / py if py else 0
    selected_months = view[["year", "month", "region_id"]].drop_duplicates()
    target_scope = targets.merge(selected_months, on=["year", "month", "region_id"])
    target = float(target_scope["target_revenue"].sum())
    return {
        "revenue": revenue,
        "grossProfit": gp,
        "margin": margin,
        "yoyGrowth": yoy,
        "targetRevenue": target,
        "targetVariance": revenue - target,
        "orders": int(view["sale_id"].nunique()),
    }


@app.get("/api/trends")
def trends(start: str | None = None, end: str | None = None, region: str = "All", segment: str = "All"):
    df, _ = model()
    view = filtered(df, start, end, region, segment)
    monthly = view.groupby(["year", "month"], as_index=False).agg(revenue=("revenue", "sum"), gross_profit=("gross_profit", "sum"))
    monthly["period"] = pd.to_datetime(monthly[["year", "month"]].assign(day=1)).dt.strftime("%Y-%m")
    return monthly.sort_values("period").to_dict("records")


@app.get("/api/breakdown")
def breakdown(by: str = "region", start: str | None = None, end: str | None = None):
    if by not in {"region", "category", "segment", "channel"}:
        raise HTTPException(status_code=400, detail="Breakdown must be region, category, segment or channel.")
    df, _ = model()
    view = filtered(df, start, end)
    grouped = view.groupby(by, as_index=False).agg(revenue=("revenue", "sum"), gross_profit=("gross_profit", "sum"))
    grouped["margin"] = grouped["gross_profit"] / grouped["revenue"]
    return grouped.sort_values("revenue", ascending=False).to_dict("records")


@app.get("/api/customers/top")
def top_customers(limit: int = 10):
    df, _ = model()
    grouped = df.groupby(["customer_name", "segment", "region"], as_index=False).agg(revenue=("revenue", "sum"), gross_profit=("gross_profit", "sum"))
    grouped["margin"] = grouped["gross_profit"] / grouped["revenue"]
    return grouped.sort_values("revenue", ascending=False).head(limit).to_dict("records")
