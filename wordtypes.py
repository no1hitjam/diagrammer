# wordtypes.py
# summary: contains data structures for holding tree of words and word types

from enum import Enum

WT = Enum(
	'Sentence',
	'Subject',
	'Predicate',
    'DirectObject',
    'Object',
	'Noun',
    'Adjective',
    'Verb'
)

def create_dic(wt_expansion_tuple_list):
	# tuple[0]: wordtype, tuple[1]: expansion
	nodes = {}
	for wt_expansion_tuple in wt_expansion_tuple_list:
		nodes[wt_expansion_tuple[0]] = wt_expansion_tuple[1]

	return nodes
	
	
nodes = create_dic([
	( WT.Sentence, [
        [WT.Subject, WT.Predicate] 
    ]),
	( WT.Subject, [
        [WT.Object], 
        [WT.Object, "and", WT.Subject], 
        [WT.Object, "or", WT.Subject]
    ]),
	( WT.Predicate, [
        [WT.Verb], 
        [WT.Verb, "and", WT.Predicate]
    ]),
    ( WT.DirectObject, [
        [WT.Object]
    ]),
    ( WT.Object, [
        [WT.Noun], 
        [WT.Adjective, WT.Object]
    ]),
    ( WT.Noun, [["Harry"]] ),
    ( WT.Adjective, [["smelly"], ["the"]] ),
    ( WT.Verb, [["sat"]] )
])

def get_expansions(node):
	if type(node) is str:
		return [[node]]
	else:
		if node in nodes:
			return nodes[node]
		else:
			return [["Error: word not it nodes dictionary"]]