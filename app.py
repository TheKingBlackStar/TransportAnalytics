import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import json

# Page config
st.set_page_config(
    page_title="Transport Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for storing multiple dataframes
if 'dataframes' not in st.session_state:
    st.session_state.dataframes = {}
if 'combined_df' not in st.session_state:
    st.session_state.combined_df = None

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

# File upload section
st.sidebar.header("File Upload")
uploaded_files = st.sidebar.file_uploader("Upload CSV files", type=['csv'], accept_multiple_files=True)

# Process uploaded files
if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            # Store each dataframe with its filename as key
            df = pd.read_csv(uploaded_file)
            st.session_state.dataframes[uploaded_file.name] = df
        except Exception as e:
            st.error(f"Error loading {uploaded_file.name}: {str(e)}")

# Data selection and combination
if st.session_state.dataframes:
    st.sidebar.subheader("Data Management")
    
    # Select which files to analyze
    selected_files = st.sidebar.multiselect(
        "Select files to analyze",
        options=list(st.session_state.dataframes.keys()),
        default=list(st.session_state.dataframes.keys())[0]
    )
    
    # Combine selected dataframes
    if selected_files:
        try:
            if len(selected_files) == 1:
                df = st.session_state.dataframes[selected_files[0]]
            else:
                # Option to choose how to combine the data
                combine_method = st.sidebar.radio(
                    "How to combine multiple files?",
                    ["Concatenate (Stack)", "Merge on Column"]
                )
                
                if combine_method == "Concatenate (Stack)":
                    df = pd.concat([st.session_state.dataframes[f] for f in selected_files], 
                                 ignore_index=True)
                else:
                    merge_on = st.sidebar.selectbox(
                        "Select column to merge on",
                        options=[col for col in st.session_state.dataframes[selected_files[0]].columns 
                               if all(col in st.session_state.dataframes[f].columns 
                                    for f in selected_files)]
                    )
                    df = st.session_state.dataframes[selected_files[0]]
                    for f in selected_files[1:]:
                        df = df.merge(st.session_state.dataframes[f], on=merge_on, how='outer')
            
            # Store combined dataframe in session state
            st.session_state.combined_df = df
            
            # Show data info
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
                    tab1, tab2, tab3, tab4 = st.tabs(["📈 Visualizations", "📊 Statistics", "📋 Raw Data", "💾 Export"])
                    
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
                        
                        # Optional grouping
                        if chart_type in ["Line Chart", "Bar Chart", "Box Plot"]:
                            group_by = st.selectbox("Group by (optional)", 
                                                  ["None"] + list(df.select_dtypes(include=['object']).columns))
                        
                        # Create visualization based on selection
                        try:
                            if chart_type == "Line Chart":
                                if group_by != "None":
                                    fig = px.line(df, x=x_axis, y=y_axis, color=group_by, 
                                                title=f"{y_axis} over {x_axis} by {group_by}")
                                else:
                                    fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                            elif chart_type == "Bar Chart":
                                if group_by != "None":
                                    fig = px.bar(df, x=x_axis, y=y_axis, color=group_by,
                                               title=f"{y_axis} by {x_axis} and {group_by}")
                                else:
                                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                            elif chart_type == "Scatter Plot":
                                fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                            elif chart_type == "Box Plot":
                                if group_by != "None":
                                    fig = px.box(df, x=x_axis, y=y_axis, color=group_by,
                                               title=f"Distribution of {y_axis} by {x_axis} and {group_by}")
                                else:
                                    fig = px.box(df, x=x_axis, y=y_axis, 
                                               title=f"Distribution of {y_axis} by {x_axis}")
                            else:  # Histogram
                                fig = px.histogram(df, x=y_axis, title=f"Distribution of {y_axis}")
                            
                            # Update layout for better visibility
                            fig.update_layout(
                                height=500,
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
                        
                        # File selection for viewing
                        if len(selected_files) > 1:
                            view_option = st.radio(
                                "View data from:",
                                ["Combined Data"] + selected_files
                            )
                            if view_option != "Combined Data":
                                current_df = st.session_state.dataframes[view_option]
                            else:
                                current_df = df
                        else:
                            current_df = df
                        
                        # Add search functionality
                        search = st.text_input("Search in data")
                        if search:
                            filtered_df = current_df[current_df.astype(str).apply(
                                lambda x: x.str.contains(search, case=False)).any(axis=1)]
                        else:
                            filtered_df = current_df
                        
                        # Show the data with pagination
                        page_size = st.selectbox("Rows per page", [10, 20, 50, 100])
                        page_number = st.number_input("Page", min_value=1, value=1)
                        start_idx = (page_number - 1) * page_size
                        end_idx = start_idx + page_size
                        
                        st.write(filtered_df.iloc[start_idx:end_idx])
                        st.info(f"Showing {start_idx+1} to {min(end_idx, len(filtered_df))} "
                               f"of {len(filtered_df)} records")
                    
                    with tab4:
                        st.subheader("Export Data")
                        
                        # Export options
                        export_format = st.selectbox(
                            "Select export format",
                            ["CSV", "Excel", "JSON"]
                        )
                        
                        if st.button("Generate Export"):
                            if export_format == "CSV":
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    "Download CSV",
                                    csv,
                                    "combined_data.csv",
                                    "text/csv"
                                )
                            elif export_format == "Excel":
                                output = StringIO()
                                df.to_excel(output, index=False)
                                excel_data = output.getvalue()
                                st.download_button(
                                    "Download Excel",
                                    excel_data,
                                    "combined_data.xlsx",
                                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                            else:  # JSON
                                json_str = df.to_json(orient='records')
                                st.download_button(
                                    "Download JSON",
                                    json_str,
                                    "combined_data.json",
                                    "application/json"
                                )
            
            else:
                st.warning("No numeric columns found in the data. Please upload files with numeric data for analysis.")
                
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
else:
    st.info("👆 Please upload CSV files to begin analysis.")
    
# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### Tips")
st.sidebar.markdown("""
- Upload multiple CSV files
- Select files to analyze
- Choose how to combine data
- Use tabs to switch views
- Export combined data
""")
