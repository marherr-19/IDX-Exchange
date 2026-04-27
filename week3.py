import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
listings = pd.read_csv("combined_listings_residential.csv", low_memory=False)

# Inspect dataset structure
print("Shape (rows, cols):", listings.shape)
print("\nColumns:")
print(listings.columns)
print("\nPreview:")
print(listings.head())
print("\nData types:")
print(listings.dtypes)

# Unique property types
property_types = listings['PropertyType'].unique()
print("\nProperty Types Found:")
print(property_types)

# Filter residential (sanity check)
listings = listings[listings['PropertyType'] == 'Residential']
print("\nShape after filtering:", listings.shape)

# Count missing values
missing_counts = listings.isnull().sum()

# Percent missing
missing_percent = (missing_counts / len(listings)) * 100

# Combine into one table
missing_df = pd.DataFrame({
    'MissingCount': missing_counts,
    'MissingPercent': missing_percent
})

print("\nMissing Value Summary:")
print(missing_df.sort_values(by='MissingPercent', ascending=False))

# Flag columns with >90% missing
high_missing = missing_df[missing_df['MissingPercent'] > 90]
print("\nColumns with >90% missing:")
print(high_missing)

# Drop high-missing columns (except core ones)
core_cols = ['ListPrice', 'LivingArea', 'DaysOnMarket']
cols_to_drop = [col for col in high_missing.index if col not in core_cols]
listings = listings.drop(columns=cols_to_drop)
print("\nDropped columns:", cols_to_drop)

# Numeric distribution summary
numeric_cols = [ 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres', 'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt' ]
numeric_cols = [col for col in numeric_cols if col in listings.columns]
summary = listings[numeric_cols].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95])
print("\nNumeric Summary:")
print(summary)

# Histograms and Boxplots
for col in numeric_cols:
    plt.figure()
    listings[col].hist(bins=50)
    plt.title(f"{col} Histogram")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.show()

    plt.figure()
    listings.boxplot(column=col)
    plt.title(f"{col} Boxplot")
    plt.show()

# Negative DaysOnMarket
invalid_dom = listings[listings['DaysOnMarket'] < 0]
print("Negative DaysOnMarket records:", len(invalid_dom))

# Zero prices
zero_prices = listings[listings['ListPrice'] == 0]
print("Zero price records:", len(zero_prices))

# Flag outliers
print("Max ListPrice:", listings['ListPrice'].max())
print("Max LivingArea:", listings['LivingArea'].max())

# Basic data cleaning
if 'DaysOnMarket' in listings.columns:
    listings = listings[listings['DaysOnMarket'] >= 0]
if 'ListPrice' in listings.columns:
    listings = listings[listings['ListPrice'] > 0]
print("After cleaning shape", listings.shape)

# Residential vs others (already filtered?)
original = pd.read_csv("combined_listings_residential.csv", low_memory=False)
type_counts = original['PropertyType'].value_counts(normalize=True) * 100
print("\nProperty Type Share (%):")
print(type_counts)

# Median and Average list price
print("Median List Price:", listings['ListPrice'].median())
print("Average List Price:", listings['ListPrice'].mean())

# Days on market distribution
print(listings['DaysOnMarket'].describe())

# Date consistency check (if available)
if 'ListingContractDate' in listings.columns and 'OnMarketDate' in listings.columns:
    listings['ListingContractDate'] = pd.to_datetime(listings['ListingContractDate'], errors='coerce')
    listings['OnMarketDate'] = pd.to_datetime(listings['OnMarketDate'], errors='coerce')
    invalid_dates = listings[listings['OnMarketDate'] < listings['ListingContractDate']]
    print("Invalid date records:", len(invalid_dates))

# Highest median prices by county
if 'CountyOrParish' in listings.columns:
    county_prices = listings.groupby('CountyOrParish')['ListPrice'].median().sort_values(ascending=False)
    print("\nMedian Price by County:")
    print(county_prices.head(10))

# Write new CSV file
listings.to_csv("filtered_residential_listings.csv", index = False)
