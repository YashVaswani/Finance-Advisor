# --- 1. IMPORTS (ALL AT THE TOP) ---
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from fpdf import FPDF
from io import BytesIO
import os
from datetime import datetime

# --- 2. PAGE CONFIG (MUST BE THE FIRST STREAMLIT COMMAND) ---
st.set_page_config(
    page_title="AI Personal Finance Advisor",
    page_icon="📒",  # Added page_icon back
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. AUTHENTICATION ---
# (Demo user=admin, password=123#)
users = {"admin": "123#", "user": "123*"}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login to AI Finance Advisor")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password (Demo: user=admin, pass=123#)")
    st.stop()  # Stop execution if not authenticated

# --- 4. DATA LOADING (ONLY ONCE) ---
@st.cache_data  # Cache the data for performance
def load_data():
    # This creates a path relative to this .py file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "Data", "Economic Data.csv")
    
    # --- INDENTATION FIXED BELOW ---
    try:
        df = pd.read_csv(file_path)
        
        # --- CORRECT FIX ---
        # First, check if the column exists
        if 'Date' in df.columns:
            # If it exists, THEN convert it
            df['Date'] = pd.to_datetime(df['Date'])
        # --- END OF FIX ---
        
        return df

    except FileNotFoundError:
        st.error(f"Error: The data file was not found.")
        st.info("Please make sure 'Economic Data.csv' is inside a 'Data' folder.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return None
    # --- END OF INDENTATION FIX ---

# Load the data
df = load_data()

# Stop the app if data loading failed
if df is None or df.empty:
    st.error("Data could not be loaded. App cannot continue.")
    st.stop()

# --- 5. STYLING & TITLE ---
# (Your custom CSS)
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        background-color: #f4f4f4 !important;
        color: #2e2e2e !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* ... (rest of your CSS styles) ... */
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
    section[data-testid="stSidebar"] {
        background-color: #e0e0e0 !important;
        color: #2e2e2e !important;
        border-right: 1px solid #cccccc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align: center; color: #2e2e2e;'>📊 AI Personal Finance Advisor</h1>
    """,
    unsafe_allow_html=True
)

# --- 6. SIDEBAR CONTROLS ---
st.sidebar.header("🎯 Your Financial Goal")
goal = st.sidebar.selectbox(
    "Choose your primary investment goal:",
    ["Retirement", "Buying a Home", "Wealth Growth", "Short-Term Savings", "Capital Preservation"]
)

st.sidebar.header("🗓️ Select Date for Analysis")
date_options = df['Date'].dt.strftime('%Y-%m-%d').tolist()
selected_date_str = st.sidebar.selectbox("Choose Date", options=date_options, index=len(date_options)-1)
selected_date = pd.to_datetime(selected_date_str)

st.sidebar.header("🔮 Economic Scenario Simulation")
st.sidebar.caption("Simulate conditions to see suggestions change.")
# Get default values from the latest data
latest_data = df.iloc[-1]
sim_gdp = st.sidebar.slider("Simulated GDP Growth (%)", -5.0, 15.0, float(latest_data["GDP Growth (%)"]))
sim_inflation = st.sidebar.slider("Simulated Inflation Rate (%)", 0.0, 15.0, float(latest_data["Inflation Rate (%)"]))
sim_unemployment = st.sidebar.slider("Simulated Unemployment Rate (%)", 0.0, 15.0, float(latest_data["Unemployment Rate (%)"]))
sim_interest = st.sidebar.slider("Simulated Interest Rate (%)", 0.0, 15.0, float(latest_data["Interest Rate (%)"]))


# --- 7. HELPER FUNCTIONS ---

# Function for goal-based suggestions
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
    # Add other goals...
    else:
        suggestions.append("Select a goal to see personalized tips.")

    return suggestions

# Function for tax efficiency tips
def tax_efficiency_tips(alloc_df):
    tips = []
    if 'Stocks' in alloc_df['Asset Class'].values and alloc_df.loc[alloc_df['Asset Class'] == 'Stocks', 'Allocation %'].values[0] > 50:
        tips.append("Consider holding stocks long-term (over 1 year) to benefit from lower capital gains tax rates.")
    if 'Municipal Bonds' in alloc_df['Asset Class'].values and alloc_df.loc[alloc_df['Asset Class'] == 'Municipal Bonds', 'Allocation %'].values[0] > 0:
        tips.append("Municipal bonds generate tax-free income at the federal level. Good choice!")
    if 'High Turnover Funds' in alloc_df['Asset Class'].values and alloc_df.loc[alloc_df['Asset Class'] == 'High Turnover Funds', 'Allocation %'].values[0] > 10:
        tips.append("Consider moving high-turnover funds to tax-advantaged accounts (like an IRA) to avoid annual tax drag.")
    if not tips:
        tips.append("Your portfolio looks tax-efficient. Remember to consult a tax professional.")
    return tips


# --- 8. APP LAYOUT (USING TABS) ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Economic Dashboard", "💡 Personalized Suggestions","📊 Portfolio Builder", "📋 Report & Feedback"])

# --- TAB 1: ECONOMIC DASHBOARD ---
with tab1:
    st.subheader("Economic Data Preview")
    st.dataframe(df.head())

    st.subheader("Summary Statistics")
    st.write(df.describe())

    st.subheader("Visualize Economic Indicators")
    # Filter out non-numeric columns for selector
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    metric = st.selectbox("Select a metric to visualize:", numeric_cols)
    if metric:
        chart_df = df[['Date', metric]].dropna()
        st.line_chart(chart_df.set_index('Date'))

    # Top 5 Investment Suggestions (if columns exist)
    if 'Return' in df.columns and 'Ticker' in df.columns:
        st.subheader("💡 Top 10 Investment Suggestions (by Avg. Return)")
        top_stocks = df.groupby("Ticker")['Return'].mean().sort_values(ascending=False).head(10)
        st.table(top_stocks)
    else:
        st.info("Note: Add 'Return' and 'Ticker' columns in your dataset for stock-specific suggestions.")

# --- TAB 2: PERSONALIZED SUGGESTIONS ---
with tab2:
    st.subheader("💡 Suggestions Based on Your Goal & Simulated Economy")
    st.markdown("---")
    st.write(f"**Your Goal:** `{goal}`")
    st.write("**Using Simulated Economic Data:**")

    # Display simulated metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Simulated GDP Growth (%)", f"{sim_gdp:.2f}")
        st.metric("Simulated Inflation Rate (%)", f"{sim_inflation:.2f}")
    with col2:
        st.metric("Simulated Unemployment Rate (%)", f"{sim_unemployment:.2f}")
        st.metric("Simulated Interest Rate (%)", f"{sim_interest:.2f}")
    
    # Generate and display personalized suggestions
    advice = generate_suggestions(goal, sim_gdp, sim_inflation, sim_unemployment, sim_interest)
    st.markdown("#### Your Personalized Advice:")
    for item in advice:
        st.markdown(f"- {item}")
    
    st.markdown("---")
    
    # --- Market Summary for Selected Date ---
    st.subheader(f"📊 Market Summary for {selected_date_str}")
    selected_data = df[df['Date'] == selected_date].iloc[0]

    # Extract key indicators dynamically
    inflation = selected_data['Inflation Rate (%)']
    gdp_growth = selected_data['GDP Growth (%)']
    unemployment = selected_data['Unemployment Rate (%)']
    interest_rate = selected_data['Interest Rate (%)']

    # Risk Indicator
    risk_level = "Moderate"
    if inflation > 5 or unemployment > 8 or interest_rate > 6:
        risk_level = "High"
    elif inflation < 2 and unemployment < 5 and interest_rate < 3:
        risk_level = "Low"
    st.markdown(f"**Market Risk Level on this date:** {risk_level}")

    # Diversification Tips
    tips = []
    if inflation > 3.0:
        tips.append("Inflation was high. Consider assets like gold and real estate to hedge.")
    if gdp_growth > 2.5:
        tips.append("Strong GDP growth detected. Equities may have been a good investment.")
    if not tips:
        tips.append("Market conditions appear stable. A balanced portfolio is recommended.")
    
    st.markdown("#### Diversification Tips for this period:")
    for tip in tips:
        st.write("- " + tip)

# --- TAB 3: PORTFOLIO BUILDER ---
with tab3:
    st.subheader("📊 Interactive Portfolio Allocation")
    st.markdown("### Set Your Target Allocations (%)")
    
    # Sliders
    stocks = st.slider("Stocks", 0, 100, 50)
    bonds = st.slider("Bonds", 0, 100, 30)
    real_estate = st.slider("Real Estate", 0, 100, 10)
    cash = st.slider("Cash", 0, 100, 10)
    
    total_alloc = stocks + bonds + real_estate + cash
    
    st.progress(total_alloc)

    # Normalize if total != 100
    if total_alloc != 100:
        st.error(f"Total allocation is {total_alloc}%. It must sum to 100%.")
    else:
        st.success("Total allocation is 100%.")

    # Risk Score & Performance (Simple rule-based example)
    risk_score = (stocks * 0.6 + real_estate * 0.3 - bonds * 0.4 - cash * 0.5) / 100
    risk_level = "High" if risk_score > 0.4 else "Medium" if risk_score > 0.15 else "Low"
    expected_return = (stocks * 0.08 + bonds * 0.03 + real_estate * 0.06 + cash * 0.02) / 100
    volatility = (stocks * 0.15 + bonds * 0.05 + real_estate * 0.1 + cash * 0.01) / 100

    st.markdown("---")
    st.subheader("Portfolio Summary")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Calculated Risk Level", risk_level)
    col2.metric("Expected Annual Return", f"{expected_return:.2%}")
    col3.metric("Estimated Volatility", f"{volatility:.2%}")

    # Risk Alert
    if risk_score > 0.4:
        st.error("⚠️ High Risk Alert: Your portfolio allocation is aggressive and may see high volatility.")
    elif risk_score > 0.15:
        st.warning("⚠️ Moderate Risk: Your portfolio is balanced but carries a moderate level of risk.")
    else:
        st.success("✅ Low Risk: Your portfolio is conservative and prioritizes capital preservation.")

    # Display as table and chart
    alloc_df = pd.DataFrame({
        "Asset Class": ["Stocks", "Bonds", "Real Estate", "Cash"],
        "Allocation %": [stocks, bonds, real_estate, cash]
    })
    
    pie_chart = alt.Chart(alloc_df).mark_arc(outerRadius=120).encode(
        theta=alt.Theta(field="Allocation %", type="quantitative"),
        color=alt.Color(field="Asset Class", type="nominal"),
        tooltip=['Asset Class', 'Allocation %']
    ).properties(title="Portfolio Allocation")
    
    st.altair_chart(pie_chart, use_container_width=True)

    # Tax Efficiency
    st.subheader("Tax Efficiency Tips")
    for tip in tax_efficiency_tips(alloc_df):
        st.info(tip)
        
    # Download Allocation
    csv_data = alloc_df.to_csv(index=False).encode("utf-8")
    st.download_button("💾 Download Allocation (CSV)", csv_data, "portfolio_allocation.csv", "text/csv")


# --- TAB 4: REPORT & FEEDBACK ---
with tab4:
    st.subheader("📄 Download Your PDF Report")
    st.write("Click the button to generate a PDF summary of your goals and portfolio.")
    
    if st.button("Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(200, 10, txt="My AI Financial Report", ln=True, align='C')
        
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt="My Financial Goal", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"- {goal}", ln=True)
        
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt="My Portfolio Allocation", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, txt=f"- Stocks: {stocks}%", ln=True)
        pdf.cell(200, 8, txt=f"- Bonds: {bonds}%", ln=True)
        pdf.cell(200, 8, txt=f"- Real Estate: {real_estate}%", ln=True)
        pdf.cell(200, 8, txt=f"- Cash: {cash}%", ln=True)
        
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt="Portfolio Profile", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, txt=f"- Risk Level: {risk_level}", ln=True)
        pdf.cell(200, 8, txt=f"- Expected Return: {expected_return:.2%}", ln=True)

        # Output PDF as bytes
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_buffer = BytesIO(pdf_bytes)

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_buffer,
            file_name=f"Financial_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        st.success("Your PDF report is ready for download!")

    st.markdown("---")
    st.subheader("💬 Feedback & Suggestions")
    st.markdown("We'd love to hear your thoughts to improve this app.")
    feedback = st.text_area("Your feedback:")
    if st.button("📩 Submit Feedback"):
        if feedback.strip():
            st.success("✅ Thanks for your feedback!")
            # Optionally, you could save this feedback to a file or database
        else:
            st.warning("⚠️ Feedback is empty. Please enter something.")