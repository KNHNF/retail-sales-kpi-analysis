import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import io

# PAGE CONFIG
st.set_page_config(
    page_title="Retail KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── STYLING ──
st.markdown("""
<style>
  .block-container { padding-top: 1.5rem; }
  .metric-card { background: #f8f9ff; border: 1px solid #e0e0f0; border-radius: 8px; padding: 1rem 1.25rem; }
  h1 { font-size: 1.6rem !important; }
  .stMetric label { font-size: 0.75rem !important; color: #666 !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA LOADING ──
@st.cache_data
def load_data(uploaded=None):
    if uploaded is not None:
        df = pd.read_csv(uploaded, encoding='latin-1')
    else:
        # Try loading from data/ folder (local dev)
        try:
            df = pd.read_csv('data/online_retail.csv', encoding='latin-1')
        except FileNotFoundError:
            return None

    # Clean
    df.columns = df.columns.str.strip()
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['CustomerID', 'InvoiceDate'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]  # remove cancellations
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
    df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    return df

# CHART STYLE
def set_style():
    plt.rcParams.update({
        'figure.facecolor': '#ffffff',
        'axes.facecolor': '#fafafa',
        'axes.edgecolor': '#dddddd',
        'axes.grid': True,
        'grid.color': '#eeeeee',
        'grid.linewidth': 0.6,
        'font.family': 'sans-serif',
        'axes.spines.top': False,
        'axes.spines.right': False,
    })

set_style()

# SIDEBAR
st.sidebar.header("📊 Retail KPI Dashboard")
st.sidebar.markdown("**Dataset:** Online Retail 2010–2011")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "Upload dataset CSV",
    type=['csv'],
    help="Download from Kaggle: 'Online Retail Dataset' by Ulrik Thyge Pedersen"
)

st.sidebar.markdown("""
**Don't have the file?**  
[Download from Kaggle ↗](https://www.kaggle.com/datasets/ulrikthygepedersen/online-retail-dataset)
""")

# LOAD 
df = load_data(uploaded_file)

if df is None:
    st.title("📊 Retail Sales KPI Dashboard")
    st.info("""
    **Upload the dataset to get started.**

    This dashboard analyses ~500K retail transactions (£10.6M revenue) across 38 countries.

    1. Download the dataset from Kaggle (link in sidebar)
    2. Upload the CSV using the sidebar uploader
    3. Explore the KPIs, trends, and product analysis

    **What you'll see:**
    - Monthly revenue trend with Q4 seasonality
    - Top 10 products and countries by revenue  
    - Data quality summary
    - Filterable transaction table
    """)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", "~£10.6M")
    col2.metric("Countries", "38")
    col3.metric("Transactions", "~400K (cleaned)")
    st.stop()

# FILTERS
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

months = sorted(df['Month'].unique())
all_countries = sorted(df['Country'].unique())

date_range = st.sidebar.select_slider(
    "Date range",
    options=months,
    value=(months[0], months[-1])
)

selected_countries = st.sidebar.multiselect(
    "Countries",
    options=all_countries,
    default=all_countries[:10] if len(all_countries) > 10 else all_countries
)

# Apply filters
mask = (df['Month'] >= date_range[0]) & (df['Month'] <= date_range[1])
if selected_countries:
    mask &= df['Country'].isin(selected_countries)
fdf = df[mask]

if fdf.empty:
    st.warning("No data for selected filters.")
    st.stop()

# HEADER 
st.title("📊 Retail Sales KPI Dashboard")
st.caption(f"Showing {len(fdf):,} transactions · {fdf['Month'].nunique()} months · {fdf['Country'].nunique()} countries")

# KPI ROW 
total_rev = fdf['Revenue'].sum()
total_orders = fdf['InvoiceNo'].nunique()
total_customers = fdf['CustomerID'].nunique()
avg_order = total_rev / total_orders if total_orders > 0 else 0
top_country = fdf.groupby('Country')['Revenue'].sum().idxmax()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Revenue", f"£{total_rev:,.0f}")
col2.metric("Orders", f"{total_orders:,}")
col3.metric("Customers", f"{total_customers:,}")
col4.metric("Avg Order Value", f"£{avg_order:,.2f}")
col5.metric("Top Country", top_country)

st.markdown("---")

# ROW 1: Monthly trend + Country breakdown
col_l, col_r = st.columns([3, 2])

with col_l:
    st.subheader("Monthly Revenue Trend")
    monthly = fdf.groupby('Month')['Revenue'].sum().reset_index()
    monthly = monthly.sort_values('Month')

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.fill_between(monthly['Month'], monthly['Revenue'], alpha=0.15, color='#6c63ff')
    ax.plot(monthly['Month'], monthly['Revenue'], color='#6c63ff', linewidth=2, marker='o', markersize=4)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x/1000:.0f}k'))
    ax.set_xlabel('')
    step = max(1, len(monthly) // 6)
    ax.set_xticks(monthly['Month'].iloc[::step])
    ax.set_xticklabels(monthly['Month'].iloc[::step], rotation=30, ha='right', fontsize=8)
    ax.tick_params(axis='y', labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_r:
    st.subheader("Revenue by Country (Top 10)")
    country_rev = fdf.groupby('Country')['Revenue'].sum().sort_values(ascending=True).tail(10)

    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.barh(country_rev.index, country_rev.values, color='#2dd4bf', edgecolor='none', height=0.6)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x/1000:.0f}k'))
    ax.tick_params(labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ROW 2: Top products + Data quality
col_l2, col_r2 = st.columns([3, 2])

with col_l2:
    st.subheader("Top 10 Products by Revenue")
    top_products = (
        fdf.groupby('Description')['Revenue']
        .sum()
        .sort_values(ascending=True)
        .tail(10)
    )

    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.barh(top_products.index, top_products.values, color='#a78bfa', edgecolor='none', height=0.6)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x/1000:.0f}k'))
    ax.tick_params(axis='y', labelsize=7.5)
    ax.tick_params(axis='x', labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_r2:
    st.subheader("Data Quality Summary")
    raw_count = len(df[df['Month'] >= date_range[0]])
    clean_count = len(fdf)
    cancelled = len(df[df['InvoiceNo'].astype(str).str.startswith('C')])

    st.markdown(f"""
    | Check | Value |
    |---|---|
    | Raw transactions | {raw_count:,} |
    | After cleaning | {clean_count:,} |
    | Cancellations removed | {cancelled:,} |
    | Countries | {fdf['Country'].nunique()} |
    | Unique products | {fdf['Description'].nunique():,} |
    | Unique customers | {fdf['CustomerID'].nunique():,} |
    | Date range | {fdf['Month'].min()} → {fdf['Month'].max()} |
    | Null CustomerIDs dropped | ✓ |
    | Negative quantities removed | ✓ |
    """)

# RAW DATA
with st.expander("View transaction sample (first 500 rows)"):
    st.dataframe(
        fdf[['InvoiceNo', 'Description', 'Quantity', 'UnitPrice', 'Revenue', 'Country', 'InvoiceDate']]
        .head(500)
        .reset_index(drop=True),
        use_container_width=True
    )

st.markdown("---")
st.caption("Data: Online Retail Dataset (UCI / Kaggle) · 2010–2011 · Built by Karan Homayounfar")
