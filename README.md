
# Finance Tracking App

Final project as part of my syllabus for CS50x

### Description:
Based upon the simple framework of flask this application performs all operations of CRUD. It utilises libraries such as flask, requests, datetime, werkzeug.security (for password hashing), calender, base64, matplotlib, BytesIO (for storing images to be converted to base64). I also used CS50 for SQL as I figured it didn't make sense to make it more complex by using the actual SQL libraries. I have created a helper functions file which basically stores 3 functions in total for keeping the main file elegant and mainting structure but that didn't help much lol. The UI of this project is based entirely on Bootstrap

Now onto the project description.

#### Below are the basic features it offers
>A password hashing system so the password isn't stored as plain text in the db.<br/>

>A Login and Registration form to seperate store user id.<br/>

>My account page for basic account controls such as changing profile, password or name and also for deleting the account altogether.<br/>

# Transactions Page Overview

The Transactions page of the web app provides tools for managing financial transactions. Users can add, update, or delete transactions, utilizing modals for interaction.

## Features

1. **Add Transaction**:
   - Users can add a transaction via a modal form.
   - The form includes dynamically generated select options sourced from the database.
   - Basic input validation checks are implemented.

2. **Update Transaction**:
   - Users can edit existing transactions by selecting a record with a radio button.
   - The edit modal pre-fills the form with values retrieved from the database based on the selected transaction's ID.
   - Users cannot change the transaction type and category during editing.

3. **Delete Transaction**:
   - Users can select multiple transactions using checkboxes for bulk deletion.
   - A confirmation modal prompts the user to confirm the deletion of selected records.
   - If no records are selected when attempting to delete, an error message is displayed.

## Search Functionality

- A search input field allows users to find specific transactions by name using SQL's `LIKE` keyword.
- The results displayed in the table will dynamically update to show only relevant records based on the search query.

## User Interface

- The main interface includes:
  - A search input field above the transaction management buttons (Add, Edit, Delete).
  - A table below displaying all user transactions or filtered results based on the search query.
  - Radio buttons for selecting a transaction for editing and checkboxes for selecting transactions for deletion.

## Error Handling

- If the user attempts to delete or edit without selecting a record, a corresponding error message is flashed.



# Dashboard overview

The dashboard is also the index page for this applicatoin, it serves as the entry point once the user logs in. 

## Features

1. **Transaction Summaries**:
   - It provides the summaries of transaction amounts such as monthly and yearly income and expense and the current balance remain for this month.

2. **Graphing**
    - For explaing things more clearly there are a total of 3 graphs, 2 of them are pie charts covering monthly and yearly expenses based on the categories. While the salary graph compares monthly expense and monthly salary over the year.



# Conclusion
 - The Finance Tracking App effectively helps users manage their financial transactions with a user-friendly interface and secure password handling. The dashboard provides insightful summaries and visualizations, allowing users to make informed decisions about their finances. I look forward to expanding its features and improving user engagement in the future.
