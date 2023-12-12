import numpy as np

class Node():

    def __init__(self, state, parent = None) -> None:
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0  # prob of being selected
        self.value = 0.0
        self.terminal = False
    

    def is_fully_expanded(self):
        """ Check if the node is fully expanded """
        return len(self.children) == len(self.state.get_legal_actions())
    

    def best_child(self, exploration_weight = 1.0):
        """ Return the best child according to Upper Confidence Bound (UCB) """
        if not self.children:
            return None

        def ucb_score(child):
            exploitation = child.value/child.visits if child.visits > 0 else 0
            exploration = exploration_weight * np.sqrt(2*np.log(self.visits)/child.visits) if child.visits > 0 else 0
            return exploitation + exploration

        return max(self.children, key=ucb_score)


    def select_unexplored_child(self):
        """ Return an unexplored child """
        legal_actions = self.state.get_legal_actions()
        explored_actions = [child.state.last_action for child in self.children]
        unexplored_actions = [act for act in legal_actions if act not in explored_actions]

        if unexplored_actions:
            action = np.random.choice(unexplored_actions)
            return Node(self.state.perform_action(action), parent=self)
        else:
            return None

    def expand(self):
        """ Expand the node by adding a new child """
        unexplored_child = self.select_unexplored_child()
        if unexplored_child:
            self.children.append(unexplored_child)
            return unexplored_child
        else:
            return None
    
    def simulate(self):
        """ Simulate the game from the current state """
        current_state = self.state
        while not current_state.is_terminal():
            random_action = random.choice(current_state.get_legal_actions())
            current_state = current_state.perform_action(random_action)
        return current_state.get_reward()            


    def backpropagate(self, reward):
        """ Update the node statistics """
        node = self 
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent  
        

    # def add_game(self, is_win):
    #     if is_win:
    #         self.value += 1
    #     self.plays+=1


class MonteCarloTreeSearch():

    def __init__(self, root_state, exploration_weight=1.0, iterations=1000):
        self.root = Node(root_state)
        self.exploration_weight = exploration_weight
        self.iterations = iterations
        
    
    def search(self):
        for _ in range(self.iterations):
            node = self.select_node_to_expand()
            if node is not None:
                new_node = node.expand()
                if new_node is not None:
                    reward = new_node.simulate()
                    new_node.backpropagate(reward)
        best_child = self.root.best_child(exploration_weight=0.0)
        return best_child.state.last_action


    def select_node_to_expand(self):
        """ Select a node to expand """
        node = self.root
        while node.is_fully_expanded() and not node.state.is_terminal():
            node = node.best_child(self.exploration_weight)
        return node
        

class GameState:
    
    def __init__(self, obs, conf, trainer):
        self.state = obs["board"]
        self.trainer = trainer
        self.conf = conf
        self.is_terminal_state = False 
        self.last_action = None

    
    def get_legal_actions(self):
        return [i for i, col in enumerate(self.state[:self.conf['columns']]) if col == 0]

    def perform_action(self, action):
        obs, reward, done, info = self.trainer.step(action)
        new_state = GameState(obs, self.conf, self.trainer)
        new_state.last_action = action
        new_state.is_terminal_state = done
        
        if done:
            obs = trainer.reset()
        return new_state

    def is_terminal(self):
        return self.is_terminal_state

    def get_reward(self):
        return 1.0 if self.is_terminal_state else 0.0

    def copy(self):
        pass

from kaggle_environments import evaluate, make, utils


env = make("connectx", debug=True)
trainer = env.train(["random", None])
obs = trainer.reset()
done = False
conf = env.configuration
env.render()
initial_state = GameState(obs, conf, trainer=trainer)
mcts = MonteCarloTreeSearch(initial_state, iterations=1000)
action = mcts.search()
obs, reward, done, info = trainer.step(action)
env.render()
print(action)

# while not done:
#     a = agent.act(obs)
#     obs, reward, done, info = trainer.step(a)
#     print(obs, reward, done, info)
#     env.render()
#     if done:
#         obs = trainer.reset()
# env.render()