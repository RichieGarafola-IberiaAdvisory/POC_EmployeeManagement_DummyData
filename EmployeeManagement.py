# Import necessary libraries and modules
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import os
from pathlib import Path
import base64
from io import BytesIO
from openpyxl import Workbook

# Set the page configuration for the Streamlit application, including the title and icon.
st.set_page_config(
    # page_title="Employee Management Database",
    page_title="Local CSV Version",
    page_icon="📊",
    layout="wide"
)

# Hide the Streamlit menu and footer.
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
# Apply the CSS styles to the Streamlit application.
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Define the CSS styles
css = """
<style>
body {
    background-color: blue; /* Set the secondary background color to blue */
    color: black; /* Set the text color to black */
    font-family: sans-serif; /* Set the font to sans serif */
}

.sidebar .sidebar-content {
    background-color: blue; /* Set the background color of the sidebar to blue */
}
</style>
"""

# Apply the CSS styles
st.markdown(css, unsafe_allow_html=True)

# Define a flag for checking if the user is logged in
is_logged_in = False

# Display the Iberia Advisory image on the Streamlit application.
st.image("./Images/iberia-logo.png")

################
# AUTHENICATION
################

# Define a function check_password() that handles user authentication.
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True
    
# Check the user password using the check_password() function and sets the is_logged_in flag to True if the password is correct.
if check_password():
    is_logged_in = True

# Check if the user is logged in. If is_logged_in is True, it executes the code block for the logged-in user. Otherwise, it displays a warning message.
# Code to execute if the user is logged in
if is_logged_in:
    
# dashboard title
st.title("Employee Management Database")
st.subheader("Iberia Employees")
    
##
    ###########################################
    # REMOVE THIS TO START WITH A BLANK CANVAS
    ###########################################
    
        # Load the data from the employee_data.csv file
# employees_df = pd.read_csv('./Resources/employees_data.csv')
##


# Upload data file
uploaded_file = st.file_uploader("Upload CSV or Excel file with employee data", type=["csv", "xlsx"])
if uploaded_file is not None:
    # Read the uploaded file into a pandas DataFrame
    if uploaded_file.name.endswith('.csv'):
        employees_df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        employees_df = pd.read_excel(uploaded_file)
    
    # Check if the uploaded data has the expected headers
    expected_headers = ["Employee Name", "Date Joined", "Terminate Date", "Veterans",
                        "Supervisor", "Job Title", "Contract Project", "Work Location",
                        "Years of Experience", "Education Level", "Clearance Level",
                        "Origination Date", "Reinvestigation Date", "Certification Name", "HubZone"]
    
    if not all(column in employees_df.columns for column in expected_headers):
        st.error("The uploaded data does not have the expected headers. Please check your file.")
    else:
        # Display the uploaded data
        st.subheader("Uploaded Employee Data")
        st.dataframe(employees_df)
    
        # Set the flag to indicate that data has been uploaded
        data_uploaded = True
else:
    # Create an empty DataFrame if no file is uploaded
    employees_df = pd.DataFrame(columns=["Employee Name", "Date Joined", "Terminate Date", "Veterans",
                                          "Supervisor", "Job Title", "Contract Project", "Work Location",
                                          "Years of Experience", "Education Level", "Clearance Level",
                                          "Origination Date", "Reinvestigation Date", "Certification Name", "HubZone"])
    data_uploaded = False

