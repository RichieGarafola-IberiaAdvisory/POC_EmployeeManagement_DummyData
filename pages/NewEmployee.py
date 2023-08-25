# Import necessary libraries and modules
import streamlit as st
import pandas as pd

import base64
from io import BytesIO

# Set the page configuration for the Streamlit application, including the title and icon.
st.set_page_config(
    page_title="Iberia Advisory New Employee",
    page_icon="📊",
    layout="wide"
)

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
    
    # Define the expected column headers for your DataFrame
    expected_headers = ["Employee Name", "Date Joined", "Terminate Date", "Veterans",
                        "Supervisor", "Job Title", "Contract Project", "Work Location",
                        "Years of Experience", "Education Level", "Clearance Level",
                        "Origination Date", "Reinvestigation Date", "Certification Name", "HubZone"]
    
    # Initialize an empty DataFrame with expected headers
    st.session_state.employees_df = st.session_state.get("employees_df", pd.DataFrame(columns=expected_headers))
    
    # Upload data file
    uploaded_file = st.file_uploader("Upload CSV or Excel file with employee data", type=["csv", "xlsx"])
    if uploaded_file is not None:
        # Check file type and read into a pandas DataFrame
        if uploaded_file.name.endswith('.csv'):
            uploaded_data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            uploaded_data = pd.read_excel(uploaded_file)
        
        # Check if the uploaded data has the expected headers
        if list(uploaded_data.columns) == expected_headers:
            # Append the uploaded data to the existing DataFrame
            st.session_state.employees_df = pd.concat([st.session_state.employees_df, uploaded_data], ignore_index=True)
            st.success('Data uploaded successfully.')
        else:
            st.error('Uploaded data has different headers. Please check the file and try again.')
    else:
        # Create an empty DataFrame with the expected headers if no file is uploaded
        employees_df = pd.DataFrame(columns=expected_headers)
    
    # Define a flag for checking if the user is logged in
    is_logged_in = False
    

    #######
    # App
    #######
        
    # Load the data from the employee_data.csv file
    # employees_df = pd.read_csv('./Resources/employees_data.csv')
        
    # Add new rows to the DataFrame
    st.subheader('Add New Employee')
    name = st.text_input('Employee Name')
    date_joined = st.date_input('Date Joined')
    
    # Checkbox for termination status
    terminated = st.checkbox('Terminated')
    if terminated:
        terminate_date = st.date_input('Termination Date')
    else:
        terminate_date = "NA"
    
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
        
        # Debug: Check if this block is executed
        st.write("Adding an employee...")
        
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
        new_employee_df = pd.DataFrame([new_employee], columns=st.session_state.employees_df.columns)
        
        # Debug: Print the new employee data
        st.write("New Employee Data:")
        st.write(new_employee_df)
        
        
        # Add the new employee to the existing DataFrame
        st.session_state.employees_df = pd.concat([st.session_state.employees_df, pd.DataFrame([new_employee], columns=expected_headers)], ignore_index=True)
        st.success('Employee added successfully.')
        
    # Create two columns for saving the data
    col1, col2 = st.columns(2)
    
    with col1:
        # Input field for Excel file name
        excel_filename = st.text_input("Enter Excel File Name (without extension)", "employees_data")
    
        # Save button to Excel
        if st.button('Save Data to Excel'):
            # Save the filtered dataframe to an Excel file in memory
            excel_buffer = BytesIO()
            st.session_state.employees_df.to_excel(excel_buffer, index=False)
            excel_data = excel_buffer.getvalue()
    
            # Generate a download link for the Excel file
            b64 = base64.b64encode(excel_data).decode('utf-8')
            excel_filename = f"{excel_filename}.xlsx"
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{excel_filename}">Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    with col2:
        # Input field for CSV file name
        csv_filename = st.text_input("Enter CSV File Name (without extension)", "employees_data")
    
        # Save button to CSV
        if st.button('Save Data to CSV'):
            # Save the filtered dataframe to a CSV file in memory
            csv_buffer = BytesIO()
            st.session_state.employees_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
    
            # Generate a download link for the CSV file
            b64 = base64.b64encode(csv_data).decode('utf-8')
            csv_filename = f"{csv_filename}.csv"
            href = f'<a href="data:text/csv;base64,{b64}" download="{csv_filename}">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    
        
    # Checkbox for viewing the database
    st.subheader('View Database')
    view_option = st.checkbox('View Employees')
        
    if view_option:
        st.write('Employees')
        st.dataframe(st.session_state.employees_df)
