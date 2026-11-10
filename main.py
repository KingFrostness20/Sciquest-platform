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
          "Interactive Skill Trees & Challenges",
          "Tiered Quests",
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
      "Welcome back! Monitor your mastery of Python, Biotechnology, and"
      " Materials Science."
  )

  c1, c2, c3, c4 = st.columns(4)
  c1.metric("Current Level", st.session_state.level)
  c2.metric("Total XP", st.session_state.xp + (st.session_state.level - 1) * 100)
  c3.metric("Quests Cleared", f"{len(st.session_state.quests_solved)} / 6")
  c4.metric("Skills Unlocked", f"{len(st.session_state.unlocked_skills)} / 9")

  st.markdown("### 📋 Platform Overview")
  st.info(
      "**Domain**: RPG-Driven Interdisciplinary Scientific Learning"
      " Platform\n**Technologies**: Streamlit, NumPy, Pandas, Plotly, Python"
      " AST Execution Engine"
  )


# ---------------------------------------------------------
# 2. INTERACTIVE SKILL TREES WITH EMBEDDED PROBLEMS
# ---------------------------------------------------------
elif menu == "Interactive Skill Trees & Challenges":
  st.title("🌳 Interactive Skill Trees & Competency Nodes")
  st.markdown(
      "Click on unlocked skill nodes to access their specific embedded coding"
      " challenges and earn skill points!"
  )

  selected_track = st.selectbox(
      "Choose Skill Track",
      ["Python Core", "Biotechnology Track", "Materials Science Track"],
  )

  if selected_track == "Python Core":
    st.subheader("🐍 Python Core Competency Tree")
    tab1, tab2, tab3 = st.tabs(
        ["Node 1: String Slicing", "Node 2: Control Flow", "Node 3: Functions"]
    )

    with tab1:
      st.markdown(
          "**Status**: ✅ Unlocked\n*Concept*: Extracting subsequences from"
          " strings."
      )
      st.write(
          "**Embedded Challenge**: Extract the first 3 characters from `seq ="
          " 'GATTACA'`."
      )
      ans = st.text_input("Python expression:", value="seq[:3]", key="sk_py1")
      if st.button("Test Skill Node 1"):
        if eval(ans, {"seq": "GATTACA"}) == "GAT":
          st.success("Challenge Passed! +30 XP")
          add_xp(30)
        else:
          st.error("Incorrect. Try `seq[:3]`.")

    with tab2:
      is_unlocked = st.session_state.level >= 2
      if not is_unlocked:
        st.warning("🔒 Locked. Reach Level 2 to unlock Control Flow.")
      else:
        st.markdown(
            "**Status**: 🔓 Unlocked\n*Concept*: Using loops and conditional"
            " statements."
        )
        st.write(
            "**Embedded Challenge**: Write a list comprehension filtering out"
            " negative values from `vals = [-1, 2, -3, 4]`."
        )
        ans2 = st.text_input(
            "Python expression:",
            value="[x for x in vals if x > 0]",
            key="sk_py2",
        )
        if st.button("Test Skill Node 2"):
          if eval(ans2, {"vals": [-1, 2, -3, 4]}) == [2, 4]:
            st.success("Challenge Passed! +50 XP")
            add_xp(50)
          else:
            st.error("Incorrect.")

    with tab3:
      is_unlocked = st.session_state.level >= 3
      if not is_unlocked:
        st.warning("🔒 Locked. Reach Level 3 to unlock Modular Functions.")
      else:
        st.markdown(
            "**Status**: 🔓 Unlocked\n*Concept*: Defining reusable functions."
        )
        st.write(
            "**Embedded Challenge**: Define a function `add(a, b)` that returns"
            " their sum."
        )
        code_box = st.text_area(
            "Code:", value="def add(a, b):\n    return a + b", key="sk_py3"
        )
        if st.button("Test Skill Node 3"):
          env = {}
          exec(code_box, {}, env)
          if "add" in env and env["add"](3, 4) == 7:
            st.success("Challenge Passed! +70 XP")
            add_xp(70)
          else:
            st.error("Function not defined correctly.")

  elif selected_track == "Biotechnology Track":
    st.subheader("🧬 Biotechnology Competency Tree")
    b_tab1, b_tab2 = st.tabs(
        ["Node 1: FASTA Parsing", "Node 2: Growth Kinetics"]
    )

    with b_tab1:
      st.markdown(
          "**Status**: ✅ Unlocked\n*Concept*: Processing nucleotide sequences."
      )
      st.write(
          "**Embedded Challenge**: Count the number of 'G' bases in `dna ="
          " 'GGCCAT'`."
      )
      b_ans = st.text_input(
          "Python expression:", value="dna.count('G')", key="sk_b1"
      )
      if st.button("Test Biotech Node 1"):
        if eval(b_ans, {"dna": "GGCCAT"}) == 3:
          st.success("Challenge Passed! +30 XP")
          add_xp(30)
        else:
          st.error("Incorrect.")

    with b_tab2:
      if st.session_state.level < 2:
        st.warning("🔒 Locked. Reach Level 2.")
      else:
        st.markdown(
            "**Status**: 🔓 Unlocked\n*Concept*: Microbial exponential growth."
        )
        st.write(
            "**Embedded Challenge**: Calculate population after 1 hour given"
            " $N_0=100$, $k=0.5$ using formula $N_0 * \\exp(k * t)$."
        )
        b_ans2 = st.text_input(
            "Python expression:", value="100 * np.exp(0.5 * 1)", key="sk_b2"
        )
        if st.button("Test Biotech Node 2"):
          if np.isclose(eval(b_ans2, {"np": np}), 164.87, atol=0.1):
            st.success("Challenge Passed! +50 XP")
            add_xp(50)
          else:
            st.error("Incorrect formula calculation.")

  else:
    st.subheader("⚙️ Materials Science Competency Tree")
    m_tab1, m_tab2 = st.tabs(
        ["Node 1: Hooke's Law", "Node 2: Elastoplasticity"]
    )

    with m_tab1:
      st.markdown(
          "**Status**: ✅ Unlocked\n*Concept*: Elastic stress computation."
      )
      st.write(
          "**Embedded Challenge**: Compute stress ($\sigma = E \\times"
          " \\epsilon$) for $E=200$ GPa and $\\epsilon=0.002$."
      )
      m_ans = st.text_input(
          "Python expression:", value="200 * 0.002", key="sk_m1"
      )
      if st.button("Test Materials Node 1"):
        if np.isclose(eval(m_ans), 0.4):
          st.success("Challenge Passed! +30 XP")
          add_xp(30)
        else:
          st.error("Incorrect.")

    with m_tab2:
      if st.session_state.level < 2:
        st.warning("🔒 Locked. Reach Level 2.")
      else:
        st.markdown(
            "**Status**: 🔓 Unlocked\n*Concept*: Yield point identification."
        )
        st.write(
            "**Embedded Challenge**: Write a condition to check if stress"
            " exceeds yield strength `sy = 300`."
        )
        m_ans2 = st.text_input(
            "Python expression:", value="stress > 300", key="sk_m2"
        )
        if st.button("Test Materials Node 2"):
          if eval(m_ans2, {"stress": 350}) is True:
            st.success("Challenge Passed! +50 XP")
            add_xp(50)
          else:
            st.error("Incorrect conditional check.")


