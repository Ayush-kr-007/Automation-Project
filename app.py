import streamlit as st
from main import get_all_ids, fetch_profile_details, clean_profiles
from ai_engine import analyze_and_generate

st.set_page_config(page_title="AI Outreach Tool", layout="wide")

st.title("🚀 AI Startup Outreach Tool")

# -------------------------------
# USER INPUT
# -------------------------------
st.sidebar.header("Search")

num_pages = st.sidebar.slider("Pages to scan", 1, 10, 2)
run_button = st.sidebar.button("Find Startups")

# -------------------------------
# FETCH DATA
# -------------------------------
if run_button:
    with st.spinner("Fetching startups..."):
        ids = get_all_ids(max_pages=num_pages)
        profiles = fetch_profile_details(ids)
        df = clean_profiles(profiles)

    st.session_state["df"] = df
    st.success(f"Found {len(df)} startups")

# -------------------------------
# LOAD DATA
# -------------------------------
df = st.session_state.get("df", None)

# -------------------------------
# FILTER UI
# -------------------------------
if df is not None and not df.empty:

    industries = sorted(df["industry"].dropna().unique())

    if len(industries) > 0:
        selected_industry = st.selectbox("Filter by Industry", industries)
        df = df[df["industry"] == selected_industry]

    keyword = st.text_input("Keyword (optional)")

    if keyword:
        df = df[df["idea"].str.lower().str.contains(keyword.lower(), na=False)]

    st.write(f"### Showing {len(df)} startups")

    df = df.head(3)  # ⚠️ keep low (free API)

    # -------------------------------
    # DISPLAY + AI
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

                if f"res_{i}" not in st.session_state:
                    lead = row.to_dict()

                    with st.spinner("Thinking..."):
                        result = analyze_and_generate(lead)

                    st.session_state[f"res_{i}"] = result

            # SHOW RESULT
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