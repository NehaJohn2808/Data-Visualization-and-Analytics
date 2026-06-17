import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Data Analytics Dashboard", layout="wide")

st.title("📊 Data Analytics & Visualization Dashboard")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("Dataset Loaded Successfully!")

    # Dataset Preview
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Dataset Information
    st.subheader("Dataset Information")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # Data Types
    st.subheader("Column Data Types")
    st.write(df.dtypes)

    # Missing Values
    st.subheader("Missing Values Analysis")
    missing = df.isnull().sum()

    st.dataframe(
        pd.DataFrame({
            "Column": missing.index,
            "Missing Values": missing.values
        })
    )

    # Summary Statistics
    st.subheader("Statistical Summary")
    st.dataframe(df.describe())

    # Visualization Section
    st.subheader("Data Visualization")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Histogram", "Scatter Plot", "Line Chart",
         "Bar Chart", "Pie Chart"]
    )

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if chart_type == "Histogram":
        column = st.selectbox("Select Numeric Column", numeric_cols)

        fig = px.histogram(
            df,
            x=column,
            title=f"Histogram of {column}"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter Plot":

        x = st.selectbox("X-axis", numeric_cols)
        y = st.selectbox("Y-axis", numeric_cols)

        fig = px.scatter(
            df,
            x=x,
            y=y,
            title=f"{x} vs {y}"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Line Chart":

        x = st.selectbox("X-axis", df.columns)
        y = st.selectbox("Y-axis", numeric_cols)

        fig = px.line(
            df,
            x=x,
            y=y,
            title=f"{y} Trend"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar Chart":

        x = st.selectbox("Category Column", df.columns)
        y = st.selectbox("Value Column", numeric_cols)

        fig = px.bar(
            df,
            x=x,
            y=y,
            title=f"{y} by {x}"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pie Chart":

        names = st.selectbox("Category", df.columns)
        values = st.selectbox("Values", numeric_cols)

        fig = px.pie(
            df,
            names=names,
            values=values,
            title=f"{values} Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")

    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            ax=ax
        )

        st.pyplot(fig)

    # Data Filtering
    st.subheader("Filter Dataset")

    selected_column = st.selectbox(
        "Select Column for Filtering",
        df.columns
    )

    unique_values = df[selected_column].dropna().unique()

    selected_values = st.multiselect(
        "Choose Values",
        unique_values
    )

    if selected_values:
        filtered_df = df[
            df[selected_column].isin(selected_values)
        ]

        st.dataframe(filtered_df)

    # Download Data
    st.subheader("Download Dataset")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download CSV",
        csv,
        "processed_data.csv",
        "text/csv"
    )

else:
    st.info("Please upload a CSV file to begin analysis.")