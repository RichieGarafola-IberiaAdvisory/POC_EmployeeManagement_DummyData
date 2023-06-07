import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os
from pathlib import Path


# Define the database URL
db_url = "postgresql://postgres:postgres@localhost:5432/EmployeeManagement"

# Create the engine object
engine = create_engine(db_url)

# Load the data from the employeemanagementdb table
employees_df = pd.read_sql_table('employeemanagementdb', engine)

# Sidebar filters
st.sidebar.header('Filter Data')
selected_contract_projects = st.sidebar.multiselect('Contract Project', employees_df['Contract Project'].unique(), default=employees_df['Contract Project'].unique())
selected_work_locations = st.sidebar.multiselect('Work Location', employees_df['Work Location'].unique(), default=employees_df['Work Location'].unique())
selected_educations = st.sidebar.multiselect('Education Level', employees_df['Education Level'].unique(), default=employees_df['Education Level'].unique())
selected_clearances = st.sidebar.multiselect('Clearance Level', employees_df['Clearance Level'].unique(), default=employees_df['Clearance Level'].unique())
selected_certifications = st.sidebar.multiselect('Certification Name', employees_df['Certification Name'].unique(), default=employees_df['Certification Name'].unique())


# Filter the data based on user selections
filtered_employees_df = employees_df.copy()

if selected_contract_projects:
    filtered_employees_df = filtered_employees_df[filtered_employees_df['Contract Project'].isin(selected_contract_projects)]

if selected_work_locations:
    filtered_employees_df = filtered_employees_df[filtered_employees_df['Work Location'].isin(selected_work_locations)]

if selected_educations:
    filtered_employees_df = filtered_employees_df[filtered_employees_df['Education Level'].isin(selected_educations)]

if selected_clearances:
    filtered_employees_df = filtered_employees_df[filtered_employees_df['Clearance Level'].isin(selected_clearances)]

if selected_certifications:
    filtered_employees_df = filtered_employees_df[filtered_employees_df['Certification Name'].isin(selected_certifications)]

# Search employees by name
search_name = st.sidebar.text_input('Search Employee by Name')
if search_name:
    filtered_employees_df = filtered_employees_df[filtered_employees_df['Employee Name'].str.contains(search_name, case=False)]

# Display the filtered data
st.write('Filtered Employees Data')
st.dataframe(filtered_employees_df)

# Display the total count of filtered employees
st.write(f'Total Employees: {len(filtered_employees_df)}')

# Get the default downloads directory
downloads_dir = str(Path.home() / "Downloads")

# Create two columns for saving the data
col1, col2 = st.columns(2)
with col1:
    # Save button to excel
    if st.button('Save Data to Excel'):
        # Save the filtered dataframe to an Excel file in the downloads directory
        excel_file_path = os.path.join(downloads_dir, 'filtered_employees_data.xlsx')
        filtered_employees_df.to_excel(excel_file_path, index=False)
        st.success(f'Data saved successfully to {excel_file_path}!')

with col2:
    # Save button to CSV
    if st.button('Save Data to CSV'):
        # Save the filtered dataframe to a CSV file in the downloads directory
        csv_file_path = os.path.join(downloads_dir, 'filtered_employees_data.csv')
        filtered_employees_df.to_csv(csv_file_path, index=False)
        st.success(f'Data saved successfully to {csv_file_path}!')
        
        
# File uploader for data upload
uploaded_file = st.file_uploader("Upload CSV or Excel file to update database", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the uploaded file into a pandas DataFrame
    if uploaded_file.name.endswith('.csv'):
        new_data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        new_data = pd.read_excel(uploaded_file)

    # Remove duplicate rows from the new data
    new_data = new_data.drop_duplicates()

    # Convert data types of columns for merge
    existing_data = pd.read_sql_table('employeemanagementdb', engine)
    existing_data['Origination Date'] = pd.to_datetime(existing_data['Origination Date'])
    existing_data['Reinvestigation Date'] = pd.to_datetime(existing_data['Reinvestigation Date'])
    new_data['Origination Date'] = pd.to_datetime(new_data['Origination Date'])
    new_data['Reinvestigation Date'] = pd.to_datetime(new_data['Reinvestigation Date'])

    # Check for duplicate rows in the existing database table
    duplicate_rows = pd.merge(existing_data, new_data, how='inner', indicator=True)

    if not duplicate_rows.empty:
        st.warning('Duplicate rows found in the uploaded file. Skipping duplicate rows.')

    # Append the new non-duplicate data to the existing database table
    new_data = new_data[~new_data.isin(duplicate_rows)].dropna()
    new_data.to_sql('employeemanagementdb', engine, if_exists='append', index=False)
    st.success('Data successfully uploaded and appended to the database!')

# Create two columns for visualizations
col1, col2 = st.columns(2)

# Bar chart of employees per contract project
with col1:
    st.subheader('Employees per Contract Project')
    if not filtered_employees_df.empty:
        contract_project_counts = filtered_employees_df['Contract Project'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=contract_project_counts.values, y=contract_project_counts.index)
        plt.xlabel('Count')
        plt.ylabel('Contract Project')
        plt.title('Employees per Contract Project')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write('No data available for the selected criteria.')

# Pie chart of employees per clearance level
with col2:
    st.subheader('Employees per Clearance Level')
    if not filtered_employees_df.empty:
        clearance_counts = filtered_employees_df['Clearance Level'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 8))
        plt.pie(clearance_counts.values, labels=clearance_counts.index, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Employees per Clearance Level')
        st.pyplot(fig)
    else:
        st.write('No data available for the selected criteria.')

# Create two columns for visualizations
col1, col2 = st.columns(2)

# Box plot of years of experience
with col1:
    st.subheader('Distribution of Years of Experience')
    if not filtered_employees_df.empty:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(y=filtered_employees_df['Years of Experience'])
        plt.ylabel('Years of Experience')
        plt.title('Distribution of Years of Experience')
        st.pyplot(fig)
    else:
        st.write('No data available for the selected criteria.')

# Histogram of education levels
with col2:
    st.subheader('Distribution of Education Levels')
    if not filtered_employees_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        education_levels = filtered_employees_df['Education Level'].unique()
        counts = filtered_employees_df['Education Level'].value_counts()
        sns.barplot(x=counts.index, y=counts.values)
        plt.xlabel('Education Level')
        plt.ylabel('Count')
        plt.title('Distribution of Education Levels')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write('No data available for the selected criteria.')
