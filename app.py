import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title
st.title("📊 Business Sales Insights Dashboard")

# Load Data
df = pd.read_csv("E:\\Project\\sales_dashboard\\train.csv")

# Clean column names (remove spaces)
df.columns = df.columns.str.strip()

# Fix Date format
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors='coerce')

# Sidebar Filter
st.sidebar.title("🔍 Filters")
region = st.sidebar.selectbox("Select Region", df["Region"].dropna().unique())

# Filtered Data
filtered_df = df[df["Region"] == region]

# Show Data
st.subheader("📄 Dataset Preview")
st.write(filtered_df.head())

# Metrics
st.subheader("📊 Key Metrics")
col1, col2 = st.columns(2)

# Total Sales (safe)
if "Sales" in filtered_df.columns:
    col1.metric("Total Sales", int(filtered_df["Sales"].sum()))
else:
    col1.metric("Total Sales", "N/A")

# Total Profit (safe)
if "Profit" in filtered_df.columns:
    col2.metric("Total Profit", int(filtered_df["Profit"].sum()))
else:
    col2.metric("Total Profit", "Not Available")

# Sales by Category
if "Category" in filtered_df.columns and "Sales" in filtered_df.columns:
    st.subheader("📦 Sales by Category")
    fig, ax = plt.subplots()
    sns.barplot(x="Category", y="Sales", data=filtered_df, ax=ax)
    st.pyplot(fig)

# Monthly Trend
if "Order Date" in filtered_df.columns and "Sales" in filtered_df.columns:
    filtered_df["Month"] = filtered_df["Order Date"].dt.month

    st.subheader("📈 Monthly Sales Trend")
    fig2, ax2 = plt.subplots()
    sns.lineplot(x="Month", y="Sales", data=filtered_df, ax=ax2)
    st.pyplot(fig2)

# Top Products
if "Sub-Category" in filtered_df.columns and "Sales" in filtered_df.columns:
    top_products = (
        filtered_df.groupby("Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    st.subheader("🏆 Top 5 Products")
    st.bar_chart(top_products)