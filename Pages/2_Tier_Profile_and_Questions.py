import streamlit as st
import json

st.set_page_config(layout="wide")

# ----------- Load Data ----------- #
@st.cache_data
def load_roadmap():
    with open("roadmap_data.json") as f:
        return json.load(f)

roadmap = load_roadmap()

st.title("Tier Profile and Roadmap Setup")

# ----------- Check Onboarding Completion ----------- #
if "completed_tasks" not in st.session_state:
    st.warning("⚠️ Please complete the onboarding first.")
    st.stop()

completed_ids = set(st.session_state["completed_tasks"])

# ----------- Full NIST Tier Definitions ----------- #
tier_definitions = {
    1: """
### Tier 1: Partial

**Privacy Risk Management Process** – Organizational privacy risk management practices are not formalized, and risk is managed in an ad hoc and sometimes reactive manner. Prioritization of privacy activities may not be directly informed by organizational risk management priorities, privacy risk assessments, or mission or business objectives.

**Integrated Privacy Risk Management Program** – There is limited awareness of privacy risk at the organizational level. The organization implements privacy risk management on an irregular, case-by-case basis due to varied experience or information gained from outside sources. The organization may not have processes that enable the sharing of information about data processing and resulting privacy risks within the organization.

**Data Processing Ecosystem Relationships** – There is limited understanding of an organization’s role(s) in the larger ecosystem with respect to other entities (e.g., buyers, suppliers, service providers, business associates, partners). The organization does not have processes for identifying how privacy risks may proliferate throughout the ecosystem or for communicating privacy risks or requirements to other entities in the ecosystem.

**Workforce** – Some personnel may have a limited understanding of privacy risks or privacy risk management processes, but have no specific privacy responsibilities. If available, privacy training is ad hoc and the content is not kept current with best practices.
""",
    2: """
### Tier 2: Risk Informed

**Privacy Risk Management Process** – Risk management practices are approved by management but may not be established as organization-wide policy. Prioritization of privacy activities is directly informed by organizational risk management priorities, privacy risk assessments, or mission or business objectives.

**Integrated Privacy Risk Management Program** – There is an awareness of privacy risk at the organizational level, but an organization-wide approach to managing privacy risk has not been established. Information about data processing and resulting privacy risks is shared within the organization on an informal basis. Consideration of privacy in organizational objectives and programs may occur at some but not all levels of the organization. Privacy risk assessment occurs, but is not typically repeatable or reoccurring.

**Data Processing Ecosystem Relationships** – There is some understanding of an organization’s role(s) in the larger ecosystem with respect to other entities (e.g., buyers, suppliers, service providers, business associates, partners). The organization is aware of the privacy ecosystem risks associated with the products and services it provides and uses, but does not act consistently or formally upon those risks.

**Workforce** – There are personnel with specific privacy responsibilities, but they may have non-privacy responsibilities as well. Privacy training is conducted regularly for privacy personnel, although there is no consistent process for updates on best practices.
""",
    3: """
### Tier 3: Repeatable

**Privacy Risk Management Process** – The organization’s risk management practices are formally approved and expressed as policy. Organizational privacy practices are regularly updated based on the application of risk management processes to changes in mission or business objectives and a changing risk, policy, and technology landscape.

**Integrated Privacy Risk Management Program** – There is an organization-wide approach to manage privacy risk. Risk-informed policies, processes, and procedures are defined, implemented as intended, and reviewed. Consistent methods are in place to respond effectively to changes in risk. Senior privacy and non-privacy executives communicate regularly regarding privacy risk. Senior executives ensure consideration of privacy through all lines of operation in the organization.

**Data Processing Ecosystem Relationships** – The organization understands its role(s), dependencies, and dependents in the larger ecosystem and may contribute to the community’s broader understanding of risks. The organization is aware of the privacy ecosystem risks associated with the products and services it provides and uses. Additionally, it usually acts formally upon those risks, including mechanisms such as written agreements to communicate privacy requirements, governance structures, and policy implementation and monitoring.

**Workforce** – Dedicated privacy personnel possess the knowledge and skills to perform their appointed roles and responsibilities. There is regular, up-to-date privacy training for all personnel.
""",
    4: """
### Tier 4: Adaptive

**Privacy Risk Management Process** – The organization adapts its privacy practices based on lessons learned from privacy events, and identification of new privacy risks. Through a process of continuous improvement incorporating advanced privacy technologies and practices, the organization actively adapts to a changing policy and technology landscape and responds in a timely and effective manner to evolving privacy risks.

**Integrated Privacy Risk Management Program** – There is an organization-wide approach to managing privacy risk that uses risk-informed policies, processes, and procedures to address problematic data actions. The relationship between privacy risk and organizational objectives is clearly understood and considered when making decisions. Senior executives monitor privacy risk in the same context as cybersecurity risk, financial risk, and other organizational risks. The organizational budget is based on an understanding of the current and predicted risk environment and risk tolerance. Business units implement executive vision and analyze system-level risks in the context of the organizational risk tolerances. Privacy risk management is part of the organizational culture and evolves from lessons learned and continuous awareness of data processing and resulting privacy risks. The organization can quickly and efficiently account for changes to business/mission objectives in how risk is approached and communicated.

**Data Processing Ecosystem Relationships** – The organization understands its role(s), dependencies, and dependents in the larger ecosystem and contributes to the community’s broader understanding of risks. The organization uses real-time or near-real-time information to understand and consistently act upon privacy ecosystem risks associated with the products and services it provides and it uses. Additionally, it communicates proactively, using formal (e.g., agreements) and informal mechanisms to develop and maintain strong ecosystem relationships.

**Workforce** – The organization has specialized privacy skillsets throughout the organizational structure; personnel with diverse perspectives contribute to the management of privacy risks. There is regular, up-to-date, specialized privacy training for all personnel. Personnel at all levels understand the organizational privacy values and their role in maintaining them.
"""
}

