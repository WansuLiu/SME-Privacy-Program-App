import streamlit as st
import json
import pandas as pd
import markdown


st.set_page_config(layout="wide")
st.title("👤 Privacy Program Profile")
st.divider()
st.subheader("Data Map Upload (Optional)")

uploaded_file = st.file_uploader("Upload your data map (PNG, JPG, SVG)", type=["png", "jpg", "jpeg", "svg"])

if uploaded_file:
    st.image(uploaded_file, caption="📌 Your Data Map", use_column_width=True)
    st.session_state["data_map_image"] = uploaded_file

# ----------- Load Data ----------- #
@st.cache_data
def load_roadmap():
    with open("roadmap_data.json") as f:
        return json.load(f)

@st.cache_data
def load_milestones():
    return pd.read_csv("SOC 2 to NIST Privacy Framework - Milestone Descriptions.csv")

roadmap = load_roadmap()
milestones = load_milestones().set_index("Task Category")

# ----------- Tier Definitions (Overall) ----------- #
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


# ----------- Check Session State ----------- #
if "completed_tasks" not in st.session_state or "questions" not in st.session_state:
    st.warning("⚠️ Please complete onboarding and roadmap setup first.")
    st.stop()

completed_ids = set(st.session_state["completed_tasks"])
questions = st.session_state["questions"]
custom_targets = questions.get("custom_targets", {})
is_controller = questions.get("is_controller", True)

# ----------- Role Filter ----------- #
def role_matches(task_type: str):
    task_type = task_type.lower()
    if "controller & processor" in task_type:
        return True
    if is_controller and "controller" in task_type:
        return True
    if not is_controller and "processor" in task_type:
        return True
    return False

def should_include(task):
    if task.get("third_party_collection") and not questions.get("third_party_collection"):
        return False
    if task.get("third_party_disclosure") and not questions.get("third_party_disclosure"):
        return False
    if not role_matches(task.get("type", "")):
        return False
    return True

# ----------- Calculate Overall Tier ----------- #
overall_tier = 0
for tier in range(1, 5):
    tier_tasks = [t for t in roadmap if t["tier"] == tier and should_include(t)]
    if tier_tasks and all(t["id"] in completed_ids for t in tier_tasks):
        overall_tier = tier
    else:
        break

# ----------- Calculate Category Tiers ----------- #
categories = sorted(set(t["category"] for t in roadmap))
category_tiers = {}

for category in categories:
    max_tier = 0
    for tier in range(1, 5):
        tier_tasks = [
            t for t in roadmap
            if t["category"] == category and t["tier"] == tier and should_include(t)
        ]
        if tier_tasks and all(t["id"] in completed_ids for t in tier_tasks):
            max_tier = tier
        else:
            break
    category_tiers[category] = max_tier

# ----------- Display Overall Tier ----------- #
st.subheader("Overall Tier")
if overall_tier > 0:
    st.success(f"You have achieved **Tier {overall_tier}**")
    st.markdown(tier_definitions[overall_tier])
else:
    st.warning("❌ No overall tier achieved yet.")
    st.info("Once Tier 1 tasks are complete, your tier status will update.")

# ----------- Category Tier Details ----------- #
st.divider()
st.subheader("Category-Specific Progress")

for category in categories:
    current_tier = category_tiers.get(category, 0)
    st.markdown(f"### 📁 {category}")
    if current_tier == 0:
        st.info("No tier achieved for this category yet.")
        continue

    for t in range(1, current_tier + 1):
        desc = milestones.loc[category, f"Tier {t}"]
        if pd.notna(desc) and desc.strip() != "-":
            st.markdown(f"**Tier {t}:** {desc.strip()}")

# ----------- Next Tier Goals ----------- #
st.divider()
st.subheader("🧭 What We Are Aiming Now")

# --- 1. Next Overall Tier ---
if overall_tier < 4:
    next_tier = overall_tier + 1
    st.markdown(f"### Next Overall Target: Tier {next_tier}")
    st.markdown(tier_definitions[next_tier])
else:
    st.success("You have achieved the highest overall tier (Tier 4)!")

