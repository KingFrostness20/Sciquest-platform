import streamlit as st
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION & STYLING (Dark Gaming Theme)
# ==========================================
st.set_page_config(
    page_title="SciQuest: RPG Scientific Learning",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0e1117; color: #c9d1d9; }
    .sidebar .sidebar-content { background-color: #161b22; }
    .stButton>button {
        background: linear-gradient(45deg, #238636, #2ea043);
        color: white; border: none; border-radius: 6px;
        padding: 0.5rem 1rem; font-weight: bold;
    }
    .card {
        background-color: #161b22; border: 1px solid #30363d;
        padding: 20px; border-radius: 10px; margin-bottom: 15px;
    }
    .metric-card {
        background-color: #21262d; border: 1px solid #30363d;
        padding: 15px; border-radius: 8px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA PERSISTENCE (JSON Save System)
# ==========================================
SAVE_FILE = "player_save.json"

DEFAULT_DATA = {
    "player_name": "Novice Researcher",
    "level": 1,
    "xp": 0,
    "next_level_xp": 100,
    "completed_quests": [],
    "unlocked_quests": ["q1_bio", "q1_mat"],
    "skills": {
        "Biotechnology": {"DNA Analysis": 0, "Cell Growth": 0, "Fermentation": 0, "Enzyme Kinetics": 0,
                          "Bioprocess Engineering": 0},
        "Materials Science": {"Mechanical Properties": 0, "Stress and Strain": 0, "Material Characterization": 0,
                              "Tensile Testing": 0, "Material Selection": 0}
    },
    "achievements": []
}


def load_game():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            return DEFAULT_DATA
    return DEFAULT_DATA


def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)


if "game_data" not in st.session_state:
    st.session_state.game_data = load_game()

data = st.session_state.game_data

# ==========================================
# QUEST DATABASE
# ==========================================
QUESTS = {
    "q1_bio": {
        "title": "Mission 1: DNA Nucleotide Composition",
        "domain": "Biotechnology", "level": "Beginner", "skill": "DNA Analysis",
        "description": "Analyze a viral DNA sequence to determine the total length and count of Adenine (A), Thymine (T), Guanine (G), and Cytosine (C).",
        "objective": "Calculate the percentage of Adenine in the sequence: 'ATCGATCGATCGTACG'",
        "xp": 50, "answer_type": "float", "correct_answer": 25.0, "tolerance": 1.0, "unlocks": ["q2_bio"]
    },
    "q2_bio": {
        "title": "Mission 2: GC Content Calculation",
        "domain": "Biotechnology", "level": "Beginner", "skill": "DNA Analysis",
        "description": "GC content affects DNA thermal stability. Higher GC content requires higher melting temperatures.",
        "objective": "Calculate GC content percentage for sequence: 'GCGCATATGCGCATAT'. Enter the percentage.",
        "xp": 75, "answer_type": "float", "correct_answer": 50.0, "tolerance": 1.0, "unlocks": ["q3_bio"]
    },
    "q3_bio": {
        "title": "Mission 3: Bacterial Population Growth",
        "domain": "Biotechnology", "level": "Intermediate", "skill": "Cell Growth",
        "description": "Simulate exponential growth of E. coli in a batch culture.",
        "objective": "If initial population N0 = 1000 cells and generation time is 30 mins, what is the population after 120 minutes?",
        "xp": 100, "answer_type": "int", "correct_answer": 16000, "tolerance": 10, "unlocks": ["q4_bio"]
    },
    "q4_bio": {
        "title": "Mission 4: Enzyme Kinetics (Michaelis-Menten)",
        "domain": "Biotechnology", "level": "Advanced", "skill": "Enzyme Kinetics",
        "description": "Calculate reaction velocity (v) given Vmax = 100 µmol/min, Km = 5 mM, and Substrate concentration [S] = 5 mM.",
        "objective": "Calculate v using v = (Vmax * [S]) / (Km + [S]). Enter the velocity in µmol/min.",
        "xp": 150, "answer_type": "float", "correct_answer": 50.0, "tolerance": 1.0, "unlocks": ["q_combined"]
    },
    "q1_mat": {
        "title": "Mission 1: Engineering Stress Calculation",
        "domain": "Materials Science", "level": "Beginner", "skill": "Stress and Strain",
        "description": "Calculate the engineering stress experienced by a titanium alloy rod under axial tension.",
        "objective": "If axial force F = 50,000 N and cross-sectional area A = 0.0005 m², what is the stress in MPa?",
        "xp": 50, "answer_type": "float", "correct_answer": 100.0, "tolerance": 1.0, "unlocks": ["q2_mat"]
    },
    "q2_mat": {
        "title": "Mission 2: Engineering Strain Determination",
        "domain": "Materials Science", "level": "Beginner", "skill": "Mechanical Properties",
        "description": "Determine strain when an initial gauge length of 50 mm extends by 0.5 mm under load.",
        "objective": "Calculate engineering strain percentage. Enter the percentage strain.",
        "xp": 75, "answer_type": "float", "correct_answer": 1.0, "tolerance": 0.1, "unlocks": ["q3_mat"]
    },
    "q3_mat": {
        "title": "Mission 3: Young's Modulus Calculation",
        "domain": "Materials Science", "level": "Intermediate", "skill": "Tensile Testing",
        "description": "Hooke's Law in elastic deformation: Stress = Young's Modulus (E) * Strain.",
        "objective": "If stress is 200 MPa and strain is 0.002, calculate Young's Modulus E in GPa.",
        "xp": 100, "answer_type": "float", "correct_answer": 100.0, "tolerance": 1.0, "unlocks": ["q4_mat"]
    },
    "q4_mat": {
        "title": "Mission 4: Yield Strength Analysis",
        "domain": "Materials Science", "level": "Advanced", "skill": "Material Characterization",
        "description": "Analyze tensile test data points to find the 0.2% offset yield strength.",
        "objective": "Find approximate yield strength where plastic strain reaches 0.002 at 250 MPa. Enter 250.",
        "xp": 150, "answer_type": "float", "correct_answer": 250.0, "tolerance": 5.0, "unlocks": ["q_combined"]
    },
    "q_combined": {
        "title": "Final Mission: Bioreactor Material Selection & Optimization",
        "domain": "Combined", "level": "Advanced", "skill": "Bioprocess Engineering",
        "description": "Select structural material for a 5000L stainless steel bioreactor.",
        "objective": "Calculate required wall thickness given pressure P = 1.2 MPa, radius r = 0.8 m, and allowable stress σ = 150 MPa using t = (P * r) / σ. Enter thickness in mm.",
        "xp": 300, "answer_type": "float", "correct_answer": 6.4, "tolerance": 0.2, "unlocks": []
    }
}

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🧬 SciQuest Platform")
st.sidebar.markdown(f"**Player:** {data['player_name']}")
st.sidebar.markdown(f"**Level:** {data['level']} | **XP:** {data['xp']}/{data['next_level_xp']}")
st.sidebar.progress(data['xp'] / data['next_level_xp'])
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation",
                        ["Dashboard", "Campaigns & Quests", "Skill Trees", "Interactive Laboratory", "Profile & Save"])


def add_xp(amount, quest_id, skill_name, domain):
    if quest_id not in data["completed_quests"]:
        data["completed_quests"].append(quest_id)
        data["xp"] += amount
        if domain in data["skills"] and skill_name in data["skills"][domain]:
            data["skills"][domain][skill_name] = min(100, data["skills"][domain][skill_name] + 25)
        elif domain == "Combined":
            for d in data["skills"]:
                for s in data["skills"][d]:
                    data["skills"][d][s] = min(100, data["skills"][d][s] + 15)
        if quest_id in QUESTS:
            for next_q in QUESTS[quest_id]["unlocks"]:
                if next_q not in data["unlocked_quests"] and next_q not in data["completed_quests"]:
                    data["unlocked_quests"].append(next_q)
        if data["xp"] >= data["next_level_xp"]:
            data["level"] += 1
            data["xp"] -= data["next_level_xp"]
            data["next_level_xp"] = int(data["next_level_xp"] * 1.25)
            st.success(f"🎉 Level Up! You reached Level {data['level']}!")
        save_game(data)
        st.success(f"Quest completed! Earned +{amount} XP!")


# ==========================================
# PAGES
# ==========================================
if menu == "Dashboard":
    st.title("🔬 Student Research Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>Level</h3><h2>{data["level"]}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>Total XP</h3><h2>{data["xp"]}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(
            f'<div class="metric-card"><h3>Quests Completed</h3><h2>{len(data["completed_quests"])}/{len(QUESTS)}</h2></div>',
            unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>Active Domain</h3><h2>Bio & Materials</h2></div>',
                    unsafe_allow_html=True)

    st.markdown("---")
    bio_avg = sum(data["skills"]["Biotechnology"].values()) / len(data["skills"]["Biotechnology"])
    mat_avg = sum(data["skills"]["Materials Science"].values()) / len(data["skills"]["Materials Science"])
    col_b, col_m = st.columns(2)
    with col_b:
        st.markdown("### 🧬 Biotechnology Proficiency")
        st.progress(int(bio_avg))
    with col_m:
        st.markdown("### ⚙️ Materials Science Proficiency")
        st.progress(int(mat_avg))

elif menu == "Campaigns & Quests":
    st.title("🎯 Scientific Campaigns & Quests")
    tab1, tab2, tab3 = st.tabs(["Biotechnology", "Materials Science", "Combined Missions"])


    def render_quest_list(domain_filter):
        for q_id, q in QUESTS.items():
            if q["domain"] == domain_filter or (domain_filter == "Combined" and q["domain"] == "Combined"):
                is_completed = q_id in data["completed_quests"]
                is_unlocked = q_id in data["unlocked_quests"]
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    status = "✅ Completed" if is_completed else ("🔓 Available" if is_unlocked else "🔒 Locked")
                    st.markdown(f"### {q['title']} — *{status}*")
                    st.write(f"**Level:** {q['level']} | **Skill:** {q['skill']} | **Reward:** {q['xp']} XP")
                    st.write(q["description"])
                    st.markdown(f"**Objective:** {q['objective']}")
                    if is_completed:
                        st.success("Mission Accomplished!")
                    elif is_unlocked:
                        user_ans = st.number_input(f"Enter calculated value:", value=0.0, step=0.1, key=f"ans_{q_id}")
                        if st.button(f"Submit Answer", key=f"btn_{q_id}"):
                            if abs(user_ans - q["correct_answer"]) <= q["tolerance"]:
                                add_xp(q["xp"], q_id, q["skill"], q["domain"])
                                st.rerun()
                            else:
                                st.error(f"❌ Incorrect. Hint: Expected ~{q['correct_answer']}")
                    else:
                        st.warning("Locked.")
                    st.markdown("</div>", unsafe_allow_html=True)


    with tab1:
        render_quest_list("Biotechnology")
    with tab2:
        render_quest_list("Materials Science")
    with tab3:
        render_quest_list("Combined")

elif menu == "Skill Trees":
    st.title("🌳 RPG Skill Trees")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🧬 Biotechnology Tree")
        for skill, level in data["skills"]["Biotechnology"].items():
            st.markdown(f"**{skill}** ({level}%)")
            st.progress(level)
    with col2:
        st.subheader("⚙️ Materials Science Tree")
        for skill, level in data["skills"]["Materials Science"].items():
            st.markdown(f"**{skill}** ({level}%)")
            st.progress(level)

elif menu == "Interactive Laboratory":
    st.title("🧪 Interactive Scientific Laboratory")
    lab_choice = st.selectbox("Select Simulation",
                              ["Bacterial Population Growth", "Tensile Stress-Strain Curve Analysis"])
    if lab_choice == "Bacterial Population Growth":
        n0 = st.number_input("Initial Population (N0)", value=1000, step=100)
        gen_time = st.slider("Generation Time (mins)", 15, 120, 30)
        total_time = st.slider("Total Time (hours)", 1, 24, 6)
        hours = np.linspace(0, total_time, 100)
        population = n0 * (2 ** ((hours * 60) / gen_time))
        fig = px.line(x=hours, y=population, labels={"x": "Time (Hours)", "y": "Population"},
                      title="Bacterial Growth Curve")
        st.plotly_chart(fig, use_container_width=True)
    elif lab_choice == "Tensile Stress-Strain Curve Analysis":
        young_modulus = st.slider("Young's Modulus E (GPa)", 50, 250, 200)
        yield_strength = st.slider("Yield Strength (MPa)", 200, 800, 400)
        strain = np.linspace(0, 0.15, 200)
        stress = np.clip(strain * young_modulus * 1000, 0, yield_strength)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(strain * 100, stress, color="#3fb950", linewidth=2)
        ax.set_title("Engineering Stress-Strain Curve", color="white")
        st.pyplot(fig)

elif menu == "Profile & Save":
    st.title("👤 Researcher Profile")
    new_name = st.text_input("Edit Name", value=data["player_name"])
    if st.button("Update Profile"):
        data["player_name"] = new_name
        save_game(data)
        st.success("Updated!")
    if st.button("Reset Progress"):
        if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
        st.session_state.game_data = DEFAULT_DATA
        save_game(DEFAULT_DATA)
        st.rerun()