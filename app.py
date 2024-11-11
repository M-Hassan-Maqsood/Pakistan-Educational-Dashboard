import streamlit as st
import pandas as pd
import plotly.express as px



# Load the dataset
file_path = r'E:\Projects\Project 4\Pakistan-educational-dataset.xlsx'
data = pd.read_excel(file_path)

# # Centered Title
# st.markdown("<h1 style='text-align: center;'>AI Bootcamp Edition 2024</h1>", unsafe_allow_html=True)


# Add custom CSS for page styling using the education-inspired palette
st.markdown("""
<style>
body {
    background-color: #87CEEB;  /* Sky Blue */
    color: #333333;  /* Dark gray text */
}

h1, h2, h3 {
    color: #CD5C5C;  /* Brick Red for headers */
}

.sidebar .sidebar-content {
    background-color: #FFD700;  /* Sunshine Yellow for sidebar */
}

.sidebar .sidebar-content .stSelectbox, 
.sidebar .sidebar-content .stMultiselect, 
.sidebar .sidebar-content .stRadio {
    background-color: #E6E6FA;  /* Lavender for sidebar inputs */
    color: #000000;  /* Black text for inputs */
}

.stButton>button {
    background-color: #32CD32;  /* Leaf Green button */
    color: white;  /* White text for button */
}

.stSelectbox, .stMultiselect, .stRadio {
    background-color: #E6E6FA;  /* Lavender background for select inputs */
    color: #000000;  /* Black text for inputs */
}

.stPlotlyChart {
    border: 2px solid #CD5C5C;  /* Brick Red border for plots */
}
</style>
""", unsafe_allow_html=True)



# Dashboard title
st.title('Pakistan Educational Dashboard')


# Sidebar for user selections
st.sidebar.header('User Selections')

# Add selection box for page navigation
page = st.sidebar.selectbox("Select Page", ["School Statistics", "Score Analysis","Enrollment Analysis"])

# Extract unique provinces and years
unique_provinces = data['Province'].unique()
unique_years = data['Year'].unique()

# Province selection
selected_provinces = st.sidebar.multiselect('Select Province(s)', unique_provinces)

# # Year selection
selected_years = st.sidebar.multiselect(
    'Select Year(s)', 
    unique_years.tolist(),  # Convert to list for multiselect
    default=[unique_years[0]]  # Pre-select the first year by default
)

