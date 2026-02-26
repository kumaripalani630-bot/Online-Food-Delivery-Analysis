# Online-Food-Delivery-Analysis
Online food orders
🍔 Online Food Delivery Analytics Project
Project Overview

This project provides a comprehensive analysis of online food delivery operations using a dataset of 100,000 orders. It focuses on understanding:

Customer behavior

Revenue trends

Delivery performance

Profit margins

Cancellation patterns

An interactive Streamlit dashboard is built for real-time KPI tracking and visualization.

Dataset Description

The dataset includes 100,000 orders with 32 columns, including:

Feature	Description
Order_ID	Unique order identifier
Customer_ID	Customer unique ID
Customer_Age	Customer age
Customer_Gender	Gender of customer
City, Area	Location information
Restaurant_ID, Restaurant_Name	Restaurant details
Cuisine_Type	Type of cuisine
Order_Date, Order_Time	Timestamp of order
Delivery_Time_Min	Delivery duration in minutes
Distance_km	Distance to customer
Order_Value, Final_Amount	Order and final prices
Discount_Applied	Discount applied (0 = no discount)
Payment_Mode	Mode of payment
Order_Status	Delivered / Cancelled / Pending
Delivery_Rating, Restaurant_Rating	Ratings
Profit_Margin	Profit margin in decimals
Peak_Hour, Order_Day_Type, etc.	Derived metrics

Source: Simulated and cleaned dataset suitable for real-world analysis.

Data Preprocessing

Missing values handled

Outliers treated

Inconsistent entries corrected

Derived metrics added:

Discount_Type (Discounted / No Discount)

Order_Day_Type (Weekday / Weekend)

Peak_Hour_Indicator (Peak / Off-Peak)

Python preprocessing example:

import pandas as pd
import numpy as np

# Load dataset
onlineorders = pd.read_csv("data/online_orders.csv")

# Create Discount Type
onlineorders['Discount_Type'] = np.where(onlineorders['Discount_Applied']==0, "No Discount", "Discounted")

# Example KPI calculations
total_orders = len(onlineorders)
total_revenue = onlineorders['Final_Amount'].sum()
avg_order_value = onlineorders['Order_Value'].mean()
avg_delivery_time = onlineorders['Delivery_Time_Min'].mean()
cancellation_rate = len(onlineorders[onlineorders['Order_Status']=="Cancelled"]) / total_orders * 100
avg_profit_margin = onlineorders['Profit_Margin'].mean() * 100

print(total_orders, total_revenue, avg_order_value, avg_delivery_time, cancellation_rate, avg_profit_margin)
Key Performance Indicators (KPIs)
KPI	Value
Total Orders	100,000
Total Revenue	₹ 151,268,398
Average Order Value	₹ 1,512.68
Average Delivery Time	124.98 mins
Cancellation Rate	15.04%
Average Delivery Rating	2.54 / 5
Profit Margin	17.88%
Exploratory Data Analysis (EDA)
1️⃣ Orders by Discount Type
import seaborn as sns
import matplotlib.pyplot as plt

sns.countplot(x='Discount_Type', data=onlineorders, palette='Set2')
plt.title("Orders: Discounted vs No Discount")
plt.show()

Insight: Majority of orders are discounted (~66% of total orders).

2️⃣ Revenue by Cuisine
revenue_by_cuisine = onlineorders.groupby('Cuisine_Type')['Final_Amount'].sum().sort_values(ascending=False)
sns.barplot(x=revenue_by_cuisine.index, y=revenue_by_cuisine.values, palette='Set3')
plt.xticks(rotation=45)
plt.title("Revenue by Cuisine Type")
plt.show()

Insight: Highest revenue comes from popular cuisines, indicating customer preference.

3️⃣ Average Delivery Time by City
avg_delivery_city = onlineorders.groupby('City')['Delivery_Time_Min'].mean()
sns.barplot(x=avg_delivery_city.index, y=avg_delivery_city.values, palette='Set1')
plt.xticks(rotation=45)
plt.title("Average Delivery Time per City")
plt.show()

Insight: Delivery time varies significantly across cities, highlighting operational inefficiencies.

4️⃣ Order Status Distribution
status_counts = onlineorders['Order_Status'].value_counts()
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%')
plt.title("Order Status Distribution")
plt.show()

Insight: Cancellation rate is ~15%, which is a key metric for operational improvement.

Streamlit Dashboard

Interactive dashboard features:

KPIs: Total Orders, Revenue, Avg Order Value, Delivery Time, Profit Margin

Filters: City, Cuisine, Order Status

Visualizations:

Orders by Discount Type

Revenue by Cuisine

Avg Delivery Time by City

Order Status Distribution

CSV download of filtered data

Run the dashboard:

pip install -r requirements.txt
streamlit run streamlit_dashboard.py
Dashboard Example

📊 Key Insights:

Discounted orders dominate revenue.

High-performing cuisines can be focused for promotions.

Cities with higher delivery time may need resource optimization.

Profit margins are ~18%, and cancellations are ~15%.

(Include screenshots of Streamlit dashboard here in images/ folder for GitHub)

Tech Stack

Python (Pandas, NumPy, Matplotlib, Seaborn)

Streamlit (Dashboard)

MySQL (Database)

SQLAlchemy (Python-MySQL interface)

Folder Structure
online-food-delivery-dashboard/
│
├── streamlit_dashboard.py
├── requirements.txt
├── README.md
├── data/
│   └── online_orders.csv
└── images/
