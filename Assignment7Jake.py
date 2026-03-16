import numpy as np
import pandas as pd
import plotly.express as px
from scipy import stats
import Benefits as ben
import Correlations as cor
import EducationAnalysis as ea
import SalaryCountryHeatmap as shm
import Skills as skills


df = pd.read_csv('ai_jobs_market_2025_2026.csv')

# Make the category columns actual categories
cols_to_convert = ['job_category', 'experience_level', 'education_required', 'company_size', 'remote_work', 'industry', 'salary_tier','city','country']
df[cols_to_convert] = df[cols_to_convert].astype('category')

for currCol in cols_to_convert:
    df[f"{currCol}Int"] = df[currCol].cat.codes

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

df["elite_salary"] = df["annual_salary_usd"] >= 300000

#print(df.info())
#print(df.describe())
#print(df.head())

# shm.generate_salary_heatmaps(df)
# ea.average_salary_by_education(df)
# ea.compare_jobs_vs_education(df)
# ben.plotBenefits(df)
# ben.computeCorrelation(df)
# cor.correlationCalculations(df)
skills.skillsProcessing(df)


# # calculate the percentage of each experience level category that have elite jobs
# experienceMean = df.groupby("experience_level")["elite_salary"].mean().mul(100).sort_values(ascending=False)

# # calculate the percetage of each education required category that have elite jobs
# educationMean = df.groupby("education_required")["elite_salary"].mean().mul(100).sort_values(ascending=False)

# # Calculate the percentage of each category that have elite jobs
# job_categoryMean = df.groupby("job_category")["elite_salary"].mean().mul(100).sort_values(ascending=False)

# print(f"\nExperience Level vs elite jobs\n{experienceMean}")
# print(f"\nEducation Required vs elite jobs\n{educationMean}")
# print(f"\nJob Category vs elite jobs\n{job_categoryMean}")
