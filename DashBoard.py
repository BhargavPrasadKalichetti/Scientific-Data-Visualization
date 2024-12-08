import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Job Market Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('AIDataset.csv')
    return df

def main():
    # Title and introduction
    st.title("🎯 AI and Tech Job Market Analysis (2010-2024)")
    st.markdown("---")

    # Load data
    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Year range
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=int(df['Year'].min()),
        max_value=int(df['Year'].max()),
        value=(int(df['Year'].min()), int(df['Year'].max()))
    )
    
    # Job categories
    job_cats = st.sidebar.multiselect(
        "Select Job Categories",
        options=df['Job_Title'].unique(),
        default=df['Job_Title'].unique()
    )
    
    # Industries
    industries = st.sidebar.multiselect(
        "Select Industries",
        options=df['Industry'].unique(),
        default=df['Industry'].unique()
    )

    # Filter data
    mask = (
        (df['Year'].between(year_range[0], year_range[1])) &
        (df['Job_Title'].isin(job_cats)) &
        (df['Industry'].isin(industries))
    )
    filtered_df = df[mask]

    # Top KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_salary = filtered_df['Salary_USD'].mean()
        st.metric("Average Salary", f"${avg_salary:,.0f}")
    
    with col2:
        avg_growth = filtered_df['Growth_Rate'].mean()
        st.metric("Average Growth Rate", f"{avg_growth:.1f}%")
    
    with col3:
        total_openings = filtered_df['Job_Openings'].sum()
        st.metric("Total Job Openings", f"{total_openings:,}")
    
    with col4:
        avg_diversity = filtered_df['Gender_Diversity_Index'].mean()
        st.metric("Avg Gender Diversity", f"{avg_diversity:.2f}")

    # Salary Analysis Section
    st.header("💰 Salary Analysis")
    col1, col2 = st.columns(2)

    with col1:
        # Salary trends over time by job title
        salary_trends = filtered_df.groupby(['Year', 'Job_Title'])['Salary_USD'].mean().reset_index()
        fig = px.line(salary_trends, x='Year', y='Salary_USD', color='Job_Title',
                     title='Salary Trends by Job Title')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Salary by experience level
        salary_exp = filtered_df.groupby(['Experience_Level', 'Job_Title'])['Salary_USD'].mean().reset_index()
        fig = px.bar(salary_exp, x='Experience_Level', y='Salary_USD', color='Job_Title',
                    title='Average Salary by Experience Level')
        st.plotly_chart(fig, use_container_width=True)

    # AI Adoption Analysis
    st.header("🤖 AI Adoption & Skills Analysis")
    col1, col2 = st.columns(2)

    with col1:
        # AI Adoption Level distribution
        ai_adoption = filtered_df.groupby(['Industry', 'AI_Adoption_Level']).size().reset_index(name='count')
        fig = px.bar(ai_adoption, x='Industry', y='count', color='AI_Adoption_Level',
                    title='AI Adoption Levels by Industry')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Skills complexity distribution
        skill_complex = filtered_df.groupby(['Job_Title', 'Skill_Complexity']).size().reset_index(name='count')
        fig = px.bar(skill_complex, x='Job_Title', y='count', color='Skill_Complexity',
                    title='Skill Complexity by Job Title')
        st.plotly_chart(fig, use_container_width=True)

    # Job Market Analysis
    st.header("📊 Job Market Insights")
    col1, col2 = st.columns(2)

    with col1:
        # Job openings by location
        location_jobs = filtered_df.groupby(['Location', 'Job_Title'])['Job_Openings'].sum().reset_index()
        fig = px.bar(location_jobs, x='Location', y='Job_Openings', color='Job_Title',
                    title='Job Openings by Location')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Remote work distribution
        remote_dist = filtered_df.groupby(['Job_Title', 'Remote_Work']).size().reset_index(name='count')
        fig = px.bar(remote_dist, x='Job_Title', y='count', color='Remote_Work',
                    title='Remote Work Distribution by Job Title')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    # Growth and Company Analysis
    st.header("📈 Growth & Company Analysis")
    col1, col2 = st.columns(2)

    with col1:
        # Growth rate by industry
        growth_industry = filtered_df.groupby(['Industry'])['Growth_Rate'].mean().reset_index()
        fig = px.bar(growth_industry, x='Industry', y='Growth_Rate',
                    title='Average Growth Rate by Industry')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Company size distribution
        company_dist = filtered_df.groupby(['Company_Size', 'Job_Title']).size().reset_index(name='count')
        fig = px.bar(company_dist, x='Company_Size', y='count', color='Job_Title',
                    title='Job Distribution by Company Size')
        st.plotly_chart(fig, use_container_width=True)

    # Detailed Data View
    st.header("🔍 Detailed Data View")
    if st.checkbox("Show Raw Data"):
        st.write(filtered_df)

if __name__ == "__main__":
    main()