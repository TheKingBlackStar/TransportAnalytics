import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# Page config
st.set_page_config(
    page_title="Transport Analytics",
    page_icon="🚗",
    layout="wide"
)

# Initialize session state
if 'dataframes' not in st.session_state:
    st.session_state.dataframes = {}

# Sidebar
st.sidebar.title("📊 Analysis Options")

# File upload section
uploaded_files = st.sidebar.file_uploader("Upload CSV files", type=['csv'], accept_multiple_files=True)

if uploaded_files:
    # Process uploaded files
    for uploaded_file in uploaded_files:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.dataframes[uploaded_file.name] = df
        except Exception as e:
            st.error(f"Error loading {uploaded_file.name}: {str(e)}")

    # Data selection
    if st.session_state.dataframes:
        selected_file = st.sidebar.selectbox(
            "Select file to analyze",
            options=list(st.session_state.dataframes.keys())
        )
        
        if selected_file:
            df = st.session_state.dataframes[selected_file]
            
            # Show basic info
            st.sidebar.info(f"Total Records: {len(df)}")
            
            # Create tabs
            tab1, tab2, tab3 = st.tabs(["📈 Charts", "📊 Statistics", "📋 Data"])
            
            with tab1:
                st.subheader("Data Visualization")
                
                # Get numeric columns
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                if len(numeric_cols) > 0:
                    # Select columns for visualization
                    y_axis = st.selectbox("Select column to visualize", numeric_cols)
                    
                    # Create simple line chart
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(y=df[y_axis], name=y_axis)
                    )
                    fig.update_layout(
                        title=f"{y_axis} Trend",
                        height=400,
                        showlegend=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Create histogram
                    fig2 = go.Figure()
                    fig2.add_trace(
                        go.Histogram(x=df[y_axis], name=y_axis)
                    )
                    fig2.update_layout(
                        title=f"Distribution of {y_axis}",
                        height=400
                    )
                    st.plotly_chart(fig2, use_container_width=True)
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
                
                # Simple search
                search = st.text_input("Search in data")
                if search:
                    filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                else:
                    filtered_df = df
                
                # Show data with simple pagination
                rows_per_page = st.selectbox("Rows per page", [10, 20, 50, 100])
                page = st.number_input("Page", min_value=1, value=1)
                start_idx = (page - 1) * rows_per_page
                end_idx = min(start_idx + rows_per_page, len(filtered_df))
                
                st.write(filtered_df.iloc[start_idx:end_idx])
                st.info(f"Showing {start_idx+1} to {end_idx} of {len(filtered_df)} records")
                
                # Add download button
                if st.button("Download Data as CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        csv,
                        f"{selected_file}_processed.csv",
                        "text/csv"
                    )
else:
    st.info("👆 Please upload CSV files to begin analysis.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
### Tips
- Upload one or more CSV files
- Select a file to analyze
- View charts and statistics
- Search and download data
""")
