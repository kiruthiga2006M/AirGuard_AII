import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

st.set_page_config(page_title='AirGuard AI', page_icon='🌍', layout='wide')
st.title('🌍 AirGuard AI')
st.subheader('Air Quality Analysis & Pollution Prediction')
st.caption('Prototype demo • Uses simulated sample data unless you connect a verified live data source.')

@st.cache_data
def make_data(city, days=30):
    rng = np.random.default_rng(sum(ord(c) for c in city))
    dates = [datetime.now().date() - timedelta(days=days-i-1) for i in range(days)]
    trend = np.linspace(0, 8, days)
    pm25 = np.clip(35 + trend + rng.normal(0, 9, days), 5, 150)
    pm10 = np.clip(pm25 * 1.65 + rng.normal(0, 12, days), 10, 250)
    no2 = np.clip(18 + rng.normal(0, 6, days), 3, 80)
    # A simple illustrative AQI proxy for demonstration, not an official regulatory AQI calculation.
    aqi = np.clip(pm25 * 2.0 + rng.normal(0, 5, days), 10, 300)
    return pd.DataFrame({'date': dates, 'PM2.5 (µg/m³)': pm25.round(1), 'PM10 (µg/m³)': pm10.round(1), 'NO₂ (µg/m³)': no2.round(1), 'AQI (demo estimate)': aqi.round(0).astype(int)})

def category(aqi):
    if aqi <= 50: return 'Good', '🟢'
    if aqi <= 100: return 'Moderate', '🟡'
    if aqi <= 150: return 'Unhealthy for sensitive groups', '🟠'
    if aqi <= 200: return 'Unhealthy', '🔴'
    if aqi <= 300: return 'Very unhealthy', '🟣'
    return 'Hazardous', '🟤'

with st.sidebar:
    st.header('Dashboard settings')
    city = st.selectbox('Choose location', ['Chennai', 'Coimbatore', 'Madurai', 'Bengaluru', 'Delhi', 'Mumbai'])
    pm25_input = st.slider('Illustrative current PM2.5 (µg/m³)', 0, 200, 48)
    pm10_input = st.slider('Illustrative current PM10 (µg/m³)', 0, 300, 82)
    no2_input = st.slider('Illustrative current NO₂ (µg/m³)', 0, 100, 24)
    st.caption('Move the sliders to test different pollution scenarios.')

df = make_data(city)
# Demo AQI proxy; do not present as an official AQI calculation.
current_aqi = int(np.clip(pm25_input * 2, 0, 400))
label, emoji = category(current_aqi)

c1, c2, c3, c4 = st.columns(4)
c1.metric('Demo AQI estimate', current_aqi, help='Simplified PM2.5-based estimate; not an official AQI calculation.')
c2.metric('PM2.5', f'{pm25_input} µg/m³')
c3.metric('PM10', f'{pm10_input} µg/m³')
c4.metric('NO₂', f'{no2_input} µg/m³')
st.info(f'{emoji} **{label}** — This is a demonstration indicator, not health advice or an official local reading.')

st.markdown('### 📈 Historical sample data')
st.line_chart(df.set_index('date')[['PM2.5 (µg/m³)', 'PM10 (µg/m³)']])
st.markdown('### 🤖 Short-term pollution trend (demo model)')
# Train a small model on the synthetic series. The forecast demonstrates the workflow only.
df['day_index'] = np.arange(len(df))
features = df[['day_index']]
model = RandomForestRegressor(n_estimators=80, random_state=42)
model.fit(features, df['PM2.5 (µg/m³)'])
future_days = np.arange(len(df), len(df)+7)
pred = model.predict(pd.DataFrame({'day_index': future_days}))
future_dates = [datetime.now().date() + timedelta(days=i+1) for i in range(7)]
forecast = pd.DataFrame({'Date': future_dates, 'Predicted PM2.5 (µg/m³) — demo': pred.round(1)})
st.line_chart(forecast.set_index('Date'))
st.dataframe(forecast, use_container_width=True, hide_index=True)
st.caption('The model is trained on generated sample data, so forecasts are not suitable for real-world decisions. Connect real, quality-controlled historical observations and validate the model before using it outside a demo.')

st.markdown('### 💡 Suggested actions')
if current_aqi > 150:
    st.warning('Demo alert: pollution indicator is high. Check an official local air-quality source before making outdoor activity decisions.')
elif current_aqi > 100:
    st.warning('Demo alert: elevated pollution indicator. Sensitive people may want to check official local guidance.')
else:
    st.success('Demo indicator is lower. Continue checking verified local readings, especially if conditions change.')

with st.expander('About this project'):
    st.write('AirGuard AI demonstrates an air-quality dashboard, pollutant comparisons, a sample prediction workflow, and threshold-based alerts. Current values are entered using sliders and the historical dataset is simulated. The AQI shown is a simplified demo estimate, not an official AQI calculation.')
