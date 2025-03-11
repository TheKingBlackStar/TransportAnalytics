import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Basic page config
st.set_page_config(page_title="Transport Analytics")

# Title
st.title("Transport Analytics Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Read data
        df = pd.read_csv(uploaded_file)
        
        # Show basic info
        st.sidebar.info(f"Total Records: {len(df)}")
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["📈 Charts", "📊 Statistics", "📋 Data"])
        
        with tab1:
            st.subheader("Data Visualization")
            
            # Get numeric columns
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_cols) > 0:
                # Select column to visualize
                column = st.selectbox("Select column to visualize", numeric_cols)
                
                # Create line plot
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(df[column])
                ax.set_title(f"{column} Trend")
                ax.grid(True)
                st.pyplot(fig)
                plt.close()
                
                # Create histogram
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.hist(df[column], bins=30)
                ax.set_title(f"Distribution of {column}")
                ax.grid(True)
                st.pyplot(fig)
                plt.close()
            else:
                st.warning("No numeric columns found for visualization")
        
        with tab2:
            st.subheader("Statistical Analysis")
            if len(numeric_cols) > 0:
                st.write("### Summary Statistics")
                st.write(df[numeric_cols].describe())
            else:
                st.warning("No numeric columns found for analysis")
        
        with tab3:
            st.subheader("Raw Data")
            
            # Search functionality
            search = st.text_input("Search in data")
            if search:
                filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            else:
                filtered_df = df
            
            # Pagination
            rows_per_page = st.selectbox("Rows per page", [10, 20, 50, 100])
            page = st.number_input("Page", min_value=1, value=1)
            start_idx = (page - 1) * rows_per_page
            end_idx = min(start_idx + rows_per_page, len(filtered_df))
            
            # Display data
            st.write(filtered_df.iloc[start_idx:end_idx])
            st.info(f"Showing {start_idx+1} to {end_idx} of {len(filtered_df)} records")
            
            # Download option
            if st.button("Download Data as CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "data_processed.csv",
                    "text/csv"
                )
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.info("👆 Please upload a CSV file to begin analysis.")

# Tips in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
### Tips
- Upload a CSV file
- Select columns to analyze
- View charts and statistics
- Search and download data
""")
