import streamlit as st
import pickle
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Maze Solver",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
with open("qtable.pkl", "rb") as f:
    q_table = pickle.load(f)

# ---------------- CONSTANTS ----------------
SIZE = 5
GOAL = (4, 4)

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

# ---------------- SESSION STATES ----------------
if "agent" not in st.session_state:
    st.session_state.agent = (0, 0)

if "moves" not in st.session_state:
    st.session_state.moves = 0

if "wins" not in st.session_state:
    st.session_state.wins = 0

if "status" not in st.session_state:
    st.session_state.status = "Ready"

# ---------------- THEME CHANGER ----------------
st.sidebar.title("🎨 Theme Settings")

theme = st.sidebar.radio(
    "Choose Theme",
    ["Light", "Dark", "Blue AI"]
)

# ---------------- THEMES ----------------
if theme == "Light":

    bg_color = "#f5f7fa"
    card_color = "white"
    text_color = "black"
    grid_color = "#ffffff"

elif theme == "Dark":

    bg_color = "#0e1117"
    card_color = "#1c1f26"
    text_color = "white"
    grid_color = "#262730"

else:

    bg_color = "#e8f4ff"
    card_color = "#d6ecff"
    text_color = "#003366"
    grid_color = "#f0f8ff"

# ---------------- CUSTOM CSS ----------------
st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}

    .card {{
        background-color: {card_color};
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }}

    .grid {{
        height: 90px;
        border-radius: 15px;
        background-color: {grid_color};
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 45px;
        border: 2px solid #ddd;
        margin: 5px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- FUNCTIONS ----------------
def move(state, action):

    x, y = state

    if action == "UP":
        x = max(0, x - 1)

    elif action == "DOWN":
        x = min(SIZE - 1, x + 1)

    elif action == "LEFT":
        y = max(0, y - 1)

    elif action == "RIGHT":
        y = min(SIZE - 1, y + 1)

    return (x, y)

# ---------------- BEST ACTION ----------------
def best_action(state):

    qs = []

    for action in ACTIONS:
        qs.append(q_table.get((state, action), 0))

    if len(qs) == 0:
        return "RIGHT"

    max_q = max(qs)

    return ACTIONS[qs.index(max_q)]

# ---------------- SIDEBAR ----------------
st.sidebar.title("📘 RL Project Information")

st.sidebar.write("""
### 🤖 Agent
Maze Solving Robot

### 🧠 Algorithm
Q-Learning

### 🌍 Environment
5×5 Maze Grid

### 🎯 Goal
Reach Destination

### 🏆 Reward
+100

### ❌ Penalty
-1 Per Step
""")

# ---------------- TITLE ----------------
st.markdown(
    f"""
    <h1 style='text-align:center;color:{text_color};'>
    🤖 AI Maze Solver Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h4 style='text-align:center;color:gray;'>
    Reinforcement Learning using Q-Learning
    </h4>
    """,
    unsafe_allow_html=True
)

st.write("")

# ---------------- DASHBOARD ----------------
col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""
        <div class='card'>
        <h3>🚶 Moves</h3>
        <h1>{st.session_state.moves}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class='card'>
        <h3>🏁 Goals</h3>
        <h1>{st.session_state.wins}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class='card'>
        <h3>📌 Status</h3>
        <h2>{st.session_state.status}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# ---------------- PROGRESS BAR ----------------
progress = min(st.session_state.moves / 20, 1.0)

st.progress(progress)

st.write("")

# ---------------- MAZE GRID ----------------
for i in range(SIZE):

    cols = st.columns(SIZE)

    for j in range(SIZE):

        emoji = "⬜"

        # Goal
        if (i, j) == GOAL:
            emoji = "🏁"

        # Agent
        if (i, j) == st.session_state.agent:
            emoji = "🤖"

        cols[j].markdown(
            f"""
            <div class='grid'>
            {emoji}
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

# ---------------- BUTTONS ----------------
col1, col2, col3 = st.columns(3)

# NEXT MOVE
with col1:

    if st.button("▶ Next Move", use_container_width=True):

        action = best_action(st.session_state.agent)

        st.session_state.agent = move(
            st.session_state.agent,
            action
        )

        st.session_state.moves += 1

        st.session_state.status = action

        if st.session_state.agent == GOAL:

            st.session_state.wins += 1

            st.session_state.status = "Goal Reached"

            st.success("🎉 Goal Reached Successfully!")

# AUTO SOLVE
with col2:

    if st.button("⚡ Auto Solve", use_container_width=True):

        for _ in range(20):

            if st.session_state.agent == GOAL:
                break

            action = best_action(
                st.session_state.agent
            )

            st.session_state.agent = move(
                st.session_state.agent,
                action
            )

            st.session_state.moves += 1

            st.session_state.status = action

            time.sleep(0.2)

        if st.session_state.agent == GOAL:

            st.session_state.wins += 1

            st.session_state.status = "Goal Reached"

            st.success("🎉 Goal Reached Successfully!")

# RESTART
with col3:

    if st.button("🔄 Restart", use_container_width=True):

        st.session_state.agent = (0, 0)

        st.session_state.moves = 0

        st.session_state.status = "Restarted"

        st.rerun()

st.write("")

# ---------------- FOOTER ----------------
st.info(
    "This project demonstrates Reinforcement Learning "
    "using Q-Learning where the AI agent learns the "
    "shortest path using rewards and penalties."
)