# # Filter cities based on selected provinces
if selected_provinces:
    filtered_data = data[data['Province'].isin(selected_provinces)]
    unique_cities = filtered_data['City'].unique()

    # City selection
    selected_cities = st.sidebar.multiselect('Select City(ies)', unique_cities)

    if selected_cities:
        # Main page code for School Statistics Page
        if page == "School Statistics":
            # Page title
            st.write("## School Statistics")
            
            # Select columns to display (dynamically retrieved from dataset)
            available_columns = [
                'Number of primary schools', 'Number of secondary schools',
                'Primary Schools with single classroom', 'Primary Schools with single teacher', 'No Facility'
            ]
            selected_columns = st.multiselect("Select Metrics:", options=available_columns)
            
            # Choose plot type
            plot_type = st.multiselect("Select Plot Type:", options=["Bar", "Pie", "Line"])
            
            # Filter data for selected cities and years
            city_data = filtered_data[
                (filtered_data['City'].isin(selected_cities)) &
                (filtered_data['Year'].isin(selected_years))
            ]
            
            if not city_data.empty and selected_columns:
                # Prepare data for plotting
                metric_data = []
                for city in selected_cities:
                    for year in selected_years:
                        city_year_data = city_data[(city_data['City'] == city) & (city_data['Year'] == year)]
                        
                        for column in selected_columns:
                            count = city_year_data[column].sum()
                            metric_data.append({
                                'City': city,
                                'Year': year,
                                'Metric': column,
                                'Count': count
                            })
                
                # Create DataFrame for plotting
                metric_data_df = pd.DataFrame(metric_data)
                # Display the metric data table
                st.subheader('School Metrics Data Table')
                st.dataframe(metric_data_df)
                

                # Plot based on selected plot type
                if "Bar" in plot_type:
                    fig = px.bar(
                        metric_data_df,
                        x='City',
                        y='Count',
                        color='Metric',
                        title=f'School Statistics in Selected Cities for {", ".join(map(str, selected_years))}',
                        labels={'Count': 'Number of Schools'},
                        height=400,
                        barmode='group'  # Group bars by city
                    )
                    fig.update_layout(
                        xaxis_title='City',
                        yaxis_title='Number of Schools',
                        title_font=dict(size=20, family='Arial, sans-serif'),
                        xaxis_title_font=dict(size=14),
                        yaxis_title_font=dict(size=14),
                        legend_title=dict(font=dict(size=14)),
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig)
                
                if "Pie" in plot_type:
                    pie_data = metric_data_df[metric_data_df['Metric'].isin(selected_columns)]
                    fig = px.pie(
                        pie_data,
                        values='Count',
                        names='Metric',
                        title='Distribution of Selected School Metrics',
                        height=400
                    )
                    st.plotly_chart(fig)

                if "Line" in plot_type:
                    # Prepare data for line plot based on year and city
                    if len(selected_years) > 1:
                        metric_data_df = metric_data_df.pivot_table(
                            index=['City', 'Year'], columns='Metric', values='Count'
                        ).reset_index().melt(id_vars=['City', 'Year'], var_name='Metric', value_name='Count')
                    else:
                        metric_data_df['Year'] = selected_years[0]

                    fig = px.line(
                        metric_data_df,
                        x='Year' if len(selected_years) > 1 else 'City',
                        y='Count',
                        color='Metric',
                        line_group='City',
                        title=f'School Metrics in Selected Cities for {", ".join(map(str, selected_years))}',
                        labels={'Count': 'Count'},
                        height=400,
                        markers=True
                    )
                    fig.update_layout(
                        xaxis_title='Year' if len(selected_years) > 1 else 'City',
                        yaxis_title='Number of Schools',
                        title_font=dict(size=20, family='Arial, sans-serif'),
                        xaxis_title_font=dict(size=14),
                        yaxis_title_font=dict(size=14),
                        legend_title=dict(font=dict(size=14)),
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig)

            else:
                st.write("No data available for the selected cities, years, and metrics.")
            
            
        elif page == "Score Analysis":
            # Score Analysis page content
            st.write("## Score Analysis")

            # Display selected cities
            st.write('You selected the following cities:')
            st.write(selected_cities)

            # Filter data for selected cities and years
            score_data = filtered_data[
            (filtered_data['City'].isin(selected_cities)) & 
            (filtered_data['Year'].isin(selected_years))
            ]

            if not score_data.empty:
        # Prepare data for plotting scores
                score_metrics = ['Education score', 'Enrolment score', 'Gender parity score', 'Learning score', 'School infrastructure score']
        
        # User selection for score metrics
                selected_metrics = st.multiselect(
                "Select score metrics to analyze:",
                options=score_metrics,
                 default=score_metrics  # Default to all available metrics
                )
        
                if not selected_metrics:
                    st.warning("Please select at least one score metric.")
                else:
            # Filter scores based on selected metrics
                    scores_df = score_data[['City', 'Year'] + selected_metrics]

            # User selection for plot type
                plot_type = st.radio("Select the type of plot to display:", ('Bar Plot', 'Line Plot'))

                if plot_type == 'Bar Plot':
                    melted_score_df = scores_df.melt(id_vars=['City', 'Year'], value_vars=selected_metrics, var_name='Score Type', value_name='Score Value')
                # Create a combined bar chart for scores
                    fig_scores = px.bar(
                        melted_score_df,
                        x='City',
                        y='Score Value',
                        color='Score Type',
                        title='Score Analysis for Selected Cities (Bar Plot)',
                        labels={'Score Value': 'Score', 'Score Type': 'Metric'},
                        height=400,
                        barmode='group'
                    )
                    st.plotly_chart(fig_scores)

                elif plot_type == 'Line Plot':
                # Create a line plot for scores with 'Year' included in x-axis
                    melted_scores_df = scores_df.melt(id_vars=['City', 'Year'], value_vars=selected_metrics, var_name='Score Type', value_name='Score Value')
                    fig_line = px.line(
                        melted_scores_df,
                        x='Year',
                        y='Score Value',
                        color='Score Type',
                        line_group='City',
                        line_shape='spline',
                        title='Score Analysis for Selected Cities (Line Plot)',
                        labels={'Score Value': 'Score', 'Score Type': 'Metric'},
                        height=400,
                        markers=True
                    )
                    st.plotly_chart(fig_line)

            # Display the scores data table
                st.subheader('Score Data Table')
                st.dataframe(scores_df)


        elif page == "Enrollment Analysis":
            st.write("## Enrollment Analysis")
            st.write("This page provides an analysis of enrollment statistics.")
            
            # Filter data for selected cities and years
            city_data = filtered_data[filtered_data['City'].isin(selected_cities) & (filtered_data['Year'].isin(selected_years))]
            
            if not city_data.empty:
                # Prepare data for plotting based on selected metrics
                enrollment_counts = []
                for city in selected_cities:
                    city_specific_data = city_data[city_data['City'] == city]
                    complete_primary_schools = city_specific_data['% Complete Primary Schools'].mean()  # Complete primary schools
                    boys_enrolled_percentage = city_specific_data['% Boys Enrolled'].mean()  # Average % boys enrolled
                    girls_enrolled_percentage = city_specific_data['% Girls Enrolled'].mean()  # Average % girls enrolled
                    
                    # Append counts based on selected options
                    enrollment_counts.append({
                        'City': city,
                        '% Complete Primary Schools': complete_primary_schools,
                        '% Boys Enrolled': boys_enrolled_percentage,
                        '% Girls Enrolled': girls_enrolled_percentage,
                        'Year': city_specific_data['Year'].unique()  # Get unique years for the city
                    })

                # Create a DataFrame for the plotting data
                enrollment_counts_df = pd.DataFrame(enrollment_counts)

                # Allow users to select which statistics to display
                selected_metrics = st.multiselect(
                    'Select Enrollment Metrics to Display',
                    options=['% Complete Primary Schools', '% Boys Enrolled', '% Girls Enrolled'],
                    default=['% Complete Primary Schools']  # Default selection
                )

                # Choose plot type
                selected_plot_types = st.multiselect("Select Plot Types:", options=["Bar", "Pie"])

                # Create a combined bar chart for selected metrics
                if "Bar" in selected_plot_types:
                    fig_enrollment_bar = px.bar(
                        enrollment_counts_df,
                        x='City',
                        y=selected_metrics,  # Use the selected metrics for the y-axis
                        title='Enrollment Statistics for Selected Cities (Bar Chart)',
                        labels={'value': 'Value', 'variable': 'Enrollment Metric'},
                        height=400,
                        barmode='group'  # Group bars by city
                    )
                    st.plotly_chart(fig_enrollment_bar)

                # Create pie chart for selected metrics
                if "Pie" in selected_plot_types:
                    # Melt the DataFrame to long format for pie chart
                    pie_data = enrollment_counts_df.melt(id_vars='City', value_vars=selected_metrics, 
                                                        var_name='Metric', value_name='Value')

                    fig_enrollment_pie = px.pie(
                        pie_data,
                        names='Metric',
                        values='Value',
                        title='Enrollment Statistics for Selected Cities (Pie Chart)',
                        height=400
                    )
                    st.plotly_chart(fig_enrollment_pie)

                # Display the enrollment data table
                st.subheader('Enrollment Data Table')
                st.dataframe(enrollment_counts_df[selected_metrics + ['City', 'Year']])  # Show selected metrics, City, and Year

            else:
                st.write("No data available for the selected cities and years.")
