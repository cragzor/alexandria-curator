import streamlit as st
import pandas as pd
import datetime

# Set mobile-friendly layout
st.set_page_config(layout="centered", page_title="Alexandria Expedition")

CSV_FILE = 'alexandria_audiobooks_clean_books.csv'

# Initialize dataset in session state so progress persists during your session
if 'df' not in st.session_state:
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        st.error(f"Could not find '{CSV_FILE}'. Please upload it to your GitHub repository root!")
        st.stop()
        
    # Ensure tracking columns exist
    for col in ['status', 'acquisition', 'focus_metric', 'narrative_vibe', 'tagged_date']:
        if col not in df.columns:
            df[col] = None
    st.session_state.df = df

df = st.session_state.df

# --- GAMIFICATION ENGINE ---
total_books = len(df)
tagged_books = df['status'].notna().sum()
untagged_books = total_books - tagged_books
progress_percent = tagged_books / total_books if total_books > 0 else 1.0

# Calculate Experience Points (XP) and Levels
xp_per_book = 25
total_xp = tagged_books * xp_per_book
current_level = (total_xp // 500) + 1
xp_into_level = total_xp % 500

# --- MOBILE UI HEADER ---
st.title("⚔️ Alexandria Expedition")
st.caption("iPhone 15 Pro Max Curation Terminal")

# Progress Dashboard
col1, col2 = st.columns(2)
with col1:
    st.metric("Expedition Level", f"LVL {current_level}")
with col2:
    st.metric("Books Chronicled", f"{tagged_books} / {total_books}")

st.progress(progress_percent, text=f"Data Purified: {progress_percent:.1%}")
st.write(f"🌟 **{xp_into_level} / 500 XP** to next level")
st.markdown("---")

# --- THE ENCOUNTER (Find next untagged book) ---
untagged_pool = df[df['status'].isna()]

if untagged_pool.empty:
    st.balloons()
    st.success("🎉 Victory! The entire library is fully chronicled and purified!")
else:
    # Pull the top item from the untagged stack
    current_idx = untagged_pool.index[0]
    book = untagged_pool.iloc[0]
    
    # Card Display
    st.subheader(f"📖 {book['book_title']}")
    st.write(f"**Author:** {book['author']}")
    if pd.notna(book['duration_human']):
        st.caption(f"⏱️ Length: {book['duration_human']}")
        
    st.markdown("### 1. Engagement Status")
    # Quick-tap grid for status
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
    # Multi-select contextual tags for advanced depth before saving
    st.markdown("### 2. Narrative Blueprint (Optional Extra XP)")
    
    vibe = st.multiselect(
        "Select Core Archetypes:",
        ["Systemic Critique", "Dense Worldbuilding", "Philosophical Ambiguity", "Grimdark / Cynical", "Character Study", "Light / Comfort Listen"]
    )
    
    focus = st.radio(
        "Mental Bandwidth Required:",
        ["Chore Listen (Low Focus)", "Deep Focus Required (High Complexity)"],
        index=0
    )
    
    source = st.selectbox(
        "Acquisition Pipeline:",
        ["Intentional Purchase", "Bulk Sourced / Hoarded", "Recommendation Target"]
    )

    if st.button("💾 Lock Tags & Claim Bonus XP (+50 XP)", use_container_width=True, type="primary"):
        st.session_state.df.at[current_idx, 'status'] = 'Completed' if not vibe else 'Fully Documented'
        st.session_state.df.at[current_idx, 'narrative_vibe'] = ", ".join(vibe)
        st.session_state.df.at[current_idx, 'focus_metric'] = focus
        st.session_state.df.at[current_idx, 'acquisition'] = source
        st.session_state.df.at[current_idx, 'tagged_date'] = datetime.date.today().isoformat()
        st.success("Bonus XP Claimed!")
        st.rerun()

st.markdown("---")
st.markdown("### 📥 Save Your Progress")
st.caption("Since we are running in the cloud, tap below to download your updated database back to your device whenever you want to save your session.")

csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Updated CSV",
    data=csv_data,
    file_name='alexandria_audiobooks_clean_books.csv',
    mime='text/csv',
    use_container_width=True
)
