import numpy as np
import pandas as pd
import plotly.express as px
from scipy import stats
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

# Look at the skills associated with jobs.
def skillsProcessing(df):
    import plotly.express as px

    skills_df = df.copy()

    # Makes the required_skills column a list of values instead of a '|' delimited string
    skills_df["required_skills"] = skills_df["required_skills"].str.split("|", regex=False)

    # Explodes each skill into it's own row.
    # JobID             Skill
    # 101               Python
    # 101               Leadership
    # 102               Python
    # 102               etc.
    skills_df = skills_df.explode("required_skills")

    skills_df.to_csv("output.csv")

    # Removes the whitespace from the values in the require_skills column
    skills_df["required_skills"] = skills_df["required_skills"].str.strip()

    # Prints the number of unique required_skills
    print(f"Number of unique skills {skills_df["required_skills"].nunique()}")

    # Print a list of the required_skills
    print(f"Unique Skills\n{skills_df['required_skills'].unique()}")

    # Set options to display all rows and columns
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)

    #
    skillsMean = (
        skills_df.groupby("required_skills")["elite_salary"]
        .agg(["mean","count"])
        .assign(percent=lambda x: (x["mean"] * 100).round(2))
        .sort_values("percent", ascending=False)
    )

    print(f"\nIf a job requires a specific skill, how likely is it to pay $300k or more?")
    for skill, row in skillsMean.iterrows():
        print(f"{skill:26}  {row['percent']:6.2f}%  ({int(row['count'])} jobs)")

    skills_plot = skillsMean.reset_index()

    # Create a scatter plot for visualizing the 
    fig = px.scatter(
        skills_plot,
        x="count",
        y="percent",
        size="count",
        text="required_skills",
        title="Skills Associated With $300k+ AI Jobs",
        labels={
            "count": "Number of Jobs Requiring Skill",
            "percent": "Elite Salary Rate (%)"
        }
    )

    # How to interpret
    # Region	    Meaning
    # top-right	    common + high paying skills
    # top-left	    rare elite skills
    # bottom-right	common but not elite
    # bottom-left	rare + low value

    fig.update_traces(textposition="top center")
    #fig.show()


    # Skills that appear most often in elite salary jobs.
    elite_skills = (
        skills_df[skills_df["elite_salary"]]
        .groupby("required_skills")
        .size()
        .sort_values(ascending=False)
    )

    print("\nSkills that appear most often in elite salary positions")
    print(elite_skills)

    elite_skills_df = elite_skills.head(20).reset_index()
    elite_skills_df.columns = ["Skill", "Elite Job Count"]

    fig = px.bar(
        elite_skills_df,
        x="Elite Job Count",
        y="Skill",
        orientation="h",
        color="Elite Job Count",
        color_continuous_scale="viridis",
        title="Most Common Skills in $300k+ AI Jobs"
    )

    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        coloraxis_colorbar=dict(title="Elite Jobs")
    )

    fig.show()

    # Plot the skill network clusters to see which skills are often paired with other skills
    #plot_elite_skill_network_with_clusters(df, min_edge_weight=5, top_n_skills=20)


    experience_order = ["Entry (0-2 yrs)", "Mid (3-5 yrs)", "Senior (6-9 yrs)", "Lead (10+ yrs)"]
    #skills_and_extra_feature(skills_df, "experience_level", "Experience Level", experience_order)
    education_order = ["Bootcamp/Self-taught", "Associate's", "Bachelor's", "Master's","PhD"]
    #skills_and_extra_feature(skills_df, "education_required", "Education Required", education_order)
    company_size_order = ["Startup (1-50)","SME (51-500)","Mid-size (501-5000)","Enterprise (5000+)","Big Tech (FAANG+)"]
    #skills_and_extra_feature(skills_df, "company_size", "Company Size", company_size_order)
    remote_work_order = ["Fully Remote","Hybrid","On-site"]
    #skills_and_extra_feature(skills_df, "remote_work", "Remote Work", remote_work_order)



    ##########################################################################################
    #skill + experience + education
    ##########################################################################################
    combo3 = (
        skills_df.groupby(
            ["required_skills", "experience_level", "education_required"])["elite_salary"]
        .agg(['mean','count']) # Get both the mean and the count so we can see if a mean of 1 is actually only 1 job.
        .assign(percent=lambda x: (x["mean"] * 100).round(2)) # Add a percent column that is the mean multipltied by 100 and rounded to two decimal places.
        .sort_values("percent", ascending=False) # Sort the values according to percent.
    )

    print("\nExperience + Education + Skills")
    for (skill, experience, education), row in combo3.iterrows():
        if(row['percent'] > 0.0):
            print(f"{skill:26}  {education:26} {experience:26} {row['percent']:6.2f}%  ({int(row['count'])} jobs)")

    combo3.to_csv("Experience_Education_Skills_groups.csv")




    group_counts = skills_df.groupby(
        ["required_skills", "experience_level"]
    ).size()

    valid_groups = group_counts[group_counts > 10].index

    combo = (
        skills_df.groupby(["required_skills", "experience_level"])["elite_salary"]
        .mean()
    )

    combo = combo.loc[valid_groups].sort_values(ascending=False).head(20)
    print("\nExperience Skills highly skilled groups")
    print(combo)

    import plotly.express as px

    elite_skill_rates = (
        skills_df.groupby("required_skills")["elite_salary"]
        .mean()
        .reset_index()
        .sort_values("elite_salary", ascending=False)
        .head(43)
    )

    fig = px.bar(
        elite_skill_rates,
        x="required_skills",
        y="elite_salary",
        title="Skills Most Associated With $300k+ AI Jobs"
    )

    #fig.show()