# ---------------------------------------------------------
# 3. TIERED QUESTS
# ---------------------------------------------------------
elif menu == "Tiered Quests":
  st.title("🎯 Tiered Gamified Quests")
  st.markdown("Complete standalone challenges across different difficulty tiers.")

  q_tab1, q_tab2, q_tab3 = st.tabs(
      ["Level 1: Novice", "Level 2: Journeyman", "Level 3: Expert"]
  )

  with q_tab1:
    st.subheader("Novice Quest: Codon Extraction")
    ans1 = st.text_input(
        "Extract 'ATC' from `dna = 'ATCGAT'`:", value="dna[:3]", key="t_q1"
    )
    if st.button("Submit Novice"):
      if eval(ans1, {"dna": "ATCGAT"}) == "ATC":
        st.success("Correct! +50 XP")
        if "q1" not in st.session_state.quests_solved:
          st.session_state.quests_solved.add("q1")
          add_xp(50)
      else:
        st.error("Incorrect.")

  with q_tab2:
    if st.session_state.level < 2:
      st.warning("🔒 Locked. Reach Level 2.")
    else:
      st.subheader("Journeyman Quest: GC Content Function")
      code_q2 = st.text_area(
          "Define `calc_gc(seq)`:",
          value=(
              "def calc_gc(seq):\n    return ((seq.count('G') +"
              " seq.count('C')) / len(seq)) * 100"
          ),
          key="t_q2",
      )
      if st.button("Submit Journeyman"):
        env = {}
        exec(code_q2, {}, env)
        if "calc_gc" in env and np.isclose(env["calc_gc"]("GCAT"), 50.0):
          st.success("Correct! +80 XP")
          if "q2" not in st.session_state.quests_solved:
            st.session_state.quests_solved.add("q2")
            add_xp(80)
        else:
          st.error("Function failed test case.")

  with q_tab3:
    if st.session_state.level < 3:
      st.warning("🔒 Locked. Reach Level 3.")
    else:
      st.subheader("Expert Quest: Bilinear Stress Function")
      code_q3 = st.text_area(
          "Define `get_stress(strain, E, sy, Ep)`:",
          value=(
              "def get_stress(strain, E, sy, Ep):\n    sy_strain = sy / E\n"
              "    return strain * E if strain <= sy_strain else sy + (strain -"
              " sy_strain) * Ep"
          ),
          key="t_q3",
      )
      if st.button("Submit Expert"):
        env = {}
        exec(code_q3, {}, env)
        if "get_stress" in env:
          st.success("Correct! +120 XP")
          if "q3" not in st.session_state.quests_solved:
            st.session_state.quests_solved.add("q3")
            add_xp(120)
        else:
          st.error("Function not found.")


