import csv
import random
from datetime import date, timedelta
from pathlib import Path


random.seed(42)
ROOT = Path(__file__).parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

regions = [
    (1, "North America", "United States", "Northeast", "Avery Stone"),
    (2, "North America", "Canada", "Ontario", "Maya Patel"),
    (3, "Europe", "United Kingdom", "England", "Noah Clarke"),
    (4, "Europe", "Germany", "Bavaria", "Lena Weber"),
    (5, "Africa", "South Africa", "Gauteng", "Thabo Mokoena"),
    (6, "Asia Pacific", "Australia", "New South Wales", "Olivia Chen"),
]

categories = {
    "Cloud": ["Analytics Platform", "Storage Suite", "AI Accelerator"],
    "Hardware": ["Edge Gateway", "Secure Laptop", "Network Appliance"],
    "Services": ["Implementation", "Premium Support", "Training"],
    "Software": ["CRM Pro", "FinanceOps", "Security Console"],
}

segments = ["Enterprise", "Mid-Market", "SMB", "Public Sector"]
channels = ["Direct", "Partner", "Marketplace"]
start_date = date(2022, 1, 1)
end_date = date(2025, 12, 31)


def write_csv(name, rows, header):
    with (DATA / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


date_rows = []
d = start_date
while d <= end_date:
    quarter = (d.month - 1) // 3 + 1
    date_rows.append(
        [
            d.isoformat(),
            d.year,
            quarter,
            f"Q{quarter}",
            d.month,
            d.strftime("%b"),
            d.day,
            d.isoweekday(),
            d.strftime("%A"),
            1 if d.month in (3, 6, 9, 12) else 0,
        ]
    )
    d += timedelta(days=1)

product_rows = []
product_id = 1
for category, names in categories.items():
    for name in names:
        unit_cost = random.randint(80, 900)
        list_price = round(unit_cost * random.uniform(1.35, 2.4), 2)
        product_rows.append([product_id, category, name, unit_cost, list_price, random.choice(["Core", "Growth", "Strategic"])])
        product_id += 1

customer_rows = []
for customer_id in range(1, 181):
    segment = random.choice(segments)
    region_id = random.choice(regions)[0]
    customer_rows.append(
        [
            customer_id,
            f"{random.choice(['Northstar', 'Apex', 'Summit', 'Vertex', 'BluePeak', 'Cobalt'])} {customer_id:03d}",
            segment,
            random.choice(["Technology", "Finance", "Retail", "Manufacturing", "Healthcare", "Education"]),
            region_id,
            random.choice(["Active", "At Risk", "Strategic"]),
        ]
    )

sales_rows = []
target_rows = []
sale_id = 1
for year in range(2022, 2026):
    for month in range(1, 13):
        for region_id, *_ in regions:
            base_target = random.randint(260_000, 520_000)
            growth_factor = 1 + (year - 2022) * random.uniform(0.05, 0.12)
            target_rows.append([year, month, region_id, round(base_target * growth_factor, 2)])

for _ in range(9500):
    order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    customer = random.choice(customer_rows)
    product = random.choice(product_rows)
    quantity = random.randint(1, 28)
    discount = random.choice([0, 0, 0.03, 0.05, 0.08, 0.12, 0.15])
    unit_price = round(product[4] * (1 - discount), 2)
    unit_cost = round(product[3] * random.uniform(0.94, 1.08), 2)
    sales_rows.append(
        [
            sale_id,
            order_date.isoformat(),
            customer[0],
            product[0],
            customer[4],
            random.choice(channels),
            quantity,
            unit_price,
            unit_cost,
            discount,
            round(quantity * unit_price, 2),
            round(quantity * unit_cost, 2),
        ]
    )
    sale_id += 1

write_csv("dim_date.csv", date_rows, ["date_key", "year", "quarter", "quarter_name", "month", "month_name", "day", "weekday_number", "weekday_name", "is_quarter_end"])
write_csv("dim_region.csv", regions, ["region_id", "region", "country", "territory", "regional_manager"])
write_csv("dim_product.csv", product_rows, ["product_id", "category", "product_name", "standard_unit_cost", "list_price", "portfolio"])
write_csv("dim_customer.csv", customer_rows, ["customer_id", "customer_name", "segment", "industry", "region_id", "account_status"])
write_csv("fact_sales.csv", sales_rows, ["sale_id", "order_date", "customer_id", "product_id", "region_id", "channel", "quantity", "unit_price", "unit_cost", "discount_rate", "revenue", "cost"])
write_csv("fact_targets.csv", target_rows, ["year", "month", "region_id", "target_revenue"])
print("Generated enterprise sales dataset in ./data")
