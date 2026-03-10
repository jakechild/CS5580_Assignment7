import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def average_salary_by_education(df):
    avg_salary = df.groupby('education_required', as_index=False)['annual_salary_usd'].mean().sort_values(by='annual_salary_usd', ascending=False)
    max_salary = df.groupby('education_required', as_index=False)['annual_salary_usd'].mean().sort_values(by='annual_salary_usd', ascending=False)
    min_salary = df.groupby('education_required', as_index=False)['annual_salary_usd'].min().sort_values(by='annual_salary_usd', ascending=False)

    colors_trace1 = ['#2ea557','#2ea567','#2ea577','#2ea587','#2ea597']
    colors_trace2 = ['#2eb557','#2eb567','#2eb577','#2eb587','#2eb597']
    colors_trace3 = ['#2ec557','#2ec567','#2ec577','#2ec587','#2ec597']
    
    fig = make_subplots(
        rows=3,
        cols=1,
        subplot_titles=[
            "Average Salary per Education Level",
            "Max Salary per Education Level",
            "Min Salary per Education Level"
        ]
    )

    fig.add_trace(go.Bar(
        x=avg_salary['education_required'],
        y=avg_salary['annual_salary_usd'],
        marker_color=colors_trace1
    ), row=1,col=1)

    fig.add_trace(go.Bar(
        x=max_salary['education_required'],
        y=max_salary['annual_salary_usd'],
        marker_color=colors_trace2
    ),row=2,col=1)

    fig.add_trace(go.Bar(
        x=min_salary['education_required'],
        y=min_salary['annual_salary_usd'],
        marker_color=colors_trace3
    ),row=3,col=1)

    fig.update_layout(showlegend=False)
    fig.write_html("education_v_salary.html")
    #fig.show()

# how many jobs required which level of education
def compare_jobs_vs_education(df):
    # Get unique values from the 'Students' column
    education_levels = df['education_required'].unique()

    counts = pd.DataFrame(columns=['education_required','jobs_available'])

    for level in education_levels:
        count = (df['education_required'] == level).sum()
        new_row_data = [level, count]
        counts.loc[len(counts)] = new_row_data

    print(counts)