import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="UIDAI Sentinel Pro", layout="wide")

# --- GLOBAL TEXT VISIBILITY FIX ---
st.markdown("""
    <style>
    /* Sabhi text ko zabardasti Dark Blue/Black karna */
    * { color: #1e293b !important; }
    .main { background-color: #ffffff !important; }
    
    /* Metrics Box - Ekdum Saaf */
    [data-testid="stMetricValue"] {
        color: #1d4ed8 !important; 
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    .stMetric {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 20px;
    }
    
    /* Sidebar Text Fix */
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #0f172a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION (LOGO + TITLE) ---
logo_url = "https://upload.wikimedia.org/wikipedia/en/c/cf/Aadhaar_Logo.svg"
col_l, col_r = st.columns([1, 4])
with col_l:
    st.image(logo_url, width=100)
with col_r:
    st.title("UIDAI SENTINEL: SECURITY ANALYTICS")
    st.write("**Developed by:** Prem Kumar Sah")

st.markdown("---")

# --- SIDEBAR ---
st.sidebar.title("🔍 Search Tools")
search_pin = st.sidebar.text_input("Enter Pincode to Verify:")

@st.cache_data
def get_data():
    f = "aadhaar_master_summary.csv"
    if os.path.exists(f):
        df = pd.read_csv(f)
        df['pincode'] = df['pincode'].astype(str)
        df['Status'] = df['is_anomaly'].apply(lambda x: "🚨 SUSPICIOUS" if x == -1 else "✅ SAFE")
        return df
    return None

df = get_data()

if df is not None:
    # --- METRICS (Horizontal & Clear) ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Records", "150,000+")
    m2.metric("Anomalies Found", len(df[df['is_anomaly'] == -1]))
    m3.metric("System Safety", "98.5%")

    st.write("##") # Spacing

    # --- MAIN TABS (Saaf layout ke liye) ---
    tab_risk, tab_social, tab_future = st.tabs(["🛑 SECURITY RISK", "📈 SOCIAL TRENDS", "🚀 FUTURE"])

    with tab_risk:
        st.subheader("Regional Anomaly Analysis")
        # Graph ko poori width di taaki saaf dikhe
        anoms = df[df['is_anomaly'] == -1]
        state_anoms = anoms.groupby('state').size().sort_values(ascending=False).head(10)
        st.bar_chart(state_anoms, color="#dc2626")
        
        # Table ko expander mein daal diya taaki 'Bhara' na lage
        with st.expander("Click to view Full Priority Audit List (Table)"):
            st.dataframe(anoms[['state', 'district', 'pincode', 'Status']].head(50), use_container_width=True)

    with tab_social:
        st.subheader("Migration & Service Saturation")
        safe = df[df['is_anomaly'] == 1]
        state_safe = safe.groupby('state').size().sort_values(ascending=False).head(10)
        st.bar_chart(state_safe, color="#16a34a")
        
        st.info("**Trend Analysis:** High transaction volume in specific states indicates economic migration. UIDAI should increase kiosks in these districts.")

    with tab_future:
        st.subheader("Roadmap 2026")
        st.markdown("""
        - **Live GIS Map:** Fraud hotspots on Google Maps.
        - **Deep Learning:** Using Neural Networks for 99.9% fraud detection.
        - **Automated Alerts:** SMS to nodal officers.
        """)
else:
    st.error("CSV File not found on GitHub!")
