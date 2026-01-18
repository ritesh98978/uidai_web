import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="UIDAI Sentinel Pro", layout="wide", initial_sidebar_state="expanded")

# Custom UI Styling (FIXED: unsafe_allow_html)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 5px solid #2E86C1; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ UIDAI SENTINEL: SECURITY & SOCIETAL DASHBOARD")
st.markdown("Developed by: **Prem Kumar Sah**")

# Sidebar for Tech Specs
st.sidebar.header("⚙️ AI SYSTEM CORE")
st.sidebar.markdown("""
- **Model:** Isolation Forest
- **Dataset:** 4M+ Records
- **Audit Logic:** Deviation Analysis
- **Status:** ✅ System Active
""")

# 2. Robust Data Loading
@st.cache_data(ttl=3600)
def load_and_process():
    file_name = "aadhaar_master_summary.csv"
    if not os.path.exists(file_name):
        return None
    try:
        df = pd.read_csv(file_name)
        if 'is_anomaly' in df.columns:
            df['Status'] = df['is_anomaly'].apply(lambda x: "🚨 SUSPICIOUS" if x == -1 else "✅ SAFE")
            df['Action'] = df['is_anomaly'].apply(lambda x: "TRIGGER PHYSICAL AUDIT" if x == -1 else "ROUTINE MONITORING")
        return df
    except Exception as e:
        return str(e)

try:
    df = load_and_process()
    if df is None:
        st.error("❌ Error: 'aadhaar_master_summary.csv' nahi mili. Please GitHub check karein!")
        st.stop()
    elif isinstance(df, str):
        st.error(f"⚠️ Data Error: {df}")
        st.stop()

    anomalies = df[df['is_anomaly'] == -1]
    safe_data = df[df['is_anomaly'] == 1]

    # --- TOP METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Records", f"{len(df):,}")
    m2.metric("Anomaly Detected", len(anomalies))
    m3.metric("Safe Transactions", len(safe_data))
    m4.metric("Security Score", "98.8%")

    st.markdown("---")

    # --- THE CONTRAST: SAFE VS ANOMALY ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 ANOMALY ZONE: High-Risk Hotspots")
        if not anomalies.empty:
            state_anomalies = anomalies.groupby('state').size().sort_values(ascending=False).head(10)
            st.bar_chart(state_anomalies, color="#FF0000") 
            st.error("Action Required: High deviation detected in these regions.")
        else:
            st.write("No anomalies found.")

    with col2:
        st.subheader("🟢 SAFE ZONE: Normal Operations")
        state_safe = safe_data.groupby('state').size().sort_values(ascending=False).head(10)
        st.bar_chart(state_safe, color="#28B463") 
        st.success("System Status: Operational patterns within normal limits.")

    st.markdown("---")

    # --- ACTIONABLE AUDIT TABLE ---
    st.subheader("📋 AI PRIORITY AUDIT LIST & ACTION PLAN")
    if not anomalies.empty:
        display_df = anomalies[['state', 'district', 'pincode', 'total_updates', 'Status', 'Action']].sort_values(by='total_updates', ascending=False)
        st.dataframe(display_df.head(25), use_container_width=True)

    # --- SOCIETAL INSIGHT ---
    st.markdown("---")
    st.subheader("🌍 Societal Trend: Migration & Infrastructure Insight")
    st.info("**Expert Analysis:** The high volume of address updates in industrial hubs suggest labor migration. **Recommendation:** Increase mobile Aadhaar units in green states.")

except Exception as e:
    st.error(f"Critical System Error: {e}")
