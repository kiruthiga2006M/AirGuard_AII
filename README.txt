AIRGUARD AI — QUICK START

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open Terminal > New Terminal.
4. (Windows) Run:
   py -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   streamlit run app.py

   If `py` is unavailable, use `python` instead.

5. A browser tab should open with the dashboard.

NOTE
This is a rapid demonstration prototype. The historical data is simulated and the forecast is trained on that simulated data. The AQI is only a simplified PM2.5-based demo estimate, not an official AQI calculation. Do not use the displayed values for health or safety decisions. For a real project, connect verified live air-quality data, use official AQI methodology for your region, and evaluate forecasts against held-out real observations.
