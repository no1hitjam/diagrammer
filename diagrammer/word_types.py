# word_types.py
# summary: contains data structures for holding tree of words and word types

import json


class WT:
    def __init__(self):
        return

    Sentence = 'WT_Sentence'
    Subject = 'WT_Subject'
    Gerund = 'WT_Gerund'
    Predicate_ = 'WT_Predicate_'
    Predicate = 'WT_Predicate'
    IndirectObject = 'WT_IndirectObject'
    DirectObject = 'WT_DirectObject'
    ObjectiveComplement = 'WT_ObjectiveComplement'
    Appositive = 'WT_Appositive'
    Object_ = 'WT_Object_'
    Object = 'WT_Object'
    Noun = 'WT_Noun'
    Adjective_ = 'WT_Adjective_'
    ComparativeAdjective = 'WT_ComparativeAdjective'
    Adjective = 'WT_Adjective'
    Verb_ = 'WT_Verb_'
    Verb = 'WT_Verb'
    VerbWord = 'WT_VerbWord'
    GerundVerb_ = 'WT_GerundVerb_'
    GerundVerb = 'WT_GerundVerb'
    InfinitivePhrase = 'WT_InfinitivePhrase'
    InfinitiveVerb_ = 'WT_InfinitiveVerb_'
    InfinitiveVerb = 'WT_InfinitiveVerb'
    Adverb_ = 'WT_Adverb_'
    Adverb = 'WT_Adverb'
    PrepositionPhrase = 'WT_PrepositionPhrase'
    Preposition = 'WT_Preposition'
    ParticiplePhrase = 'WT_ParticiplePhrase'
    Participle = 'WT_Participle'


def create_dic(expansion_blueprint_list):
    # summary: create dictionary of possible parse nodes from list of tuples
    # tuple[0]: word type, tuple[1]: expansion, tuple[2]: post-expansions
    dic_nodes = {}
    for expansion_blueprint in expansion_blueprint_list:
        key = expansion_blueprint[0]
        expansions = expansion_blueprint[1]
        post_expansions = []
        if len(expansion_blueprint) == 3:
            post_expansions = expansion_blueprint[2]

        dic_nodes[key] = list(expansions)

        # the third item in the input list is an optional list of post-expansions
        # these go at the end of every possibility
        # the reason for this is to avoid infinite loops when parsing
        # it's a little crude, so I'll consider changing this eventually.
        for post_expansion in post_expansions:
            for expansion in expansions:
                # this if statement reduces almost duplicate tree results
                if expansion[-1:][0] != key:
                    dic_nodes[key].append(list(expansion) + list(post_expansion))
    return dic_nodes


def compound(word_types, compoundable_type):
    # TODO: "or" and "but", and general smartness
    return [word_types,
            word_types + [",", compoundable_type],
            word_types + ["and", compoundable_type]]


def expand_csv(csv_str):
    return map(lambda x: x.split(" "), csv_str[:-2].split(", "))


def list2d_first_word_dic(list2d):
    result = {}
    for word_list in list2d:
        first_word = word_list[0]
        if first_word in result:
            result[first_word].append(word_list)
        else:
            result[first_word] = [word_list]
    return result


def first_word_dict_get(item, fw_dict):
    return fw_dict[item] if item in fw_dict else []

# import words
# TODO: actual importing
nouns = list2d_first_word_dic(expand_csv("Fred, Harry, chair, chairs, couch, table, down, "))

participles = list2d_first_word_dic(expand_csv("crumbling, fighting, "))

comparative_adjectives = list2d_first_word_dic(expand_csv("taller, shorter, smarter, purpler, better, "))

adjectives = list2d_first_word_dic(expand_csv("the, a, smelly, purple, green, blue, nice, "))

gerund_verbs = list2d_first_word_dic(expand_csv("sitting, painting, being, "))

infinitive_verbs = list2d_first_word_dic(expand_csv("to sit, to paint, to be, "))

# verbs = list2D_firstWordDic(expand_csv("sat, sit, sits, painted, paint, paints, is, was, be, will be, are, "))


with open('diagrammer/data/verbs.json') as verbs_json:
    verbs = json.load(verbs_json)

adverbs = list2d_first_word_dic(expand_csv("quickly, smartly, smellily, quietly, "))

prepositions = list2d_first_word_dic(expand_csv("in, under, around, on, "))

word_strings = {
    WT.Noun: lambda x: first_word_dict_get(x, nouns),
    WT.Participle: lambda x: first_word_dict_get(x, participles),
    WT.ComparativeAdjective: lambda x: first_word_dict_get(x, comparative_adjectives),
    WT.Adjective: lambda x:
        first_word_dict_get(x, adjectives) +
        first_word_dict_get(x, comparative_adjectives) +
        first_word_dict_get(x, participles),
    WT.GerundVerb: lambda x: [[x]] if x in verbs['gerunds'] else [],
    WT.InfinitiveVerb: lambda x: [[x]] if x in verbs['infinitives'] else [],
    WT.VerbWord: lambda x: [[x]] if x in verbs['all'] else [],
    WT.Adverb: lambda x: first_word_dict_get(x, adverbs),
    WT.Preposition: lambda x: first_word_dict_get(x, prepositions)
}

