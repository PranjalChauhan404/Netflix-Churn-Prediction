import streamlit as st
import pandas as pd
import joblib
import base64

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Netflix Churn Prediction",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --nf-red: #E50914;
    --nf-red-bright: #f40612;
    --nf-green: #46d369;
    --nf-gold: #f5c518;
    --nf-bg: #090909;
    --nf-card: #141414;
    --nf-border: #262626;
    --nf-text-dim: #8a8a8a;
}

html, body, [class*="css"] {
    font-family: 'Manrope', 'Netflix Sans', 'Helvetica Neue', Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% -15%, rgba(229, 9, 20, 0.10), transparent 38%),
        radial-gradient(circle at 90% 10%, rgba(229, 9, 20, 0.05), transparent 30%),
        var(--nf-bg);
    color: #f5f5f5;
}

.block-container {
    max-width: 1380px;
    padding: 1.4rem 3rem 3.5rem 3rem;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

header[data-testid="stHeader"] {
    background: transparent;
}

/* Keyboard accessibility */
:focus-visible {
    outline: 2px solid var(--nf-red) !important;
    outline-offset: 2px;
}

/* Custom scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #0d0d0d; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--nf-red); }

/* =========================================================
   MOTION
   ========================================================= */

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes pulseDot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.45; transform: scale(0.8); }
}

@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
    .metric-card, .result-card, .recommendation-card { opacity: 1 !important; }
}

/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: #101010;
    border-right: 1px solid var(--nf-border);
}

section[data-testid="stSidebar"] .block-container {
    padding: 2.2rem 1.5rem;
}

.sidebar-logo {
    color: var(--nf-red);
    font-family: 'Bebas Neue', sans-serif;
    font-size: 30px;
    letter-spacing: 3px;
    margin-bottom: 4px;
}

.sidebar-tagline {
    color: #5a5a5a;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--nf-border) 20%, var(--nf-border) 80%, transparent);
    margin: 22px 0;
    border: none;
}

.sidebar-section {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #7d7d7d;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin: 22px 0 10px 0;
}

.sidebar-item {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #d8d8d8;
    font-size: 14px;
    font-weight: 500;
    margin: 7px 0;
}

.sidebar-item.active {
    color: #ffffff;
    font-weight: 700;
    background: rgba(229, 9, 20, 0.12);
    border-left: 3px solid var(--nf-red);
    padding: 7px 10px;
    border-radius: 0 6px 6px 0;
    margin-left: -13px;
}

.live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--nf-green);
    display: inline-block;
    animation: pulseDot 1.8s ease-in-out infinite;
    flex-shrink: 0;
}

.badge-pill {
    display: inline-block;
    background: rgba(70, 211, 105, 0.14);
    color: var(--nf-green);
    font-size: 12px;
    font-weight: 700;
    padding: 2px 9px;
    border-radius: 20px;
    margin-left: auto;
}

/* =========================================================
   HERO
   ========================================================= */

.hero { text-align: center; padding: 0.6rem 0 1.6rem 0; }

