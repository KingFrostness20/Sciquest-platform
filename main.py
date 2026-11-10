import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="SciQuest: RPG Driven Science & Python Learning",
    page_icon="🧬",
    layout="wide",
)

# Initialize session state for RPG progression & coding stats
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "quests_completed" not in st.session_state:
    st.session_state.quests_completed = 0
if "python_skill" not in st.session_state:
    st.session_state.python_skill = "Novice Coder"

# Sidebar RPG HUD
st.sidebar.markdown("## 🧬 SciQuest Platform")
st.sidebar.markdown(f"**Player:** {st.session_state.python_skill}")
st.sidebar.markdown(
    f"**Level:** {st.session_state.level} | **XP:** {st.session_state.xp}/100"
)
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Gamified Coding Quests",
        "Interactive Lab & Code Sandbox",
        "Debugging Escape Room",
        "Profile & Save",
    ],
)

# ---------------------------------------------------------
# 1. DASHBOARD
# ---------------------------------------------------------
if menu == "Dashboard":
  st.title("🔬 Student Research & Python Mastery Dashboard")
  st.markdown(
      "Welcome to **SciQuest**, an interdisciplinary platform blending"
      " Biotechnology & Materials Science with Python programming!"
  )

  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Player Level", st.session_state.level)
  col2.metric("Total XP", st.session_state.xp)
  col3.metric("Quests Completed", f"{st.session_state.quests_completed}/9")
  col4.metric("Active Domain", "Bio & Materials Python")

  st.markdown("### 🌟 Core Learning Pillars")
  c1, c2, c3 = st.columns(3)
  with c1:
    st.info(
        "**1. Gamified Python Quests**\n\nDecode DNA sequences and calculate"
        " stress-strain tolerances using Python loops and functions."
    )
  with c2:
    st.success(
        "**2. Interactive Sandboxes**\n\nTweak parameters for bacterial cell"
        " growth and alloy deformation while viewing live matplotlib/plotly"
        " code."
    )
  with c3:
    st.warning(
        "**3. Debugging Escape Rooms**\n\nFix broken Python scripts to"
        " calibrate lab spectrometers and escape before time runs out!"
    )

# ---------------------------------------------------------
# 2. GAMIFIED CODING QUESTS (Biotech/Materials + Python)
# ---------------------------------------------------------
elif menu == "Gamified Coding Quests":
  st.title("🎯 Gamified Coding Quests")
  st.markdown(
      "Write and execute Python logic to solve real scientific challenges and"
      " earn XP!"
  )

  quest_tab = st.tabs(
      [
          "Quest 1: DNA Sequence Slicing (Biotech)",
          "Quest 2: Hooke's Law Stress Calculator (Materials)",
      ]
  )

  with quest_tab[0]:
    st.subheader("Mission 1: Extracting Codons from Viral DNA")
    st.markdown(
        "*Objective*: Given a DNA string `dna = 'ATCGATCGATCG'`, write a Python"
        " expression or snippet using string slicing to extract the first 3"
        " bases (codon)."
    )

    sample_dna = "ATCGATCGATCG"
    st.code(f"dna = '{sample_dna}'\n# Write your slicing logic below", language="python")

    user_code = st.text_input(
        "Enter Python code/expression (e.g., dna[0:3]):", value="dna[0:3]"
    )

    if st.button("Submit Python Code"):
      try:
        # Safe evaluation of basic expression
        result = eval(user_code, {"dna": sample_dna})
        if result == "ATC":
          st.success(
              f"Correct! Output: `{result}`. You unlocked a codon!"
          )
          st.session_state.xp += 50
          st.session_state.quests_completed += 1
          if st.session_state.xp >= 100:
            st.session_state.level += 2
            st.session_state.python_skill = "Python Bio-Specialist"
          st.rerun()
        else:
          st.error(
              f"Incorrect output: `{result}`. Expected `'ATC'`. Try again!"
          )
      except Exception as e:
        st.error(f"Python Syntax Error: {e}")

  with quest_tab[1]:
    st.subheader("Mission 2: Alloy Yield Strength Function")
    st.markdown(
        "*Objective*: Define a Python function `calculate_stress(strain,"
        " youngs_modulus)` that returns stress ($\sigma = E \times \epsilon$)."
    )

    st.code(
        "def calculate_stress(strain, youngs_modulus):\n    # Return"
        " calculated stress\n    pass",
        language="python",
    )

    user_func = st.text_area(
        "Complete the function body:",
        value="    return strain * youngs_modulus",
    )

    if st.button("Test Function"):
      try:
        namespace = {}
        full_code = (
            "def calculate_stress(strain, youngs_modulus):\n" + user_func
        )
        exec(full_code, namespace)
        test_val = namespace["calculate_stress"](0.002, 200)
        if test_val == 0.4:
          st.success(
              "Function works perfectly! Stress = 0.4 GPa. +50 XP Earned!"
          )
          st.session_state.xp += 50
          st.session_state.quests_completed += 1
          st.rerun()
        else:
          st.error(
              f"Tested with strain=0.002, E=200. Got {test_val}, expected"
              " 0.4."
          )
      except Exception as e:
        st.error(f"Error executing code: {e}")

