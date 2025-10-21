# By Yash Vaswani (Project-AI Finance Advisor)

#TO VISIT DASHBOARD RUN - streamlit run app.py
#demo user name=admin,,password=123#

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import streamlit as st
import pandas as pd

# User authentication
users = {"admin": "123#", "user": "123*"}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password( Demo user=admin,123*=123#)")
    st.stop()

# Properly call set_page_config with parentheses and arguments:
st.set_page_config(
    page_title="AI Finance Advisor",
    page_icon="📒",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        background-color: #f4f4f4 !important;
        color: #2e2e2e !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Buttons */
    .stButton > button {
        background-color: #5a5a5a !important;
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }

    .stButton > button:hover {
        background-color: #3f3f3f !important;
        color: #ffffff !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #e0e0e0 !important;
        color: #2e2e2e !important;
        border-right: 1px solid #cccccc;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #2e2e2e !important;
    }

    /* Widgets */
    .stTextInput > div > div > input,
    .stSelectbox > div,
    .stSlider,
    .stRadio > div {
        background-color: #ffffff !important;
        color: #2e2e2e !important;
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
    }

    /* Markdown text container */
    .markdown-text-container {
        background-color: #fafafa;
        padding: 1rem;
        border-radius: 5px;
    }

    /* Padding and layout */
    .block-container {
        padding: 2rem 4rem;
    }
    </style>
@media (max-width: 768px) {
    .block-container {
        padding: 1rem !important;
    }
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align: center; color: #2e2e2e;'>📊 AI Personal Finance Advisor</h1>
    """,
    unsafe_allow_html=True
)

   # Load your dataset
df = pd.read_csv(r"C:\Users\Admin\Documents\AI Personal Finance Advisor\Data\Economic Data.csv")  # Make sure this path is correct

# Show the data
st.subheader("📊 Economic Data Preview")
st.dataframe(df.head())

# Suggest top 5 investments by average return if available
if 'Return' in df.columns and 'Ticker' in df.columns:
    st.subheader("💡 Top 5 Investment Suggestions")
    top_stocks = df.groupby("Ticker")['Return'].mean().sort_values(ascending=False).head(10)
    st.table(top_stocks)
else:
    st.info("Note: Add 'Return' and 'Ticker' columns in your dataset for suggestions.")
import streamlit as st
import pandas as pd

# Load your dataset
df = pd.read_csv(r"C:\Users\Admin\Documents\AI Personal Finance Advisor\Data\Economic Data.csv")

# Show data preview
st.write("### 📊 Economic Data Preview")
st.dataframe(df)
import streamlit as st
import pandas as pd

# Load your dataset
df = pd.read_csv(r"C:\Users\Admin\Documents\AI Personal Finance Advisor\Data\Economic Data.csv")

st.write("Summary Statistics:")
st.write(df.describe())

st.write("Available columns:", df.columns.tolist())

metric = st.selectbox(
    "Select a metric to visualize:",
    df.columns[2:]  # Skips 'Date' if it's the first column
)

st.line_chart(df["GDP Growth (%)"])
# --- Financial Suggestions with Visuals ---
st.header("📊 Financial Suggestions Based on Economic Indicators")
st.markdown("---")

latest_data = df.iloc[-1]  # Get the most recent data row

# Extract key indicators
gdp = latest_data["GDP Growth (%)"]
inflation = latest_data["Inflation Rate (%)"]
unemployment = latest_data["Unemployment Rate (%)"]
interest_rate = latest_data["Interest Rate (%)"]

# Visual suggestion logic
st.subheader("📈 Economic Overview:")

col1, col2 = st.columns(2)

with col1:
    st.metric("GDP Growth (%)", f"{gdp:.2f}")
    st.metric("Inflation Rate (%)", f"{inflation:.2f}")
with col2:
    st.metric("Unemployment Rate (%)", f"{unemployment:.2f}")
    st.metric("Interest Rate (%)", f"{interest_rate:.2f}")

st.markdown("---")
st.subheader("💡 Investment Suggestions:")

if gdp > 2:
    st.success("✅ **Strong GDP Growth**: Consider investing in growth stocks, tech sectors, or ETFs.")
else:
    st.warning("⚠️ **Weak GDP Growth**: Be cautious. Focus on defensive assets like bonds or stable-dividend stocks.")

if inflation > 4:
    st.error("🔥 **High Inflation**: Protect purchasing power—consider gold, commodities, or inflation-protected bonds (TIPS).")
else:
    st.info("💠 **Stable Inflation**: Favorable for long-term equity investments and bonds.")

if unemployment > 6:
    st.warning("📉 **High Unemployment**: Economic slowdown likely. Defensive sectors like healthcare or utilities may perform better.")
else:
    st.success("🧑‍💼 **Healthy Job Market**: Supports retail, travel, and consumer discretionary sectors.")

if interest_rate > 5:
    st.error("💸 **High Interest Rates**: Borrowing costs are high. Prioritize short-duration bonds or savings accounts.")
else:
    st.info("🏡 **Low Interest Rates**: Real estate and growth stocks may benefit from cheaper borrowing.")

st.markdown("---")
st.caption("📘 These are general suggestions. Always consider your risk profile and consult a financial advisor.")
st.sidebar.header("🎯 Your Financial Goal")

goal = st.sidebar.selectbox(
    "Choose your primary investment goal:",
    ["Retirement", "Buying a Home", "Wealth Growth", "Short-Term Savings", "Capital Preservation"]
)
st.subheader("💡 Personalized Investment Suggestions:")

# Function for logic based on goal + economic data
def generate_suggestions(goal, gdp, inflation, unemployment, interest_rate):
    suggestions = []

    # Retirement
    if goal == "Retirement":
        suggestions.append("💼 Contribute regularly to retirement accounts (e.g., 401(k), IRA).")
        if inflation > 4:
            suggestions.append("🛡️ Use inflation-protected assets like TIPS and dividend-paying stocks.")
        else:
            suggestions.append("📈 Consider a balanced mix of stocks and bonds.")

    # Buying a Home
    elif goal == "Buying a Home":
        suggestions.append("🏠 Start or grow a high-yield savings account for your down payment.")
        if interest_rate > 5:
            suggestions.append("⏳ Mortgage rates are high—consider delaying purchase or locking rates now.")
        else:
            suggestions.append("✅ Low rates—evaluate mortgage options and affordability.")

    # Wealth Growth
    elif goal == "Wealth Growth":
        suggestions.append("🚀 Focus on long-term growth assets like ETFs, tech stocks, or index funds.")
        if gdp > 2 and inflation < 4:
            suggestions.append("🌱 Strong economy supports aggressive growth investing.")
        else:
            suggestions.append("🔍 Diversify with stable sectors (e.g., healthcare, utilities) for balance.")

    # Short-Term Savings
    elif goal == "Short-Term Savings":
        suggestions.append("💰 Use liquid instruments like money market funds, short-term bonds, or savings accounts.")
        if inflation > 4:
            suggestions.append("⚠️ Avoid holding too much cash—seek higher-yield alternatives.")
        else:
            suggestions.append("🧊 Inflation is manageable—prioritize safety and liquidity.")

    # Capital Preservation
    elif goal == "Capital Preservation":
        suggestions.append("🔒 Focus on minimizing risk with government bonds, CDs, or blue-chip dividend stocks.")
        if inflation > 4:
            suggestions.append("🏦 Consider I-bonds or short-duration TIPS to guard against inflation.")
        else:
            suggestions.append("📉 Low-risk environment—stay diversified and cautious.")

    return suggestions

# Generate and display personalized suggestions
advice = generate_suggestions(goal, gdp, inflation, unemployment, interest_rate)
for item in advice:
    st.markdown(f"- {item}")

st.sidebar.header("🔮 Economic Scenario Simulation")

sim_gdp = st.sidebar.slider("GDP Growth (%)", min_value=-5.0, max_value=15.0, value=float(df["GDP Growth (%)"].iloc[-1]))
sim_inflation = st.sidebar.slider("Inflation Rate (%)", min_value=0.0, max_value=15.0, value=float(df["Inflation Rate (%)"].iloc[-1]))
sim_unemployment = st.sidebar.slider("Unemployment Rate (%)", min_value=0.0, max_value=15.0, value=float(df["Unemployment Rate (%)"].iloc[-1]))
sim_interest = st.sidebar.slider("Interest Rate (%)", min_value=0.0, max_value=15.0, value=float(df["Interest Rate (%)"].iloc[-1]))

import streamlit as st
import pandas as pd
import altair as alt

# Load your data (adjust path as needed)
df = pd.read_csv(r"C:\Users\Admin\Documents\AI Personal Finance Advisor\Data\Economic Data.csv")

# Sidebar: Select Date for Analysis
st.sidebar.header("Select Date")
date_options = df['Date'].tolist()
selected_date = st.sidebar.selectbox("Choose Date", options=date_options, index=len(date_options)-1)

# Filter data for the selected date
selected_data = df[df['Date'] == selected_date].iloc[0]

# Extract key indicators dynamically
inflation = selected_data['Inflation Rate (%)']
gdp_growth = selected_data['GDP Growth (%)']
gold_price = selected_data['Gold Price (USD per Ounce)']
real_estate_index = selected_data['Real Estate Index']
unemployment = selected_data['Unemployment Rate (%)']
interest_rate = selected_data['Interest Rate (%)']

# Portfolio Diversification Tips based on data
tips = []
if inflation > 3.0:
    tips.append("Inflation is high. Consider investing more in gold and real estate to protect your portfolio.")
if gdp_growth > 2.5:
    tips.append("Strong GDP growth detected. Increasing equity exposure could benefit your portfolio.")
if inflation <= 3.0 and gdp_growth <= 2.5:
    tips.append("Market conditions are stable. Maintain a balanced portfolio across asset classes.")
if gold_price > df['Gold Price (USD per Ounce)'].mean():
    tips.append("Gold prices are currently above average; be cautious with new gold investments.")
if real_estate_index < df['Real Estate Index'].mean():
    tips.append("Real estate market seems undervalued; could be a buying opportunity.")
if not tips:
    tips.append("No specific diversification recommendations at this time.")

# Risk Indicator based on simple rules
risk_level = "Moderate"
if inflation > 5 or unemployment > 8 or interest_rate > 6:
    risk_level = "High"
elif inflation < 2 and unemployment < 5 and interest_rate < 3:
    risk_level = "Low"

# Display selected date and risk level
st.header(f"Market Summary for {selected_date}")
st.markdown(f"**Risk Level:** {risk_level}")

# Show Diversification Tips
st.subheader("Portfolio Diversification Tips")
for tip in tips:
    st.write("- " + tip)

# Prepare chart data for selected date's key indicators
chart_data = pd.DataFrame({
    "Indicator": ["Inflation Rate (%)", "GDP Growth (%)", "Gold Price (USD per Ounce)", "Real Estate Index", "Unemployment Rate (%)", "Interest Rate (%)"],
    "Value": [inflation, gdp_growth, gold_price, real_estate_index, unemployment, interest_rate]
})

# Bar chart with Altair
bar_chart = alt.Chart(chart_data).mark_bar(color="#4e79a7").encode(
    x=alt.X('Value:Q', title='Value'),
    y=alt.Y('Indicator:N', sort='-x', title='Economic Indicator')
).properties(height=300)

st.altair_chart(bar_chart, use_container_width=True)

import streamlit as st

# Example risk score (calculate based on your data/logic)
risk_score = 0.75  # Just a dummy value between 0 (low) and 1 (high)

# Thresholds for alerts
if risk_score > 0.7:
    st.error("⚠️ High Risk Alert: Your portfolio risk has increased significantly!")
elif risk_score > 0.4:
    st.warning("⚠️ Moderate Risk Alert: Keep an eye on your portfolio's risk.")
else:
    st.success("✅ Risk level is low and stable.")

from fpdf import FPDF
import streamlit as st
from io import BytesIO

# Example PDF generation
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Portfolio Suggestions", ln=True)
pdf.cell(200, 10, txt="Diversify your assets across equities, bonds, and real estate.", ln=True)

# Output PDF as a byte string
pdf_bytes = pdf.output(dest='S').encode('latin1')

# Wrap in BytesIO for download
pdf_buffer = BytesIO(pdf_bytes)

# Streamlit download button
st.download_button(
    label="📄 Download PDF",
    data=pdf_buffer,
    file_name="portfolio_suggestions.pdf",
    mime="application/pdf"
)
import streamlit as st
import pandas as pd
import numpy as np

st.subheader("📊 Interactive Portfolio Allocation")

# Slider inputs
st.markdown("### Set Your Target Allocations (%)")
stocks = st.slider("Stocks", 0, 100, 50)
bonds = st.slider("Bonds", 0, 100, 30)
real_estate = st.slider("Real Estate", 0, 100, 10)
cash = st.slider("Cash", 0, 100, 10)

total_alloc = stocks + bonds + real_estate + cash

# Normalize if total != 100
if total_alloc != 100:
    st.warning(f"Total is {total_alloc}%. Normalizing...")
    total = stocks + bonds + real_estate + cash
    stocks, bonds, real_estate, cash = [round(x / total * 100) for x in [stocks, bonds, real_estate, cash]]

# Risk Score (simple rule-based example)
risk_score = (stocks * 0.6 + real_estate * 0.3 - bonds * 0.4 - cash * 0.5) / 100
risk_level = "High" if risk_score > 0.5 else "Medium" if risk_score > 0.2 else "Low"

# Simulate performance (example returns + stdev)
expected_return = stocks * 0.08 + bonds * 0.03 + real_estate * 0.06 + cash * 0.02
volatility = stocks * 0.15 + bonds * 0.05 + real_estate * 0.1 + cash * 0.01

st.markdown(f"**Risk Level:** `{risk_level}`")
st.markdown(f"**Expected 1-Year Return:** `{expected_return:.2f}%`")
st.markdown(f"**Estimated Volatility:** `{volatility:.2f}%`")

# Display as table
alloc_df = pd.DataFrame({
    "Asset Class": ["Stocks", "Bonds", "Real Estate", "Cash"],
    "Allocation (%)": [stocks, bonds, real_estate, cash]
})

st.dataframe(alloc_df)

# Download
csv_data = alloc_df.to_csv(index=False).encode("utf-8")
st.download_button("💾 Download Allocation (CSV)", csv_data, "portfolio_allocation.csv", "text/csv")
import streamlit as st
import pandas as pd
import numpy as np

# --- Tax Efficient Suggestions ---
def tax_efficiency_tips(portfolio_df):
    tips = []
    # Simple rules for demo
    if portfolio_df['Allocation %'].loc[portfolio_df['Asset Class'] == 'Stocks'].values.sum() > 50:
        tips.append("Consider holding stocks long-term to reduce capital gains tax.")
    if portfolio_df['Allocation %'].loc[portfolio_df['Asset Class'] == 'Municipal Bonds'].values.sum() > 0:
        tips.append("Municipal bonds generate tax-free income. Good choice!")
    if portfolio_df['Allocation %'].loc[portfolio_df['Asset Class'] == 'High Turnover Funds'].values.sum() > 10:
        tips.append("Consider moving high-turnover funds to tax-advantaged accounts.")
    if not tips:
        tips.append("Your portfolio looks tax-efficient.")
    return tips

# --- Summary Dashboard ---
def portfolio_summary(portfolio_df, total_value):
    st.subheader("Portfolio Summary")
    st.write(f"Total Portfolio Value: ${total_value:,.2f}")
    
    st.write("**Allocation Breakdown:**")
    st.bar_chart(portfolio_df.set_index('Asset Class')['Allocation %'])
    
    # Example KPIs
    ytd_return = np.random.uniform(-0.1, 0.2)  # placeholder for real calc
    volatility = np.random.uniform(0.05, 0.25)  # placeholder
    
    st.write(f"Year-to-Date Return: {ytd_return*100:.2f}%")
    st.write(f"Volatility: {volatility*100:.2f}%")
    
    tax_tips = tax_efficiency_tips(portfolio_df)
    st.write("### Tax Efficiency Tips:")
    for tip in tax_tips:
        st.info(tip)

# Usage example
portfolio_df = pd.DataFrame({
    'Asset Class': ['Stocks', 'Bonds', 'Municipal Bonds', 'High Turnover Funds', 'Cash'],
    'Allocation %': [60, 20, 5, 10, 5]
})
total_value = 100000  # example

portfolio_summary(portfolio_df, total_value)
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Replace this with your actual portfolio data loading logic.
portfolio_df = pd.DataFrame({
    'Asset Class': ['Stocks', 'Bonds', 'Municipal Bonds', 'High Turnover Funds', 'Cash'],
    'Allocation %': [60, 20, 5, 10, 5],
    'YTD Return %': [12, 4, 2, 8, 0.5],  # example returns
})

total_value = 100000  # Example total portfolio value, replace with your variable
risk_level = "Balanced"  # Replace with user-selected or calculated risk level

# --- Helper functions ---
def annualized_return(returns, periods=252):
    return ((1 + np.mean(returns) / 100) ** periods - 1) * 100

def volatility(returns):
    return np.std(returns) * np.sqrt(252) * 100

def sharpe_ratio(avg_return, vol, risk_free_rate=2):
    return (avg_return - risk_free_rate) / vol if vol != 0 else 0

def tax_efficiency_score(portfolio):
    muni = portfolio.loc[portfolio['Asset Class'] == 'Municipal Bonds', 'Allocation %'].sum()
    cash = portfolio.loc[portfolio['Asset Class'] == 'Cash', 'Allocation %'].sum()
    score = muni * 2 + cash
    return min(score, 100)

def tax_efficiency_tips(portfolio):
    tips = []
    if portfolio['Allocation %'].loc[portfolio['Asset Class']=='High Turnover Funds'].sum() > 10:
        tips.append("Consider moving high-turnover funds to tax-advantaged accounts.")
    if portfolio['Allocation %'].loc[portfolio['Asset Class']=='Municipal Bonds'].sum() > 0:
        tips.append("Municipal bonds provide tax-free income—good for tax efficiency.")
    if not tips:
        tips.append("Your portfolio looks tax-efficient.")
    return tips

# --- Calculations ---
avg_ytd_return = portfolio_df['YTD Return %'].mean()
vol = volatility(portfolio_df['YTD Return %'])
sharpe = sharpe_ratio(avg_ytd_return, vol)
tax_score = tax_efficiency_score(portfolio_df)

# --- Streamlit UI Section ---
def portfolio_summary_dashboard():
    st.header("📊 Portfolio Summary Dashboard")

    # Portfolio Overview
    st.subheader("Portfolio Overview")
    st.write(f"**Total Portfolio Value:** ${total_value:,.2f}")
    pie_chart = alt.Chart(portfolio_df).mark_arc().encode(
        theta=alt.Theta(field="Allocation %", type="quantitative"),
        color=alt.Color(field="Asset Class", type="nominal"),
        tooltip=['Asset Class', 'Allocation %']
    ).properties(width=350, height=350)
    st.altair_chart(pie_chart)

    # Performance Metrics
    st.subheader("Performance Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("YTD Return (%)", f"{avg_ytd_return:.2f}")
    col2.metric("Annualized Volatility (%)", f"{vol:.2f}")
    col3.metric("Sharpe Ratio", f"{sharpe:.2f}")

    # Risk & Allocation
    st.subheader("Risk & Allocation")
    st.write(f"Risk Level: **{risk_level}**")
    max_drawdown = -0.15  # Placeholder: Replace with your data-driven value
    beta = 1.1            # Placeholder
    st.write(f"Max Drawdown (historical): {max_drawdown*100:.2f}%")
    st.write(f"Beta vs Market: {beta:.2f}")

    # Tax Efficiency
    st.subheader("Tax Efficiency")
    st.write(f"Tax Efficiency Score: {tax_score:.0f}/100")
    for tip in tax_efficiency_tips(portfolio_df):
        st.info(tip)

    # Alerts (example)
    st.subheader("Alerts & Notifications")
    st.success("No immediate alerts. Your portfolio is balanced.")

# Call this function somewhere in your app where you want the dashboard to show
portfolio_summary_dashboard()
import streamlit as st
import pandas as pd
import numpy as np

# Custom CSS for nicer fonts and spacing
st.markdown("""
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Portfolio Assessment")

# Sidebar inputs & navigation
with st.sidebar:
    st.header("Configure your Portfolio")
    
    risk_level = st.selectbox(
        "Select Risk Level 🎯",
        ["Conservative", "Balanced", "Aggressive"],
        key="risk_level"
    )
    
    st.markdown("---")
    st.header("Filters & Export")
    
    export_format = st.radio("Export Portfolio As:", ["CSV", "PDF"], index=0)
    export_button = st.button("💾 Export Portfolio")
    
    st.markdown("---")
    st.caption("Developed by Yash Vaswani")

# Dummy portfolio data for demonstration
portfolio_df = pd.DataFrame({
    "Asset": ["Stocks", "Bonds", "Real Estate", "Cash", "Commodities"],
    "Allocation (%)": [50, 25, 15, 5, 5],
})

# Tabs for organizing content
tab1, tab2, tab3 = st.tabs(["📈 Portfolio Overview", "💡 Suggestions", "📋 Summary Dashboard"])

with tab1:
    st.subheader("Portfolio Allocation")
    
    # Interactive sliders for allocation with total check
    allocations = []
    total_allocation = 0
    cols = st.columns(len(portfolio_df))
    for i, col in enumerate(cols):
        alloc = col.slider(
            f"{portfolio_df.loc[i, 'Asset']} %",
            min_value=0,
            max_value=100,
            value=portfolio_df.loc[i, 'Allocation (%)'],
            key=f"alloc_{i}"
        )
        allocations.append(alloc)
        total_allocation += alloc

    st.markdown(f"**Total Allocation: {total_allocation}%**")
    if total_allocation != 100:
        st.error("⚠️ Total allocation must sum to 100%!")
with st.expander("📊 View Portfolio Breakdown"):
    st.dataframe(portfolio_df)

    # Show pie chart for allocations
    if total_allocation == 100:
        alloc_df = pd.DataFrame({
            "Asset": portfolio_df["Asset"],
            "Allocation": allocations
        })
        st.pyplot(
            alloc_df.set_index("Asset").plot.pie(
                y='Allocation',
                autopct='%1.1f%%',
                legend=False,
                figsize=(5,5)
            ).figure
        )

with tab2:
    st.subheader("Financial Suggestions")
    # Dummy suggestions based on risk
    if risk_level == "Conservative":
        st.info("💡Consider increasing bond allocation and holding more cash.")
    elif risk_level == "Balanced":
        st.success("Maintain your diversified portfolio with a mix of stocks and bonds.")
    else:
        st.warning("Higher stock allocation might increase volatility but with higher potential returns.")

with tab3:
    st.subheader("Summary Dashboard")
    # Dummy KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Portfolio Value", "$120,000", "+2.3%")
    col2.metric("Risk Level", risk_level)
    col3.metric("Projected Annual Return", "7.5%", "+0.2%")

    st.markdown("### Performance Chart")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    values = np.cumsum(np.random.randn(30)) + 100
    perf_df = pd.DataFrame({"Date": dates, "Value": values})
    perf_df = perf_df.set_index("Date")
    st.line_chart(perf_df)

# Handle export button logic
if export_button:
    with st.spinner("Preparing export..."):
        if export_format == "CSV":
            csv_data = portfolio_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Portfolio CSV",
                data=csv_data,
                file_name="portfolio.csv",
                mime="text/csv"
            )
        else:
            # For PDF export, you could use fpdf or reportlab, simplified here
            st.warning("PDF export is coming soon!")

    st.success("Export ready! Choose format and download.")
if export_button:
    st.success("✅ Portfolio exported successfully!")

import streamlit as st
import pandas as pd
import numpy as np

# Load your data (update path as needed)
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:/Users/Admin/Documents/AI Personal Finance Advisor/Data/Economic Data.csv")
    return df

df = load_data()

# Example portfolio data - replace or update as needed
portfolio_df = pd.DataFrame({
    "Asset": ["Stocks", "Bonds", "Real Estate", "Cash", "Commodities"],
    "Allocation (%)": [50, 25, 15, 5, 5],
})

# --- UI Layout ---
st.markdown("""
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

import streamlit as st

st.progress(int(total_allocation))  # `total_allocation` should be your current slider sum
    
# Export functionality
if export_button:
    with st.spinner("Preparing export..."):
        export_df = portfolio_df.copy()
        export_df["Allocation (%)"] = allocations  # use updated allocations

        if export_format == "CSV":
            csv_data = export_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Portfolio CSV",
                data=csv_data,
                file_name="portfolio.csv",
                mime="text/csv"
            )
        else:
            # You can integrate your PDF export logic here
            st.warning("PDF export is coming soon!")

    st.success("Export ready! Choose format and download.")
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# --- Load and Clean Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/Admin/Documents/AI Personal Finance Advisor/Data/Economic Data.csv")

    df.dropna(subset=['Date'], inplace=True)
    return df

econ_df = load_data()

# --- Branding & Styling ---

st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Dummy Portfolio Data ---
assets = ["Stocks", "Bonds", "Real Estate", "Cash", "Commodities"]
default_alloc = [50, 25, 15, 5, 5]

# --- Export Button ---
if export_button and total_alloc == 100:
    export_df = pd.DataFrame({"Asset": assets, "Allocation (%)": allocations})
    if export_format == "CSV":
        csv_data = export_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", data=csv_data, file_name="portfolio.csv", mime="text/csv")
    else:
        st.warning("📄 PDF export is under development.")
with st.sidebar.expander("💬 Feedback / Suggestions"):
    st.markdown("We'd love to hear your thoughts or suggestions to improve this app.")
    feedback = st.text_area("Your feedback:")
    if st.button("📩 Submit Feedback"):
        if feedback.strip():
            st.success("✅ Thanks for your feedback!")
            # Optionally, save it to a file or database here.
        else:
            st.warning("⚠️ Feedback is empty. Please enter something.")

