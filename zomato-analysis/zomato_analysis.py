# # import pandas as pd
# # import numpy as np
# # import matplotlib.pyplot as plt
# # import seaborn as sns
# # # Load the dataset
# # df = pd.read_csv("zomato.csv")   # or your file name
# # print(df.head())

# # print(df.shape)
# # print(df.columns)
# # print(df.info())
# # print(df.describe())

# # Step 1: Import libraries
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Step 2: Load dataset

# df = pd.read_csv(r"C:\Users\ASUS\Downloads\zomato.csv")
# print(df.head())

# # Step 3: Explore data
# print(df.shape)
# print(df.columns)
# print(df.info())

# # Step 4: Data cleaning
# df.drop(['url','phone'], axis=1, inplace=True)

# df['rate'] = df['rate'].str.replace('/5', '')
# df['rate'] = pd.to_numeric(df['rate'], errors='coerce')

# df['approx_cost(for two people)'] = df['approx_cost(for two people)'].str.replace(',', '')
# df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'])

# df.dropna(inplace=True)

# # Step 5: Analysis
# print(df['location'].value_counts().head(10))
# print(df.groupby('online_order')['rate'].mean())

# # Step 6: Visualization
# sns.histplot(df['rate'], bins=20)
# plt.title("Rating Distribution")
# plt.show()

# df['location'].value_counts().head(10).plot(kind='bar')
# plt.title("Top Locations")
# plt.show()
# # Step 7: Advanced Analysis

# # Top rated restaurants
# top_restaurants = df.sort_values(by=['rate', 'votes'], ascending=False)
# print(top_restaurants[['name','rate','votes']].head(10))

# # Most popular cuisines
# print(df['cuisines'].value_counts().head(10))

# # Location-wise average rating
# location_rating = df.groupby('location')['rate'].mean().sort_values(ascending=False)
# print(location_rating.head(10))
# # Heatmap (important)
# plt.figure(figsize=(10,6))
# sns.heatmap(df.corr(numeric_only=True), annot=True)
# plt.title("Correlation Heatmap")
# plt.show()

# # Online order vs rating
# sns.boxplot(x='online_order', y='rate', data=df)
# plt.title("Online Order vs Rating")
# plt.show()
# # ---------------- INSIGHTS ----------------
# # 1. Most restaurants are located in popular areas like BTM and Koramangala
# # 2. Online ordering has a slight effect on ratings
# # 3. High cost does not always mean high rating
# # 4. Some cuisines dominate the market
# # -----------------------------------------
# df.to_csv("cleaned_zomato.csv", index=False)

# ================= ZOMATO DATA ANALYSIS PROJECT =================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- STEP 1: LOAD DATASET SAFELY ---
# This part automatically finds the folder where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "zomato.csv")

try:
    df = pd.read_csv(file_path)
    print(f"Successfully loaded: {file_path}")
except FileNotFoundError:
    print(f"ERROR: 'zomato.csv' not found in {script_dir}")
    print("Please move the CSV file into the same folder as this script.")
    exit()

# --- STEP 2: DATA CLEANING ---
# 1. Clean column names
df.columns = df.columns.str.strip()

# 2. Drop unnecessary columns (using errors='ignore' to prevent crashes)
cols_to_drop = ['url', 'address', 'phone', 'menu_item', 'reviews_list']
df.drop(columns=[c for c in cols_to_drop if c in df.columns], inplace=True, errors='ignore')

# 3. Clean 'rate' column (Handles '4.1/5', 'NEW', '-', and NaNs)
def clean_rate(value):
    if isinstance(value, str):
        value = value.split('/')[0].strip()
        if value == 'NEW' or value == '-':
            return np.nan
        try:
            return float(value)
        except ValueError:
            return np.nan
    return value

df['rate'] = df['rate'].apply(clean_rate)

# 4. Clean 'approx_cost(for two people)' column
cost_col = 'approx_cost(for two people)'
if cost_col in df.columns:
    df[cost_col] = df[cost_col].astype(str).str.replace(',', '', regex=False)
    df[cost_col] = pd.to_numeric(df[cost_col], errors='coerce')

# 5. Remove missing values in critical columns
df.dropna(subset=['rate', cost_col, 'cuisines', 'location'], inplace=True)

print("\nData Cleaning Complete!")
print(f"Remaining rows: {df.shape[0]}")

# --- STEP 3: VISUALIZATIONS ---
sns.set_theme(style="whitegrid")

# Create a figure with multiple plots
plt.figure(figsize=(15, 10))

# Plot 1: Rating Distribution
plt.subplot(2, 2, 1)
sns.histplot(df['rate'], bins=15, kde=True, color='teal')
plt.title("Distribution of Ratings")

# Plot 2: Top 10 Locations
plt.subplot(2, 2, 2)
df['location'].value_counts().head(10).plot(kind='bar', color='coral')
plt.title("Top 10 Locations (Count)")
plt.xticks(rotation=45)

# Plot 3: Online Order vs Rating
plt.subplot(2, 2, 3)
sns.boxplot(x='online_order', y='rate', data=df, palette='Set2')
plt.title("Online Order vs Rating")

# Plot 4: Correlation Heatmap
plt.subplot(2, 2, 4)
numeric_df = df.select_dtypes(include=[np.number])
sns.heatmap(numeric_df.corr(), annot=True, cmap='YlGnBu', fmt=".2f")
plt.title("Correlation Heatmap")

plt.tight_layout()
plt.show()

# --- STEP 4: ANALYSIS & INSIGHTS ---
print("\n" + "="*40)
print("             FINAL INSIGHTS")
print("="*40)

# Top 5 Cuisines
print(f"\n1. Top 5 Most Popular Cuisines:\n{df['cuisines'].value_counts().head(5)}")

# Best Rated Locations
loc_rating = df.groupby('location')['rate'].mean().sort_values(ascending=False).head(5)
print(f"\n2. Best Rated Locations (Average):\n{loc_rating}")

# Relation between Cost and Rating
correlation = df['rate'].corr(df[cost_col])
print(f"\n3. Correlation between Cost and Rating: {correlation:.2f}")
print("   (Interpretation: Values near 0 mean cost doesn't dictate quality)")

# --- STEP 5: SAVE CLEANED DATA ---
output_name = "cleaned_zomato_data.csv"
df.to_csv(output_name, index=False)
print(f"\nCleaned dataset saved as: {output_name}")