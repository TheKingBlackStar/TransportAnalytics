import streamlit as st
import pandas as pd

# Basic page config
st.set_page_config(
    page_title="Data Analysis",
    layout="centered"
)

# Simple title
st.write("# Transportation Data Analysis")

# Basic file upload
uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

# Process file if uploaded
if uploaded_file is not None:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)
        
        # Show basic info
        st.write("### Data Preview")
        st.write(df.head())
        
        st.write("### Basic Statistics")
        st.write(df.describe())
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.title('Transport Analytics')
st.write('Hello! This is a test page.')
st.write('If you can see this, the app is working correctly.')
