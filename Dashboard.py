import streamlit as st
import pandas as pd
import sqlalchemy
import time
import altair as alt

# --- Config ---
st.set_page_config(page_title="Aegis Dashboard", page_icon="🛡️", layout="wide")
DATABASE_URL = "sqlite:///./aegis.db"
engine = sqlalchemy.create_engine(DATABASE_URL)

st.title("🛡️ Aegis: Live Fraud Monitor (Advanced)")

# --- Auto-Refresh Logic ---
placeholder = st.empty()

while True:
    try:
        # 1. Fetch recent data
        # नया डेटाबेस स्कीमा अपने आप नए कॉलम्स (hour, frequency) ले आएगा
        query = "SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 200"
        df = pd.read_sql(query, engine)
        
        if not df.empty:
            # 2. Process Data
            df['status'] = df['prediction'].apply(lambda x: 'BLOCKED' if x == -1 else 'APPROVED')
            
            total_txns = len(df)
            fraud_txns = len(df[df['status'] == 'BLOCKED'])
            fraud_rate = (fraud_txns / total_txns) * 100 if total_txns > 0 else 0
            
            with placeholder.container():
                # 3. KPI Metrics
                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric("Recent Transactions", total_txns)
                kpi2.metric("Fraud Detected", fraud_txns)
                kpi3.metric("Fraud Rate", f"{fraud_rate:.1f}%")
                
                # 4. Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Transaction Analysis")
                    # अपडेटेड चार्ट: Tooltip में नए फीचर्स भी दिखाएं
                    chart = alt.Chart(df).mark_circle(size=60).encode(
                        x='timestamp',
                        y='amount',
                        color=alt.Color('status', scale=alt.Scale(domain=['APPROVED', 'BLOCKED'], range=['green', 'red'])),
                        tooltip=['amount', 'distance_km', 'hour', 'frequency', 'status']
                    ).interactive()
                    st.altair_chart(chart, use_container_width=True)
                    
                with col2:
                    st.subheader("Recent Logs (Live)")
                    # अपडेटेड टेबल: नए कॉलम्स (Hour, Frequency) को डिस्प्ले में शामिल किया
                    display_cols = ['timestamp', 'amount', 'distance_km', 'hour', 'frequency', 'status']
                    # अगर पुराने डेटाबेस में ये कॉलम नहीं हैं तो एरर से बचने के लिए चेक
                    cols_to_show = [c for c in display_cols if c in df.columns]
                    st.dataframe(df[cols_to_show].head(15))
        else:
            with placeholder.container():
                st.warning("Waiting for data... Start the 'simulation/producer.py' script.")
                
        time.sleep(1) # तेज़ रिफ्रेश के लिए 1 सेकंड

    except Exception as e:
        # अगर डेटाबेस लॉक है या कनेक्ट नहीं हो पा रहा
        with placeholder.container():
            st.error(f"Database connecting... ({e})")
        time.sleep(2)