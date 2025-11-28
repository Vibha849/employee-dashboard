import streamlit as st
import pandas as pd

st.set_page_config(page_title="Employee Performance Dashboard", layout="wide")
st.title("📊 Employee Performance Dashboard")

# -------------------------------------------
# Exact column mapping (based on your screenshot)
# -------------------------------------------
COLUMN_MAP = {
    "talk": "Total Talktime",
    "connect": "Total Connected",
    "calls_gt_3": "Calls(>3 mins)",
    "sv_done": "Site Visit Done",
    "sv_planned": "SV Planned",
}

# -------------------------------------------
# Load CSV
# -------------------------------------------
@st.cache_data
def load_data(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.read_csv(path, encoding="latin1")

csv_path = r"C:\Users\USER\Downloads\New_Dashboard_Employee\InputReportData (1).csv"
df = load_data(csv_path)

# Cleanup whitespace
df.columns = [str(c).strip() for c in df.columns]

# -------------------------------------------
# Sidebar Filters
# -------------------------------------------
name_col = "Employee Name"
level_col = "Level"
supervisor_col = "Supervisor Name"

st.sidebar.header("🔍 Filters")

levels = sorted(df[level_col].dropna().unique()) if level_col in df.columns else []
supervisors = sorted(df[supervisor_col].dropna().unique()) if supervisor_col in df.columns else []

selected_levels = st.sidebar.multiselect("Filter by Level", levels)
selected_supervisors = st.sidebar.multiselect("Filter by Supervisor", supervisors)
search_name = st.sidebar.text_input("Search Employee Name")

filtered_df = df.copy()

if selected_levels:
    filtered_df = filtered_df[filtered_df[level_col].isin(selected_levels)]

if selected_supervisors:
    filtered_df = filtered_df[filtered_df[supervisor_col].isin(selected_supervisors)]

if search_name:
    filtered_df = filtered_df[filtered_df[name_col].str.contains(search_name, case=False, na=False)]

# -------------------------------------------
# Summary KPIs
# -------------------------------------------
st.subheader("📈 Summary Metrics")

def safe_sum(col):
    return filtered_df[col].fillna(0).astype(float).sum() if col in filtered_df.columns else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Talktime", round(safe_sum(COLUMN_MAP["talk"]), 2))
col2.metric("Total Connected", int(safe_sum(COLUMN_MAP["connect"])))
col3.metric("Calls > 3 mins", int(safe_sum(COLUMN_MAP["calls_gt_3"])))
col4.metric("Site Visit Done", int(safe_sum(COLUMN_MAP["sv_done"])))
col5.metric("SV Planned", int(safe_sum(COLUMN_MAP["sv_planned"])))

# -------------------------------------------
# Data Table
# -------------------------------------------
st.subheader("📄 Employee Data Table")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------------------------
# Download Button
# -------------------------------------------
st.download_button(
    label="⬇ Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_employee_data.csv",
    mime="text/csv"
)

