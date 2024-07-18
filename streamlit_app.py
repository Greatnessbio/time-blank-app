import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
from datetime import datetime, timedelta

def main():
    st.title("Interactive Project Timeline")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Display raw data
        st.subheader("Raw Data")
        st.write(df)

        # Check if required columns exist
        required_columns = ['Task', 'Start', 'Finish']
        if not all(col in df.columns for col in required_columns):
            st.error("The CSV file must contain 'Task', 'Start', and 'Finish' columns.")
            return

        # Convert 'Start' and 'Finish' columns to datetime
        df['Start'] = pd.to_datetime(df['Start'])
        df['Finish'] = pd.to_datetime(df['Finish'])

        # Optional: Resource column
        resource_column = None
        if 'Resource' in df.columns:
            resource_column = 'Resource'

        # Create Gantt chart
        st.subheader("Project Timeline (Gantt Chart)")

        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color=resource_column,
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
                             args=[{"xaxis.range": [df['Start'].min(), df['Finish'].max()]}]),
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
        if resource_column:
            resources = df[resource_column].unique().tolist()
            selected_resources = st.multiselect("Filter by Resource", options=resources, default=resources)
            filtered_df = df[df[resource_column].isin(selected_resources)]
        else:
            filtered_df = df

        # Create filtered Gantt chart
        st.subheader("Filtered Project Timeline")

        fig_filtered = px.timeline(filtered_df, x_start="Start", x_end="Finish", y="Task", color=resource_column,
                                   title="Filtered Project Timeline")
        fig_filtered.update_yaxes(autorange="reversed")
        fig_filtered.update_xaxes(rangeslider_visible=True)

        st.plotly_chart(fig_filtered)

        # Summary statistics
        st.subheader("Project Summary")
        st.write(f"Total number of tasks: {len(filtered_df)}")
        st.write(f"Project start date: {filtered_df['Start'].min().date()}")
        st.write(f"Project end date: {filtered_df['Finish'].max().date()}")
        if resource_column:
            st.write(f"Number of resources: {filtered_df[resource_column].nunique()}")

if __name__ == "__main__":
    main()
