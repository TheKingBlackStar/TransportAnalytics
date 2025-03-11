import streamlit as st
import pandas as pd

# Simple title
st.title("Transport Data Viewer")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Load and display the data
        df = pd.read_csv(uploaded_file)
        
        # Show basic info
        st.write(f"Total Records: {len(df)}")
        
        # Show column names
        st.write("### Columns in your data:")
        st.write(", ".join(df.columns.tolist()))
        
        # Show first few rows
        st.write("### Preview of your data:")
        st.write(df.head())
        
        # Basic statistics
        st.write("### Summary Statistics:")
        st.write(df.describe())
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.write("Please upload a CSV file to begin.")