##########################################################################################
# Skills plus extra feature
# Get the percentage of jobs in that extra feature/skill group that have an elite salary
##########################################################################################
def skills_and_extra_feature(skills_df, extra_feature, feature_readable_name, feature_order):
    # Group by skill and extra feature.
    # Get the percentage of jobs in that extra feature/skill group that have an elite salary
    combo = (
        skills_df.groupby(["required_skills", extra_feature])["elite_salary"]
        .agg(["mean","count"])
        .assign(percent=lambda x: (x["mean"] * 100).round(2))
        .sort_values("percent", ascending=False)
    )

    print(f"\nSkill + {feature_readable_name} combinations most associated with $300k+ jobs:")
    for (skill, feature), row in combo.head(20).iterrows():
        print(f"{skill:26} {feature:26} {row['percent']:6.2f}%  ({int(row['count'])} jobs)")

    print(combo.groupby(["required_skills", extra_feature]).size().sort_values(ascending=False).head(20))

    combo = (
        skills_df.groupby(["required_skills", extra_feature])["elite_salary"]
        .agg(["mean", "count"])
        .assign(percent=lambda x: (x["mean"] * 100).round(2))
        .reset_index()
    )

    # Optional filtering
    skill_counts = skills_df.groupby("required_skills").size()
    valid_skills = skill_counts[skill_counts >= 10].index
    combo = combo[combo["required_skills"].isin(valid_skills)]

    top_skills = (
        skills_df.groupby("required_skills")
        .size()
        .sort_values(ascending=False)
        .head(100)
        .index
    )
    combo = combo[combo["required_skills"].isin(top_skills)]

    combo[extra_feature] = pd.Categorical(
        combo[extra_feature],
        categories=feature_order,
        ordered=True
    )

    percent_matrix = combo.pivot_table(
        index="required_skills",
        columns=extra_feature,
        values="percent",
        aggfunc="mean"
    )

    count_matrix = combo.pivot_table(
        index="required_skills",
        columns=extra_feature,
        values="count",
        aggfunc="sum"
    )

    fig = px.imshow(
        percent_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Viridis",
        labels=dict(
            x=feature_readable_name,
            y="Skill",
            color="Elite Salary %"
        ),
        title=f"Elite Salary Rate by Skill and {feature_readable_name}"
    )

    fig.update_traces(
        customdata=count_matrix,
        hovertemplate=(
            "Skill: %{y}<br>"
            "{feature_readable_name}: %{x}<br>"
            "Elite Salary Rate: %{z:.2f}%<br>"
            "Job Count: %{customdata}<extra></extra>"
        )
    )

    fig.update_layout(
        title=f"Percentage of jobs in the Skill and {feature_readable_name} group with an Elite Salary",
        xaxis_title=feature_readable_name,
        yaxis_title="Skill",
        height=1200
    )

    fig.update_xaxes(side="top")
    fig.show()

