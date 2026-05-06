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

# --- 3. GLOBAL STYLING (injected before login so login page is also styled) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* === BASE THEME === */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    color: #e2e8f0 !important;
}
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%) !important;
}

/* === SCROLLBAR === */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.4); border-radius: 4px; }

/* === SIDEBAR === */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #0f0c29 100%) !important;
    border-right: 1px solid rgba(139,92,246,0.2) !important;
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] header {
    color: #e9d5ff !important; font-weight: 700 !important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] small {
    color: #cbd5e1 !important;
}

/* === GLOBAL LABELS (sliders, inputs) === */
label[data-testid="stWidgetLabel"] {
    color: #e2e8f0 !important; font-weight: 500 !important;
}

/* === BUTTONS === */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important; font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important; box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(139,92,246,0.45) !important;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px; background: rgba(255,255,255,0.03);
    border-radius: 16px; padding: 6px;
    border: 1px solid rgba(139,92,246,0.15);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important; padding: 10px 24px !important;
    font-family: 'Inter', sans-serif !important; font-weight: 500 !important;
    color: #a5b4fc !important; transition: all 0.3s ease !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: #fff !important; box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
}

/* === METRICS === */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 16px !important; padding: 20px !important;
    backdrop-filter: blur(10px); transition: all 0.3s ease;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(139,92,246,0.4) !important;
    transform: translateY(-2px); box-shadow: 0 8px 25px rgba(139,92,246,0.15);
}
[data-testid="stMetricLabel"] { color: #a5b4fc !important; font-weight: 500 !important; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-weight: 700 !important; }

/* === INPUTS / SLIDERS / SELECTS === */
.stSlider > div > div > div { background: #7c3aed !important; }
.stSelectbox > div > div, .stTextInput > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
}

/* === DATAFRAME === */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 12px !important; overflow: hidden;
}

/* === ALERTS === */
.stAlert { border-radius: 12px !important; backdrop-filter: blur(10px); }

/* === DOWNLOAD BUTTON === */
.stDownloadButton > button {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important; font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(139,92,246,0.45) !important;
}

/* === ALTAIR CHART TEXT (legends, labels, titles) === */
#vg-tooltip-element table { color: #1e1b4b !important; }

/* === PROGRESS BAR === */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #a78bfa) !important;
    border-radius: 8px !important;
}

/* === TABLE TEXT === */
.stTable, .stTable td, .stTable th,
[data-testid="stTable"] { color: #e2e8f0 !important; }

/* === TEXT AREA === */
.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
}

