# wordtypes.py
# summary: contains data structures for holding tree of words and word types

from enum import Enum

#class ParseOption:
#    def __init__(self, key, expansions

WT = Enum(
    'Sentence',
    'Subject',
    'Gerund',
    'Predicate',
    'IndirectObject',
    'DirectObject',
    'ObjectiveComplement',
    'Appositive',
    'Object_',
    'Object',
    'Noun',
    'Adjective_',
    'ComparativeAdjective',
    'Adjective',
    'Verb_',
    'Verb',
    'Adverb_',
    'Adverb',
    "PrepositionPhrase",
    'Preposition',
    'ParticiplePhrase',
    'Participle'
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

def Compound( word_type, compoundable_type ):
# TODO: "or" and "but", and general smartness
    return [ [ word_type ],
             [ word_type, ",", compoundable_type ],
             [ word_type, "and", compoundable_type ] ]


def expand_csv(csv_str):
    return map(lambda x: x.split(" "), csv_str[:-2].split(", "))
   
# import words
# TODO: actual importing
nouns = "Fred, Harry, chair, couch, table, down, "

participles =  "crumbling, fighting, "

adjectives = "the, a, smelly, purple, green, blue, "

comparative_adjectives = "taller, shorter, smarter, purpler, better, "

gerund_verbs = "sitting, painting, being"

verbs = "sat, sit, sits, painted, paint, paints, is, was, will be, are, "

adverbs = "quickly, smartly, smellily, quietly, "

prepositions = "in, under, around, on, "


# create tree structure
nodes = create_dic([

    [ WT.Sentence, [ [ WT.Subject, WT.Predicate ],      # [1] Simple subject and predicate
                     [ WT.Subject, ",", WT.Predicate ], # [19] Direct address
                     [ WT.Predicate ]                   # [2] Understood subject (for commands, directives) 
    ] ],

    [ WT.Subject, [ [ WT.Object_ ] ] ],

    [ WT.Predicate, [ [ WT.Verb_ ], 
                      [ WT.Verb_, WT.IndirectObject, WT.DirectObject ],                       # [12] Indirect object
                      [ WT.Verb_, WT.DirectObject ],                                          # [7] Direct object
                      [ WT.Verb_, WT.Adjective ],                                             # [23] Predicate adjective
                      [ WT.Verb_, WT.ComparativeAdjective, "than", WT.Object_ ],
                      [ WT.Adverb_, WT.Predicate ]
    ] , [ # added to the end of every expansion
        [ WT.Adverb_ ],
        [ WT.PrepositionPhrase ]
    ] ],

    [ WT.IndirectObject, [ [ WT.Object_ ] ] ],

    [ WT.DirectObject, [ [ WT.Object_ ] ] ],

    [ WT.Appositive, [ [ WT.Object_ ] ] ],

    [ WT.ObjectiveComplement, [ [ WT.Adjective_ ] ] ],

    [ WT.PrepositionPhrase, [ [ WT.Preposition, WT.Object_ ],
                              [ WT.Preposition, WT.Object_, "and", WT.PrepositionPhrase ],
                              [ WT.Preposition, WT.Object_, WT.PrepositionPhrase ]
    ] ],

    [ WT.Object, [ [ WT.Noun ], 
                   [ WT.Gerund ], 
                   [ WT.Noun, WT.ObjectiveComplement ],       # [17] Objective Complement
                   [ WT.Noun, ",", WT.Appositive, "," ],      # [18] Appositive
                   [ WT.Adjective_, WT.Object ]
    ] ],

    [ WT.Gerund, [ [ WT.Verb_ ],
                   [ WT.Verb_, WT.Adjective_ ]            
    ] ],

    [ WT.ParticiplePhrase, [ [ WT.Participle ],
                             [ WT.Participle, WT.PrepositionPhrase ]
    ] ],

    # compoundables
    [ WT.Object_, Compound( WT.Object, WT.Object_ ) ],

    [ WT.Verb_, Compound( WT.Verb, WT.Verb_ ) ],

    [ WT.Adjective_, Compound( WT.Adjective, WT.Adjective_ ) ],

    [ WT.Adverb_, Compound ( WT.Adverb, WT.Adverb_ ), 
        [ # added to the end of every expansion
        [ WT.PrepositionPhrase ]
    ] ],

    # strings

    [ WT.Noun, expand_csv( nouns ) ],

    [ WT.Participle, expand_csv(participles) ],

    [ WT.Adjective, expand_csv( adjectives + comparative_adjectives + participles) ],

    [ WT.ComparativeAdjective, expand_csv( comparative_adjectives ) ],

    [ WT.Verb, expand_csv( verbs + gerund_verbs ) ],

    [ WT.Adverb, expand_csv( adverbs ) ],

    [ WT.Preposition, expand_csv( prepositions ) ]
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