
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
df = pd.read_csv("car_prices.csv", low_memory=False)

print("Original dataset shape:", df.shape)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows that are completely empty
df = df.dropna(how="all")

# Save cleaned dataset
df.to_csv("car_prices_cleaned.csv", index=False)

print("\nMissing values:")
print(df.isnull().sum().sort_values(ascending=False).head(10))

print("\nDataset information:")
print(df.info())

# Find useful columns for analysis
print("\nAvailable columns:", df.columns.tolist())

# Create charts for common car-price dataset columns
price_col = next(
    (c for c in ["sellingprice", "selling_price", "price"] if c in df.columns),
    None
)
year_col = next(
    (c for c in ["year", "model_year"] if c in df.columns),
    None
)
make_col = next(
    (c for c in ["make", "brand"] if c in df.columns),
    None
)

if price_col:
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
    df[price_col].dropna().plot(kind="hist", bins=30, title="Car Price Distribution")
    plt.xlabel("Price")
    plt.tight_layout()
    plt.savefig("chart1_price_distribution.png")
    plt.close()

if year_col and price_col:
    df[year_col] = pd.to_numeric(df[year_col], errors="coerce")
    df.groupby(year_col)[price_col].mean().dropna().sort_index().plot(
        kind="line", title="Average Price by Year"
    )
    plt.ylabel("Average Price")
    plt.tight_layout()
    plt.savefig("chart2_average_price_by_year.png")
    plt.close()

if make_col and price_col:
    df.groupby(make_col)[price_col].mean().dropna().nlargest(10).sort_values().plot(
        kind="barh", title="Top 10 Makes by Average Price"
    )
    plt.xlabel("Average Price")
    plt.tight_layout()
    plt.savefig("chart3_top_makes.png")
    plt.close()

print("\nCleaning complete. Charts created where matching columns exist.")

