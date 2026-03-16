import plotly.express as px
import pandas as pd

def plotBenefits(df):
    fig = px.scatter(
        df,
        x="benefits_score_10",
        y="annual_salary_usd",
        color="experience_level",
        title="Salary vs Benefits Score",
        labels={
            "benefits_score_10": "Benefits Score",
            "annual_salary_usd": "Annual Salary (USD)"
        }
    )

    #fig.show()

    fig = px.box(
        df,
        x="benefits_score_10",
        y="annual_salary_usd",
        title="Salary Distribution by Benefits Score"
    )

    #fig.show()

    fig = px.scatter(
        df,
        x="benefits_score_10",
        y="annual_salary_usd",
        color="industry",
        title="Salary vs Benefits by Industry"
    )

    #fig.show()

    fig = px.box(
        df,
        x="experience_level",
        y="benefits_score_10",
        title="Benefits Score by Experience Level"
    )

    #fig.show()

    fig = px.box(
        df,
        x="salary_tier",
        y="benefits_score_10",
        title="Benefits Score by Salary Tier"
    )

    #fig.show()

    fig = px.box(
        df,
        x="remote_work",
        y="benefits_score_10",
        title="Benefits Score by Remote Work Policy"
    )

    #fig.show()


def computeCorrelation(df):
    correlationTable = df[['benefits_score_10','annual_salary_usd']].corr()
    heatFig = px.imshow(
        correlationTable, 
        text_auto=True, 
        aspect="auto",
        color_continuous_scale='RdBu_r', # Red-Blue scale is great for correlations
        range_color=[-1, 1],
        title="Multivariate Visualization Heatmap"
    )

    heatFig.write_html("Benefits_score_vs_salary_Heatmap.html")

    correlationTable = df[['benefits_score_10','salary_min_usd','salary_max_usd','annual_salary_usd']].corr()
    heatFig = px.imshow(
        correlationTable, 
        text_auto=True, 
        aspect="auto",
        color_continuous_scale='RdBu_r', # Red-Blue scale is great for correlations
        range_color=[-1, 1],
        title="Multivariate Visualization Heatmap"
    )

    heatFig.write_html("Benefits_score_vs_all_salary_Heatmap.html")
    