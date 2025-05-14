import streamlit as st

st.set_page_config(layout="wide")

import json
import pandas as pd

# ------------------ Load Data ------------------ #
@st.cache_data
def load_roadmap():
    with open("roadmap_data.json", "r") as f:
        return json.load(f)

@st.cache_data
def load_tier_descriptions():
    return pd.read_csv("SOC 2 to NIST Privacy Framework - Milestone Descriptions.csv")

roadmap = load_roadmap()
tier_df = load_tier_descriptions()

st.title("Onboarding: Answer Questions to Assess Your Privacy Tier")
st.markdown("### For each category, select the **highest tier** you've completed. All lower tiers will be included.")

selected_tiers = {}
completed_ids = []

with st.form("tier_selection_form"):
    for _, row in tier_df.iterrows():
        category = row["Task Category"]

        # Identify available tiers
        available_tiers = {
            tier: str(row.get(f"Tier {tier}", "")).strip()
            for tier in range(1, 5)
            if pd.notna(row.get(f"Tier {tier}")) and str(row.get(f"Tier {tier}")).strip() != "-"
        }

        if not available_tiers:
            continue

        st.markdown(f"---\n### {category}")
        for tier, desc in available_tiers.items():
            st.markdown(f"**Tier {tier}:** {desc}")

        # Build choices: always allow "0: Not started"
        tier_choices = [0] + sorted(available_tiers.keys())
        tier_labels = {0: "0: Not started", **{t: f"{t}: Tier {t}" for t in available_tiers}}

        selected = st.selectbox(
            "Select highest tier completed:",
            options=tier_choices,
            format_func=lambda x: tier_labels[x],
            key=f"select_{category}"
        )

        selected_tiers[category] = selected

    submitted = st.form_submit_button("🎯 Generate My Profile")

# ------------------ Submission Logic ------------------ #
if submitted:
    for category, selected_tier in selected_tiers.items():
        for task in roadmap:
            if task["category"] == category and int(task["tier"]) <= selected_tier:
                completed_ids.append(task["id"])

    st.session_state["completed_tasks"] = list(set(completed_ids))
    st.success("✅ Profile generated! You can now continue to Tier Profile.")
