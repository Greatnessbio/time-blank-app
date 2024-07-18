import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("Interactive CSV Dashboard")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Display raw data
        st.subheader("Raw Data")
        st.write(df)

        # Select columns for visualization
        st.subheader("Select Columns for Visualization")
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

        x_axis = st.selectbox("Select X-axis", options=df.columns)
        y_axis = st.selectbox("Select Y-axis", options=numeric_columns)
        color_column = st.selectbox("Select Color Column (optional)", options=['None'] + categorical_columns)

        # Create layers of visualizations
        st.subheader("Data Visualization")

        # Scatter plot
        fig_scatter = px.scatter(df, x=x_axis, y=y_axis, color=color_column if color_column != 'None' else None,
                                 title=f"Scatter Plot: {x_axis} vs {y_axis}")
        st.plotly_chart(fig_scatter)

        # Bar chart
        if x_axis in categorical_columns:
            fig_bar = px.bar(df, x=x_axis, y=y_axis, color=color_column if color_column != 'None' else None,
                             title=f"Bar Chart: {x_axis} vs {y_axis}")
            st.plotly_chart(fig_bar)

        # Line chart
        if x_axis in numeric_columns:
            fig_line = px.line(df, x=x_axis, y=y_axis, color=color_column if color_column != 'None' else None,
                               title=f"Line Chart: {x_axis} vs {y_axis}")
            st.plotly_chart(fig_line)

        # Data filtering
        st.subheader("Data Filtering")
        filter_column = st.selectbox("Select column to filter", options=df.columns)
        unique_values = df[filter_column].unique().tolist()
        selected_values = st.multiselect(f"Select values for {filter_column}", options=unique_values, default=unique_values)

        filtered_df = df[df[filter_column].isin(selected_values)]

        st.subheader("Filtered Data")
        st.write(filtered_df)

        # Summary statistics
        st.subheader("Summary Statistics")
        st.write(filtered_df.describe())

if __name__ == "__main__":
    main()