/* === CUSTOM GLASS CARD === */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(139,92,246,0.15);
    border-radius: 20px; padding: 28px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(139,92,246,0.35);
    box-shadow: 0 12px 40px rgba(139,92,246,0.12);
}
.glass-card h3 { color: #c4b5fd; margin-top: 0; }
.glass-card p, .glass-card li { color: #cbd5e1; line-height: 1.7; }

/* === HEADER BANNER === */
.header-banner {
    text-align: center; padding: 2.5rem 1rem 1.5rem;
    animation: fadeSlideIn 0.8s ease-out;
}
.header-banner h1 {
    font-size: 2.4rem; font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #818cf8, #c084fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.header-banner p { color: #94a3b8; font-size: 1.05rem; font-weight: 400; }

/* === LOGIN CARD === */
.login-card {
    max-width: 420px; margin: 6rem auto;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 24px; padding: 2.5rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    text-align: center;
    animation: fadeSlideIn 0.6s ease-out;
}
.login-card h2 {
    font-size: 1.8rem; font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #c084fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.login-card p { color: #94a3b8; font-size: 0.9rem; }

/* === SUGGESTION ITEM === */
.suggestion-item {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #7c3aed;
    border-radius: 0 12px 12px 0;
    padding: 14px 20px; margin-bottom: 10px;
    color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;
    transition: all 0.2s ease;
}
.suggestion-item:hover { background: rgba(139,92,246,0.08); }

/* === ANIMATION === */
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* === DIVIDER === */
.styled-divider {
    height: 1px; border: none; margin: 2rem 0;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.3), transparent);
}
</style>
""", unsafe_allow_html=True)

# --- 4. AUTHENTICATION ---
# (Demo user=admin, password=123#)
users = {"admin": "123#", "user": "123*"}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <div class="login-card">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔐</div>
        <h2>Welcome Back</h2>
        <p>Sign in to your AI Finance Advisor</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        if st.button("🚀 Sign In", use_container_width=True):
            if username in users and users[username] == password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials — Demo: user=admin, pass=123#")
        st.caption("🔑 Demo accounts: admin/123# or user/123*")
    st.stop()

# --- 5. DATA LOADING (ONLY ONCE) ---
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "Data", "Economic Data.csv")
    try:
        df = pd.read_csv(file_path)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        st.error("Error: The data file was not found.")
        st.info("Please make sure 'Economic Data.csv' is inside a 'Data' folder.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return None

df = load_data()
if df is None or df.empty:
    st.error("Data could not be loaded. App cannot continue.")
    st.stop()

# --- 6. HEADER BANNER ---
st.markdown("""
<div class="header-banner">
    <h1>📊 AI Personal Finance Advisor</h1>
    <p>Smart insights powered by economic data & AI-driven analysis</p>
</div>
""", unsafe_allow_html=True)

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
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Economic Dashboard",
    "💡 Personalized Suggestions",
    "📊 Portfolio Builder",
    "📋 Report & Feedback"
])

# Altair dark theme config
dark_theme = {
    "config": {
        "background": "transparent",
        "title": {"color": "#c4b5fd", "font": "Inter"},
        "axis": {
            "labelColor": "#94a3b8", "titleColor": "#a5b4fc",
            "gridColor": "rgba(139,92,246,0.08)", "domainColor": "rgba(139,92,246,0.2)"
        },
        "legend": {"labelColor": "#cbd5e1", "titleColor": "#a5b4fc"},
        "view": {"stroke": "transparent"}
    }
}
alt.themes.register("dark_custom", lambda: dark_theme)
alt.themes.enable("dark_custom")

# --- TAB 1: ECONOMIC DASHBOARD ---
with tab1:
    st.markdown('<div class="glass-card"><h3>📋 Economic Data Preview</h3></div>', unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>📊 Summary Statistics</h3></div>', unsafe_allow_html=True)
    st.write(df.describe())

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>📉 Visualize Economic Indicators</h3></div>', unsafe_allow_html=True)
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    metric = st.selectbox("Select a metric to visualize:", numeric_cols)
    if metric:
        chart_df = df[['Date', metric]].dropna()
        line_chart = alt.Chart(chart_df).mark_area(
            line={"color": "#8b5cf6"},
            color=alt.Gradient(gradient="linear", stops=[
                alt.GradientStop(color="rgba(139,92,246,0.4)", offset=0),
                alt.GradientStop(color="rgba(139,92,246,0.0)", offset=1)
            ], x1=0, x2=0, y1=1, y2=0)
        ).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y(f"{metric}:Q", title=metric),
            tooltip=["Date:T", f"{metric}:Q"]
        ).properties(height=350)
        st.altair_chart(line_chart, use_container_width=True)

    # Top Investment Suggestions (if columns exist)
    if 'Return' in df.columns and 'Ticker' in df.columns:
        st.markdown('<div class="glass-card"><h3>💡 Top 10 Investments (by Avg. Return)</h3></div>', unsafe_allow_html=True)
        top_stocks = df.groupby("Ticker")['Return'].mean().sort_values(ascending=False).head(10)
        st.table(top_stocks)
    else:
        st.info("ℹ️ Add 'Return' and 'Ticker' columns in your dataset for stock-specific suggestions.")

# --- TAB 2: PERSONALIZED SUGGESTIONS ---
with tab2:
    st.markdown(f"""
    <div class="glass-card">
        <h3>💡 Goal-Based Insights</h3>
        <p>Your selected goal: <strong style="color:#a78bfa">{goal}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Display simulated metrics in 4 columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("GDP Growth", f"{sim_gdp:.2f}%")
    with col2:
        st.metric("Inflation", f"{sim_inflation:.2f}%")
    with col3:
        st.metric("Unemployment", f"{sim_unemployment:.2f}%")
    with col4:
        st.metric("Interest Rate", f"{sim_interest:.2f}%")

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

    # Generate and display personalized suggestions with styled cards
    advice = generate_suggestions(goal, sim_gdp, sim_inflation, sim_unemployment, sim_interest)
    st.markdown('<div class="glass-card"><h3>🎯 Your Personalized Advice</h3></div>', unsafe_allow_html=True)
    for item in advice:
        st.markdown(f'<div class="suggestion-item">{item}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

    # --- Market Summary for Selected Date ---
    st.markdown(f"""
    <div class="glass-card">
        <h3>📊 Market Summary — {selected_date_str}</h3>
    </div>
    """, unsafe_allow_html=True)
    selected_data = df[df['Date'] == selected_date].iloc[0]

    inflation = selected_data['Inflation Rate (%)']
    gdp_growth = selected_data['GDP Growth (%)']
    unemployment = selected_data['Unemployment Rate (%)']
    interest_rate = selected_data['Interest Rate (%)']

    # Risk Indicator with color coding
    risk_level = "Moderate"
    risk_color = "#eab308"
    if inflation > 5 or unemployment > 8 or interest_rate > 6:
        risk_level = "High"
        risk_color = "#ef4444"
    elif inflation < 2 and unemployment < 5 and interest_rate < 3:
        risk_level = "Low"
        risk_color = "#22c55e"

    st.markdown(f"""
    <div class="suggestion-item" style="border-left-color: {risk_color};">
        <strong>Market Risk Level:</strong> <span style="color:{risk_color}; font-weight:700;">{risk_level}</span>
    </div>
    """, unsafe_allow_html=True)

    # Diversification Tips
    tips = []
    if inflation > 3.0:
        tips.append("📈 Inflation was high. Consider assets like gold and real estate to hedge.")
    if gdp_growth > 2.5:
        tips.append("💪 Strong GDP growth detected. Equities may have been a good investment.")
    if not tips:
        tips.append("⚖️ Market conditions appear stable. A balanced portfolio is recommended.")

    for tip in tips:
        st.markdown(f'<div class="suggestion-item">{tip}</div>', unsafe_allow_html=True)

# --- TAB 3: PORTFOLIO BUILDER ---
with tab3:
    st.markdown('<div class="glass-card"><h3>🏗️ Build Your Portfolio</h3><p>Adjust the sliders to set your target asset allocations.</p></div>', unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        stocks = st.slider("📈 Stocks", 0, 100, 50)
        bonds = st.slider("🏦 Bonds", 0, 100, 30)
    with col_s2:
        real_estate = st.slider("🏠 Real Estate", 0, 100, 10)
        cash = st.slider("💵 Cash", 0, 100, 10)

    total_alloc = stocks + bonds + real_estate + cash
    st.progress(min(total_alloc, 100))

    if total_alloc != 100:
        st.error(f"⚠️ Total allocation is **{total_alloc}%** — it must sum to exactly 100%.")
    else:
        st.success("✅ Perfect! Your allocation sums to 100%.")

    # Risk Score & Performance
    risk_score = (stocks * 0.6 + real_estate * 0.3 - bonds * 0.4 - cash * 0.5) / 100
    risk_level = "High" if risk_score > 0.4 else "Medium" if risk_score > 0.15 else "Low"
    expected_return = (stocks * 0.08 + bonds * 0.03 + real_estate * 0.06 + cash * 0.02) / 100
    volatility = (stocks * 0.15 + bonds * 0.05 + real_estate * 0.1 + cash * 0.01) / 100

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)
    st.markdown('<div class="glass-card"><h3>📊 Portfolio Summary</h3></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Risk Level", risk_level)
    col2.metric("Expected Return", f"{expected_return:.2%}")
    col3.metric("Volatility", f"{volatility:.2%}")

    # Risk Alert
    if risk_score > 0.4:
        st.error("🔴 High Risk: Your portfolio is aggressive and may see high volatility.")
    elif risk_score > 0.15:
        st.warning("🟡 Moderate Risk: Balanced but carries moderate risk.")
    else:
        st.success("🟢 Low Risk: Conservative — prioritizes capital preservation.")

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

    # Display chart
    alloc_df = pd.DataFrame({
        "Asset Class": ["Stocks", "Bonds", "Real Estate", "Cash"],
        "Allocation %": [stocks, bonds, real_estate, cash]
    })

    pie_chart = alt.Chart(alloc_df).mark_arc(
        outerRadius=140, innerRadius=60, cornerRadius=6
    ).encode(
        theta=alt.Theta(field="Allocation %", type="quantitative"),
        color=alt.Color(field="Asset Class", type="nominal",
            scale=alt.Scale(range=["#22d3ee", "#a78bfa", "#facc15", "#fb7185"])
        ),
        tooltip=["Asset Class", "Allocation %"]
    ).properties(title="Portfolio Allocation", height=380)

    st.altair_chart(pie_chart, use_container_width=True)

    # Tax Efficiency
    st.markdown('<div class="glass-card"><h3>🧾 Tax Efficiency Tips</h3></div>', unsafe_allow_html=True)
    for tip in tax_efficiency_tips(alloc_df):
        st.markdown(f'<div class="suggestion-item">{tip}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)
    csv_data = alloc_df.to_csv(index=False).encode("utf-8")
    st.download_button("💾 Download Allocation (CSV)", csv_data, "portfolio_allocation.csv", "text/csv")

# --- TAB 4: REPORT & FEEDBACK ---
with tab4:
    st.markdown("""
    <div class="glass-card">
        <h3>📄 Generate Your Report</h3>
        <p>Create a downloadable PDF summary of your financial goals and portfolio allocation.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Generate PDF Report", use_container_width=True):
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

        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_buffer = BytesIO(pdf_bytes)

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_buffer,
            file_name=f"Financial_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        st.success("✅ Your PDF report is ready for download!")

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h3>💬 Share Your Feedback</h3>
        <p>We'd love to hear your thoughts to improve this advisor.</p>
    </div>
    """, unsafe_allow_html=True)
    feedback = st.text_area("Your feedback:", placeholder="Tell us what you think...")
    if st.button("📩 Submit Feedback", use_container_width=True):
        if feedback.strip():
            st.success("✅ Thanks for your feedback!")
        else:
            st.warning("⚠️ Feedback is empty. Please enter something.")

# --- FOOTER ---
st.markdown("""
<hr class="styled-divider">
<div style="text-align:center; padding: 1rem; color: #64748b; font-size: 0.85rem;">
    Built with ❤️ using <strong style="color:#a78bfa;">Streamlit</strong> • AI Personal Finance Advisor
</div>
""", unsafe_allow_html=True)