.hero-eyebrow {
    color: var(--nf-red);
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.main-title {
    color: #ffffff;
    font-family: 'Bebas Neue', 'Manrope', sans-serif;
    font-size: 68px;
    line-height: 1;
    letter-spacing: 5px;
    margin: 0;
}

.sub-title {
    color: #a3a3a3;
    font-size: 16px;
    font-weight: 500;
    line-height: 1.5;
    max-width: 560px;
    margin: 14px auto 0 auto;
}

/* Logo: rendered as our own <div><img></div> below (not st.image),
   so centering is plain, ordinary CSS on markup we fully control -
   no dependency on Streamlit's internal DOM/testids. */
.logo-wrap {
    display: flex;
    justify-content: center;
    margin: 0 auto 10px auto;
}

.logo-wrap img {
    filter: drop-shadow(0 4px 18px rgba(229, 9, 20, 0.35));
}

/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {
    color: #ffffff;
    font-size: 21px;
    font-weight: 800;
    letter-spacing: 0.3px;
    margin: 4px 0 20px 0;
    padding-left: 13px;
    border-left: 4px solid var(--nf-red);
}

.group-label {
    color: #6f6f6f;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin: 0 0 12px 0;
}

/* =========================================================
   INPUTS
   ========================================================= */

label { color: #cfcfcf !important; font-weight: 600 !important; }

.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #171717 !important;
    color: #ffffff !important;
    border: 1px solid #303030 !important;
    border-radius: 9px !important;
    min-height: 42px;
    transition: border-color 0.2s ease;
}

.stNumberInput input:focus,
.stSelectbox div[data-baseweb="select"]:focus-within > div {
    border-color: var(--nf-red) !important;
}

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--nf-red) !important;
    border-color: var(--nf-red) !important;
    box-shadow: 0 0 0 6px rgba(229, 9, 20, 0.15) !important;
}

/* =========================================================
   BUTTON
   ========================================================= */

.stButton > button {
    width: 100%;
    min-height: 54px;
    background: var(--nf-red) !important;
    color: #ffffff !important;
    border: 1px solid var(--nf-red) !important;
    border-radius: 9px !important;
    font-size: 16px !important;
    font-weight: 800 !important;
    letter-spacing: 0.8px;
    box-shadow: 0 8px 25px rgba(229, 9, 20, 0.2);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: var(--nf-red-bright) !important;
    border-color: var(--nf-red-bright) !important;
    color: #ffffff !important;
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(229, 9, 20, 0.32);
}

.stButton > button:active { transform: translateY(0); }

/* =========================================================
   CARDS
   ========================================================= */

.metric-card, .result-card, .recommendation-card {
    background: linear-gradient(145deg, #171717, #121212);
    border: 1px solid var(--nf-border);
    border-radius: 14px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
    /* Visible by default (opacity: 1). The animation below only ever
       ADDS a fade-in on top of that; it never depends on it, so if
       the animation is skipped or disabled (e.g. reduced-motion),
       the card is still fully visible instead of stuck invisible. */
    animation: fadeInUp 0.55s ease forwards;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.metric-card:hover, .result-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.38);
}

.metric-card { padding: 20px 18px; text-align: center; min-height: 112px; }

.metric-label {
    color: #888888;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 9px;
}

.metric-value {
    color: #ffffff;
    font-size: 25px;
    font-weight: 800;
    font-variant-numeric: tabular-nums;
}

.result-card { padding: 26px; text-align: center; border-top: 3px solid var(--nf-red); }

.result-title {
    color: #858585;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.result-value {
    font-size: 32px;
    font-weight: 800;
    font-variant-numeric: tabular-nums;
}

/* Risk meter */
.risk-label-row {
    display: flex;
    justify-content: space-between;
    color: #777777;
    font-size: 11px;
    font-weight: 600;
    margin-top: 8px;
}

.risk-container {
    background: #202020;
    border-radius: 20px;
    height: 16px;
    overflow: hidden;
}

.risk-bar {
    height: 100%;
    border-radius: 20px;
}

/* Recommendation */
.recommendation-card { border-left: 4px solid var(--nf-red); padding: 20px 22px; }

.recommendation-title {
    color: #ffffff;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 8px;
}

