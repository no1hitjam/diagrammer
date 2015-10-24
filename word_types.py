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
	'ComparativeAdjective',
    'Adjective',
    'Verb',
	'CompoundableAdverb',
	'Adverb',
	'Preposition'
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
		[WT.Subject, ",", WT.Predicate], # [19] Direct address
		[WT.Predicate]	# [2] Understood subject (for commands, directives) 
    ]),
	( WT.Subject, [
        [WT.CompoundableObject]
    ]),
	( WT.Predicate, [
        [WT.Verb], 
		[WT.Verb, WT.IndirectObject, WT.DirectObject], # [12] Indirect object
		[WT.Verb, WT.DirectObject], # [7] Direct object
		[WT.Verb, ",", WT.Predicate], # [4] Compound predicate
        [WT.Verb, "and", WT.Predicate], # [4] Compound predicate
		[WT.Verb, WT.ComparativeAdjective, "than", WT.CompoundableObject],
		[WT.Verb, WT.CompoundableAdverb],
		[WT.CompoundableAdverb, WT.Verb],
		[WT.CompoundableAdverb, WT.Verb, WT.CompoundableAdverb],
		[WT.Verb, WT.Preposition, WT.CompoundableObject]
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
	( WT.CompoundableAdverb, [
		[WT.Adverb],
		[WT.Adverb, ",", WT.CompoundableAdverb],
		[WT.Adverb, "and", WT.CompoundableAdverb]
	]),
    ( WT.Noun, convert_csv_to_expansion(
		"Fred, Harry, chair, couch, table, down"
	)),
    ( WT.Adjective, convert_csv_to_expansion(
		"the, a, smelly, purple, green, blue"
	)),
	( WT.ComparativeAdjective, convert_csv_to_expansion(
		"taller, shorter, smarter, purpler, better"
	)),
    ( WT.Verb, convert_csv_to_expansion(
		"sat, sit, sits, painted, paint, paints, is, was, will be"
	)),
	( WT.Adverb, convert_csv_to_expansion(
		"quickly, smartly, smellily"
	)),
	( WT.Preposition, convert_csv_to_expansion(
		"in, under, around"
	))
])

# chck [14], [15], [20], [23], [27]

def get_expansions(node):
# summary: return list of child nodes
	if type(node) is str:
		return [[node]]
	else:
		if node in nodes:
			return nodes[node]
		else:
			return [["Error: word not it nodes dictionary"]]