# ---------------------------------------------------------
# 3. INTERACTIVE LAB & CODE SANDBOX
# ---------------------------------------------------------
elif menu == "Interactive Lab & Code Sandbox":
  st.title("🧪 Interactive Engineering & Biotech Sandbox")
  st.markdown(
      "Tweak variables below and see the underlying Python code and live"
      " Matplotlib/Plotly graphs!"
  )

  sim_type = st.selectbox(
      "Select Simulation Domain",
      ["Bacterial Population Growth (Biotech)", "Tensile Stress-Strain Curve (Materials)"],
  )

  if sim_type == "Bacterial Population Growth (Biotech)":
    st.subheader("Microbial Exponential Growth Model")
    n0 = st.number_input("Initial Population (N0)", value=1000)
    gen_time = st.slider("Generation Time (mins)", 20, 60, 30)
    total_time = st.slider("Total Time (hours)", 1, 12, 6)

    # Live Python Code Display
    st.markdown("**Underlying Python Code Executed Live:**")
    st.code(
        f"""import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, {total_time}, 100)
k = np.log(2) / ({gen_time} / 60)
population = {n0} * np.exp(k * t)

plt.plot(t, population, color='cyan')
plt.xlabel('Time (hours)')
plt.ylabel('Population')
""",
        language="python",
    )

    # Generate live plot
    t = np.linspace(0, total_time, 100)
    k = np.log(2) / (gen_time / 60)
    population = n0 * np.exp(k * t)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t, population, color="#00ffcc", linewidth=2)
    ax.set_facecolor("#1e1e1e")
    fig.patch.set_facecolor("#121212")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    st.pyplot(fig)

  else:
    st.subheader("Alloy Stress-Strain Simulation")
    youngs = st.slider("Young's Modulus E (GPa)", 50, 300, 200)
    yield_str = st.slider("Yield Strength (MPa)", 200, 1000, 400)

    st.markdown("**Underlying Python Code Executed Live:**")
    st.code(
        f"""import numpy as np
import plotly.express as px

strain = np.linspace(0, 0.05, 100)
stress = np.where(strain < {yield_str}/({youngs}*1000), 
                  strain * {youngs} * 1000, 
                  {yield_str})
fig = px.line(x=strain, y=stress, labels={{'x': 'Strain', 'y': 'Stress (MPa)'}})
""",
        language="python",
    )

    strain = np.linspace(0, 0.05, 100)
    stress = np.where(
        strain < yield_str / (youngs * 1000), strain * youngs * 1000, yield_str
    )
    fig = px.line(
        x=strain,
        y=stress,
        labels={"x": "Strain ($\epsilon$)", "y": "Stress ($\sigma$ MPa)"},
    )
    fig.update_layout(
        paper_bgcolor="#121212", plot_bgcolor="#121212", font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 4. DEBUGGING ESCAPE ROOM
# ---------------------------------------------------------
elif menu == "Debugging Escape Room":
  st.title("🚨 Lab Debugging Escape Room")
  st.markdown(
      "A spectrometer calibration script in the lab is throwing a bug! Fix"
      " the broken Python code below to unlock the door."
  )

  st.error("Buggy Code Snippet:\n```python\nwavelengths = [400, 500, 600, 700]\n# ERROR: TypeError during iteration average\navg_wavelength = sum(wavelengths) / len(wavelengths)\nprint(avg_wavelength)\n```")

  st.markdown(
      "*Hint*: The syntax looks correct here, but imagine the list contained"
      " strings like `'400nm'`. How would you sanitize it using a list"
      " comprehension with `int()`?"
  )

  user_fix = st.text_input(
      "Write the corrected list comprehension for sanitizing raw data:",
      value="[int(w.replace('nm','')) for w in ['400nm', '500nm']]",
  )

  if st.button("Attempt Escape"):
    if "int(" in user_fix:
      st.success(
          "🎉 Laboratory Door Unlocked! Instrument calibrated successfully."
          " +50 XP!"
      )
      st.session_state.xp += 50
      st.session_state.quests_completed += 1
      st.rerun()
    else:
      st.error(
          "Still malfunctioning. Make sure you convert string elements to"
          " integers using `int()`."
      )

# ---------------------------------------------------------
# 5. PROFILE & SAVE
# ---------------------------------------------------------
elif menu == "Profile & Save":
  st.title("👤 Researcher Profile & Progress")
  st.write(f"**Current Title**: {st.session_state.python_skill}")
  st.write(f"**Level**: {st.session_state.level}")
  st.write(f"**Total XP**: {st.session_state.xp}")
  st.write(f"**Quests Solved**: {st.session_state.quests_completed}")

  if st.button("Reset Progress"):
    st.session_state.xp = 0
    st.session_state.level = 1
    st.session_state.quests_completed = 0
    st.rerun()
