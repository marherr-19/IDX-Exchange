import pandas as pd

# -----------------------------
# Helper function to load monthly files
# -----------------------------
def load_monthly_data(prefix, start_ym, end_ym):
    dfs = []

    start_year = start_ym // 100
    start_month = start_ym % 100

    end_year = end_ym // 100
    end_month = end_ym % 100

    year = start_year
    month = start_month

    while (year < end_year) or (year == end_year and month <= end_month):

        file = f"raw/{prefix}{year}{month:02d}.csv"

        try:
            df = pd.read_csv(file, low_memory=False)
            dfs.append(df)
        except FileNotFoundError:
            print(f"Missing file: {file}")

        # increment month properly
        month += 1
        if month > 12:
            month = 1
            year += 1

    return dfs


# -----------------------------
# Define file ranges
# -----------------------------
START = 202401
END = 202603

# -----------------------------
# LOAD SOLD DATA
# -----------------------------
sold_dfs = load_monthly_data("CRMLSSold", START, END)

print("\nSOLD dataset before concat:", sum(len(df) for df in sold_dfs))

if len(sold_dfs) > 0:
    sold = pd.concat(sold_dfs, ignore_index=True)
else:
    print("No SOLD files found.")
    sold = pd.DataFrame()

print("SOLD dataset after concat:", len(sold))


# -----------------------------
# LOAD LISTINGS DATA
# -----------------------------
listings_dfs = load_monthly_data("CRMLSListing", START, END)

print("\nLISTINGS dataset before concat:", sum(len(df) for df in listings_dfs))

if len(listings_dfs) > 0:
    listings = pd.concat(listings_dfs, ignore_index=True)
else:
    print("No LISTINGS files found.")
    listings = pd.DataFrame()

print("LISTINGS dataset after concat:", len(listings))


# -----------------------------
# FILTER: Residential only
# -----------------------------
if not sold.empty:
    print("\nSOLD before Residential filter:", len(sold))
    sold = sold[sold["PropertyType"] == "Residential"]
    print("SOLD after Residential filter:", len(sold))

if not listings.empty:
    print("\nLISTINGS before Residential filter:", len(listings))
    listings = listings[listings["PropertyType"] == "Residential"]
    print("LISTINGS after Residential filter:", len(listings))


# -----------------------------
# SAVE OUTPUT FILES
# -----------------------------
sold.to_csv("combined_sold_residential.csv", index=False)
listings.to_csv("combined_listings_residential.csv", index=False)

print("\nSaved combined datasets successfully.")
