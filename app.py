import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

st.set_page_config(page_title="Student Academic Performance Trend Analyzer", layout="centered")

st.title("📊 Student Academic Performance Trend Analyzer")
st.write("Upload an Excel file with columns **Semester** and **Marks**")

# File uploader
uploaded_file = st.file_uploader(
    "Upload Excel file (.xlsx or .xls)",
    type=["xlsx", "xls"],
    accept_multiple_files=False
)

if uploaded_file is not None:
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file)

        st.subheader("Dataset Preview")
        st.dataframe(df)

        # Validate required columns
        required_cols = {"Semester", "Marks"}
        if not required_cols.issubset(df.columns):
            st.error("❌ The uploaded file must contain columns: 'Semester' and 'Marks'")
        else:
            # Sort by Semester (important for trend analysis)
            df = df.sort_values(by="Semester")

            semesters = df["Semester"].values
            marks = df["Marks"].values

            # Linear regression for trend
            slope, intercept, r_value, p_value, std_err = linregress(semesters, marks)
            trend_line = intercept + slope * semesters

            # Trend interpretation
            if slope > 0:
                trend_text = "📈 Increasing Performance"
            elif slope < 0:
                trend_text = "📉 Decreasing Performance"
            else:
                trend_text = "➖ Stable Performance"

            st.subheader("Performance Trend Result")
            st.success(trend_text)

            st.write(f"**Slope:** {slope:.3f}")
            st.write(f"**R-squared:** {r_value**2:.3f}")

            # Plot
            st.subheader("Marks Trend Visualization")
            fig, ax = plt.subplots()
            ax.plot(semesters, marks, marker='o', label='Actual Marks')
            ax.plot(semesters, trend_line, linestyle='--', label='Trend Line')
            ax.set_xlabel("Semester")
            ax.set_ylabel("Marks")
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
else:
    st.info("Please upload an Excel file to analyze student performance.")
