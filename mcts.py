class Node():
    def __init__(self) -> None:
        self.value = 0
        self.plays = 0
        self.children = {}
        self.terminal = False
    
    def get_value(self):
        if self.plays:
            return self.value/self.plays
        return 0
    
    def add_game(self, is_win):
        if is_win:
            self.value += 1
        self.plays+=1


class MCTS():
    
    def __init__(self, env, num_simulations) -> None:
        self.env = env
        self.num_simulations = num_simulations
        
    
    def mcts(self, state):
        root = Node()
        node = root
        #trajectory = [root] 
        
        while node.children:
            # TODO
            # 1. Select action according to tree policy
            # 2. Consider the children node according to the action
            # 3. Extecute the action and update values 
            # 4. Append new node 

            act = self.treepolicy() # -> Restituisce un azione
            next_node = node.children[act]
            
            obs, reward, done, info = self.env.step(act)
            next_node.value, next_node.terminal = reward, done
			
			#trajectory.append(next_node)
            node = next_node

			# Check if node is terminal 
            if node.terminal:
                 value = # Se ho vinto perso/vinto/ pareggio
        