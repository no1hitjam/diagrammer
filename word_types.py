# wordtypes.py
# summary: contains data structures for holding tree of words and word types

from enum import Enum

WT = Enum(
	'Sentence',
	'Subject',
	'Predicate',
	'IndirectObject',
    'DirectObject',
	'ObjectiveComplement',
	'Appositive',
	'CompoundableObject',
    'Object',
	'Noun',
	'CompoundableAdjective',
    'Adjective',
    'Verb'
)

def create_dic(wt_expansion_tuple_list):
# summary: create dictionary of possible parse nodes from list of tuples
# tuple[0]: wordtype, tuple[1]: expansion
	nodes = {}
	for wt_expansion_tuple in wt_expansion_tuple_list:
		nodes[wt_expansion_tuple[0]] = wt_expansion_tuple[1]

	return nodes

def convert_csv_to_expansion(csv_str):
	return map(lambda x: x.split(" "), csv_str.split(", "))
	
nodes = create_dic([
	( WT.Sentence, [
		[WT.Subject, WT.Predicate], # [1] Simple subject and predicate
		[WT.Predicate]	# [2] Understood subject (for commands, directives) 
    ]),
	( WT.Subject, [
        [WT.Object], 
        [WT.Object, "and", WT.Subject], # [5] Compound subject
        [WT.Object, "or", WT.Subject]
    ]),
	( WT.Predicate, [
        [WT.Verb], 
		[WT.Verb, WT.IndirectObject, WT.DirectObject], # [12] Indirect object
		[WT.Verb, WT.DirectObject], # [7] Direct object
        [WT.Verb, "and", WT.Predicate] # [4] Compound predicate
    ]),
	( WT.IndirectObject, [ 
        [WT.CompoundableObject]
    ]),
    ( WT.DirectObject, [ 
        [WT.CompoundableObject]
    ]),
	( WT.Appositive, [ 
        [WT.CompoundableObject]
    ]),
	( WT.ObjectiveComplement, [ 
        [WT.CompoundableAdjective]
    ]),
	( WT.CompoundableObject, [
		[WT.Object],
		[WT.Object, "and", WT.CompoundableObject] # [8] Compound direct objects
	]),
    ( WT.Object, [
        [WT.Noun], 
		[WT.Noun, WT.ObjectiveComplement], # [17] Objective Complement
		[WT.Noun, ",", WT.Appositive, ","], # [18] Appositive
        [WT.CompoundableAdjective, WT.Object]
    ]),
	( WT.CompoundableAdjective, [
		[WT.Adjective],
		[WT.Adjective, ",", WT.CompoundableAdjective],
		[WT.Adjective, "and", WT.CompoundableAdjective]
	]),
    ( WT.Noun, convert_csv_to_expansion(
		"Fred, Harry, chair, couch, table, down"
	)),
    ( WT.Adjective, convert_csv_to_expansion(
		"the, a, smelly, purple, green, blue"
	)),
    ( WT.Verb, convert_csv_to_expansion(
		"sat, sit, sits, painted"
	))
	
])

# chck [14], [15]

def get_expansions(node):
# summary: return list of child nodes
	if type(node) is str:
		return [[node]]
	else:
		if node in nodes:
			return nodes[node]
		else:
			return [["Error: word not it nodes dictionary"]]