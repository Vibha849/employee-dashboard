import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# Page Setup
# ------------------------------------------------------------
st.set_page_config(page_title="Employee Performance Dashboard", layout="wide")
st.title("📊 Employee Performance Dashboard")

# ------------------------------------------------------------
# Load CSV
# ------------------------------------------------------------
uploaded_file = st.file_uploader("Upload Employee CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ------------------------------------------------------------
    # Robust KPI column detection
    # ------------------------------------------------------------
    def find_column(df, possible_names):
        """Return first matching column from possible_names in df, ignoring spaces, underscores, and case."""
        cols_clean = {c.lower().replace(" ", "").replace("_",""): c for c in df.columns}
        for name in possible_names:
            key = name.lower().replace(" ", "").replace("_","")
            if key in cols_clean:
                return cols_clean[key]
        return None

    kpi_columns = {
        "Total Talk Time": find_column(df, ["Total Talktime", "totaltalktime"]),
        "Total Connected": find_column(df, ["Total Connected", "totalconnected"]),
        "Total Cold Connected": find_column(df, ["Total Cold Connected", "totalcoldconnected"]),
        "Unique Cold Connected": find_column(df, ["Unique Cold Connected", "uniquecoldconnected"]),
        "Site Visit Done": find_column(df, ["Site Visit Done", "sitevisitdone"]),
        "Meetings Done": find_column(df, ["Meetings Done", "meetingsdone"]),
        "SV Planned": find_column(df, ["SV Planned", "svplanned"]),
        "Calls > 3 mins": find_column(df, ["Calls(>3 mins)", "calls>3mins", "calls>3min"])
    }

    # ------------------------------------------------------------
    # Sidebar Filters
    # ------------------------------------------------------------
    st.sidebar.header("🔍 Filters")
    emp_filter = st.sidebar.multiselect(
        "Select Employee",
        options=df["Employee Name"].unique()
    )
    sup_filter = st.sidebar.multiselect(
        "Select Supervisor",
        options=df["Supervisor Name"].unique()
    )
    loc_filter = st.sidebar.multiselect(
        "Select Location",
        options=df["Location"].unique()
    )

    filtered = df.copy()
    if emp_filter:
        filtered = filtered[filtered["Employee Name"].isin(emp_filter)]
    if sup_filter:
        filtered = filtered[filtered["Supervisor Name"].isin(sup_filter)]
    if loc_filter:
        filtered = filtered[filtered["Location"].isin(loc_filter)]

    # ------------------------------------------------------------
    # KPI ROW 1
    # ------------------------------------------------------------
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Employees", f"{len(filtered):,}")
    kpi2.metric("Unique Supervisors", f"{filtered['Supervisor Name'].nunique():,}")
    kpi3.metric("Total Locations", f"{filtered['Location'].nunique():,}")

    st.markdown("---")

    # ------------------------------------------------------------
    # Employee Card
    # ------------------------------------------------------------
    st.subheader("👤 Employee Card")
    selected_emp = st.selectbox("Choose an employee", filtered["Employee Name"].unique())
    emp = filtered[filtered["Employee Name"] == selected_emp].iloc[0]

    st.markdown(
        f"""
        <div style="
            padding: 20px;
            border-radius: 12px;
            background-color: #2c2c2c;
            color: white;
        ">
            <h3 style="margin:0;">{emp['Employee Name']}</h3>
            <p>🔖 <strong>Employee ID:</strong> {emp['Employee Code']}</p>
            <p>⭐ <strong>Level:</strong> {emp['Level']}</p>
            <p>👨‍💼 <strong>Supervisor:</strong> {emp['Supervisor Name']}</p>
            <p>📍 <strong>Location:</strong> {emp['Location']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ------------------------------------------------------------
    # Function to get KPI value safely
    # ------------------------------------------------------------
    def get_kpi_value(kpi_name):
        col = kpi_columns.get(kpi_name)
        return emp[col] if col and col in emp.index else 0

    # ------------------------------------------------------------
    # Function to format KPI value with color
    # ------------------------------------------------------------
    def format_metric(value):
        formatted = f"{value:,}"
        color = "green" if value > 0 else "red"
        return f"<span style='color:{color}; font-weight:bold'>{formatted}</span>"

    # ------------------------------------------------------------
    # KPI ROW 2
    # ------------------------------------------------------------
    n1, n2, n3, n4 = st.columns([2,2,2,2])
    n5, n6, n7, n8 = st.columns([2,2,2,2])

    n1.metric("Total Talk Time", f"{get_kpi_value('Total Talk Time'):,}")
    n2.metric("Total Connected", f"{get_kpi_value('Total Connected'):,}")
    n3.metric("Total Cold Connected", f"{get_kpi_value('Total Cold Connected'):,}")
    n4.metric("Unique Cold Connected", f"{get_kpi_value('Unique Cold Connected'):,}")

    n5.metric("Site Visit Done", f"{get_kpi_value('Site Visit Done'):,}")
    n6.metric("Meetings Done", f"{get_kpi_value('Meetings Done'):,}")
    n7.metric("SV Planned", f"{get_kpi_value('SV Planned'):,}")
    n8.metric("Calls > 3 mins", f"{get_kpi_value('Calls > 3 mins'):,}")

    st.markdown("---")

    # ------------------------------------------------------------
    # KPI Charts
    # ------------------------------------------------------------
    st.subheader("📈 KPI Visual Insights")

    connected_df = pd.DataFrame({
        "Metric": ["Total Connected", "Total Cold Connected", "Unique Cold Connected"],
        "Value": [
            get_kpi_value("Total Connected"),
            get_kpi_value("Total Cold Connected"),
            get_kpi_value("Unique Cold Connected")
        ]
    })
    fig1 = px.bar(connected_df, x="Metric", y="Value",
                  title="Connected Call Metrics",
                  text="Value",
                  color="Value",
                  color_continuous_scale=px.colors.sequential.Teal)

    productivity_df = pd.DataFrame({
        "Metric": ["Meetings Done", "SV Planned", "Site Visit Done"],
        "Value": [
            get_kpi_value("Meetings Done"),
            get_kpi_value("SV Planned"),
            get_kpi_value("Site Visit Done")
        ]
    })
    fig2 = px.bar(productivity_df, x="Metric", y="Value",
                  title="Meetings & Site Visits",
                  text="Value",
                  color="Value",
                  color_continuous_scale=px.colors.sequential.Viridis)

    c1, c2 = st.columns(2)
    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ------------------------------------------------------------
    # Employee Table
    # ------------------------------------------------------------
    table_cols = ["Employee Name", "Level", "Supervisor Name", "Location"]
    st.subheader("📋 Employee Table")
    st.dataframe(filtered[table_cols], use_container_width=True)

else:
    st.info("📥 Please upload your employee CSV file to begin.")
