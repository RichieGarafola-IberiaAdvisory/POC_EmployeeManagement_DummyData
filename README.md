https://iberiaemployeedatabase.streamlit.app/

# Employee Management

Employee Management is a comprehensive web application designed to simplify the management of employee records. It provides a robust set of features for creating, viewing, updating, and deleting employee information, making it an ideal solution for businesses and organizations of all sizes.

Managing employee data efficiently is crucial for HR departments and team leads. This application aims to streamline the process by offering an intuitive user interface and powerful functionality. With Employee Management, you can effortlessly keep track of employee details, such as contact information, job roles, departments, and more.

Whether you are a small startup or a large enterprise, Employee Management offers a scalable and customizable solution to meet your specific requirements. It serves as a solid foundation for building upon, enabling you to extend and enhance the application based on your organization's unique needs.

---

## Table of Contents

- [Installation](#Installation)
- [Instructions](#Instructions)
- [Usage](#Usage)
- [Features](#Features)
- [Contributing](#Contributing)

---

## Installation

To run the Employee Management application locally, follow these steps:

1. Clone this repository: `git clone https://github.com/RichieGarafola/EmployeeManagement.git`
2. Navigate to the project directory: `cd EmployeeManagement`
3. Install the dependencies: `npm install`
4. Start the application: `npm start`
5. Open your browser and visit: `http://localhost:3000`

---

## Instructions

### Step 1: Install PostgreSQL:

- Download and install PostgreSQL from the official website (https://www.postgresql.org/download/).
- Follow the installation instructions specific to your operating system.

---

### Step 2: Connect to PostgreSQL:

- Open a command prompt or terminal and connect to the PostgreSQL database using the psql command-line tool or a graphical interface like pgAdmin.
- Use the following command to connect to the default PostgreSQL database

    psql -U postgres
    
- Enter the password for the "postgres" user when prompted.

---

### Step 3: Create a New Database:

- Create a new database for the employee management system using the following command:

    CREATE DATABASE employee_management;
    
---

### Step 4: Connect to the New Database:

Connect to the newly created database using the following command:

    \c employee_management
---

### Step 5: Design the Database Schema:

- Determine the tables you need based on the requirements.
- For this example, let's create five tables: contract_projects, work_locations, educations, clearances, and employees.


    -- Create the contract_projects table
    
    CREATE TABLE contract_projects (
        
        contract_project_id SERIAL PRIMARY KEY,
        
        name VARCHAR(255)
    );

    -- Create the work_locations table
    
    CREATE TABLE work_locations (
        
        work_location_id SERIAL PRIMARY KEY,
       
        name VARCHAR(255)
    );

    -- Create the educations table
    
    CREATE TABLE educations (
        
        education_id SERIAL PRIMARY KEY,
        
        level VARCHAR(255)
    );

    -- Create the clearances table
    
    CREATE TABLE clearances (
    
        clearance_id SERIAL PRIMARY KEY,
        
        level VARCHAR(255),
        
        status VARCHAR(255)
    );

    -- Create the employees table
    
    CREATE TABLE employees (
            
        name VARCHAR(255),
        
        contract_project_id INT,
        
        work_location_id INT,
        
        years_of_experience INT,
        
        education_id INT,
        
        clearance_id INT,
        
        origination_date DATE,
        
        reinvestigation_date DATE,
        
        FOREIGN KEY (contract_project_id) REFERENCES contract_projects (contract_project_id),
        
        FOREIGN KEY (work_location_id) REFERENCES work_locations (work_location_id),
        
        FOREIGN KEY (education_id) REFERENCES educations (education_id),
        
        FOREIGN KEY (clearance_id) REFERENCES clearances (clearance_id)
    );
    
    -- Create the certifications table
    
        CREATE TABLE certifications (
        certification_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        description VARCHAR(255)
    );
    
    -- Create the unnormalize EmployeeManagementDB table
    
        CREATE TABLE EmployeeManagementDB (
        employee_name VARCHAR(255),
        contract_project_name VARCHAR(255),
        work_location_name VARCHAR(255),
        years_of_experience INT,
        education_level VARCHAR(255),
        clearance_level VARCHAR(255),
        origination_date DATE,
        reinvestigation_date DATE,
        certification_name VARCHAR(255)
    );

    

---

## Usage

After starting the application and visiting the specified URL, you will see the Employee Management interface. The application offers the following key functionalities:

- **Add Employee:** Click on the "Add Employee" button to create a new employee record. Fill in the required fields, including contact information, job details, and department affiliation.

- **View Employees:** Access the list of employees and their details by clicking on the "View Employees" button. This feature enables you to search, sort, and filter employee records, facilitating easy access to the information you need.

- **Update Employee:** To modify an existing employee's information, select the desired employee from the list and click on the "Edit" button. Update the relevant fields and save your changes.

- **Delete Employee:** If an employee is no longer with the company or their record needs to be removed, select the employee from the list and click on the "Delete" button. Confirm the deletion to remove the employee from the system.

---

## Features


The Employee Management application offers the following powerful features:

- **User-Friendly Interface:** The application boasts an intuitive and user-friendly interface, making it easy for HR professionals, managers, and administrators to navigate and utilize its functionalities.

- **Secure Authentication:** Protect employee data with secure authentication mechanisms. Users can log in securely using their credentials to ensure only authorized personnel can access and manage employee information.

- **Role-Based Access Control:** Assign different roles to users based on their responsibilities and grant access accordingly. Control the level of access and privileges for different user types, ensuring data confidentiality and integrity.

- **Search and Filter:** Seamlessly search, sort, and filter employee records based on various criteria, such as name, department, position, and more. Quickly locate specific employees

---

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. Here are the steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push the branch to your forked repository: `git push origin my-feature-branch`
5. Open a pull request in this repository.

Please ensure that your contributions adhere to the project's coding standards and follow the existing patterns.
