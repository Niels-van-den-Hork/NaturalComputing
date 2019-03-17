import numpy as np

def flatten(xs):
	for x in xs:
		for x_ in x:
			yield x_

class Pos:
	def __init__(self,p):
		self.x = p[0]
		self.y = p[1]
		self.p = p
		self.value = -1
		self.possible = set(range(1,9+1))
		self.ppselected = False #for 'selecting' a location ONLY in pretty printing
	
	def	copy(self,):
		p = Pos(self.p)
		p.value = self.value
		p.possible = self.possible.copy()
		return p
		
	def gen_peers(self,sudoku):
		rx = 3*int(self.x/3) #rx := root (lefttop) position of x
		ry = 3*int(self.y/3)
		
		peers = set()
		peers.update( [(x	   , self.y	) for x in range(9)] )
		peers.update( [(self.x , y		) for y in range(9)] )
		peers.update( flatten( [[ (rx + dx, ry + dy) for dx in range(3)] for dy in range(3)] ) )
		peers.remove(self.p)
		
		assert(len(peers) == 20)
		
		self.peers = [sudoku.get_pos(peer) for peer in peers]
		
	def get_peers(self):
		return self.peers
	
	def set_value(self,val ):#set definite value
		self.value = val
		if val > 0:
			self.possible = set([val])
		
	def get_value(self):
		return self.value
		
	def remove_possibility(self,value): #remove one possible value from this pos (when a peer has that value already)
		assert (value in self.possible)
		self.possible.remove(value)
		
	def __str__(self):
		return f'({self.x},{self.y}) {self.value} {self.possible}'
	
	def __repr__(self):
		return f'({self.x},{self.y}) {self.value} {self.possible}'
	
	def ppselect(self):
		self.ppselected = True
	
	def ppunselect(self):
		self.ppselected = False
	
	def pprint_pos(self):
		#print(self.possible)
		if self.ppselected:
			return '(' + ''.join([str(v) for v in self.possible]) +') '+ ' ' * (5-len(self.possible))
		return     ' ' + ''.join([str(v) for v in self.possible]) +'  '+ ' ' * (5-len(self.possible))
				
	def pprint_val(self):
		if self.ppselected:
			return "(" + str(self.value) + ")" if self.value > 0 else '(_)'
		return     " " + str(self.value) + " " if self.value > 0 else ' _ '
		
class Sudoku:
	def __init__(self,filename,outputfile):
		self.board = [[Pos((x,y)) for x in range(9)] for y in range(9)]
		self.output_log = open(outputfile,'w+')
		self.input_sudoku = open(filename,'r')
		
		for p,val in zip(flatten(self.board), flatten(self.load(self.input_sudoku))):
			p.gen_peers(self)
			p.set_value(val)
		
		self.pprint_val()
		self.pprint_pos()
		self.simplify()
		self.backup = [[pos.copy() for pos in row] for row in self.board]
		print([p for p in self.backup])
		
	def simplify(self,):
		while self.propagate():
			print('iter')
			self.pprint_val()
			self.pprint_pos()
		
		print('done')	
	
	def isValid(self,):
		pass
	
	def load(self,file):
		return [list(map(int,line[:-2].split(' '))) for line in file]

	def reset(self):
		self.board = self.backup
		
	def propagate(self,):
		update = False
		for pos in flatten(self.board):
			#if pos.x == 8 and pos.y == 7:
			#	print(pos)
			if pos.value <= 0:
				for peer in pos.peers:
					if peer.value > 0 and peer.value in pos.possible:
						pos.remove_possibility(peer.value)
						update = True
					
					#if pos.x == 8 and pos.y == 7 and peer.value > 0:
					#	print(peer)
			if len(pos.possible) == 1:
				pos.value = list(pos.possible)[0]
				
		return update

	def get_pos(self,tpos): # tpos is tuple
		return self.board[tpos[1]][tpos[0]]
	
	def pprint_pos(self):
		str = '\nPossible values:\n'
		str += '+' + ('-' * 8 * 3 + '+') * 3 + '\n'
		for ri,row in enumerate(self.board):
			for pi,pos in enumerate(row):
				if pi == 0:
					str += '|'
				str += pos.pprint_pos()
				if pi % 3 == 2:
					str += '|'
				
			str += '\n'
			if ri % 3 == 2:
				str += '+' + ('-' * 8 * 3 + '+') * 3 + '\n'
		#print(str)
		self.output_log.write(str)
				
	def pprint_val(self):
		str = '\nValues:\n'
		str += '+' + ('-' * 3 * 3 + '+') * 3 + '\n'
		for ri,row in enumerate(self.board):
			for pi,pos in enumerate(row):
				if pi == 0:
					str += '|'
				str += pos.pprint_val() 
				if pi % 3 == 2:
					str += '|'
			str += '\n'
			if ri % 3 == 2:
				str += '+' + ('-' * 3 * 3 + '+') * 3 + '\n'
		#print(str)
		self.output_log.write(str)
		
class Colony:
	def __init__(self,sudoku):
		self.pheremone = np.zeros((9,9,9))
		self.sudoku = sudoku
		
		
sudoku = Sudoku('s01a.txt','output.log')

colony = Colony(sudoku)
#[sel.ppselect() for sel in x.get_pos((8,7)).peers]
#x.pprint_val()
#x.pprint_pos()
#[sel.ppunselect() for sel in x.get_pos((8,7)).peers]

