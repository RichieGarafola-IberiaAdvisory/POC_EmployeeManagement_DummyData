# Import necessary libraries and modules
import streamlit as st
import pandas as pd

# Set the page configuration for the Streamlit application, including the title and icon.
st.set_page_config(
    page_title="Employee Management Database",
    page_icon="📊",
    layout="wide"
)

# Display the Iberia Advisory image on the Streamlit application.
st.image("./Images/iberia-logo.png")

# Load the data from the employee_data.csv file
employees_df = pd.read_csv('./Resources/employees_data.csv')

# Add new rows to the DataFrame
st.subheader('Add New Employee')
name = st.text_input('Employee Name')
date_joined = st.date_input('Date Joined')
terminate_date = st.date_input('Terminate Date')
veterans = st.selectbox('Veterans', ["NA", "Army", "Navy", "Air Force", "Marines", "Coast Guard"])
supervisor = st.text_input('Supervisor')
job_title = st.text_input('Job Title')
contract_project = st.text_input('Contract Project')
work_location = st.text_input('Work Location')
years_of_experience = st.number_input('Years of Experience', min_value=0)
education_level = st.selectbox('Education Level', ['High School', "Bachelor's", "Master's", 'Ph.D.'])
clearance_level = st.selectbox('Clearance Level', ['Confidential', 'Secret', 'Top Secret'])
origination_date = st.date_input('Origination Date')
reinvestigation_date = st.date_input('Reinvestigation Date')
certification_name = st.text_input('Certification Name')
hubzone = st.selectbox('HubZone', ['Yes', 'No'])

if st.button('Add Employee'):
    new_employee = {
        'Employee Name': name,
        'Date Joined': date_joined,
        'Terminate Date': terminate_date,
        'Veterans': veterans,
        'Supervisor': supervisor,
        'Job Title': job_title,
        'Contract Project': contract_project,
        'Work Location': work_location,
        'Years of Experience': years_of_experience,
        'Education Level': education_level,
        'Clearance Level': clearance_level,
        'Origination Date': origination_date,
        'Reinvestigation Date': reinvestigation_date,
        'Certification Name': certification_name,
        'HubZone': hubzone
    }
    new_employee_df = pd.DataFrame(new_employee, index=[0])
    employees_df = pd.concat([employees_df, new_employee_df], ignore_index=True)
    st.success('Employee added successfully.')

# Save the updated DataFrame to a CSV file
if st.button('Save Data'):
    employees_df.to_csv('employees_data_updated.csv', index=False)
    st.success('Data saved successfully.')

# Checkbox for viewing the database
st.subheader('View Database')
view_option = st.checkbox('View Employees')

if view_option:
    st.write('Employees')
    st.dataframe(employees_df)