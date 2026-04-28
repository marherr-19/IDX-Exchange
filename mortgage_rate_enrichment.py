import pandas as pd

# Load filtered datasets
sold = pd.read_csv("filtered_residential_sold.csv", low_memory=False)
listings = pd.read_csv("filtered_residential_listings.csv", low_memory=False)

# Fetch the data
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])

# Lightly inspect the data
mortgage.columns = ['date', 'rate_30yr_fixed']
print("\nMortgage Data Preview:")
print(mortgage.head())

# Resample to monthly
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed']
    .mean()
    .reset_index()
)
print("\nMonthly Mortgage Rates:")
print(mortgage_monthly.head())

# Create join keys
# SOLD → use CloseDate
sold['CloseDate'] = pd.to_datetime(sold['CloseDate'], errors='coerce')
sold['year_month'] = sold['CloseDate'].dt.to_period('M')
# LISTINGS → use ListingContractDate
listings['ListingContractDate'] = pd.to_datetime(listings['ListingContractDate'], errors='coerce')
listings['year_month'] = listings['ListingContractDate'].dt.to_period('M')

# Merge
sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')

# Validate
print("\nMissing mortgage rates (sold):", sold_with_rates['rate_30yr_fixed'].isnull().sum())
print("Missing mortgage rates (listings):", listings_with_rates['rate_30yr_fixed'].isnull().sum())

# Preview
print("\nSold Preview with Rates:")
print(sold_with_rates[['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']].head())

# Write as CSV files
sold_with_rates.to_csv("sold_with_mortgage_rates.csv", index=False)
listings_with_rates.to_csv("listings_with_mortgage_rates.csv", index=False)
