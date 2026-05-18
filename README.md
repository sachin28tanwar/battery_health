# Battery Health Analytics Dashboard 🔋

A modern, interactive Streamlit dashboard for analyzing battery health data and predicting battery condition.

## Features

- **Overview**: Get a quick glance at the average voltage, temperature, charge cycles, charging duration, and an overall battery health score.
- **Dataset**: View and analyze the uploaded raw battery data along with descriptive statistics.
- **Graphs**: Compare the actual battery performance metrics (voltage, temperature, cycles) against an ideal battery profile using interactive Plotly charts.
- **Predictor**: Use sliders to input custom battery parameters and instantly predict the battery health score.
- **Insights**: Receive automated recommendations and alerts based on the uploaded battery data (e.g., temperature warnings, voltage stability).

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sachin28tanwar/battery_health.git
   cd battery_health
   ```

2. Install the required dependencies:
   ```bash
   pip install streamlit pandas plotly
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the provided local URL in your web browser.
3. Upload a CSV file containing your battery data. The CSV must contain the following columns (or similar variations):
   - Voltage
   - Temperature
   - Charge Cycles
   - Current
   - Charging Duration

## Example Data

A sample `battery_data.csv` is included in this repository to test the dashboard's features immediately.
