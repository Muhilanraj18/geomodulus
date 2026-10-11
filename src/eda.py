import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# PATHS
# =====================================================

DATA_PATH = os.path.join(
    "data",
    "processed",
    "cleaned_soil_data.csv"
)

PLOT_PATH = os.path.join(
    "reports",
    "plots"
)

os.makedirs(PLOT_PATH, exist_ok=True)

# =====================================================
# HELPER FUNCTION
# =====================================================

def safe_filename(name):
    """
    Convert column names into safe filenames.
    """
    return re.sub(r'[\\/*?:"<>|()]', "_", str(name)).replace(" ", "_")


# =====================================================
# LOAD DATA
# =====================================================

print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# =====================================================
# DATASET INFO
# =====================================================

print("\n" + "=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

print(df.info())

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

print("\nStatistical Summary")
print(df.describe(include="all"))

# =====================================================
# CORRELATION HEATMAP
# =====================================================

plt.figure(figsize=(14, 10))

sns.heatmap(
    df.corr(numeric_only=True),
    annot=True,
    cmap="coolwarm",
    linewidths=0.5,
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_PATH,
        "correlation_heatmap.png"
    )
)

plt.close()

# =====================================================
# MISSING VALUE HEATMAP
# =====================================================

plt.figure(figsize=(12, 6))

sns.heatmap(
    df.isnull(),
    cbar=False,
    cmap="viridis"
)

plt.title("Missing Value Heatmap")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_PATH,
        "missing_value_heatmap.png"
    )
)

plt.close()

# =====================================================
# HISTOGRAMS
# =====================================================

numeric_columns = df.select_dtypes(include=["number"]).columns

print("\nGenerating Histograms...")

for column in numeric_columns:

    plt.figure(figsize=(7,5))

    sns.histplot(
        df[column],
        kde=True,
        bins=20
    )

    plt.title(f"{column} Distribution")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PLOT_PATH,
            f"{safe_filename(column)}_distribution.png"
        )
    )

    plt.close()

# =====================================================
# BOXPLOTS
# =====================================================

print("Generating Boxplots...")

for column in numeric_columns:

    plt.figure(figsize=(6,4))

    sns.boxplot(
        y=df[column]
    )

    plt.title(f"{column} Boxplot")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PLOT_PATH,
            f"{safe_filename(column)}_boxplot.png"
        )
    )

    plt.close()

# =====================================================
# TARGET DISTRIBUTIONS
# =====================================================

targets = [
    "PLT E",
    "Geogauge E",
    "DCP E",
    "LWD E"
]

print("Generating Target Distributions...")

for target in targets:

    if target in df.columns:

        plt.figure(figsize=(7,5))

        sns.histplot(
            df[target].dropna(),
            kde=True,
            bins=20,
            color="green"
        )

        plt.title(target)

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                PLOT_PATH,
                f"{safe_filename(target)}_target_distribution.png"
            )
        )

        plt.close()

# =====================================================
# SAVE CLEAN SUMMARY
# =====================================================

summary = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values,
    "Data Type": df.dtypes.astype(str).values
})

summary.to_csv(
    os.path.join(
        "reports",
        "dataset_summary.csv"
    ),
    index=False
)

# =====================================================
# FINISHED
# =====================================================

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"Plots saved to : {PLOT_PATH}")
print("Dataset summary saved to : reports/dataset_summary.csv")
print(f"Total plots generated : {len(os.listdir(PLOT_PATH))}")