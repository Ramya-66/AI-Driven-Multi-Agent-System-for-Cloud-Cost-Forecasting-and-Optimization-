# dashboard/app.py

import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px

# ---------------------------
# Ensure project root is in Python path
# ---------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------------------
# Imports
# ---------------------------
from main import main

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(
    page_title="Cloud Cost AI Dashboard",
    layout="wide",
    page_icon="☁️"
)

st.title("☁️ Cloud Cost AI Dashboard")
st.markdown(
    "Visualize AWS cost drivers, forecasts, optimization suggestions, "
    "simulation savings, and budget alerts."
)

# ---------------------------
# Budget slider
# ---------------------------
budget_limit = st.sidebar.slider(
    "Monthly Cloud Budget (USD)",
    min_value=500,
    max_value=100000,
    value=15000,
    step=1000
)

# ---------------------------
# Run Cloud Cost AI system
# ---------------------------
try:
    results = main(budget_limit=budget_limit)
except FileNotFoundError as e:
    st.error(f"Error loading data: {e}")
    st.stop()
except Exception as e:
    st.error(f"Unexpected error: {e}")
    st.stop()

# ---------------------------
# Display Cost Driver Report
# ---------------------------
st.subheader("📊 Cost Driver Report")
driver_report = results["driver_report"].reset_index()
st.dataframe(driver_report)

fig_service = px.bar(
    driver_report.groupby("service")["cost_usd"].sum().reset_index(),
    x="service",
    y="cost_usd",
    title="Total Cost per Service",
    labels={"cost_usd": "Cost (USD)", "service": "Service"}
)
st.plotly_chart(fig_service, use_container_width=True)

# ---------------------------
# Optimization Recommendations
# ---------------------------
st.subheader("💡 Optimization Recommendations")
for rec in results["recommendations"]:
    st.info(rec)

# ---------------------------
# Simulation Savings
# ---------------------------
st.subheader("💰 Simulation Savings")
simulation_df = pd.DataFrame(
    list(results["simulation"].items()),
    columns=["Service", "Potential Savings"]
)
st.dataframe(simulation_df)

fig_saving = px.bar(
    simulation_df,
    x="Service",
    y="Potential Savings",
    title="Potential Savings per Service",
    labels={"Potential Savings": "Savings (USD)", "Service": "Service"}
)
st.plotly_chart(fig_saving, use_container_width=True)

# =========================================================
# ✅ FORECAST PLOTS — MOVED ABOVE BUDGET STATUS
# =========================================================
st.subheader("📈 Cost Forecasts")

plot_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "outputs", "plots")
)

if not os.path.exists(plot_dir):
    st.error("Forecast plots not found. Run python main.py first.")
else:
    plots = sorted(os.listdir(plot_dir))
    if not plots:
        st.warning("No forecast images found.")
    else:
        for plot in plots:
            st.image(
                os.path.join(plot_dir, plot),
                caption=plot.replace("_forecast.png", ""),
                use_container_width=True
            )

# ---------------------------
# Budget Status (NOW BELOW GRAPH)
# ---------------------------
st.subheader("🚨 Budget Status")
budget_status = results.get("budget_status", "Budget check not available")

if "exceeded" in budget_status.lower():
    st.error(budget_status)
else:
    st.success(budget_status)

st.markdown("---")
st.markdown("✅ Cloud Cost AI System executed successfully.")