# --- 2. Per Category: Next Unachieved Tier Descriptions ---
remaining_targets = {
    cat: tier + 1 for cat, tier in category_tiers.items()
    if tier < 4 and pd.notna(milestones.loc[cat, f"Tier {tier + 1}"])
}

if remaining_targets:
    st.markdown("### Category-Specific Next Milestones")

    for cat, next_t in remaining_targets.items():
        desc = milestones.loc[cat, f"Tier {next_t}"]
        if isinstance(desc, str) and desc.strip() and desc.strip() != "-":
            st.markdown(f"**{cat} → Tier {next_t}**")
            st.markdown(desc.strip())
else:
    st.success("You’ve completed all tier descriptions across all categories!")

import base64
from io import BytesIO
from xhtml2pdf import pisa

def export_profile_to_pdf(html_content):
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html_content.encode("utf-8")), dest=pdf)
    return pdf.getvalue()

def image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode()

# Export button
st.divider()
if st.button("📥 Export This Profile as PDF"):
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 2em;
            color: #333;
        }}
        h1 {{
            color: #111;
            border-bottom: 2px solid #ccc;
            padding-bottom: 0.3em;
        }}
        h2 {{
            color: #222;
            margin-top: 1.5em;
            border-left: 4px solid #4CAF50;
            padding-left: 0.5em;
        }}
        h3 {{
            color: #333;
            margin-top: 1em;
        }}
        .tier-card {{
            background-color: #f2f2f2;
            padding: 1em;
            margin: 1em 0;
            border-left: 6px solid #2196F3;
        }}
        .category {{
            margin-top: 1.5em;
        }}
        .category h4 {{
            margin-bottom: 0.2em;
            color: #444;
        }}
        .milestone {{
            margin-bottom: 0.8em;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin-top: 1em;
            border: 1px solid #ccc;
        }}
    </style>
</head>
<body>
    {f'<img src="data:image/png;base64,{image_to_base64(st.session_state["data_map_image"])}" alt="Data Map"/>' if "data_map_image" in st.session_state else ""}

    <h1>👤 Privacy Program Profile</h1>
      {f'<img src="data:image/png;base64,{image_to_base64(st.session_state["data_map_image"])}" alt="Data Map"/>' if "data_map_image" in st.session_state else ""}

    <h2>🎯 Overall Tier</h2>
    <div class="tier-card">
        <strong>Tier {overall_tier}</strong><br/>
       {markdown.markdown(tier_definitions.get(overall_tier, ""))}
    </div>

    <h2>Category-Specific Progress</h2>
    {''.join(
        f'<div class="category"><h3>📁 {cat}</h3>' +
        ''.join(
            f'<div class="milestone"><strong>Tier {i}:</strong> {milestones.loc[cat, f"Tier {i}"]}</div>'
            for i in range(1, t+1)
            if pd.notna(milestones.loc[cat, f"Tier {i}"]) and milestones.loc[cat, f"Tier {i}"].strip() != "-"
        ) + '</div>'
        for cat, t in category_tiers.items() if t > 0
    )}

    <h2>🧭 What We Are Aiming Now</h2>
   {
    f'<div class="tier-card"><h3>Next Overall Tier: Tier {overall_tier + 1}</h3>{markdown.markdown(tier_definitions[overall_tier + 1])}</div>'
    if overall_tier < 4
    else '<p>🎉 You have achieved the highest overall tier!</p>'
}


    {''.join(
        f'<div class="category"><h4>{cat} → Tier {nt}</h4><div class="milestone">{milestones.loc[cat, f"Tier {nt}"]}</div></div>'
        for cat, nt in remaining_targets.items()
        if pd.notna(milestones.loc[cat, f"Tier {nt}"]) and milestones.loc[cat, f"Tier {nt}"].strip() != "-"
    )}

</body>
</html>
"""

    # Generate PDF
    pdf_bytes = export_profile_to_pdf(html)
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="privacy_profile.pdf">📄 Download PDF Report</a>'
    st.markdown(href, unsafe_allow_html=True)
