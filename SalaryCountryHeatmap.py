
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as psp
from plotly.subplots import make_subplots

def generate_salary_heatmaps(df):
    # Remove the global entries from the data.
    df = df[df['country'] != 'Global'].copy()

    # Drop anything that still failed to map
    df = df.dropna(subset=["iso_country_code"])

    avg_salary = df.groupby(['country', 'iso_country_code'], as_index=False)['annual_salary_usd'].mean()
    min_salary = df.groupby(['country', 'iso_country_code'], as_index=False)['salary_min_usd'].mean()
    max_salary = df.groupby(['country', 'iso_country_code'], as_index=False)['salary_max_usd'].mean()

    # Shared scale across all maps so colors are comparable
    all_values = pd.concat([
        avg_salary["annual_salary_usd"],
        min_salary["salary_min_usd"],
        max_salary["salary_max_usd"]
    ])

    zmin = all_values.min()
    zmax = all_values.max()

    fig = make_subplots(
        rows=3,
        cols=1,
        specs=[
            [{"type": "choropleth"}],
            [{"type": "choropleth"}],
            [{"type": "choropleth"}]
        ],
        subplot_titles=[
            "Average Salary by Country",
            "Minimum Salary by Country",
            "Maximum Salary by Country"
        ],
        vertical_spacing=0.06
    )


    fig.add_trace(
        go.Choropleth(
            locations=avg_salary["iso_country_code"],
            z=avg_salary["annual_salary_usd"],
            text=avg_salary["country"],
            locationmode="ISO-3",
            colorscale="Viridis",
            zmin=zmin,
            zmax=zmax,
            colorbar_title="Salary (USD)",
            hovertemplate="<b>%{text}</b><br>Average Salary: $%{z:,.0f}<extra></extra>"
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Choropleth(
            locations=min_salary["iso_country_code"],
            z=min_salary["salary_min_usd"],
            text=min_salary["country"],
            locationmode="ISO-3",
            colorscale="Viridis",
            zmin=zmin,
            zmax=zmax,
            showscale=False,
            hovertemplate="<b>%{text}</b><br>Minimum Salary: $%{z:,.0f}<extra></extra>"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Choropleth(
            locations=max_salary["iso_country_code"],
            z=max_salary["salary_max_usd"],
            text=max_salary["country"],
            locationmode="ISO-3",
            colorscale="Viridis",
            zmin=zmin,
            zmax=zmax,
            showscale=False,
            hovertemplate="<b>%{text}</b><br>Maximum Salary: $%{z:,.0f}<extra></extra>"
        ),
        row=3, col=1
    )

    # Configure each geo subplot
    fig.update_geos(
        projection_type="natural earth",
        showframe=False,
        showcoastlines=True
    )

    fig.update_layout(
        title="Salary Heatmaps by Country",
        height=1200,
        margin=dict(t=80, b=30, l=20, r=20)
    )


    fig.write_html("salary_heatmaps.html")
    #fig.show()