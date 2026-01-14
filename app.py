import streamlit as st
import pandas as pd

st.set_page_config(page_title="UIDAI AI Dashboard", layout="wide")

st.title("🛡️ UIDAI Aadhaar AI Dashboard")
st.write("Developed by: **Prem Kumar Sah**")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("aadhaar_master_summary.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

try:
    df = load_data()

    # --- Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("AI Flagged Anomalies", len(df[df['is_anomaly'] == -1]))
    col3.metric("Avg Saturation Score", f"{df['sat_score'].mean():.2f}")

    # --- Chart 1: State Activity (Using Streamlit Inbuilt Bar Chart) ---
    st.subheader("📊 State-wise System Load")
    state_data = df.groupby('state')['total_updates'].sum()
    st.bar_chart(state_data)

    # --- Chart 2: Anomaly Summary ---
    st.subheader("🚨 AI Security: Anomaly Detection Summary")
    anomaly_counts = df['is_anomaly'].value_counts().rename({1: "Normal", -1: "Suspicious"})
    st.bar_chart(anomaly_counts)

    # --- Data Table for Audit ---
    st.subheader("📋 AI Audit List: Priority Pincodes")
    audit_data = df[df['is_anomaly'] == -1][['pincode', 'state', 'total_updates']].sort_values(by='total_updates', ascending=False).head(10)
    st.table(audit_data)

    st.success("Dashboard is live using Streamlit Native Charts!")

except Exception as e:
    st.error(f"Error: {e}")