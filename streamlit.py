import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Future Sales Forecast Dashboard")

data = {
    "year":  [2018, 2018, 2018, 2018, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019],
    "month": [9,    10,   11,   12,   1,    2,    3,    4,    5,    6,    7,    8,    9   ],
    "predicted_sales": [
        940100.9375, 926625.6875, 937185.3125, 923155.6875,
        873438.6875, 852133.4375, 880764.3125, 881573.1875,
        888721.5625, 874418.4375, 876659.9375, 894834.3125,
        925460.9375
    ]
}

df = pd.DataFrame(data)
df["date"] = df["year"].astype(str) + "-" + df["month"].astype(str)
df_display = df[["date", "predicted_sales"]]

col1, col2 = st.columns([4, 3])   # ⬅️ أكبر يسار (الرسم) وأصغر يمين (الجدول)

with col1:
    st.subheader("📈 Predicted Sales Over Time")
    plt.figure(figsize=(8, 5))    # ⬅️ حجم أفضل
    plt.plot(df_display["date"], df_display["predicted_sales"], marker="o")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

with col2:
    st.subheader("📋 Forecasted Sales Data")
    st.dataframe(df_display, height=350)   # ⬅️ حجم مناسب
