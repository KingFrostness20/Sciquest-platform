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
    page_title="SciQuest: Advanced RPG Science & Python",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "xp" not in st.session_state:
  st.session_state.xp = 0
if "level" not in st.session_state:
  st.session_state.level = 1
if "quests_solved" not in st.session_state:
  st.session_state.quests_solved = set()
if "unlocked_skills" not in st.session_state:
  st.session_state.unlocked_skills = {"py_basics", "bio_intro", "mat_intro"}


def add_xp(amount):
  st.session_state.xp += amount
  needed = st.session_state.level * 100
  if st.session_state.xp >= needed:
    st.session_state.xp -= needed
    st.session_state.level += 1
    st.balloons()
    st.toast(
        f"🎉 Level Up! You are now Level {st.session_state.level}!", icon="⭐"
    )


def get_title(level):
  if level == 1:
    return "Novice Researcher"
  elif level == 2:
    return "Junior Lab Assistant"
  elif level == 3:
    return "Bio-Materials Analyst"
  else:
    return "Principal Investigator"


# ---------------------------------------------------------
# SIDEBAR HUD
# ---------------------------------------------------------
with st.sidebar:
  st.title("🧬 SciQuest Platform")
  st.caption("Advanced Interdisciplinary Learning HUD")

  st.markdown(f"**Title:** `{get_title(st.session_state.level)}`")
  st.markdown(f"**Level:** {st.session_state.level}")

  next_level_xp = st.session_state.level * 100
  progress = min(1.0, st.session_state.xp / next_level_xp)
  st.progress(progress)
  st.caption(f"XP: {st.session_state.xp} / {next_level_xp} to next rank")

  st.markdown("---")
  menu = st.radio(
      "Navigation",
      [
          "Dashboard",
          "Skill Trees",
          "Tiered Quests & Challenges",
          "Interactive Laboratory",
          "Escape Room Debugger",
      ],
  )


# ---------------------------------------------------------
# 1. DASHBOARD
# ---------------------------------------------------------
if menu == "Dashboard":
  st.title("🔬 Student Research & Progress Dashboard")
  st.markdown(
      "Welcome back, team! Monitor your mastery of Python, Biotechnology, and"
      " Materials Science."
  )

  c1, c2, c3, c4 = st.columns(4)
  c1.metric("Current Level", st.session_state.level)
  c2.metric("Total XP", st.session_state.xp + (st.session_state.level - 1) * 100)
  c3.metric("Quests Cleared", f"{len(st.session_state.quests_solved)} / 6")
  c4.metric("Skills Unlocked", f"{len(st.session_state.unlocked_skills)} / 9")

  st.markdown("### 📋 Project Team Context")
  st.info(
      "**Authors**: Ibrahim Faraz C H (B250876BT) | Vasanth R Menon"
      " (B251289MT) | Muhammed Sinan P M (B251033MT)\n**Domain**: RPG-Driven"
      " Interdisciplinary Scientific Platform (Streamlit + NumPy + Pandas +"
      " Plotly)"
  )


# ---------------------------------------------------------
# 2. SKILL TREES
# ---------------------------------------------------------
elif menu == "Skill Trees":
  st.title("🌳 Interdisciplinary Skill Trees")
  st.markdown(
      "Unlock advanced computational and laboratory methodologies using your"
      " earned rank."
  )

  skills = {
      "Python Core": [
          ("py_basics", "Basic Slicing & Strings", 1),
          ("py_loops", "Control Flow & Iterables", 2),
          ("py_funcs", "Modular Functions & AST", 3),
      ],
      "Biotechnology": [
          ("bio_intro", "FASTA Sequence Parsing", 1),
          ("bio_growth", "Microbial Kinetics (Monod)", 2),
          ("bio_enzyme", "Enzyme Inhibition Models", 3),
      ],
      "Materials Science": [
          ("mat_intro", "Hooke's Law & Elasticity", 1),
          ("mat_plastic", "Elastoplastic Deformation", 2),
          ("mat_fracture", "Stress Tensor Integration", 3),
      ],
  }

  cols = st.columns(3)
  for idx, (track, nodes) in enumerate(skills.items()):
    with cols[idx]:
      st.subheader(track)
      for skill_id, name, req_lvl in nodes:
        is_unlocked = skill_id in st.session_state.unlocked_skills
        can_unlock = st.session_state.level >= req_lvl

        with st.container(border=True):
          if is_unlocked:
            st.markdown(f"✅ **{name}**")
            st.caption("Status: UNLOCKED")
          else:
            st.markdown(f"🔒 **{name}**")
            st.caption(f"Required Level: {req_lvl}")
            if can_unlock:
              if st.button(f"Unlock Skill", key=skill_id):
                st.session_state.unlocked_skills.add(skill_id)
                st.toast(f"Unlocked {name}!", icon="🔓")
                st.rerun()


