import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail Sales & Business Insights", page_icon="📊", layout="wide")

st.title("📊 Retail Sales & Business Insights Dashboard")
st.caption("Explore retail performance, identify trends, and turn data into business decisions.")

@st.cache_data
def load_sample_data():
    df = pd.read_csv("sample_sales_data.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

uploaded_file = st.sidebar.file_uploader("Upload your sales CSV (optional)", type=["csv"])
try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        required = ["Order ID", "Order Date", "City", "Category", "Product", "Quantity", "Sales", "Profit"]
        missing = [col for col in required if col not in df.columns]
        if missing:
            st.error("CSV is missing required columns: " + ", ".join(missing))
            st.stop()
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    else:
        df = load_sample_data()
except FileNotFoundError:
    st.error("sample_sales_data.csv was not found. Add it to the same GitHub repository as app.py.")
    st.stop()

df = df.dropna(subset=["Order Date", "Sales", "Profit"])
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

st.sidebar.header("Filters")
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

cities = st.sidebar.multiselect("City", sorted(df["City"].dropna().unique()), default=sorted(df["City"].dropna().unique()))
categories = st.sidebar.multiselect("Category", sorted(df["Category"].dropna().unique()), default=sorted(df["Category"].dropna().unique()))

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df["Order Date"].dt.date >= start_date) &
    (df["Order Date"].dt.date <= end_date) &
    (df["City"].isin(cities)) &
    (df["Category"].isin(categories))
]

if filtered.empty:
    st.warning("No records match these filters. Try changing the selections.")
    st.stop()

total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_orders = filtered["Order ID"].nunique()
total_units = filtered["Quantity"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Sales", f"₹{total_sales:,.0f}")
c2.metric("Total Profit", f"₹{total_profit:,.0f}")
c3.metric("Orders", f"{total_orders:,}")
c4.metric("Units Sold", f"{total_units:,}")
c5.metric("Profit Margin", f"{profit_margin:.1f}%")

st.divider()
left, right = st.columns(2)
with left:
    monthly = filtered.groupby("Month", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    fig = px.line(monthly, x="Month", y=["Sales", "Profit"], markers=True, title="Monthly Sales & Profit Trend")
    st.plotly_chart(fig, use_container_width=True)
with right:
    category_sales = filtered.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(category_sales, x="Category", y="Sales", color="Category", title="Sales by Category")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    city_sales = filtered.groupby("City", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(city_sales, x="City", y="Sales", title="Sales by City", color="Sales")
    st.plotly_chart(fig, use_container_width=True)
with right:
    product_sales = filtered.groupby("Product", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).sort_values("Sales", ascending=False).head(10)
    fig = px.bar(product_sales, x="Sales", y="Product", orientation="h", title="Top 10 Products by Sales")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Business Insights")
best_category = category_sales.iloc[0]["Category"] if not category_sales.empty else "N/A"
best_city = city_sales.iloc[0]["City"] if not city_sales.empty else "N/A"
best_product = product_sales.iloc[0]["Product"] if not product_sales.empty else "N/A"
low_profit = filtered.groupby("Category")["Profit"].sum().sort_values()

insights = [
    f"**Leading category:** {best_category} contributes the highest sales in the selected data.",
    f"**Leading city:** {best_city} has the highest sales among the selected cities.",
    f"**Top product:** {best_product} is the best-selling product by sales value.",
]
if not low_profit.empty:
    insights.append(f"**Review opportunity:** {low_profit.index[0]} has the lowest total profit among the selected categories. Check its pricing and costs.")
for item in insights:
    st.markdown("- " + item)

st.subheader("Filtered Sales Data")
st.dataframe(filtered.sort_values("Order Date", ascending=False), use_container_width=True)
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", data=csv, file_name="filtered_sales_data.csv", mime="text/csv")

st.caption("Note: This project uses illustrative sample data. Replace it with verified business data before making real business decisions.")
