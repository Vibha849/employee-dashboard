# 📊 Employee Performance Dashboard

This repository contains a **Streamlit-based Employee Performance Dashboard** for analyzing employee performance using an uploaded CSV file.  

It allows you to:
- Filter employees by **Level**, **Supervisor**, and **Location**
- View **overall KPIs** (Total Employees, Unique Supervisors, Total Locations)
- See detailed **employee-wise performance metrics**
- Visualize performance using **interactive charts**

---

## 🧩 Features

### 1. CSV Upload
- Upload an employee performance CSV file (e.g. `Import_Emp_Data (1).csv`).
- The app reads the CSV and automatically cleans column names (trims spaces, etc.).
- Shows a message if no file is uploaded.

### 2. Filters
- Filter data using:
  - **Level**
  - **Supervisor Name**
  - **Location**
- All KPIs, charts and tables update based on selected filters.

### 3. Top-Level KPIs
The dashboard shows three main metrics:

- **Total Employees** – Count of employees in the filtered dataset.
- **Unique Supervisors** – Number of distinct supervisors.
- **Total Locations** – Number of distinct locations.

### 4. Employee Summary Card
For a selected employee, the dashboard shows:

- 👤 **Employee Name**
- 🆔 **Employee ID / Code**
- ⭐ **Level**
- 👨‍💼 **Supervisor Name**
- 📍 **Location**

Displayed in a nicely styled card at the top of the app.

### 5. Performance KPIs (Numeric)
Additional numeric KPIs (depending on the columns present in the CSV), such as:

- **Total Talk Time**
- **Total Connected**
- **Total Cold Connected**
- **Unique Cold Connected**
- **Site Visit Done**
- **Meetings Done**
- **SV Planned**
- **Calls > 3 mins**

> These KPIs are calculated based on grouped sums from the uploaded CSV file.

### 6. Visualizations
The app uses **Plotly** to create interactive charts, for example:

- Bar charts comparing performance metrics by **Employee** or **Supervisor**
- Visual summary of talk time and connected calls

### 7. Employee Table
A clean table view of employees with key columns like:

- Employee Name  
- Level  
- Supervisor Name  
- Location  

---

## 🛠 Tech Stack

- **Python**
- **Streamlit** – for the web UI
- **Pandas** – for data handling and aggregation
- **Plotly Express** – for interactive charts

---

## 📁 Project Structure

```text
.
├─ app.py                     # Main Streamlit app
└─ Import_Emp_Data (1).csv    # Sample employee performance data (example input file)