# ---------------------------------------------------------
# 3. TIERED QUESTS & CHALLENGES
# ---------------------------------------------------------
elif menu == "Tiered Quests & Challenges":
  st.title("🎯 Tiered Gamified Quests")
  st.markdown(
      "Challenges scale with your level. Complete lower-tier quests to unlock"
      " advanced missions!"
  )

  quest_tab = st.tabs(
      [
          "Level 1: Novice Quests",
          "Level 2: Journeyman Quests",
          "Level 3: Expert Quests",
      ]
  )

  # LEVEL 1 QUESTS
  with quest_tab[0]:
    st.subheader("Novice Mission 1: DNA Codon Slicing")
    st.write(
        "Extract the first codon (`ATC`) from `dna = 'ATCGATCG'` using Python"
        " string slicing."
    )
    ans1 = st.text_input("Your expression (e.g., dna[...]):", value="dna[:3]")
    if st.button("Submit Novice Quest"):
      try:
        res = eval(ans1, {"dna": "ATCGATCG"})
        if res == "ATC":
          st.success("Correct! +50 XP")
          if "q1" not in st.session_state.quests_solved:
            st.session_state.quests_solved.add("q1")
            add_xp(50)
            st.rerun()
        else:
          st.error(f"Got '{res}', expected 'ATC'.")
      except Exception as e:
        st.error(f"Error: {e}")

  # LEVEL 2 QUESTS
  with quest_tab[1]:
    if st.session_state.level < 2:
      st.warning(
          "🔒 Locked! Reach **Level 2** to unlock Journeyman Quests."
      )
    else:
      st.subheader("Journeyman Mission 2: GC-Content Percentage Calculator")
      st.write(
          "Write a Python function `calc_gc(seq)` that calculates the"
          " percentage of 'G' and 'C' in a DNA string."
      )
      code_q2 = st.text_area(
          "Function definition:",
          value=(
              "def calc_gc(seq):\n    gc_count = seq.count('G') +"
              " seq.count('C')\n    return (gc_count / len(seq)) * 100"
          ),
      )
      if st.button("Evaluate Journeyman Quest"):
        try:
          scope = {}
          exec(code_q2, {}, scope)
          if "calc_gc" in scope:
            val = scope["calc_gc"]("GCGCAT")
            if np.isclose(val, 66.666, atol=0.01):
              st.success("Correct calculation! +80 XP")
              if "q2" not in st.session_state.quests_solved:
                st.session_state.quests_solved.add("q2")
                add_xp(80)
                st.rerun()
            else:
              st.error(f"Tested with 'GCGCAT', got {val}%, expected ~66.67%.")
          else:
            st.error("Function `calc_gc` not defined.")
        except Exception as e:
          st.error(f"Error: {e}")

  # LEVEL 3 QUESTS
  with quest_tab[2]:
    if st.session_state.level < 3:
      st.warning("🔒 Locked! Reach **Level 3** to unlock Expert Quests.")
    else:
      st.subheader("Expert Mission 3: Bilinear Yield Stress Function")
      st.write(
          "Define a function `compute_plastic_stress(strain, E, sy, E_p)` that"
          " returns stress based on elastoplastic behavior."
      )
      code_q3 = st.text_area(
          "Python Function:",
          value=(
              "def compute_plastic_stress(strain, E, sy, E_p):\n    "
              "strain_y = sy / E\n    if strain <= strain_y:\n        return"
              " strain * E\n    else:\n        return sy + (strain - "
              "strain_y) * E_p"
          ),
      )
      if st.button("Verify Expert Quest"):
        try:
          scope = {}
          exec(code_q3, {}, scope)
          if "compute_plastic_stress" in scope:
            val = scope["compute_plastic_stress"](0.003, 200000, 300, 5000)
            st.success(f"Expert calculation verified! Stress = {val} MPa. +120 XP")
            if "q3" not in st.session_state.quests_solved:
              st.session_state.quests_solved.add("q3")
              add_xp(120)
              st.rerun()
          else:
            st.error("Function `compute_plastic_stress` not found.")
        except Exception as e:
          st.error(f"Error: {e}")


