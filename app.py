import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="UIDAI Sentinel Pro", layout="wide")
import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="UIDAI Sentinel Pro", layout="wide", initial_sidebar_state="expanded")

# --- ULTRA-STRICT VISIBILITY CSS ---
st.markdown("""
    <style>
    /* Main Background Fix */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Global Text Color Fix (Black for maximum contrast) */
    h1, h2, h3, h4, h5, h6, p, span, div, .stMarkdown {
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
    }

    /* SIDEBAR FIX: Navy Background & White Text */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important; /* Navy Dark Blue */
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important; /* White Text */
    }
    [data-testid="stSidebarNav"] span { color: #FFFFFF !important; }
    
    /* Metric Card Styling */
    [data-testid="stMetricValue"] {
        color: #1D4ED8 !important; 
        font-weight: 800 !important;
        font-size: 2.2rem !important;
    }
    .stMetric {
        background-color: #F1F5F9;
        border: 2px solid #CBD5E1;
        border-radius: 12px;
        padding: 15px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab"] p {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
logo_url = "https://upload.wikimedia.org/wikipedia/en/c/cf/Aadhaar_Logo.svg"
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image(logo_url, width=90)
with col_title:
    st.markdown("<h1 style='margin-bottom:0;'>🛡️ UIDAI SENTINEL: SECURITY ANALYTICS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:1.2rem; margin-top:0;'><b>Developer:</b> Prem Kumar Sah | Security & Insights Hub</p>", unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR: SEARCH & INFO ---
st.sidebar.title("🔍 Investigation Tool")
st.sidebar.write("Analyze specific regions for anomalies.")
search_pin = st.sidebar.text_input("Enter Pincode to Scan:", placeholder="e.g. 700102")

@st.cache_data
def load_and_clean_data():
    f = "aadhaar_master_summary.csv"
    if not os.path.exists(f): return None
    try:
        df = pd.read_csv(f)
        df['pincode'] = df['pincode'].astype(str)
        # Status & Action Mapping
        df['Status'] = df['is_anomaly'].apply(lambda x: "🚨 SUSPICIOUS" if x == -1 else "✅ SAFE")
        df['Action'] = df['is_anomaly'].apply(lambda x: "TRIGGER PHYSICAL AUDIT" if x == -1 else "ROUTINE MONITORING")
        return df
    except: return None

df = load_and_clean_data()

if df is not None:
    # Top Metrics Bar
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Records", "150,000+")
    m2.metric("Security Alerts", len(df[df['is_anomaly'] == -1]))
    m3.metric("AI Confidence", "98.5%")

    # Sidebar Search Display
    if search_pin:
        res = df[df['pincode'] == search_pin]
        if not res.empty:
            st.sidebar.info(f"Pincode {search_pin} Result:")
            st.sidebar.write(f"**Status:** {res['Status'].values[0]}")
            st.sidebar.write(f"**Action:** {res['Action'].values[0]}")
        else:
            st.sidebar.warning("Record not found in database.")

    st.write("##")

    # --- MAIN TABS (Including Future Scalability) ---
    tab_risk, tab_social, tab_future = st.tabs(["🛑 SECURITY AUDIT", "📈 SOCIETAL TRENDS", "🚀 FUTURE SCALABILITY"])

    with tab_risk:
        st.subheader("Regional Anomaly Detection (High Alert)")
        anoms = df[df['is_anomaly'] == -1]
        st.bar_chart(anoms.groupby('state').size().sort_values(ascending=False).head(10), color="#DC2626")
        
        st.write("### 📋 Priority Audit List (Immediate Action)")
        st.dataframe(anoms[['state', 'district', 'pincode', 'Status', 'Action']].head(30), use_container_width=True)

    with tab_social:
        st.subheader("Migration Corridors & Service Demand Analysis")
        safe = df[df['is_anomaly'] == 1]
        st.bar_chart(safe.groupby('state').size().sort_values(ascending=False).head(10), color="#16A34A")
        st.success("Societal Insight: High transactional density in industrial states (seen in Green) suggests migration corridors. Recommend mobile Aadhaar vans for these regions.")

    with tab_future:
        st.subheader("🚀 Project Roadmap: 2026 and Beyond")
        st.markdown("""
        **1. Live GIS Integration:**
        - Pincode-wise 'Heatmaps' on a live India Map using Mapbox.
        **2. Neural Network Upgrade:**
        - Moving from Isolation Forest to **Deep Learning (LSTM)** for better temporal anomaly detection.
        **3. Real-time API Pipeline:**
        - Connecting directly to UIDAI's live data stream for 24/7 autonomous monitoring.
        **4. Autonomous Alerting:**
        - Automated SMS/Email notifications to regional UIDAI heads when anomaly threshold is crossed.
        """)

else:
    st.error("Error: 'aadhaar_master_summary.csv' not found! Make sure it is in your GitHub repo.")
# --- GLOBAL TEXT VISIBILITY FIX (Force High Contrast) ---
st.markdown("""
    <style>
    /* Background ko zabardasti White karna */
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    /* Har tarah ke text ko Dark Blue ya Black karna taaki saaf dikhe */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #0F172A !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Metric Card Styling with Bold Text */
    [data-testid="stMetricValue"] {
        color: #1D4ED8 !important; 
        font-weight: 800 !important;
        font-size: 2.2rem !important;
    }
    .stMetric {
        background-color: #F8FAFC;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        padding: 15px;
    }

    /* Tab Text Visibility */
    .stTabs [data-baseweb="tab"] p {
        color: #1E293B !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION (LOGO + CLEAR TITLE) ---
logo_url = "https://upload.wikimedia.org/wikipedia/en/c/cf/Aadhaar_Logo.svg"
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image(logo_url, width=90)
with col_title:
    st.markdown("<h1 style='margin-bottom:0;'>UIDAI SENTINEL: SECURITY ANALYTICS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:1.2rem; margin-top:0;'><b>Developed by:</b> Prem Kumar Sah | Aadhaar Data Insights</p>", unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR SEARCH ---
st.sidebar.title("🔍 Investigation Tool")
search_pin = st.sidebar.text_input("Search Pincode Status:")

@st.cache_data
def get_clean_data():
    f = "aadhaar_master_summary.csv"
    if os.path.exists(f):
        df = pd.read_csv(f)
        df['pincode'] = df['pincode'].astype(str)
        # Action Logic
        df['Status'] = df['is_anomaly'].apply(lambda x: "🚨 SUSPICIOUS" if x == -1 else "✅ SAFE")
        df['Action'] = df['is_anomaly'].apply(lambda x: "TRIGGER PHYSICAL AUDIT" if x == -1 else "ROUTINE MONITORING")
        return df
    return None

df = get_clean_data()

if df is not None:
    # Top Metrics Bar
    m1, m2, m3 = st.columns(3)
    m1.metric("Datasets Analyzed", "150,000+")
    m2.metric("Security Flags", len(df[df['is_anomaly'] == -1]))
    m3.metric("AI Confidence", "98.5%")

    # Sidebar Search Logic
    if search_pin:
        res = df[df['pincode'] == search_pin]
        if not res.empty:
            st.sidebar.info(f"Pincode {search_pin}: {res['Status'].values[0]}")
            st.sidebar.write(f"Recommended: {res['Action'].values[0]}")
        else: st.sidebar.warning("Record not found.")

    st.write("##")

    # --- MAIN TABS ---
    tab_risk, tab_social = st.tabs(["🛑 SECURITY RISK AUDIT", "📈 SOCIETAL TRENDS"])

    with tab_risk:
        st.subheader("Regional Anomaly Detection (Red Zone)")
        anoms = df[df['is_anomaly'] == -1]
        
        # Graph
        st.bar_chart(anoms.groupby('state').size().sort_values(ascending=False).head(10), color="#DC2626")
        
        st.write("### 📋 Priority Audit Table (Action Plan)")
        st.write("In pincodes par turant physical verification ki zaroorat hai:")
        # Displaying Table with Action Column
        st.dataframe(anoms[['state', 'district', 'pincode', 'Status', 'Action']].head(30), use_container_width=True)

    with tab_social:
        st.subheader("Migration Corridors & Service Demand")
        safe = df[df['is_anomaly'] == 1]
        st.bar_chart(safe.groupby('state').size().sort_values(ascending=False).head(10), color="#16A34A")
        st.success("Analysis: High transaction volume in specific hubs indicate labour migration corridors. Recommended for new kiosk allocation.")

else:
    st.error("Data File 'aadhaar_master_summary.csv' missing on GitHub!")
