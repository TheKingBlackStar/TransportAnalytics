import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Transport Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom styling
st.markdown("""
    <style>
        .main > div {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Analysis Options")

# Main content
st.title('Transport Analytics Dashboard')

# File upload
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)
        
        # Show data info
        st.sidebar.subheader("Data Overview")
        st.sidebar.info(f"Total Records: {len(df)}")
        
        # Column selection
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_columns) > 0:
            selected_columns = st.sidebar.multiselect(
                "Select columns for analysis",
                numeric_columns,
                default=numeric_columns[0] if len(numeric_columns) > 0 else None
            )
            
            if selected_columns:
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📈 Visualizations", "📊 Statistics", "📋 Raw Data"])
                
                with tab1:
                    st.subheader("Data Visualization")
                    
                    # Chart type selection
                    chart_type = st.selectbox(
                        "Select chart type",
                        ["Line Chart", "Bar Chart", "Scatter Plot", "Box Plot", "Histogram"]
                    )
                    
                    # Layout columns for chart controls
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        x_axis = st.selectbox("Select X-axis", df.columns)
                    with col2:
                        y_axis = st.selectbox("Select Y-axis", selected_columns)
                    
                    # Create visualization based on selection
                    try:
                        if chart_type == "Line Chart":
                            fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                        elif chart_type == "Bar Chart":
                            fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                        elif chart_type == "Scatter Plot":
                            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                        elif chart_type == "Box Plot":
                            fig = px.box(df, x=x_axis, y=y_axis, title=f"Distribution of {y_axis} by {x_axis}")
                        else:  # Histogram
                            fig = px.histogram(df, x=y_axis, title=f"Distribution of {y_axis}")
                        
                        # Update layout for better visibility
                        fig.update_layout(
                            height=500,
                            width=None,
                            margin=dict(l=20, r=20, t=40, b=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            hovermode='x unified'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"Error creating visualization: {str(e)}")
                
                with tab2:
                    st.subheader("Statistical Analysis")
                    
                    # Basic statistics
                    st.write("### Summary Statistics")
                    st.write(df[selected_columns].describe())
                    
                    # Correlation matrix if multiple columns selected
                    if len(selected_columns) > 1:
                        st.write("### Correlation Matrix")
                        corr = df[selected_columns].corr()
                        fig = px.imshow(
                            corr,
                            title="Correlation Matrix",
                            color_continuous_scale="RdBu"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                with tab3:
                    st.subheader("Raw Data")
                    
                    # Add search functionality
                    search = st.text_input("Search in data")
                    if search:
                        filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
                    else:
                        filtered_df = df
                    
                    # Show the data with pagination
                    page_size = st.selectbox("Rows per page", [10, 20, 50, 100])
                    page_number = st.number_input("Page", min_value=1, value=1)
                    start_idx = (page_number - 1) * page_size
                    end_idx = start_idx + page_size
                    
                    st.write(filtered_df.iloc[start_idx:end_idx])
                    st.info(f"Showing {start_idx+1} to {min(end_idx, len(filtered_df))} of {len(filtered_df)} records")
        
        else:
            st.warning("No numeric columns found in the data. Please upload a file with numeric data for analysis.")
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("👆 Please upload a CSV file to begin analysis.")
    
# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### Tips")
st.sidebar.markdown("""
- Upload a CSV file to start
- Select columns for analysis
- Choose different visualizations
- Use tabs to switch views
- Search and filter data as needed
""")
