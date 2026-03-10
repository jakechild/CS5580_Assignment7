import numpy as np
import pandas as pd
import plotly.express as px
import SalaryCountryHeatmap as shm


df = pd.read_csv('ai_jobs_market_2025_2026.csv')

# Make the category columns actual categories
cols_to_convert = ['job_category', 'experience_level', 'education_required', 'company_size', 'remote_work', 'industry', 'salary_tier']
df[cols_to_convert] = df[cols_to_convert].astype('category')

# Fix the country names for plotly
iso_map = {
    "USA": "USA",
    "UK": "GBR",
    "Singapore": "SGP",
    "India": "IND",
    "Japan": "JPN",
    "China": "CHN",
    "Canada": "CAN",
    "UAE": "ARE",
    "Netherlands": "NLD",
    "France": "FRA",
    "Australia": "AUS",
    "Germany": "DEU",
    "Switzerland": "CHE"
}

df['iso_country_code'] = df['country'].map(iso_map)

print(df.info())
print(df.describe())
print(df.head())

shm.generate_salary_heatmaps(df)
