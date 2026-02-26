# streamlit_food_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="🍔 Food Delivery Dashboard", layout="wide")
st.title("🍔 Online Food Delivery Dashboard")

# -----------------------------
# Database Connection
# -----------------------------
engine = create_engine("mysql+pymysql://root:shivanika@localhost:3306/food_delivery")

@st.cache_data
def load_data():
    query = "SELECT * FROM online_orders"
    df = pd.read_sql(query, engine)
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

city_filter = st.sidebar.multiselect(
    "Select City",
    options=df["City"].unique(),
    default=df["City"].unique()
)

cuisine_filter = st.sidebar.multiselect(
    "Select Cuisine",
    options=df["Cuisine_Type"].unique(),
    default=df["Cuisine_Type"].unique()
)

status_filter = st.sidebar.multiselect(
    "Order Status",
    options=df["Order_Status"].unique(),
    default=df["Order_Status"].unique()
)

# Apply filters
filtered_df = df[
    (df["City"].isin(city_filter)) &
    (df["Cuisine_Type"].isin(cuisine_filter)) &
    (df["Order_Status"].isin(status_filter))
]

# -----------------------------
st.markdown("📊 Key Performance Indicators")
# -----------------------------
total_orders = filtered_df.shape[0]
total_revenue = filtered_df["Final_Amount"].sum()
avg_order_value = filtered_df["Final_Amount"].mean()
avg_delivery_time = filtered_df["Delivery_Time_Min"].mean()
cancellation_rate = (
    filtered_df[filtered_df["Order_Status"] == "Cancelled"].shape[0]
    / total_orders * 100
)
avg_delivery_rating = filtered_df["Delivery_Rating"].mean()
profit_margin = filtered_df["Profit_Margin"].mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
col3.metric("Avg Order Value", f"₹ {avg_order_value:.2f}")
col4.metric("Avg Delivery Time", f"{avg_delivery_time:.2f} mins")

col5, col6, col7 = st.columns(3)
col5.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
col6.metric("Avg Delivery Rating", f"{avg_delivery_rating:.2f}/5")
col7.metric("Profit Margin %", f"{profit_margin:.2f}%")

st.markdown("---")

# -----------------------------
# Charts
# -----------------------------

# 1️⃣ Orders by Discount Type
st.subheader("Orders by Discount Type")
filtered_df['Discount_Type'] = np.where(
    filtered_df['Discount_Applied'] == 0, "No Discount", "Discounted"
)
discount_counts = filtered_df['Discount_Type'].value_counts()

fig1, ax1 = plt.subplots()
sns.barplot(x=discount_counts.index, y=discount_counts.values, palette="Set2", ax=ax1)
ax1.set_ylabel("Number of Orders")
ax1.set_title("Orders: Discounted vs No Discount")
st.pyplot(fig1)

# 2️⃣ Revenue by Cuisine
st.subheader("Revenue by Cuisine")
cuisine_revenue = filtered_df.groupby("Cuisine_Type")["Final_Amount"].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(10,4))
sns.barplot(x=cuisine_revenue.index, y=cuisine_revenue.values, palette="Set3", ax=ax2)
ax2.set_ylabel("Revenue (₹)")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
ax2.set_title("Total Revenue by Cuisine")
st.pyplot(fig2)

# 3️⃣ Distance vs Delivery Time
st.subheader("Distance vs Delivery Time")
fig3, ax3 = plt.subplots()
sns.scatterplot(x=filtered_df["Distance_km"], y=filtered_df["Delivery_Time_Min"], alpha=0.6, ax=ax3)
ax3.set_xlabel("Distance (km)")
ax3.set_ylabel("Delivery Time (min)")
ax3.set_title("Distance vs Delivery Time")
st.pyplot(fig3)

# 4️⃣ Order Status Distribution
st.subheader("Order Status Distribution")
status_counts = filtered_df["Order_Status"].value_counts()

fig4, ax4 = plt.subplots()
ax4.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2"))
ax4.set_title("Order Status Distribution")
st.pyplot(fig4)

# -----------------------------
# Download Filtered Data
# -----------------------------
st.markdown("---")
st.subheader("⬇ Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_online_orders.csv",
    mime="text/csv"
)

# -----------------------------
# Dashboard Creator Info
# -----------------------------
st.markdown("---")
st.subheader("👩‍💻 Dashboard Creator")
st.write("""
**Project:** Online Food Delivery Analytics Dashboard  
**Developer:** Palanikumari  
**Tools:** Python, Streamlit, MySQL, Pandas, Matplotlib, Seaborn  
**Features:** KPI Monitoring, Revenue Trends, Delivery Insights, Interactive Filters  
""")