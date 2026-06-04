import streamlit as st
import pandas as pd
import datetime

# Optimize page layout and hide default Streamlit clutter
st.set_page_config(
    layout="centered", 
    page_title="Alexandria Expedition",
    initial_sidebar_state="collapsed"
)

# Premium Custom CSS for an Atmospheric Dark Curation Terminal
st.markdown("""
    <style>
    /* Hide top header bars and menus for native app feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* App Background and Font Smoothing */
    .stApp {
        background-color: #0d0f12;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Compact Header Metrics Row */
    .dashboard-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(135deg, #161a22, #11141a);
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid #222a36;
        margin-bottom: 15px;
    }
    .dash-stat {
        text-align: center;
    }
    .dash-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #6c7a89;
        letter-spacing: 1px;
        margin-bottom: 2px;
    }
    .dash-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    /* The Vault Card (Glassmorphism effect) */
    .vault-card {
        background: #161a22;
        border: 1px solid #263244;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Premium Button Stylings Override */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        transition: all 0.2s ease-in-out !important;
        border: none !important;
    }
    /* Button variants */
    div.stButton > button[key^="btn_done"] { background-color: #1b4d3e !important; color: #a3e635 !important; }
    div.stButton > button[key^="btn_active"] { background-color: #1e3a8a !important; color: #60a5fa !important; }
    div.stButton > button[key^="btn_tbr"] { background-color: #5b21b6 !important; color: #c084fc !important; }
    div.stButton > button[key^="btn_dnf"] { background-color: #3f3f46 !important; color: #d4d4d8 !important; }
    </style>
""", unsafe_allow_html=True)

CSV_FILE = 'alexandria_audiobooks_clean_books.csv'

if 'df' not in st.session_state:
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        st.error(f"Could not find '{CSV_FILE}' in repository root.")
        st.stop()
        
    for col in ['status', 'acquisition', 'focus_metric', 'narrative_vibe', 'tagged_date']:
        if col not in df.columns:
            df[col] = None
    st.session_state.df = df

df = st.session_state.df

# --- DATA COMPILATION ---
total_books = len(df)
tagged_books = df['status'].notna().sum()
progress_percent = tagged_books / total_books if total_books > 0 else 1.0

xp_per_book = 25
total_xp = tagged_books * xp_per_book
current_level = (total_xp // 500) + 1
xp_into_level = total_xp % 500

# --- PREMIUM COMPACT DASHBOARD ---
st.markdown(f"""
    <div class="dashboard-row">
        <div class="dash-stat">
            <div class="dash-label">Expedition</div>
            <div class="dash-value">👑 LVL {current_level}</div>
        </div>
        <div class="dash-stat">
            <div class="dash-label">Progress</div>
            <div class="dash-value">⚔️ {tagged_books}/{total_books}</div>
        </div>
        <div class="dash-stat">
            <div class="dash-label">Next Level</div>
            <div class="dash-value">✨ {xp_into_level}/500 XP</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Subdued progress bar line
st.progress(progress_percent)

# --- THE ITEM ENCOUNTER ---
untagged_pool = df[df['status'].isna()]

if untagged_pool.empty:
    st.balloons()
    st.success("🎉 All audiobooks purified and cataloged!")
else:
    current_idx = untagged_pool.index[0]
    book = untagged_pool.iloc[0]
    
    # Styled Item Card Component
    duration_str = f" • {book['duration_human']}" if pd.notna(book['duration_human']) else ""
    st.markdown(f"""
        <div class="vault-card">
            <span style="color:#6c7a89; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Current Artifact</span>
            <h2 style="margin: 5px 0 2px 0; color:#ffffff; font-size:1.4rem; line-height:1.2;">{book['book_title']}</h2>
            <p style="margin:0; color:#94a3b8; font-size:1rem;">by {book['author']}{duration_str}</p>
        </div>
    """, unsafe_allow_html=True)
        
    st.caption("⚡ QUICK CHRONICLE")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎧 Listened / Done", use_container_width=True, key="btn_done"):
            st.session_state.df.at[current_idx, 'status'] = 'Completed'
            st.session_state.df.at[current_idx, 'tagged_date'] = datetime.date.today().isoformat()
            st.rerun()
        if st.button("⏳ Listening Now", use_container_width=True, key="btn_active"):
            st.session_state.df.at[current_idx, 'status'] = 'Listening'
            st.session_state.df.at[current_idx, 'tagged_date'] = datetime.date.today().isoformat()
            st.rerun()
    with c2:
        if st.button("🎯 Want to Listen", use_container_width=True, key="btn_tbr"):
            st.session_state.df.at[current_idx, 'status'] = 'Want to Listen'
            st.session_state.df.at[current_idx, 'tagged_date'] = datetime.date.today().isoformat()
            st.rerun()
        if st.button("❌ DNF / Skip", use_container_width=True, key="btn_dnf"):
            st.session_state.df.at[current_idx, 'status'] = 'DNF/Skipped'
            st.session_state.df.at[current_idx, 'tagged_date'] = datetime.date.today().isoformat()
            st.rerun()

    st.markdown("---")
    
    with st.expander("🔮 DEEP BLUEPRINT TAGS (BONUS XP)"):
        vibe = st.multiselect(
            "Select Core Archetypes:",
            ["Systemic Critique", "Dense Worldbuilding", "Philosophical Ambiguity", "Grimdark / Cynical", "Character Study", "Light / Comfort Listen"]
        )
        focus = st.radio(
            "Mental Bandwidth Required:",
            ["Chore Listen (Low Focus)", "Deep Focus Required (High Complexity)"]
        )
        source = st.selectbox(
            "Acquisition Pipeline:",
            ["Intentional Purchase", "Bulk Sourced / Hoarded", "Recommendation Target"]
        )

        if st.button("💾 Lock Deep Blueprint (+50 XP)", use_container_width=True, type="primary"):
            st.session_state.df.at[current_idx, 'status'] = 'Completed' if not vibe else 'Fully Documented'
            st.session_state.df.at[current_idx, 'narrative_vibe'] = ", ".join(vibe)
            st.session_state.df.at[current_idx, 'focus_metric'] = focus
            st.session_state.df.at[current_idx, 'acquisition'] = source
            st.session_state.df.at[current_idx, 'tagged_date'] = datetime.date.today().isoformat()
            st.rerun()

st.markdown("---")
csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Export Purified Ledger",
    data=csv_data,
    file_name='alexandria_audiobooks_clean_books.csv',
    mime='text/csv',
    use_container_width=True
)
