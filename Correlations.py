import numpy as np
import pandas as pd
import plotly.express as px
from scipy import stats
import SalaryCountryHeatmap as shm
import EducationAnalysis as ea
import Benefits as ben

def correlationCalculations(df):
    correlationTable = df[[
        'job_categoryInt',
        'experience_levelInt',
        'years_of_experience',
        'education_requiredInt',
        'annual_salary_usd',
        'salary_min_usd',
        'salary_max_usd',
        'cityInt',
        'countryInt',
        'remote_workInt',
        'company_sizeInt',
        'industryInt',
        'ai_salary_premium_pct',
        'demand_score',
        'demand_growth_yoy_pct',
        'benefits_score_10',
        'posting_year',
        'posting_month',
        'is_senior',
        'is_remote_friendly',
        'is_llm_role',
        'salary_tierInt']].corr(method='pearson')

    heatFig = px.imshow(
        correlationTable, 
        text_auto=True, 
        aspect="auto",
        color_continuous_scale='RdBu_r', # Red-Blue scale is great for correlations
        range_color=[-1, 1],
        title="Multivariate Visualization Heatmap"
    )

    heatFig.write_html("Multivariate_Visualization_Heatmap.html")
    #heatFig.show()

    contingency_table = pd.crosstab(df['is_senior'], df['salary_tier'], margins=False)
    chi2Results = stats.chi2_contingency(contingency_table)[0:3]
    print('\nChi-Squared on is_senior with salary_tier as the dependent variable.')
    print(f"p-value: {chi2Results[1]}")
    print(stats.chi2_contingency(contingency_table)[0:3])

    contingency_table = pd.crosstab(df['country'], df['salary_tier'], margins=False)
    chi2Results = stats.chi2_contingency(contingency_table)[0:3]
    print('\nChi-Squared on country with salary_tier as the dependent variable.')
    print(f"p-value: {chi2Results[1]}")
    print(stats.chi2_contingency(contingency_table)[0:3])

    contingency_table = pd.crosstab(df['experience_level'], df['salary_tier'], margins=False)
    chi2Results = stats.chi2_contingency(contingency_table)[0:3]
    print('\nChi-Squared on experience_level with salary_tier as the dependent variable.')
    print(f"p-value: {chi2Results[1]}")
    print(stats.chi2_contingency(contingency_table)[0:3])

    contingency_table = pd.crosstab(df['company_size'], df['salary_tier'], margins=False)
    chi2Results = stats.chi2_contingency(contingency_table)[0:3]
    print('\nChi-Squared on company_size with salary_tier as the dependent variable.')
    print(f"p-value: {chi2Results[1]}")
    print(stats.chi2_contingency(contingency_table)[0:3])

    contingency_table = pd.crosstab(df['remote_work'], df['salary_tier'], margins=False)
    chi2Results = stats.chi2_contingency(contingency_table)[0:3]
    print('\nChi-Squared on remote_work with salary_tier as the dependent variable.')
    print(f"p-value: {chi2Results[1]}")
    print(stats.chi2_contingency(contingency_table)[0:3])
