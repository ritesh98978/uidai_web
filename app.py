import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="UIDAI AI Dashboard", layout="wide")

st.title("🛡️ UIDAI AI-Powered Analytics Dashboard")
st.write("Developed by: **Prem Kumar Sah**")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("aadhaar_master_summary.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

try:
    df = load_data()

    # --- KPI Section ---
    st.markdown("### 📈 Key Intelligence Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric("Records Analyzed", f"{len(df):,}")
    m2.metric("AI Flagged Anomalies", len(df[df['is_anomaly'] == -1]))
    m3.metric("System Efficiency Score", f"{df['sat_score'].mean():.2f}%")

    # --- AI Anomaly Section ---
    st.markdown("---")
    st.subheader("🚨 AI Security Tool: Anomaly Detection")
    st.write("Our **Isolation Forest AI model** has identified the following suspicious activity patterns:")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.scatterplot(data=df, x='total_enrolment', y='total_updates', 
                    hue='is_anomaly', palette={1: 'blue', -1: 'red'}, alpha=0.6, ax=ax)
    plt.title("Red Dots = Suspicious Transactions Detected")
    st.pyplot(fig)

    # --- AI Prediction Section ---
    st.markdown("---")
    st.subheader("🔮 AI Predictive Planning: 30-Day Forecast")
    
    # Simple Prediction Logic for Website
    daily = df.groupby('date')['total_updates'].sum().reset_index()
    daily['day_num'] = np.arange(len(daily))
    
    X = daily[['day_num']]
    y = daily['total_updates']
    model = LinearRegression().fit(X, y)
    
    # Forecast
    future_days = np.array([len(daily) + i for i in range(30)]).reshape(-1, 1)
    preds = model.predict(future_days)
    
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    plt.plot(daily['date'], y, label='Current Load', color='blue', linewidth=2)
    plt.plot(pd.date_range(daily['date'].max(), periods=30), preds, label='AI Predicted Load', linestyle='--', color='red')
    plt.legend()
    plt.title("Predicted Aadhaar Service Demand (Next 30 Days)")
    st.pyplot(fig2)

    st.success("Analysis Complete: AI System is Operating Normally.")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Bhai, check karo ki 'aadhaar_master_summary.csv' file GitHub repo ke main page par hai.")