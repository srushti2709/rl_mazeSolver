import random
import pickle

# Maze size
SIZE = 5

# Goal position
GOAL = (4, 4)

# Actions
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

# Q-table
q_table = {}

# Parameters
alpha = 0.1
gamma = 0.9
epsilon = 0.2

# Move function
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

# Reward
def reward(state):

    if state == GOAL:
        return 100

    return -1

# Choose action
def choose_action(state):

    if random.uniform(0,1) < epsilon:
        return random.choice(ACTIONS)

    qs = [q_table.get((state,a),0)
          for a in ACTIONS]

    max_q = max(qs)

    return ACTIONS[qs.index(max_q)]

# Training
for episode in range(5000):

    state = (0,0)

    while state != GOAL:

        action = choose_action(state)

        next_state = move(state, action)

        r = reward(next_state)

        old_q = q_table.get((state,action),0)

        future_q = max([
            q_table.get((next_state,a),0)
            for a in ACTIONS
        ])

        new_q = old_q + alpha * (
            r + gamma * future_q - old_q
        )

        q_table[(state,action)] = new_q

        state = next_state

# Save model
with open("qtable.pkl","wb") as f:
    pickle.dump(q_table,f)

print("Training Complete")