# create tree structure
nodes = create_dic([

    [WT.Sentence, [
        [WT.Subject, WT.Predicate_],      # [1] Simple subject and predicate
        [WT.Subject, ",", WT.Predicate_],  # [19] Direct address
        [WT.Predicate_]                   # [2] Understood subject (for commands, directives)
    ]],

    [WT.Subject, [[WT.Object_]]],

    [WT.Predicate_, compound([WT.Predicate], WT.Predicate_)],

    [WT.Predicate, [
        [WT.Verb],
        [WT.Verb, WT.IndirectObject, WT.DirectObject],     # [12] Indirect object
        [WT.Verb, WT.DirectObject],                        # [7] Direct object
        [WT.Verb, WT.Adjective_],                           # [23] Predicate adjective
        [WT.Verb, WT.ComparativeAdjective, "than", WT.Object_],
        [WT.Adverb_, WT.Predicate_]
    ], [  # added to the end of every expansion
        [WT.Adverb_],
        [WT.PrepositionPhrase]
    ]],

    [WT.IndirectObject, [[WT.Object_]]],

    [WT.DirectObject, [[WT.Object_]]],

    [WT.Appositive, [[WT.Object_]]],

    [WT.ObjectiveComplement, [[WT.Adjective_]]],

    [WT.PrepositionPhrase, [
        [WT.Preposition, WT.Object_],
        [WT.Preposition, WT.Object_, "and", WT.PrepositionPhrase],
        [WT.Preposition, WT.Object_, WT.PrepositionPhrase]
    ]],

    [WT.Object, [
        [WT.Noun],
        [WT.GerundVerb_],
        [WT.Noun, WT.ObjectiveComplement],       # [17] Objective Complement
        [WT.Noun, ",", WT.Appositive, ","],      # [18] Appositive
        [WT.Adjective_, WT.Object]
    ]],

    [WT.InfinitivePhrase, [
        [WT.InfinitiveVerb_],
        [WT.InfinitiveVerb_, WT.IndirectObject, WT.DirectObject],     # [12] Indirect object
        [WT.InfinitiveVerb_, WT.DirectObject],                        # [7] Direct object
        [WT.InfinitiveVerb_, WT.Adjective],                           # [23] Predicate adjective
        [WT.InfinitiveVerb_, WT.ComparativeAdjective, "than", WT.Object_],
        [WT.Adverb_, WT.InfinitivePhrase]
    ], [  # added to the end of every expansion
        [WT.Adverb_],
        [WT.PrepositionPhrase]
    ]],

    [WT.ParticiplePhrase, [
        [WT.Participle],
        [WT.Participle, WT.PrepositionPhrase]
    ]],

    # compoundables
    [WT.Object_, compound([WT.Object], WT.Object_) + [
        [WT.InfinitivePhrase]
    ]],

    [WT.Verb_, compound([WT.Verb], WT.Verb_)],

    [WT.GerundVerb_, compound([WT.GerundVerb], WT.GerundVerb_)],

    [WT.InfinitiveVerb_, compound(["to", WT.InfinitiveVerb], WT.Verb_)],

    [WT.Adjective_, compound([WT.Adjective], WT.Adjective_)],

    [WT.Adverb_, compound([WT.Adverb], WT.Adverb_),
        [  # added to the end of every expansion
        [WT.PrepositionPhrase]
        ]
     ],

    [WT.Verb, [
        [WT.VerbWord],
        ["will", WT.VerbWord],
        ["will", "have", WT.VerbWord],
        ["will", "be", WT.VerbWord],
        ["will", "have", "been", WT.VerbWord],
        ["would", WT.VerbWord],
        ["would", "have", WT.VerbWord],
        ["would", "be", WT.VerbWord],
        ["would", "have", "been", WT.VerbWord],
        ["have", WT.VerbWord],
        ["have", "been", WT.VerbWord],
        ["has", WT.VerbWord],
        ["has", "been", WT.VerbWord],
        ["had", WT.VerbWord],
        ["had", "been", WT.VerbWord],
        ["am", WT.VerbWord],
        ["is", WT.VerbWord],
        ["are", WT.VerbWord],
        ["were", WT.VerbWord],
        ["was", WT.VerbWord],
        ["to", WT.InfinitiveVerb]
    ]]
])

# check [14], [15], [20], [23], [27]


def get_expansions(node):
    # summary: return list of child nodes
    if node.find('WT_') == 0:
        if node in nodes:
            return nodes[node]
        else:
            return [["Error: word not in nodes dictionary"]]
    else:
        return [[node]]
