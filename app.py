import streamlit as st
from main import get_all_ids, fetch_profile_details, clean_profiles
from ai_engine import analyze_and_generate
import os
import pandas as pd

st.set_page_config(page_title="AI Outreach Tool", layout="wide")

st.title("🚀 AI Startup Outreach Tool")

# -------------------------------
# STATE
# -------------------------------
if "df" not in st.session_state:
    st.session_state["df"] = None



OUTPUT_FILE = "startup_leads.csv"

def save_result(lead):
    df = pd.DataFrame([lead])

    if os.path.exists(OUTPUT_FILE):
        df.to_csv(OUTPUT_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(OUTPUT_FILE, index=False)
# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("Search")
num_pages = st.sidebar.slider("Pages to scan", 1, 10, 3)
run_button = st.sidebar.button("Find Startups")

# -------------------------------
# FETCH
# -------------------------------

if run_button:
    with st.spinner("Fetching startups..."):
        ids = get_all_ids(max_pages=num_pages)
        profiles = fetch_profile_details(ids)
        df = clean_profiles(profiles)

        # 🔥 SAVE RAW DATA
        df.to_csv("raw_startups.csv", index=False)

    st.session_state["df"] = df
    st.success(f"Found {len(df)} startups")


df = st.session_state["df"]

# -------------------------------
# FILTER
# -------------------------------
if df is not None and not df.empty:

    industries = sorted(df["industry"].dropna().unique()) if "industry" in df.columns else []

    if industries:
        selected_industry = st.selectbox("Filter by Industry", industries)
        df = df[df["industry"] == selected_industry]

    keyword = st.text_input("Keyword (optional)")

    if keyword:
        df = df[df["idea"].str.lower().str.contains(keyword.lower(), na=False)]

    st.write(f"### Showing {len(df)} startups")

    # 🔥 LIMIT (save quota)
    df = df.head(5)

    # -------------------------------
    # DISPLAY
    # -------------------------------
    for i, row in df.iterrows():
        st.divider()
        col1, col2 = st.columns([2, 3])

        with col1:
            st.subheader(row["name"])
            st.write(row["idea"])
            st.caption(row.get("website", ""))

        with col2:
            if st.button(f"Generate Insights {i}", key=f"btn_{i}"):

                # 🔒 prevent re-calling API
                if f"res_{i}" not in st.session_state:

                    lead = row.to_dict()

                    with st.spinner("Thinking..."):
                        result = analyze_and_generate(lead)

                        # merge original + generated
                        full_data = {**lead, **result}

                        # 💾 SAVE TO FILE
                        save_result(full_data)

                    st.session_state[f"res_{i}"] = full_data

            # -------------------------------
            # SHOW RESULT
            # -------------------------------
            if f"res_{i}" in st.session_state:
                res = st.session_state[f"res_{i}"]

                st.markdown("**Pain Point**")
                st.write(res.get("pain_point", ""))

                st.markdown("**Automation Idea**")
                st.write(res.get("automation_idea", ""))

                st.markdown("**Email**")
                st.code(res.get("generated_email", ""))

else:
    st.info("Click 'Find Startups' to begin")