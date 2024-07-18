import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.title("Interactive CSV Timeline Dashboard")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Display raw data
        st.subheader("Raw Data")
        st.write(df)

        # Identify date columns
        date_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
        if not date_columns:
            # If no datetime columns found, try to convert object columns to datetime
            for col in df.select_dtypes(include=['object']):
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_columns.append(col)
                except:
                    pass

        if not date_columns:
            st.error("No date columns found in the CSV. Please ensure your CSV contains at least one column with dates.")
            return

        # Select date column for timeline
        date_column = st.selectbox("Select Date Column", options=date_columns)

        # Select value column for timeline
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        value_column = st.selectbox("Select Value Column", options=numeric_columns)

        # Select category column for color (optional)
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        color_column = st.selectbox("Select Category Column for Color (optional)", options=['None'] + categorical_columns)

        # Create interactive timeline
        st.subheader("Interactive Timeline")

        fig = px.line(df, x=date_column, y=value_column, color=color_column if color_column != 'None' else None,
                      title=f"Timeline: {value_column} over {date_column}")
        
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
                             args=[{"xaxis.range": [df[date_column].min(), df[date_column].max()]}]),
                        dict(label="Last Month",
                             method="relayout",
                             args=[{"xaxis.range": [df[date_column].max() - pd.Timedelta(days=30), df[date_column].max()]}]),
                        dict(label="Last Week",
                             method="relayout",
                             args=[{"xaxis.range": [df[date_column].max() - pd.Timedelta(days=7), df[date_column].max()]}]),
                    ]),
                )
            ]
        )

        st.plotly_chart(fig)

        # Data filtering
        st.subheader("Data Filtering")
        filter_column = st.selectbox("Select column to filter", options=df.columns)
        unique_values = df[filter_column].unique().tolist()
        selected_values = st.multiselect(f"Select values for {filter_column}", options=unique_values, default=unique_values)

        filtered_df = df[df[filter_column].isin(selected_values)]

        # Create filtered timeline
        st.subheader("Filtered Timeline")

        fig_filtered = px.line(filtered_df, x=date_column, y=value_column, color=color_column if color_column != 'None' else None,
                               title=f"Filtered Timeline: {value_column} over {date_column}")
        
        fig_filtered.update_xaxes(rangeslider_visible=True)

        st.plotly_chart(fig_filtered)

        # Summary statistics
        st.subheader("Summary Statistics")
        st.write(filtered_df.describe())

if __name__ == "__main__":
    main()