def plot_elite_skill_network_with_clusters(df, min_edge_weight=5, top_n_skills=20):
    # Create elite salary flag if it does not already exist
    if "elite_salary" not in df.columns:
        df = df.copy()
        df["elite_salary"] = df["annual_salary_usd"] >= 300000

    # Keep only elite jobs
    elite_df = df[df["elite_salary"]].copy()

    # Split skills into lists
    elite_df["required_skills"] = elite_df["required_skills"].str.split("|", regex=False)

    # Clean whitespace and handle missing values
    elite_df["required_skills"] = elite_df["required_skills"].apply(
        lambda skills: [skill.strip() for skill in skills if skill.strip()]
        if isinstance(skills, list) else []
    )

    # Count overall skill frequency in elite jobs
    all_skills = elite_df["required_skills"].explode().dropna()
    top_skills = all_skills.value_counts().head(top_n_skills)

    # Build pair counts
    edge_counts = {}

    for skills in elite_df["required_skills"]:
        filtered_skills = sorted(set(skill for skill in skills if skill in top_skills.index))
        for skill1, skill2 in combinations(filtered_skills, 2):
            edge = (skill1, skill2)
            edge_counts[edge] = edge_counts.get(edge, 0) + 1

    # Build graph
    G = nx.Graph()

    for skill, count in top_skills.items():
        G.add_node(skill, size=count)

    for (skill1, skill2), weight in edge_counts.items():
        if weight >= min_edge_weight:
            G.add_edge(skill1, skill2, weight=weight)

    # Remove isolated nodes
    G.remove_nodes_from(list(nx.isolates(G)))

    if len(G.nodes) == 0:
        print("No network to display. Try lowering min_edge_weight.")
        return

    # Detect communities / clusters
    communities = list(nx.algorithms.community.greedy_modularity_communities(G))

    # Assign each node a cluster id
    node_to_cluster = {}
    for cluster_id, community in enumerate(communities):
        for node in community:
            node_to_cluster[node] = cluster_id

    # Color palette
    cmap = plt.colormaps["tab10"]
    node_colors = [cmap(node_to_cluster[node] % 10) for node in G.nodes]

    # Layout
    pos = nx.spring_layout(G, seed=42, k=0.9)

    # Sizes
    node_sizes = [G.nodes[node]["size"] * 120 for node in G.nodes]
    edge_widths = [G[u][v]["weight"] * 0.5 for u, v in G.edges]

    # Draw
    plt.figure(figsize=(16, 12))
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.9,
        edgecolors="black",
        linewidths=0.8
    )
    nx.draw_networkx_edges(
        G,
        pos,
        width=edge_widths,
        alpha=0.35
    )
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=10
    )

    plt.title("Skill Co-Occurrence Network in $300k+ AI Jobs", fontsize=16)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    # Legend-like text summary
    print("\nCluster Summary:")
    for cluster_id, community in enumerate(communities, start=1):
        sorted_skills = sorted(
            list(community),
            key=lambda skill: G.nodes[skill]["size"],
            reverse=True
        )
        top_cluster_skills = sorted_skills[:8]
        print(f"Cluster {cluster_id}: {', '.join(top_cluster_skills)}")