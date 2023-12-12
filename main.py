from kaggle_environments import evaluate, make, utils
    
class TreePolicy:
	def __init__(self, board):
		self.board = board
		self.plays = 0
		self.wins = 0	
		self.children = dict() # <act, TreePolicy>

	def update_values(self):

		
	

class Actor:
	def __init__(self, config):
		self.treepolicy = TreePolicy(config)
		self.moves = list()

	def act(self, obs):


	def select_leaf(self):
		for board, action in reversed(self.moves):



def act(obs, conf):
    board = tuple(obs['board'])
    return 0

def col_playable(obs, conf):
    return (i for i, col in enumerate(obs["board"][:conf['columns']]) if col == 0)	


env = make("connectx", debug=True)
trainer = env.train([None, 'random'])
obs = trainer.reset()
done = False
while not done:
	a = act(obs, env.configuration)
	obs, reward, done, info = trainer.step(a)
	print(obs, reward, done, info)
	env.render()
env.render()