# ----------- Calculate Overall Tier ----------- #
overall_tier = 0
for tier in range(1, 5):
    tier_tasks = [t for t in roadmap if t["tier"] == tier]
    if tier_tasks and all(t["id"] in completed_ids for t in tier_tasks):
        overall_tier = tier
    else:
        break

st.session_state["overall_tier"] = overall_tier

# ----------- Display Overall Tier ----------- #
st.subheader("🎯 Your Overall Tier")

if overall_tier > 0:
    st.success(f"You have achieved **Tier {overall_tier}**")
    st.markdown(tier_definitions[overall_tier])
else:
    st.warning("❌ No overall tier achieved yet.")
    st.info("Complete all Tier 1 tasks to unlock Tier 1 status.")

# ----------- Roadmap Setup Questions ----------- #
st.divider()
st.subheader("🧩 Roadmap Setup Questions")

with st.form("roadmap_questions"):
    q1 = st.radio("1. Do you collect personal information from third parties?", ["Yes", "No"])
    q2 = st.radio("2. Do you disclose information to third parties?", ["Yes", "No"])
    q3 = st.radio("3. Do you determine the purposes and means of the personal information you process?", ["Yes", "No"])

    certificate = st.radio("4. Are you pursuing a certification?", ["SOC 2", "None"])
    st.caption("Only SOC 2 is available for now. More will be added soon.")

    custom_targets = {}
    categories = sorted(set(t["category"] for t in roadmap))

    if certificate == "None":
        st.markdown("### 🎯 Choose Your Target Tier Per Category")
        for category in categories:
            selected = st.selectbox(
                f"{category}",
                options=[1, 2, 3, 4],
                index=0,
                key=f"target_tier_{category}"
            )
            custom_targets[category] = selected

    submitted = st.form_submit_button("Generate My Roadmap")

# ----------- Save Questions to Session ----------- #
if submitted:
    st.session_state["questions"] = {
        "third_party_collection": q1 == "Yes",
        "third_party_disclosure": q2 == "Yes",
        "is_controller": q3 == "Yes",
        "certificate": certificate,
        "custom_targets": custom_targets
    }
    st.success("✅ Responses saved! You can now continue to your roadmap.")
