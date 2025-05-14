import streamlit as st
import json

# --- Load roadmap data ---
@st.cache_data
def load_roadmap():
    with open("roadmap_data.json", "r") as f:
        return json.load(f)

roadmap = load_roadmap()

# ✅ Sort roadmap by tier before display
roadmap.sort(key=lambda x: x["tier"])

st.title("Your Roadmap")

# --- Validate session state ---
if "questions" not in st.session_state or "completed_tasks" not in st.session_state:
    st.warning("Please complete onboarding and tier profile first.")
    st.stop()

completed = set(st.session_state["completed_tasks"])
questions = st.session_state["questions"]
custom_targets = questions.get("custom_targets", {})

# --- Role filter options (with 'All Roles' option) ---
user_roles = ["All Roles", "Process Manager", "Operations Level", "Executive Level"]
selected_role = st.selectbox("Filter tasks by role (optional):", user_roles)

# --- Prepare roadmap display ---
st.subheader("📋 Remaining Tasks")
new_completions = []
roadmap_displayed = False

for task in roadmap:
    task_id = task["id"]
    category = task["category"]
    tier = task["tier"]
    role = task.get("role", "")
    task_type = task.get("type", "").lower()

    # Skip completed tasks
    if task_id in completed:
        continue

    # Skip if tier exceeds selected target
    if custom_targets:
        max_tier = custom_targets.get(category, 4)
        if tier > max_tier:
            continue

    # --- ✅ Skip by role only if a specific role is selected ---
    if selected_role != "All Roles" and selected_role.lower() not in role.lower():
        continue

    # Skip based on third-party and controller logic
    if task.get("third_party_collection") and not questions.get("third_party_collection"):
        continue
    if task.get("third_party_disclosure") and not questions.get("third_party_disclosure"):
        continue
    if "controller" in task_type and not questions.get("is_controller"):
        continue

    # Show the task
    roadmap_displayed = True
    label = f"**[{category}] (Tier {tier})** {task['task']}"
    checked = st.checkbox(label, key=f"todo_{task_id}")
    if checked:
        new_completions.append(task_id)

# --- Update session state if needed ---
if new_completions:
    st.session_state["completed_tasks"] = list(completed.union(new_completions))

# --- Feedback if all done ---
if not roadmap_displayed:
    st.success("🎉 All tasks for your selected filters and target tiers are complete!")
