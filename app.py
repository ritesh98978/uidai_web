import streamlit as st
import pandas as pd

st.set_page_config(page_title="UIDAI AI Audit Tool", layout="wide")

st.title("🛡️ UIDAI AI Fraud Detection & Audit Dashboard")
st.markdown("Developed by: **Prem Kumar Sah**")

@st.cache_data
def load_data():
    df = pd.read_csv("aadhaar_master_summary.csv")
    return df

try:
    df = load_data()

    # 1. Main Metrics
    m1, m2, m3 = st.columns(3)
    anomalies_df = df[df['is_anomaly'] == -1]
    
    m1.metric("Total Records Analyzed", f"{len(df):,}")
    # Suspicious ko highlight karne ke liye
    m2.subheader(f"🚨 Suspicious: {len(anomalies_df)}")
    m3.metric("Normal Transactions", len(df[df['is_anomaly'] == 1]))

    st.markdown("---")

    # 2. RED CHART: Suspicious Activity Hotspots
    st.subheader("📍 Suspicious Activity Hotspots (By State)")
    st.write("Ye graph sirf un areas ko dikha raha hai jise AI ne **-1 (Suspicious)** mark kiya hai:")
    
    if not anomalies_df.empty:
        state_anomaly_count = anomalies_df.groupby('state').size().sort_values(ascending=False)
        
        # Streamlit bar_chart default color blue hota hai, 
        # isliye hum color parameter use karke ise RED karenge
        st.bar_chart(state_anomaly_count, color="#FF0000") 
        
        # 3. Priority Audit Table
        st.subheader("📋 AI Priority Audit List (Pincode Level)")
        st.error("ACTION REQUIRED: In Pincodes par turant physical audit bhejein (Status: -1)")
        
        audit_display = anomalies_df[['state', 'district', 'pincode', 'total_updates']].sort_values(by='total_updates', ascending=False).head(15)
        st.table(audit_display)
    else:
        st.success("Safe: No suspicious patterns detected.")

    st.markdown("---")
    
    # 4. Normal System Load
    st.subheader("📊 General System Load (Normal Activity)")
    st.write("Total updates volume per state (Status: 1):")
    state_load = df[df['is_anomaly'] == 1].groupby('state')['total_updates'].sum()
    st.bar_chart(state_load, color="#0000FF") # Normal ke liye Blue

except Exception as e:
    st.error(f"Error: {e}")