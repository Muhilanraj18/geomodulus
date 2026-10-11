import os
import pandas as pd


# ============================================================
# PATHS
# ============================================================

DATA_PATH = os.path.join(
    "data",
    "raw",
    "Correlation by ML_Data (1).xlsx"
)

OUTPUT_PATH = os.path.join(
    "data",
    "processed",
    "cleaned_soil_data.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("\n" + "=" * 60)
print("FEATURE ENGINEERING")
print("=" * 60)

df = pd.read_excel(DATA_PATH)

print("\nOriginal Dataset Shape:")
print(df.shape)


# ============================================================
# REMOVE UNWANTED COLUMNS
# ============================================================

df.drop(
    columns=[
        "S. No.",
        "Unnamed: 14",
        "Unnamed: 15"
    ],
    errors="ignore",
    inplace=True
)


# ============================================================
# HANDLE DEPTH OF REINFORCEMENT
# ============================================================

df["Depth of reinforcement"] = (
    df["Depth of reinforcement"].fillna(0)
)


# ============================================================
# CHECK ORIGINAL REINFORCEMENT CATEGORIES
# ============================================================

print("\nOriginal Reinforcement Categories:")

print(
    df["Reinforced/Unreinforced"]
    .dropna()
    .unique()
)


# ============================================================
# REINFORCEMENT ENCODING
# ============================================================

# Convert to string, remove spaces and convert to lowercase

reinforcement = (
    df["Reinforced/Unreinforced"]
    .astype("string")
    .str.strip()
    .str.lower()
)


# Explicit mapping

reinforcement_mapping = {

    "ur": 0,

    "unreinforced": 0,

    "400 gsm": 1,

    "700 gsm": 2

}


# Apply mapping

df["Reinforced/Unreinforced"] = (
    reinforcement.map(reinforcement_mapping)
)


# Blank / missing reinforcement means Unreinforced

df["Reinforced/Unreinforced"] = (
    df["Reinforced/Unreinforced"]
    .fillna(0)
    .astype(int)
)


# ============================================================
# REINFORCEMENT ENCODING INFORMATION
# ============================================================

print("\nReinforcement Encoding:")

print("0 = Unreinforced / UR")
print("1 = 400 GSM")
print("2 = 700 GSM")


print("\nReinforcement Distribution:")

print(
    df["Reinforced/Unreinforced"]
    .value_counts()
    .sort_index()
)


# ============================================================
# SOAKED / UNSOAKED ENCODING
# ============================================================

soaked = (
    df["Soaked/Unsoaked"]
    .astype("string")
    .str.strip()
    .str.lower()
)


soaked_mapping = {

    "unsoaked": 0,

    "soaked": 1

}


df["Soaked/Unsoaked"] = (
    soaked.map(soaked_mapping)
)


# ============================================================
# CHECK SOAKED / UNSOAKED VALUES
# ============================================================

if df["Soaked/Unsoaked"].isna().any():

    print("\n❌ Unknown Soaked/Unsoaked category found.")

    raise ValueError(
        "Unknown Soaked/Unsoaked category found in dataset."
    )


df["Soaked/Unsoaked"] = (
    df["Soaked/Unsoaked"].astype(int)
)


print("\nSoaked Condition Encoding:")

print("0 = Unsoaked")
print("1 = Soaked")


# ============================================================
# VERIFY PI
# ============================================================

df["Calculated_PI"] = (
    df["LL"] - df["PL"]
)


print("\nChecking PI Difference:")

pi_difference = (
    df["PI"] - df["Calculated_PI"]
).abs().max()


print(pi_difference)


# ============================================================
# REMOVE HELPER COLUMN
# ============================================================

df.drop(
    columns=["Calculated_PI"],
    inplace=True
)


# ============================================================
# FINAL DATASET INFORMATION
# ============================================================

print("\nFinal Dataset Shape:")

print(df.shape)


print("\nMissing Values:")

print(
    df.isnull().sum()
)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)


# ============================================================
# SAVE CLEANED DATASET
# ============================================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 60)

print("✅ Cleaned dataset saved successfully")

print("=" * 60)

print("\nLocation:")

print(OUTPUT_PATH)