try:
    # Check if data has been uploaded before using it
    if data_uploaded:

        # Sidebar filters for selecting contract projects, work locations, education levels, clearance levels, certifications, and other columns.
        st.sidebar.header('Filter Data')
        selected_contract_projects = st.sidebar.multiselect('Contract Project', employees_df['Contract Project'].unique(),
                                                            default=employees_df['Contract Project'].unique())
        selected_work_locations = st.sidebar.multiselect('Work Location', employees_df['Work Location'].unique(),
                                                         default=employees_df['Work Location'].unique())
        selected_educations = st.sidebar.multiselect('Education Level', employees_df['Education Level'].unique(),
                                                     default=employees_df['Education Level'].unique())
        selected_clearances = st.sidebar.multiselect('Clearance Level', employees_df['Clearance Level'].unique(),
                                                     default=employees_df['Clearance Level'].unique())
        selected_certifications = st.sidebar.multiselect('Certification Name',
                                                             employees_df['Certification Name'].unique(),
                                                             default=employees_df['Certification Name'].unique())

        # Date range filters for Date Joined
        selected_dates_joined = st.sidebar.date_input('Date Joined Range',
                                                      value=(pd.to_datetime(employees_df['Date Joined'].min()),
                                                                 pd.to_datetime(employees_df['Date Joined'].max())))

        # Date range filters for Termination Date 
        selected_terminate_dates = st.sidebar.date_input('Terminated Date',
                                                      value=(pd.to_datetime(employees_df['Terminate Date'].min()),
                                                             pd.to_datetime(employees_df['Terminate Date'].max())))

        selected_veterans = st.sidebar.multiselect('Veterans',
                                                   employees_df['Veterans'].unique(),
                                                   default=employees_df['Veterans'].unique())

        selected_job_titles = st.sidebar.multiselect('Job Title',
                                                     employees_df['Job Title'].unique(),
                                                     default=employees_df['Job Title'].unique())
        selected_years_of_experience = st.sidebar.multiselect('Years of Experience',
                                                                  employees_df['Years of Experience'].unique(),
                                                                  default=employees_df['Years of Experience'].unique())

        # Date range filters for Origination Date 
        selected_origination_dates = st.sidebar.date_input('Origination Date',
                                                      value=(pd.to_datetime(employees_df['Origination Date'].min()),
                                                             pd.to_datetime(employees_df['Origination Date'].max())))

        # Date range filters for Reinvestigation Date 
        selected_reinvestigation_dates = st.sidebar.date_input('Reinvestigation Date',
                                                      value=(pd.to_datetime(employees_df['Reinvestigation Date'].min()),
                                                             pd.to_datetime(employees_df['Reinvestigation Date'].max())))

        selected_hubzone = st.sidebar.multiselect('HubZone',
                                                  employees_df['HubZone'].unique(),
                                                  default=employees_df['HubZone'].unique())

        # Filter the data based on user selections
        filtered_employees_df = employees_df.copy()

        if selected_contract_projects:
            filtered_employees_df = filtered_employees_df[
                filtered_employees_df['Contract Project'].isin(selected_contract_projects)]

        if selected_work_locations:
            filtered_employees_df = filtered_employees_df[filtered_employees_df['Work Location'].isin(selected_work_locations)]

        if selected_educations:
            filtered_employees_df = filtered_employees_df[filtered_employees_df['Education Level'].isin(selected_educations)]

        if selected_clearances:
            filtered_employees_df = filtered_employees_df[filtered_employees_df['Clearance Level'].isin(selected_clearances)]

        if selected_certifications:
            filtered_employees_df = filtered_employees_df[
                filtered_employees_df['Certification Name'].isin(selected_certifications)]

        if selected_dates_joined:
            start_date = selected_dates_joined[0]
            end_date = selected_dates_joined[1]
            filtered_employees_df['Date Joined'] = pd.to_datetime(filtered_employees_df['Date Joined']).dt.date
            filtered_employees_df = filtered_employees_df[
                (filtered_employees_df['Date Joined'] >= start_date) &
                (filtered_employees_df['Date Joined'] <= end_date)]

        if selected_terminate_dates:
            start_date = selected_dates_joined[0]
            end_date = selected_dates_joined[1]
            filtered_employees_df['Terminate Date'] = pd.to_datetime(filtered_employees_df['Terminate Date']).dt.date
            filtered_employees_df = filtered_employees_df[
                (filtered_employees_df['Terminate Date'] >= start_date) &
                (filtered_employees_df['Terminate Date'] <= end_date)]

        if selected_veterans:
            filtered_employees_df = filtered_employees_df[
                filtered_employees_df['Veterans'].isin(selected_veterans)]

        if selected_job_titles:
            filtered_employees_df = filtered_employees_df[
                filtered_employees_df['Job Title'].isin(selected_job_titles)]

        if selected_years_of_experience:
            filtered_employees_df = filtered_employees_df[
                filtered_employees_df['Years of Experience'].isin(selected_years_of_experience)]

        if selected_origination_dates:
            start_date = selected_dates_joined[0]
            end_date = selected_dates_joined[1]
            filtered_employees_df['Origination Date'] = pd.to_datetime(filtered_employees_df['Origination Date']).dt.date
            filtered_employees_df = filtered_employees_df[
                (filtered_employees_df['Origination Date'] >= start_date) &
                (filtered_employees_df['Origination Date'] <= end_date)]

        if selected_reinvestigation_dates:
            start_date = selected_dates_joined[0]
            end_date = selected_dates_joined[1]
            filtered_employees_df['Reinvestigation Date'] = pd.to_datetime(filtered_employees_df['Reinvestigation Date']).dt.date
            filtered_employees_df = filtered_employees_df[
                (filtered_employees_df['Reinvestigation Date'] >= start_date) &
                (filtered_employees_df['Reinvestigation Date'] <= end_date)]


        if selected_hubzone:
            filtered_employees_df = filtered_employees_df[
                filtered_employees_df['HubZone'].isin(selected_hubzone)]

        # Search employees by name
        search_name = st.sidebar.text_input('Search Employee by Name')
        if search_name:
            filtered_employees_df = filtered_employees_df[filtered_employees_df['Employee Name'].str.contains(search_name,
                                                                                                                 case=False)]
        # Search Supervisor by name
        search_name = st.sidebar.text_input('Search Supervisor by Name')
        if search_name:
            filtered_employees_df = filtered_employees_df[filtered_employees_df['Supervisor'].str.contains(search_name,
                                                                                                                 case=False)]    
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
        # Save button to Excel
            if st.button('Save Data to Excel'):
                        # Save the filtered dataframe to an Excel file in memory
                excel_buffer = BytesIO()
                filtered_employees_df.to_excel(excel_buffer, index=False)
                excel_data = excel_buffer.getvalue()

                       # Generate a download link for the Excel file
                b64 = base64.b64encode(excel_data).decode('utf-8')
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="filtered_employees_data.xlsx">Download Excel File</a>'
                st.markdown(href, unsafe_allow_html=True)

        with col2:
                # Save button to CSV
            if st.button('Save Data to CSV'):
                    # Save the filtered dataframe to a CSV file in memory
                csv_buffer = BytesIO()
                filtered_employees_df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()

                        # Generate a download link for the CSV file
                b64 = base64.b64encode(csv_data).decode('utf-8')
                href = f'<a href="data:text/csv;base64,{b64}" download="filtered_employees_data.csv">Download CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)

            # File uploader for data upload
        uploaded_file = st.file_uploader("Upload CSV or Excel file to update data", type=["csv", "xlsx"],
                                             key="file_uploader")

        if uploaded_file is not None:
                # Read the uploaded file into a pandas DataFrame
            if uploaded_file.name.endswith('.csv'):
                new_data = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xls', '.xlsx')):
                new_data = pd.read_excel(uploaded_file)

                # Remove duplicate rows from the new data
            new_data = new_data.drop_duplicates()

                # Save the original DataFrame for archive if it doesn't exist
            if not os.path.isfile('./Resources/employee_data_archive.csv'):
                employees_df.to_csv('./Resources/employee_data_archive.csv', index=False)

                # Append only non-duplicate data to the existing dataset
            merged_df = pd.concat([employees_df, new_data], ignore_index=True)
            employees_df = merged_df.drop_duplicates()

                # Save the updated dataset to a CSV or Excel file
            if uploaded_file.name.endswith('.csv'):
                    employees_df.to_csv('./Resources/employee_data.csv', index=False)
                    st.success('Data successfully uploaded and appended to employee_data.csv!')
            elif uploaded_file.name.endswith(('.xls', '.xlsx')):
                employees_df.to_excel('./Resources/employee_data.xlsx', index=False)
                st.success('Data successfully uploaded and appended to employee_data.xlsx!')

               # Set the color palette to different shades of blue
        sns.set_palette("Blues")

                # Create two columns for visualizations
        col1, col2 = st.columns(2)

                # Bar chart of employees per contract project
        with col1:
            st.subheader('Employees per Contract Project')
            if not filtered_employees_df.empty:
                contract_project_counts = filtered_employees_df['Contract Project'].value_counts()
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(x=contract_project_counts.index, y=contract_project_counts.values, palette="Blues")
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

        col1, col2 = st.columns(2)
        with col1:
            # Calculate the percentage of employees in each HubZone category
            hubzone_counts = employees_df['HubZone'].value_counts()
            hubzone_percentages = hubzone_counts / hubzone_counts.sum() * 100

            # Create a pie chart to visualize the percentages
            fig, ax = plt.subplots()
            ax.pie(hubzone_percentages, labels=hubzone_percentages.index, autopct='%1.1f%%')
            ax.set_title('HubZone Distribution')

            # Display the pie chart
            st.pyplot(fig)
            
except NameError:
    st.warning("Please upload data first.")
