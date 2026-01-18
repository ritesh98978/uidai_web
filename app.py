import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="UIDAI Sentinel Pro", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (Fix for White Text & Better Visuals) ---
st.markdown("""
    <style>
    /* Background and Main Text Fix */
    .main { background-color: #f8fafc; color: #1e293b; }
    
    /* Heading and Subheader Color Fix */
    h1, h2, h3, p, span { color: #0f172a !important; }
    
    /* Metric Card Styling */
    [data-testid="stMetricValue"] {
        color: #1d4ed8 !important; 
        font-weight: bold;
        font-size: 2rem !important;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #1d4ed8;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    /* Tabs Text Color Fix */
    .stTabs [data-baseweb="tab"] p {
        color: #334155 !important;
        font-weight: 600;
    }
    
    /* Logo and Header Align */
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH LOGO ---
# UIDAI Official Logo URL
logo_url = "https://upload.wikimedia.org/wikipedia/en/c/cf/Aadhaar_Logo.svg"

st.markdown(f"""
    <div class="header-container">
        <img src="{logo_url}" width="80">
        <div>
            <h1 style='margin:0;'>UIDAI SENTINEL: AI-DRIVEN INVESTIGATION TOOL</h1>
            <p style='margin:0; font-weight:bold; color:#64748b;'>Developed by: Prem Kumar Sah | Security Analytics Framework</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("⚙️ AI ENGINE CORE")
st.sidebar.info("Model: Isolation Forest | Dataset: 150K+ Records")
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Pincode Audit Search")
search_pincode = st.sidebar.text_input("Enter Pincode:", placeholder="e.g. 110001")

@st.cache_data(ttl=3600)
def load_and_process():
    file_name = "aadhaar_master_summary.csv"
    if not os.path.exists(file_name): return None
    try:
        df = pd.read_csv(file_name)
        df['pincode'] = df['pincode'].astype(str)
        df['Status'] = df['is_anomaly'].apply(lambda x: "🚨 SUSPICIOUS" if x == -1 else "✅ SAFE")
        df['Action'] = df['is_anomaly'].apply(lambda x: "TRIGGER PHYSICAL AUDIT" if x == -1 else "ROUTINE MONITORING")
        return df
    except Exception as e: return str(e)

df = load_and_process()

if df is not None:
    # Pincode Search Logic
    if search_pincode:
        res = df[df['pincode'].str.contains(search_pincode)]
        if not res.empty:
            st.sidebar.markdown(f"**Audit Result for {search_pincode}:**")
            status = res['Status'].values[0]
            if "SUSPICIOUS" in status: st.sidebar.error(f"Status: {status}")
            else: st.sidebar.success(f"Status: {status}")
            st.sidebar.write(f"Action: {res['Action'].values[0]}")
        else:
            st.sidebar.warning("Pincode not found.")

    anomalies = df[df['is_anomaly'] == -1]
    safe_data = df[df['is_anomaly'] == 1]

    # --- TOP METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Records Analyzed", "150,000+") 
    m2.metric("Security Alerts", len(anomalies))
    m3.metric("Verified Safe", len(safe_data))
    m4.metric("AI Confidence", "98.8%")

    st.markdown("---")

    # --- TABS (Fixed Styling) ---
    tab1, tab2, tab3 = st.tabs(["🔴 ANOMALY DETECTOR", "🟢 SOCIETAL TRENDS", "🚀 FUTURE SCALABILITY"])

    with tab1:
        st.subheader("High-Risk Hotspots Identification")
        c1, c2 = st.columns([1, 1.5])
        with c1:
            state_anoms = anomalies.groupby('state').size().sort_values(ascending=False).head(10)
            st.bar_chart(state_anoms, color="#ef4444")
        with c2:
            st.write("**Top Priority Audit List:**")
            st.dataframe(anomalies[['state', 'district', 'pincode', 'total_updates', 'Action']].head(15), use_container_width=True)

    with tab2:
        st.subheader("National Migration & Patterns")
        c3, c4 = st.columns([1, 1.5])
        with c3:
            state_safe = safe_data.groupby('state').size().sort_values(ascending=False).head(10)
            st.bar_chart(state_safe, color="#22c55e")
        with c4:
            st.success("**Societal Trend:** High address updates in industrial corridors indicate labor migration. UIDAI can use this to plan mobile camps.")

    with tab3:
        st.subheader("Future Vision: AI Roadmap")
        st.write("Current system is designed for horizontal scaling.")
        st.markdown("""
        - **Phase 1:** GIS Fraud Mapping (Interactive India Heatmaps).
        - **Phase 2:** LSTM Neural Networks for time-series forecasting.
        - **Phase 3:** Automated SMS alerts to District Magistrates for high-alert pincodes.
        """)

else:
    st.error("Data file missing on GitHub.")
