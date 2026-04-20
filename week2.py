import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
sold = pd.read_csv("combined_sold_residential.csv", low_memory=False)

# Inspect dataset structure
print("Shape (rows, cols):", sold.shape)
print("\nColumns:")
print(sold.columns)
print("\nPreview:")
print(sold.head())
print("\nData types:")
print(sold.dtypes)

# Unique property types
property_types = sold['PropertyType'].unique()
print("\nProperty Types Found:")
print(property_types)

# Filter residential (sanity check)
sold = sold[sold['PropertyType'] == 'Residential']
print("\nShape after filtering:", sold.shape)

# Count missing values
missing_counts = sold.isnull().sum()

# Percent missing
missing_percent = (missing_counts / len(sold)) * 100

# Combine into one table
missing_df = pd.DataFrame({
    'MissingCount': missing_counts,
    'MissingPercent': missing_percent
})

print("\nMissing Value Summary:")
print(missing_df.sort_values(by = 'MissingPercent', ascending=False))

# Flag columns with >90% missing
high_missing = missing_df[missing_df['MissingPercent'] > 90]
print("\nColumns with >90% missing:")
print(high_missing)

# Numeric distribution summary
numeric_cols = [ 'ClosePrice', 'LivingArea', 'DaysOnMarket' ]
summary = sold[numeric_cols].describe(percentiles = [0.25, 0.5, 0.75, 0.9, 0.95])
print("\nNumeric Summary:")
print(summary)

# Histograms and Boxplots
for col in numeric_cols:
    plt.figure()
    sold[col].hist(bins = 50)
    plt.title(f"{col} Histogram")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.show()

    plt.figure()
    sold.boxplot(column = col)
    plt.title(f"{col} Boxplot")
    plt.show()

# Negative DaysOnMarket
invalid_dom = sold[sold['DaysOnMarket'] < 0]
print("Negative DaysOnMarket records:", len(invalid_dom))

# Zero prices
zero_prices = sold[sold['ClosePrice'] == 0]
print("Zero price records:", len(zero_prices))

# Flag outliers
print("Max ClosePrice:", sold['ClosePrice'].max())
print("Max LivingArea:", sold['LivingArea'].max())

# Residential vs others (already filtered?)
original = pd.read_csv("combined_sold_residential.csv", low_memory=False)
type_counts = original['PropertyType'].value_counts(normalize=True) * 100
print("\nProperty Type Share (%):")
print(type_counts)

# Median and Average close price
print("Median Close Price:", sold['ClosePrice'].median())
print("Average Close Price:", sold['ClosePrice'].mean())

# Days on market distribution
print(sold['DaysOnMarket'].describe())

# Above vs below list price
sold['AboveList'] = sold['ClosePrice'] > sold['ListPrice']
percent_above = sold['AboveList'].mean() * 100
print("Percent sold above list:", percent_above)

sold['BelowList'] = sold['ClosePrice'] < sold['ListPrice']
percent_below = sold['BelowList'].mean() * 100
print("Percent sold below list:", percent_below)

# Date consistency check
sold['CloseDate'] = pd.to_datetime(sold['CloseDate'], errors = 'coerce')
sold['ListingContractDate'] = pd.to_datetime(sold['ListingContractDate'], errors = 'coerce')
invalid_dates = sold[sold['CloseDate'] < sold['ListingContractDate']]
print("Invalid date records:", len(invalid_dates))

# Highest median prices by county
county_prices = sold.groupby('CountyOrParish')['ClosePrice'].median().sort_values(ascending=False)
print("\nMedian Price by County:")
print(county_prices.head(10))


# Check difference between old and new CSV
sold.to_csv("filtered_residential_sold.csv", index=False)
new = pd.read_csv("filtered_residential_sold.csv", low_memory=False)
print("Shape (rows, cols):", new.shape)
old = pd.read_csv("combined_sold_residential.csv", low_memory=False)
print("New columns:")
print(set(new.columns) - set(old.columns))
