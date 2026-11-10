import ast
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG & INITIAL SESSION STATE
# ---------------------------------------------------------
st.set_page_config(
    page_title="SciQuest: Interdisciplinary Python Platform",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Core State Initialization
if "xp" not in st.session_state:
  st.session_state.xp = 0
if "level" not in st.session_state:
  st.session_state.level = 1
if "quests_solved" not in st.session_state:
  st.session_state.quests_solved = set()
if "unlocked_skills" not in st.session_state:
  st.session_state.unlocked_skills = {"py_basics", "bio_intro", "mat_intro"}


# Helper Functions for RPG Progress
def add_xp(amount):
  st.session_state.xp += amount
  needed = st.session_state.level * 100
  if st.session_state.xp >= needed:
    st.session_state.xp -= needed
    st.session_state.level += 1
    st.toast(
        f"🎉 Level Up! You reached Level {st.session_state.level}!", icon="⭐"
    )


def get_title(level):
  if level < 2:
    return "Novice Coder"
  elif level < 4:
    return "Junior Research Assistant"
  elif level < 6:
    return "Interdisciplinary Scientist"
  else:
    return "Principal Investigator"


# ---------------------------------------------------------
# SIDEBAR HUD & NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
  st.title("🧬 SciQuest Platform")
  st.caption("RPG-Driven Interdisciplinary Learning")

  st.markdown(f"**Researcher:** `{get_title(st.session_state.level)}`")
  st.markdown(f"**Level:** {st.session_state.level}")

  next_level_xp = st.session_state.level * 100
  progress = min(1.0, st.session_state.xp / next_level_xp)
  st.progress(progress)
  st.caption(f"XP: {st.session_state.xp} / {next_level_xp}")

  st.markdown("---")
  menu = st.radio(
      "Navigation",
      [
          "Dashboard",
          "Skill Trees",
          "Gamified Quests",
          "Interactive Laboratory",
          "Escape Room Debugger",
      ],
  )


# ---------------------------------------------------------
# 1. DASHBOARD
# ---------------------------------------------------------
if menu == "Dashboard":
  st.title("🔬 Student Research Dashboard")
  st.markdown(
      "Welcome to **SciQuest**, an interactive environment designed to teach"
      " Python programming through practical Biotechnology and Materials"
      " Science challenges."
  )

  c1, c2, c3, c4 = st.columns(4)
  c1.metric("Player Level", st.session_state.level)
  c2.metric("Total XP Earned", st.session_state.xp + (st.session_state.level - 1) * 100)
  c3.metric("Quests Cleared", f"{len(st.session_state.quests_solved)} / 4")
  c4.metric("Skills Unlocked", f"{len(st.session_state.unlocked_skills)} / 9")

  st.markdown("### 🗺️ Learning Roadmap")
  col_a, col_b = st.columns(2)
  with col_a:
    st.info(
        "**🧬 Biotechnology Track**\n\n- DNA/RNA Sequence Processing\n-"
        " Exponential & Logistic Microbial Growth Models\n- Spectrophotometer"
        " Data Cleaning"
    )
  with col_b:
    st.success(
        "**⚙️ Materials Science Track**\n\n- Stress-Strain Curve Analysis\n-"
        " Young's Modulus & Yield Strength Computation\n- Instrument Signal"
        " Calibration"
    )

# ---------------------------------------------------------
# 2. PROPER SKILL TREE
# ---------------------------------------------------------
elif menu == "Skill Trees":
  st.title("🌳 Scientific & Python Skill Trees")
  st.markdown(
      "Spend your progress to unlock specialized domain techniques and coding"
      " capabilities."
  )

  skills_db = {
      "Python Fundamentals": [
          (
              "py_basics",
              "Variable Types & Slicing",
              1,
              "Unlocked by default",
          ),
          (
              "py_loops",
              "Control Flow & Loops",
              2,
              "Req: Level 2 & Variable Slicing",
          ),
          (
              "py_funcs",
              "Modular Functions & AST",
              3,
              "Req: Level 3 & Control Flow",
          ),
      ],
      "Biotechnology Track": [
          ("bio_intro", "FASTA Sequence Parsing", 1, "Unlocked by default"),
          (
              "bio_growth",
              "Bacterial Kinetics Modeling",
              2,
              "Req: Level 2 & Sequence Parsing",
          ),
          (
              "bio_enzyme",
              "Michaelis-Menten Kinetics",
              4,
              "Req: Level 4 & Kinetics",
          ),
      ],
      "Materials Science Track": [
          (
              "mat_intro",
              "Hooke's Law & Elasticity",
              1,
              "Unlocked by default",
          ),
          (
              "mat_plastic",
              "Bilinear Plastic Strain",
              2,
              "Req: Level 2 & Elasticity",
          ),
          (
              "mat_fracture",
              "Toughness & Integration",
              4,
              "Req: Level 4 & Plasticity",
          ),
      ],
  }

  cols = st.columns(3)
  for idx, (category, nodes) in enumerate(skills_db.items()):
    with cols[idx]:
      st.subheader(category)
      for skill_id, name, req_lvl, req_text in nodes:
        is_unlocked = skill_id in st.session_state.unlocked_skills
        can_unlock = st.session_state.level >= req_lvl

        with st.container(border=True):
          if is_unlocked:
            st.markdown(f"✅ **{name}**")
            st.caption("Status: ACTIVE")
          else:
            st.markdown(f"🔒 **{name}**")
            st.caption(f"Requirements: {req_text}")
            if can_unlock:
              if st.button(f"Unlock ({skill_id})", key=skill_id):
                st.session_state.unlocked_skills.add(skill_id)
                st.toast(f"Skill '{name}' unlocked!", icon="🔓")
                st.rerun()

# ---------------------------------------------------------
# 3. GAMIFIED QUESTS
# ---------------------------------------------------------
elif menu == "Gamified Quests":
  st.title("🎯 Gamified Coding Quests")
  st.markdown(
      "Solve practical domain problems using target Python constructs."
  )

  t1, t2 = st.tabs(["Biotech Quests", "Materials Quests"])

  with t1:
    st.subheader("Quest 1: DNA GC-Content & Codon Extraction")
    st.write(
        "Write a Python expression to extract the first 6 bases of sequence"
        " `dna = 'ATGCGATCGAT'` and calculate its length."
    )

    code_input = st.text_input("Enter code:", value="dna[:6]")
    if st.button("Run Quest 1"):
      sample_dna = "ATGCGATCGAT"
      try:
        res = eval(code_input, {"dna": sample_dna})
        if res == "ATGCGA":
          st.success(f"Correct Output: '{res}'")
          if "q1" not in st.session_state.quests_solved:
            st.session_state.quests_solved.add("q1")
            add_xp(60)
            st.rerun()
        else:
          st.error(f"Got '{res}', expected 'ATGCGA'")
      except Exception as e:
        st.error(f"Execution Error: {e}")

  with t2:
    st.subheader("Quest 2: Hooke's Law Function Implementation")
    st.write(
        "Define a function `calculate_stress(strain, E)` that returns stress in"
        " MPa."
    )

    func_code = st.text_area(
        "Python Code:",
        value=(
            "def calculate_stress(strain, E):\n    # Return stress in"
            " MPa\n    return strain * E"
        ),
    )

    if st.button("Evaluate Function"):
      try:
        local_scope = {}
        exec(func_code, {}, local_scope)
        if "calculate_stress" in local_scope:
          val = local_scope["calculate_stress"](0.002, 210000)
          if np.isclose(val, 420.0):
            st.success(
                f"Validation Passed: calculate_stress(0.002, 210000) = {val}"
                " MPa"
            )
            if "q2" not in st.session_state.quests_solved:
              st.session_state.quests_solved.add("q2")
              add_xp(80)
              st.rerun()
          else:
            st.error(f"Incorrect result: Expected 420.0, got {
