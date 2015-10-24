# wordtypes.py
# summary: contains data structures for holding tree of words and word types

from enum import Enum

WT = Enum(
	'Sentence',
	'Subject',
	'Predicate',
	'Noun'
)

class WordTypeNode:
	def __init__(self, parent, expansions):
		self.parent = parent
		self.expansions = expansions

def create_dic(wt_expansion_tuple_list):
	# tuple[0]: wordtype, tuple[1]: expansion
	nodes = {}
	for wt_expansion_tuple in wt_expansion_tuple_list:
		nodes[wt_expansion_tuple[0]] = WordTypeNode(wt_expansion_tuple[0], wt_expansion_tuple[1])
	return nodes
	
	
nodes = create_dic([
	( WT.Sentence, [[WT.Subject, WT.Predicate]] ),
	( WT.Subject, [[WT.Noun], [WT.Noun, "and", WT.Subject], [WT.Noun, "or", WT.Subject]] ),
	( WT.Noun, [["Harry"]] ),
	( WT.Predicate, [["sat"]] )
])

def get_expansions(node):
	if type(node) is str:
		return [[node]]
	else:
		if node in nodes:
			return nodes[node].expansions
		else:
			return [["Error: word not it nodes dictionary"]]