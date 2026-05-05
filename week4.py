import pandas as pd

# Load datasets
listings = pd.read_csv("listings_with_mortgage_rates.csv", low_memory=False)
sold = pd.read_csv("sold_with_mortgage_rates.csv", low_memory=False)

def clean_dataset(df, name="dataset"):
    print(f"\n--- Cleaning {name} ---")
    
    before_rows = df.shape[0]

    # Convert date columns
    date_cols = [
        "CloseDate",
        "PurchaseContractDate",
        "ListingContractDate",
        "ContractStatusChangeDate"
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Remove unnecessary columns
    drop_cols = [col for col in df.columns if "Unnamed" in col]
    df = df.drop(columns=drop_cols, errors='ignore')

    # Ensure numeric types
    numeric_cols = [
        "ClosePrice", "LivingArea", "DaysOnMarket",
        "BedroomsTotal", "BathroomsTotalInteger", "Latitude", "Longitude"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Handle missing values
    df = df.dropna(subset=["ClosePrice", "LivingArea"], how='any')

    # Flag invalid numeric values
    df["invalid_price_flag"] = df["ClosePrice"] <= 0
    df["invalid_area_flag"] = df["LivingArea"] <= 0
    df["invalid_dom_flag"] = df["DaysOnMarket"] < 0
    df["invalid_beds_flag"] = df["BedroomsTotal"] < 0
    df["invalid_baths_flag"] = df["BathroomsTotalInteger"] < 0

    # Date consistency checks
    df["listing_after_close_flag"] = (
        df["ListingContractDate"] > df["CloseDate"]
    )
    df["purchase_after_close_flag"] = (
        df["PurchaseContractDate"] > df["CloseDate"]
    )
    df["negative_timeline_flag"] = (
        df["ListingContractDate"] > df["PurchaseContractDate"]
    )

    # Geographic checks
    df["missing_coords_flag"] = df["Latitude"].isna() | df["Longitude"].isna()
    df["zero_coords_flag"] = (df["Latitude"] == 0) | (df["Longitude"] == 0)
    df["positive_longitude_flag"] = df["Longitude"] > 0

    # California rough bounds 
    df["out_of_bounds_flag"] = (
        (df["Latitude"] < 32) | (df["Latitude"] > 42) |
        (df["Longitude"] < -125) | (df["Longitude"] > -114)
    )

    # Summary stats
    after_rows = df.shape[0]

    print(f"Rows before: {before_rows}")
    print(f"Rows after: {after_rows}")
    print("\nData types:\n", df.dtypes)

    print("\nDate flag counts:")
    print("listing_after_close:", df["listing_after_close_flag"].sum())
    print("purchase_after_close:", df["purchase_after_close_flag"].sum())
    print("negative_timeline:", df["negative_timeline_flag"].sum())

    print("\nGeographic flag counts:")
    print("missing_coords:", df["missing_coords_flag"].sum())
    print("zero_coords:", df["zero_coords_flag"].sum())
    print("positive_longitude:", df["positive_longitude_flag"].sum())
    print("out_of_bounds:", df["out_of_bounds_flag"].sum())

    return df


# Apply cleaning
listings_clean = clean_dataset(listings, "Listings")
sold_clean = clean_dataset(sold, "Sold")

# Save outputs
listings_clean.to_csv("listings_cleaned.csv", index=False)
sold_clean.to_csv("sold_cleaned.csv", index=False)