.recommendation-text { color: #bdbdbd; font-size: 14px; line-height: 1.65; }

/* Footer */
.app-footer {
    text-align: center;
    color: #4a4a4a;
    font-size: 11.5px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 46px;
}

div[data-testid="stVerticalBlock"] { gap: 0.65rem; }

</style>
""", unsafe_allow_html=True)


def divider():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# =========================================================
# LOAD MODEL AND DATA
# =========================================================

model = joblib.load("Netflix_Churn_Model.pkl")
scaler = joblib.load("scaler.pkl")
df = pd.read_csv("netflix_customer_churn.csv")

# =========================================================
# ENCODING MAPS
# =========================================================

gender_map = {value: index for index, value in enumerate(df["gender"].unique())}
subscription_map = {value: index for index, value in enumerate(df["subscription_type"].unique())}
region_map = {value: index for index, value in enumerate(df["region"].unique())}
device_map = {value: index for index, value in enumerate(df["device"].unique())}
payment_map = {value: index for index, value in enumerate(df["payment_method"].unique())}
genre_map = {value: index for index, value in enumerate(df["favorite_genre"].unique())}

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown('<div class="sidebar-logo">NETFLIX</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-tagline">Retention Intelligence</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">Dashboard</div>', unsafe_allow_html=True)
st.sidebar.markdown(
    '<div class="sidebar-item active">📊 Customer Prediction</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown('<div class="sidebar-section">Model</div>', unsafe_allow_html=True)
st.sidebar.markdown(
    '<div class="sidebar-item"><span class="live-dot"></span> XGBoost <span class="badge-pill">Live</span></div>',
    unsafe_allow_html=True
)
st.sidebar.markdown('<div class="sidebar-item">🎯 Accuracy: 99.5%</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-item">📈 ROC-AUC: 1.00</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">Dataset</div>', unsafe_allow_html=True)
st.sidebar.markdown(
    f'<div class="sidebar-item">🗂 Customers: {len(df):,}</div>',
    unsafe_allow_html=True
)
st.sidebar.markdown(
    f'<div class="sidebar-item">🧬 Features: {len(df.columns) - 2}</div>',
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================

# Render the logo as our own <img> (base64-embedded) inside a div
# we control, instead of st.image. st.image's wrapper markup varies
# across Streamlit versions, which is why centering it via CSS kept
# failing. A div with display:flex + justify-content:center around
# a plain <img> is ordinary, version-proof CSS.
with open("assets/netflix_logo.png", "rb") as _logo_file:
    _logo_base64 = base64.b64encode(_logo_file.read()).decode("utf-8")

st.markdown(
    f'<div class="logo-wrap"><img src="data:image/png;base64,{_logo_base64}" width="112" alt="Netflix logo"></div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Machine Learning · Retention Analytics</div>
    <div class="main-title">CHURN PREDICTION</div>
    <div class="sub-title">Estimate a subscriber's cancellation risk from their profile and viewing
    behavior, and get a tailored retention play in return.</div>
</div>
""", unsafe_allow_html=True)

divider()

# =========================================================
# CUSTOMER DETAILS
# =========================================================

st.markdown('<div class="section-title">Customer Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="group-label">Account</div>', unsafe_allow_html=True)

    age = st.number_input("Age", min_value=18, max_value=100, value=30)

    gender = st.selectbox("Gender", list(gender_map.keys()))

    subscription_type = st.selectbox(
        "🎬 Subscription Type",
        list(subscription_map.keys())
    )

    monthly_fee = st.number_input(
        "Monthly Fee",
        min_value=0.0,
        value=15.99
    )

    payment_method = st.selectbox(
        "💳 Payment Method",
        list(payment_map.keys())
    )

    region = st.selectbox("🌍 Region", list(region_map.keys()))

with col2:
    st.markdown('<div class="group-label">Usage &amp; Preferences</div>', unsafe_allow_html=True)

    device = st.selectbox("📱 Device", list(device_map.keys()))

    watch_hours = st.number_input(
        "Watch Hours",
        min_value=0.0,
        value=10.0
    )

    avg_watch_time_per_day = st.number_input(
        "Average Watch Time Per Day",
        min_value=0.0,
        value=2.5
    )

    last_login_days = st.number_input(
        "Last Login Days",
        min_value=0,
        value=5
    )

    number_of_profiles = st.slider(
        "Number of Profiles",
        min_value=1,
        max_value=5,
        value=2
    )

    favorite_genre = st.selectbox(
        "🎭 Favorite Genre",
        list(genre_map.keys())
    )

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# =========================================================
# PREDICT BUTTON
# =========================================================

