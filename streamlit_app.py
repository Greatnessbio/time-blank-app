import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def main():
    st.title("Custom Project Timeline")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Display raw data
        st.subheader("Raw Data")
        st.write(df)

        # Check if required columns exist
        required_columns = ['Name', 'Start Date', 'Due Date']
        if not all(col in df.columns for col in required_columns):
            st.error("The CSV file must contain 'Name', 'Start Date', and 'Due Date' columns.")
            return

        # Convert date columns to datetime
        date_columns = ['Start Date', 'Due Date', 'Created At', 'Completed At', 'Last Modified']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Create Gantt chart
        st.subheader("Project Timeline (Gantt Chart)")

        fig = px.timeline(df, x_start="Start Date", x_end="Due Date", y="Name", color="Assignee",
                          hover_data=["Task ID", "Projects", "Estimated Hours", "Deliverable Status"],
                          title="Project Timeline")
        fig.update_yaxes(autorange="reversed")  # Reverse the order of tasks
        
        # Add range slider
        fig.update_xaxes(rangeslider_visible=True)

        # Add buttons for time range selection
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    x=0.7,
                    y=1.2,
                    showactive=True,
                    buttons=list([
                        dict(label="All",
                             method="relayout",
                             args=[{"xaxis.range": [df['Start Date'].min(), df['Due Date'].max()]}]),
                        dict(label="Next Month",
                             method="relayout",
                             args=[{"xaxis.range": [datetime.now(), datetime.now() + timedelta(days=30)]}]),
                        dict(label="Next Week",
                             method="relayout",
                             args=[{"xaxis.range": [datetime.now(), datetime.now() + timedelta(days=7)]}]),
                    ]),
                )
            ]
        )

        st.plotly_chart(fig)

        # Task filtering
        st.subheader("Task Filtering")
        
        # Filter by Assignee
        assignees = df['Assignee'].dropna().unique().tolist()
        selected_assignees = st.multiselect("Filter by Assignee", options=assignees, default=assignees)
        
        # Filter by Project
        projects = df['Projects'].dropna().unique().tolist()
        selected_projects = st.multiselect("Filter by Project", options=projects, default=projects)
        
        # Filter by Deliverable Status
        statuses = df['Deliverable Status'].dropna().unique().tolist()
        selected_statuses = st.multiselect("Filter by Deliverable Status", options=statuses, default=statuses)

        # Apply filters
        filtered_df = df[
            (df['Assignee'].isin(selected_assignees)) &
            (df['Projects'].isin(selected_projects)) &
            (df['Deliverable Status'].isin(selected_statuses))
        ]

        # Create filtered Gantt chart
        st.subheader("Filtered Project Timeline")

        fig_filtered = px.timeline(filtered_df, x_start="Start Date", x_end="Due Date", y="Name", color="Assignee",
                                   hover_data=["Task ID", "Projects", "Estimated Hours", "Deliverable Status"],
                                   title="Filtered Project Timeline")
        fig_filtered.update_yaxes(autorange="reversed")
        fig_filtered.update_xaxes(rangeslider_visible=True)

        st.plotly_chart(fig_filtered)

        # Summary statistics
        st.subheader("Project Summary")
        st.write(f"Total number of tasks: {len(filtered_df)}")
        st.write(f"Project start date: {filtered_df['Start Date'].min().date()}")
        st.write(f"Project end date: {filtered_df['Due Date'].max().date()}")
        st.write(f"Number of assignees: {filtered_df['Assignee'].nunique()}")
        st.write(f"Total estimated hours: {filtered_df['Estimated Hours'].sum():.2f}")
        
        # Overdue tasks
        overdue_tasks = filtered_df[filtered_df['Overdue'] == True]
        st.write(f"Number of overdue tasks: {len(overdue_tasks)}")

        # Task completion status
        completed_tasks = filtered_df[filtered_df['Completed At'].notna()]
        st.write(f"Completed tasks: {len(completed_tasks)} ({len(completed_tasks)/len(filtered_df)*100:.2f}%)")

if __name__ == "__main__":
    main()
