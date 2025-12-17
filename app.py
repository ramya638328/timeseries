import streamlit as st
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt

st.title("Student Academic Performance Trend Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload Excel file with columns 'Semester' and 'Marks'", type=["xlsx", "xls"])

if uploaded_file:
    # Load dataset
    df = pd.read_excel(uploaded_file)
    
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Check columns
    if 'Semester' in df.columns and 'Marks' in df.columns:
        semesters = df['Semester'].values
        marks = df['Marks'].values

        # Compute linear regression
        slope, intercept, r_value, p_value, std_err = linregress(semesters, marks)

        # Determine trend
        if slope > 0:
            trend = "Increasing"
        elif slope < 0:
            trend = "Decreasing"
        else:
            trend = "Stable"

        st.subheader("Trend Analysis")
        st.write(f"Trend of student academic performance: **{trend}**")
        st.write(f"Slope: **{slope:.2f}** (positive means improving, negative means declining)")

        # Visualization
        st.subheader("Performance Trend Plot")
        fig, ax = plt.subplots()
        ax.plot(semesters, marks, 'o', label='Actual Marks')
        ax.plot(semesters, intercept + slope*semesters, 'r', label='Trend Line')
        ax.set_xlabel("Semester")
        ax.set_ylabel("Marks")
        ax.set_title("Student Academic Performance Trend")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("The uploaded file must contain columns: 'Semester' and 'Marks'.")
