import streamlit as st
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Retail Sales & Profitability",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("Retail Sales & Profitability Dashboard")
st.write(
    "Interactive analysis of retail sales, profitability, "
    "regional performance and customer behaviour."
)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("data/merged.csv")

# Convert Order Date to datetime
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True,
    errors="coerce"
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Dashboard Filters")


# Category filter
category_options = sorted(
    df["Category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    category_options,
    default=category_options
)


# State filter
state_options = sorted(
    df["State"].dropna().unique()
)

selected_states = st.sidebar.multiselect(
    "Select State",
    state_options,
    default=state_options
)


# Date filter
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    df["Category"].isin(selected_categories)
    & df["State"].isin(selected_states)
]


if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date)
        & (filtered_df["Order Date"].dt.date <= end_date)
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["Amount"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()

if total_sales != 0:
    profit_margin = (
        total_profit / total_sales
    ) * 100
else:
    profit_margin = 0


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "Total Profit",
    f"₹{total_profit:,.0f}"
)

col3.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)

col4.metric(
    "Total Orders",
    f"{total_orders:,}"
)


# =========================================================
# CATEGORY + SUB-CATEGORY
# =========================================================

col1, col2 = st.columns(2)


# -------------------------
# CATEGORY
# -------------------------

with col1:

    st.subheader("Sales & Profit by Category")

    category_summary = (
        filtered_df
        .groupby("Category")
        .agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum")
        )
        .reset_index()
    )

    st.bar_chart(
        category_summary.set_index("Category")[
            ["Total_Sales", "Total_Profit"]
        ]
    )


# -------------------------
# SUB-CATEGORY
# -------------------------

with col2:

    st.subheader("Profitability by Sub-Category")

    subcategory_summary = (
        filtered_df
        .groupby("Sub-Category")
        .agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum")
        )
        .reset_index()
    )

    subcategory_summary["Profit_Margin (%)"] = (
        subcategory_summary["Total_Profit"]
        / subcategory_summary["Total_Sales"]
    ) * 100

    subcategory_summary = (
        subcategory_summary
        .sort_values("Profit_Margin (%)")
    )

    st.bar_chart(
        subcategory_summary.set_index("Sub-Category")[
            "Profit_Margin (%)"
        ]
    )


# =========================================================
# STATE + MONTHLY TREND
# =========================================================

col1, col2 = st.columns(2)


# -------------------------
# STATE PERFORMANCE
# -------------------------

with col1:

    st.subheader("State-wise Sales & Profit")

    state_summary = (
        filtered_df
        .groupby("State")
        .agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values(
            "Total_Profit",
            ascending=False
        )
    )

    st.bar_chart(
        state_summary.set_index("State")[
            ["Total_Sales", "Total_Profit"]
        ]
    )


# -------------------------
# MONTHLY PROFIT MARGIN
# -------------------------

with col2:

    st.subheader("Monthly Profit Margin Trend")

    monthly_trend = (
        filtered_df
        .groupby(
            pd.Grouper(
                key="Order Date",
                freq="MS"
            )
        )
        .agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum")
        )
        .reset_index()
    )

    monthly_trend["Profit_Margin (%)"] = (
        monthly_trend["Total_Profit"]
        / monthly_trend["Total_Sales"]
    ) * 100

    st.line_chart(
        monthly_trend.set_index("Order Date")[
            "Profit_Margin (%)"
        ]
    )


# =========================================================
# ORDER SIZE ANALYSIS
# =========================================================

st.subheader("Profit Margin by Order Size")

order_size_summary = (
    filtered_df
    .groupby(
        "Order_Size",
        observed=True
    )
    .agg(
        Total_Sales=("Amount", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .reset_index()
)

order_size_summary["Profit_Margin (%)"] = (
    order_size_summary["Total_Profit"]
    / order_size_summary["Total_Sales"]
) * 100

st.bar_chart(
    order_size_summary.set_index("Order_Size")[
        "Profit_Margin (%)"
    ]
)


# =========================================================
# CUSTOMER ANALYSIS
# =========================================================

st.subheader("Repeat vs One-Time Customers")

customer_summary = (
    filtered_df
    .groupby("Customer_Type")
    .agg(
        Total_Sales=("Amount", "sum"),
        Total_Profit=("Profit", "sum"),
        Customers=("CustomerName", "nunique")
    )
    .reset_index()
)

customer_summary["Profit_Margin (%)"] = (
    customer_summary["Total_Profit"]
    / customer_summary["Total_Sales"]
) * 100

st.bar_chart(
    customer_summary.set_index("Customer_Type")[
        ["Total_Sales", "Total_Profit"]
    ]
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Retail Sales & Profitability Analysis | "
    "Built with Python, Pandas and Streamlit"
)