# Master Rule Book: Reinforcement Learning (RL) Optimizer
# This agent learns to maximize (Fees - Impermanent Loss)
import numpy as np
import random

class RLOptimizer:
    """
    Expert Brain: Q-Learning Agent for Range Optimization.
    Satisfies Requirement: RL agent to optimize LP range based on past performance.
    """
    def __init__(self, actions=[0.8, 1.0, 1.2, 1.5]):
        self.actions = actions  # Possible range multipliers
        self.q_table = {}       # Knowledge base: {state: [scores_for_actions]}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1      # Exploration rate

    def get_state(self, regime, news_risk):
        # Simplify the world into a 'State' string
        return f"{regime}_{round(news_risk, 1)}"

    def choose_action(self, state):
        # Master Rule: Epsilon-Greedy (Try new things 10% of the time)
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))
        
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(range(len(self.actions)))
        else:
            return np.argmax(self.q_table[state])

    def update_knowledge(self, state, action_idx, reward, next_state):
        """
        The 'Learning' part. Reward = (Fees Earned - Impermanent Loss).
        """
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(len(self.actions))
            
        old_value = self.q_table[state][action_idx]
        next_max = np.max(self.q_table[next_state])
        
        # Bellman Equation: Update the Q-value
        new_value = (1 - self.learning_rate) * old_value + \
                    self.learning_rate * (reward + self.discount_factor * next_max)
        
        self.q_table[state][action_idx] = new_value

    def get_optimal_multiplier(self, regime, news_risk):
        state = self.get_state(regime, news_risk)
        action_idx = self.choose_action(state)
        return self.actions[action_idx]
