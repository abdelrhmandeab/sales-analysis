# 1. Load your trained XGBoost model (saved during training)
import joblib
model = joblib.load('xgb_sales_model.pkl')   # or whatever name you used

# 2. Take the LAST known monthly row (August 2018) — this is our starting point
# This row contains all the features the model expects
last_row = monthly.iloc[-1]  # monthly is your final aggregated dataframe

# Example of what last_row looks like (August 2018):
# sales                957k
# sales_lag_1          923k   (July sales)
# sales_lag_2          937k   (June sales)
# sales_lag_3          926k   (May sales)
# rolling_3            928k
# qty_lag_1            68,000
# price_lag_1          120
# freight_lag_1         18.5
# review_lag_1          4.1
# is_holiday               0
# month                    8
# year                  2018

# 3. Extract only the feature columns (in the exact order the model was trained on)
feature_columns = ['sales_lag_1', 'sales_lag_2', 'sales_lag_3',
                   'rolling_3', 'qty_lag_1', 'price_lag_1',
                   'freight_lag_1', 'review_lag_1', 'is_holiday']

current_features = last_row[feature_columns].values  # → numpy array of 9 values

# 4. Start forecasting 12 future months (Sep 2018 → Sep 2019)
forecasts = []
future_dates = []

current_year = 2018
current_month = 9  # We start predicting from September 2018

for i in range(13):  # 13 points = Sep 2018 to Sep 2019 (matches your dashboard)
    
    # Predict next month's sales
    predicted_sales = model.predict([current_features])[0]
    forecasts.append(predicted_sales)
    
    # Save the date
    future_dates.append(f"{current_year}-{current_month:02d}")
    
    # UPDATE LAGS for the next prediction (this is the key!)
    # Shift everything one step back
    current_features[0] = current_features[1]   # lag_2 → lag_1
    current_features[1] = current_features[2]   # lag_3 → lag_2
    current_features[2] = predicted_sales       # new prediction → lag_3
    
    # Update rolling mean (simple approximation)
    if i >= 2:
        current_features[3] = (current_features[0] + current_features[1] + current_features[2]) / 3
    
    # Update holiday flag (Black Friday = Nov, Christmas = Dec, New Year = Jan)
    if current_month in [11, 12, 1]:
        current_features[8] = 1   # is_holiday = True
    else:
        current_features[8] = 0   # is_holiday = False
    
    # Move to next month
    current_month += 1
    if current_month > 12:
        current_month = 1
        current_year += 1

# 5. Print the final result — these are the EXACT numbers in your Streamlit app!
result = pd.DataFrame({
    'date': future_dates,
    'predicted_sales': forecasts
})

print(result.round(2))