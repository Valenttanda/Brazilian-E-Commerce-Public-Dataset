import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from datetime import datetime

# Memuat data reviews_sales_df
df = pd.read_csv("reviews_sales_df.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

st.title("Dashboard Analisis Data E-Commerce Brazil")


# Menambah filter
st.sidebar.header("Filter Tanggal")
start_date = st.sidebar.date_input("Tanggal Awal", df["order_purchase_timestamp"].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", df["order_purchase_timestamp"].max().date())

start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.max.time())

filtered_df = df[(df["order_purchase_timestamp"] >= start_date) & (df["order_purchase_timestamp"] <= end_date)]

# Visualisasi pertanyaan 1
st.header("Jumlah Pemesan Terbanyak Berdasarkan Kota dan State")
sum_orders_city_df = filtered_df.groupby(by="customer_city").order_id.nunique().sort_values(ascending=False).reset_index()
sum_orders_state_df = filtered_df.groupby(by="customer_state").order_id.nunique().sort_values(ascending=False).reset_index()

sum_orders_city_df.rename(columns={
    "order_id": "sum_orders"
}, inplace=True)

sum_orders_state_df.rename(columns={
    "order_id": "sum_orders"
}, inplace=True)

## Visualisasi pemesan terbanyak berdasarkan kota
fig, ax= plt.subplots(figsize=(40,25))

sns.barplot(
    x="sum_orders",
    y="customer_city",
    data=sum_orders_city_df.sort_values(by="sum_orders", ascending=False).head(10),
    palette="pastel",
    ax=ax
)

ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Pemesan Terbanyak Berdasarkan Kota", loc="center", fontsize=40)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)
st.pyplot(fig)

## Visualisasi pemesan terbanyak berdasarkan state
fig, ax= plt.subplots(figsize=(40,25))
sns.barplot(
    x="sum_orders",
    y="customer_state",
    data=sum_orders_state_df.sort_values(by="sum_orders", ascending=False).head(10),
    palette="pastel",
    ax=ax
)

ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Pemesan Terbanyak Berdasarkan State", loc="center", fontsize=40)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)
st.pyplot(fig)

# Visualisasi pertanyaan 2
st.header("Produk yang Paling Banyak dan Paling Sedikit Dipesan")
most_orders_df = filtered_df.groupby(by=["product_category_name_english"]).order_id.nunique().sort_values(ascending=False).reset_index()
least_orders_df = filtered_df.groupby(by=["product_category_name_english"]).order_id.nunique().sort_values(ascending=True).reset_index()

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40,25))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="order_id",
    y="product_category_name_english",
    data=most_orders_df.head(5),
    palette=colors,
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk yang Paling Banyak Dipesan", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(
    x="order_id",
    y="product_category_name_english",
    data=least_orders_df.head(5),
    palette=colors,
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk yang Paling Sedikit Dipesan", loc="center", fontsize=40)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)
st.caption("Dibuat oleh: Mohammad Valeriant (MC-31)")