# ---------------------------------------------------------
# 4. INTERACTIVE LABORATORY
# ---------------------------------------------------------
elif menu == "Interactive Laboratory":
  st.title("🧪 Interactive Engineering & Biotech Sandboxes")
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
# 5. ADVANCED ESCAPE ROOM DEBUGGER
# ---------------------------------------------------------
elif menu == "Escape Room Debugger":
  st.title("🚨 Lab Escape Room: Multi-Stage Instrument Calibration")
  st.markdown(
      "A corrupted sensor log is causing a laboratory spectrophotometer system"
      " failure. Complete the multi-stage diagnostic script to sanitize data"
      " and unlock the facility exit!"
  )

  stage = st.radio(
      "Calibration Stage",
      [
          "Stage 1: String Sanitization",
          "Stage 2: Outlier Filtering",
          "Stage 3: Final Mean Calibration",
      ],
  )

  if stage == "Stage 1: String Sanitization":
    st.markdown(
        "**Task**: Write a list comprehension that converts raw sensor strings"
        " like `['340nm', '450nm']` into integers by removing `'nm'`."
    )
    s1_code = st.text_input(
        "Python Code:",
        value="[int(x.replace('nm', '')) for x in raw_readings]",
    )
    if st.button("Execute Stage 1"):
      raw_readings = ["340nm", "450nm", "520nm"]
      env = {"raw_readings": raw_readings}
      try:
        exec(f"res = {s1_code}", {}, env)
        if env["res"] == [340, 450, 520]:
          st.success("Stage 1 Passed! Sensor strings parsed.")
          add_xp(40)
        else:
          st.error(f"Got {env['res']}, expected [340, 450, 520].")
      except Exception as e:
        st.error(f"Error: {e}")

  elif stage == "Stage 2: Outlier Filtering":
    st.markdown(
        "**Task**: Filter out any corrupted entries (where entries equal"
        " `'ERROR'`) before casting to integers."
    )
    s2_code = st.text_area(
        "Python Code:",
        value=(
            "[int(x.replace('nm', '')) for x in raw_readings if x !="
            " 'ERROR']"
        ),
    )
    if st.button("Execute Stage 2"):
      raw_readings = ["340nm", "ERROR", "520nm"]
      env = {"raw_readings": raw_readings}
      try:
        exec(f"res = {s2_code}", {}, env)
        if env["res"] == [340, 520]:
          st.success("Stage 2 Passed! Outliers successfully filtered.")
          add_xp(50)
        else:
          st.error(f"Got {env['res']}, expected [340, 520].")
      except Exception as e:
        st.error(f"Error: {e}")

  else:
    st.markdown(
        "**Task**: Calculate the final calibrated mean wavelength from"
        " `cleaned = [340, 450, 530, 600]`."
    )
    s3_code = st.text_input(
        "Python Code:", value="sum(cleaned) / len(cleaned)"
    )
    if st.button("Calibrate & Escape Lab"):
      cleaned = [340, 450, 530, 600]
      env = {"cleaned": cleaned}
      try:
        res = eval(s3_code, {}, env)
        if np.isclose(res, 480.0):
          st.balloons()
          st.success(
              "🎉 Full Laboratory Calibration Complete! Mean Wavelength ="
              f" {res} nm. Exit Door Unlocked! +100 XP"
          )
          add_xp(100)
        else:
          st.error(f"Incorrect mean calculated: {res}")
      except Exception as e:
        st.error(f"Error: {e}")