# ---------------------------------------------------------
# 4. INTERACTIVE LABORATORY
# ---------------------------------------------------------
elif menu == "Interactive Laboratory":
  st.title("🧪 Interactive Engineering & Biotech Sandboxes")
  st.markdown(
      "Adjust parameters to simulate physical responses and view underlying"
      " Python code."
  )

  sim_type = st.selectbox(
      "Select Laboratory Simulator",
      [
          "Bacterial Logistic Growth (Biotech)",
          "Alloy Stress-Strain Curve (Materials)",
      ],
  )

  if sim_type == "Bacterial Logistic Growth (Biotech)":
    c1, c2 = st.columns([1, 2])
    with c1:
      N0 = st.slider("Initial Population ($N_0$)", 100, 2000, 500)
      K = st.slider("Carrying Capacity ($K$)", 10000, 100000, 50000, step=5000)
      r = st.slider("Growth Rate ($r$)", 0.1, 1.0, 0.3, step=0.05)
    with c2:
      t = np.linspace(0, 24, 200)
      N = K / (1 + ((K - N0) / N0) * np.exp(-r * t))

      fig = go.Figure(
          data=go.Scatter(
              x=t, y=N, mode="lines", line=dict(color="#00E676", width=3)
          )
      )
      fig.update_layout(
          title="Bacterial Population Dynamics",
          xaxis_title="Time (Hours)",
          yaxis_title="Population Count",
          template="plotly_dark",
      )
      st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 View Executed Python Code"):
      st.code(
          f"""import numpy as np
import plotly.graph_objects as go

t = np.linspace(0, 24, 200)
N = {K} / (1 + (({K} - {N0}) / {N0}) * np.exp(-{r} * t))
""",
          language="python",
      )

  else:
    c1, c2 = st.columns([1, 2])
    with c1:
      E = st.slider("Young's Modulus E (GPa)", 50, 210, 200)
      sy = st.slider("Yield Strength (MPa)", 200, 800, 400)
    with c2:
      strain_y = sy / (E * 1000)
      strain = np.linspace(0, 0.04, 200)
      stress = np.where(
          strain <= strain_y, strain * E * 1000, sy + (strain - strain_y) * 2000
      )

      fig = go.Figure(
          data=go.Scatter(
              x=strain, y=stress, mode="lines", line=dict(color="#FF9100", width=3)
          )
      )
      fig.update_layout(
          title="Tensile Stress-Strain Response",
          xaxis_title="Strain (ε)",
          yaxis_title="Stress (σ MPa)",
          template="plotly_dark",
      )
      st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 View Executed Python Code"):
      st.code(
          f"""import numpy as np
E = {E} * 1000
sy = {sy}
strain = np.linspace(0, 0.04, 200)
stress = np.where(strain <= (sy/E), strain * E, sy + (strain - (sy/E)) * 2000)
""",
          language="python",
      )


# ---------------------------------------------------------
# 5. ESCAPE ROOM DEBUGGER
# ---------------------------------------------------------
elif menu == "Escape Room Debugger":
  st.title("🚨 Lab Escape Room: Spectrometer Calibration")
  st.markdown(
      "Fix the broken Python snippet to sanitize corrupted sensor data and"
      " unlock the laboratory."
  )

  st.code(
      """# CORRUPTED SCRIPT:
raw_readings = ["400nm", "450nm", "ERROR", "550nm"]
cleaned = [int(x.replace("nm", "")) for x in raw_readings] # Fails on "ERROR"!
""",
      language="python",
  )

  fix_input = st.text_area(
      "Fix the list comprehension with a conditional check:",
      value=(
          "cleaned = [int(x.replace('nm', '')) for x in raw_readings if"
          " x.endswith('nm')]"
      ),
  )

  if st.button("Calibrate & Escape"):
    raw_readings = ["400nm", "450nm", "ERROR", "550nm"]
    try:
      local_env = {"raw_readings": raw_readings}
      exec(fix_input, {}, local_env)
      if "cleaned" in local_env and local_env["cleaned"] == [400, 450, 550]:
        st.balloons()
        st.success(
            "🎉 Successfully calibrated instrument! Clean data: [400, 450, 550]."
            " +100 XP!"
        )
        if "escape" not in st.session_state.quests_solved:
          st.session_state.quests_solved.add("escape")
          add_xp(100)
      else:
        st.error(f"Extracted incorrect result: {local_env.get('cleaned')}")
    except Exception as e:
      st.error(f"Execution Error: {e}")
