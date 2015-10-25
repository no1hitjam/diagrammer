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
	"PrepositionPhrase",
	'Preposition'
)

def create_dic(expansion_blueprint_list):
# summary: create dictionary of possible parse nodes from list of tuples
# tuple[0]: wordtype, tuple[1]: expansion, tuple[2]: post-expansions
	nodes = {}
	for expansion_blueprint in expansion_blueprint_list:
		key = expansion_blueprint[0]
		expansions = expansion_blueprint[1]
		post_expansions = []
		if len(expansion_blueprint) == 3:
			post_expansions = expansion_blueprint[2]

		nodes[key] = list(expansions)

		# the third item in the input list is an optional list of post-expansions
		# these go at the end of every possibility
		# the reason for this is to avoid infinite loops when parsing
		# it's a little crude, so I'll consider changing this eventually.
		for post_expansion in post_expansions:
			for expansion in expansions:
				# this if statement reduces almost duplicate tree results
				if expansion[-1:][0] != key:
					nodes[key].append(list(expansion) + list(post_expansion))
	return nodes

def expand_csv(csv_str):
	return map(lambda x: x.split(" "), csv_str.split(", "))
	
nodes = create_dic([

	[ WT.Sentence, [ [ WT.Subject, WT.Predicate ],		# [1] Simple subject and predicate
					 [ WT.Subject, ",", WT.Predicate ], # [19] Direct address
					 [ WT.Predicate ]					# [2] Understood subject (for commands, directives) 
    ] ],

	[ WT.Subject, [ [ WT.CompoundableObject ] ] ],

	[ WT.Predicate, [ [ WT.Verb ], 
					  [ WT.Verb, WT.IndirectObject, WT.DirectObject ],						# [12] Indirect object
					  [ WT.Verb, WT.DirectObject ],											# [7] Direct object
					  [ WT.Verb, ",", WT.Predicate ],										# [4] Compound predicate
					  [ WT.Verb, "and", WT.Predicate ],										# [4] Compound predicate
					  [ WT.Verb, WT.ComparativeAdjective, "than", WT.CompoundableObject ],
					  [ WT.CompoundableAdverb, WT.Predicate ]
    ], [ # added to the end of every expansion
	   [ WT.CompoundableAdverb ],
	   [ WT.PrepositionPhrase ]
	] ],

	[ WT.IndirectObject, [ [ WT.CompoundableObject ] ] ],

    [ WT.DirectObject, [ [ WT.CompoundableObject ] ] ],

	[ WT.Appositive, [ [ WT.CompoundableObject ] ] ],

	[ WT.ObjectiveComplement, [ [ WT.CompoundableAdjective ] ] ],

	[ WT.CompoundableObject, [ [ WT.Object ],
							   [ WT.Object, "and", WT.CompoundableObject ] # [8] Compound direct objects
	] ],

	[ WT.PrepositionPhrase, [ [ WT.Preposition, WT.CompoundableObject ],
							  [ WT.Preposition, WT.CompoundableObject, "and", WT.PrepositionPhrase ],
							  [ WT.Preposition, WT.CompoundableObject, WT.PrepositionPhrase ]
	] ],

    [ WT.Object, [ [WT.Noun], 
				   [WT.Noun, WT.ObjectiveComplement], # [17] Objective Complement
				   [WT.Noun, ",", WT.Appositive, ","], # [18] Appositive
		           [WT.CompoundableAdjective, WT.Object]
    ] ],

	[ WT.CompoundableAdjective, [ [WT.Adjective],
								  [WT.Adjective, ",", WT.CompoundableAdjective],
								  [WT.Adjective, "and", WT.CompoundableAdjective]
	] ],

	[ WT.CompoundableAdverb, [ [WT.Adverb],
							   [WT.Adverb, ",", WT.CompoundableAdverb],
							   [WT.Adverb, "and", WT.CompoundableAdverb]
	] , [ # added to the end of every expansion
		[WT.PrepositionPhrase]
	] ],

    [ WT.Noun, expand_csv( "Fred, Harry, chair, couch, table, down" ) ],

    [ WT.Adjective, expand_csv( "the, a, smelly, purple, green, blue") ],

	[ WT.ComparativeAdjective, expand_csv( "taller, shorter, smarter, purpler, better" ) ],

    [ WT.Verb, expand_csv( "sat, sit, sits, painted, paint, paints, is, was, will be" ) ],

	[ WT.Adverb, expand_csv( "quickly, smartly, smellily, quietly" ) ],

	[ WT.Preposition, expand_csv( "in, under, around, on" ) ]
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