predict = st.button("▶  Predict Churn", use_container_width=True)

# =========================================================
# PREDICTION
# =========================================================

if predict:

    input_data = pd.DataFrame([{
        "age": age,
        "gender": gender_map[gender],
        "subscription_type": subscription_map[subscription_type],
        "watch_hours": watch_hours,
        "last_login_days": last_login_days,
        "region": region_map[region],
        "device": device_map[device],
        "monthly_fee": monthly_fee,
        "payment_method": payment_map[payment_method],
        "number_of_profiles": number_of_profiles,
        "avg_watch_time_per_day": avg_watch_time_per_day,
        "favorite_genre": genre_map[favorite_genre]
    }])

    numerical_cols = [
        "age",
        "watch_hours",
        "last_login_days",
        "monthly_fee",
        "number_of_profiles",
        "avg_watch_time_per_day"
    ]

    input_data[numerical_cols] = scaler.transform(input_data[numerical_cols])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    probability_percent = probability * 100

    divider()

    # =====================================================
    # RESULT
    # =====================================================

    if prediction == 1:
        result_text = "HIGH CHURN RISK"
        result_color = "#E50914"
    else:
        result_text = "LOW CHURN RISK"
        result_color = "#46d369"

    st.markdown(f"""
    <div class="result-card" style="box-shadow: 0 14px 40px {result_color}26;">
        <div class="result-title">Prediction</div>
        <div class="result-value" style="color:{result_color};">
            {result_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # =====================================================
    # METRICS
    # =====================================================

    if probability_percent < 40:
        risk = "Low"
    elif probability_percent < 70:
        risk = "Medium"
    else:
        risk = "High"

    metric1, metric2, metric3 = st.columns(3, gap="medium")

    with metric1:
        st.markdown(f"""
        <div class="metric-card" style="animation-delay:0.05s;">
            <div class="metric-label">Churn Probability</div>
            <div class="metric-value">{probability_percent:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with metric2:
        st.markdown(f"""
        <div class="metric-card" style="animation-delay:0.12s;">
            <div class="metric-label">Risk Level</div>
            <div class="metric-value">{risk}</div>
        </div>
        """, unsafe_allow_html=True)

    with metric3:
        st.markdown("""
        <div class="metric-card" style="animation-delay:0.19s;">
            <div class="metric-label">Prediction Model</div>
            <div class="metric-value">XGBoost</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    # =====================================================
    # RISK METER
    # =====================================================

    st.markdown('<div class="section-title">Churn Risk Meter</div>', unsafe_allow_html=True)

    if probability_percent < 40:
        meter_color = "#46d369"
    elif probability_percent < 70:
        meter_color = "#f5c518"
    else:
        meter_color = "#E50914"

    st.markdown(f"""
    <div class="risk-container">
        <div class="risk-bar"
             style="width:{probability_percent}%; background:{meter_color};">
        </div>
    </div>

    <div class="risk-label-row">
        <span>Low</span>
        <span>Medium</span>
        <span>High</span>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    if probability_percent < 40:
        recommendation = (
            "The customer shows a low likelihood of churn. "
            "Continue engagement through personalized content "
            "and regular recommendations."
        )
    elif probability_percent < 70:
        recommendation = (
            "The customer shows a moderate likelihood of churn. "
            "Consider personalized recommendations, engagement "
            "campaigns, or targeted offers."
        )
    else:
        recommendation = (
            "The customer shows a high likelihood of churn. "
            "Consider immediate retention strategies such as "
            "personalized offers, plan benefits, or targeted "
            "re-engagement campaigns."
        )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="recommendation-card" style="animation-delay:0.25s;">
        <div class="recommendation-title">Retention Recommendation</div>
        <div class="recommendation-text">{recommendation}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="app-footer">Netflix · Retention Intelligence Platform</div>', unsafe_allow_html=True)
