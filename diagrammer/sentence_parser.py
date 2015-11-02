# parser.py
# summary: where imported string lists are parsed into trees

import word_types
from word_types import WT
from word_types import get_expansions

def print_node_lists(node_lists):
# summary: debug function for printing node lists
    for node_list in node_lists:
        print_str = ""
        for node in node_list:
            print_str += str(node) + " "
        print print_str
    print "-------"

class ParseNode:
# summary: node of parse tree
    def __init__(self, word, parent):
        self.word = word
        self.parent = parent
    def __str__(self):
        return str(self.word)

def ParseNodifyExpansions2(parent):
# summary: store parent information at every node
    expansions = word_types.get_expansions(parent.word)
    parsed_expansions = []
    for expansion in expansions:
        parsed_expansion = []
        for word in expansion:
            parsed_expansion.append(ParseNode(word, parent))
        parsed_expansions.append(parsed_expansion)
    return parsed_expansions

def ParseNodifyExpansions(parent, expansions):
# summary: store parent information at every expansion node
    parsed_expansions = []
    for expansion in expansions:
        parsed_expansion = []
        for word in expansion:
            parsed_expansion.append(ParseNode(word, parent))
        parsed_expansions.append(parsed_expansion)
    return parsed_expansions

def parse_string_list(input_word_list):
# summary: turn a sentence string list into a parse tree
    node_lists = [[ParseNode(WT.Sentence, None)]]
    idx = 0
    while idx < len(input_word_list):
        # get next string in the input sentence
        cur_word = input_word_list[idx]
        # fill str_match_lists with node_lists with matching ParseNoded strings up to the idx.
        str_match_lists = []
        while len(node_lists) > 0:
            node_list = node_lists.pop() 
            # check if node_list is too small and needs to be skipped
            if len(node_list) <= idx: continue
            # if the current index is a str, check if it matches the current word
            node_list_word = node_list[idx].word
            if type(node_list_word) is str:
                #print node_list[idx] + ", " + cur_word
                if node_list_word == cur_word:    
                    str_match_lists.append(node_list)
                    continue
                else:
                    continue
            def insertExpansion(expansion, idx, node_list):
            # summary: replace idx in node list with expansion
                return node_list[:idx] + expansion + (node_list[idx + 1:] if idx + 1 < len(node_list) else [])
            # if the current index can get a string, check if it can get a match to the current word
            if node_list_word in word_types.word_strings:
                # if so, create nodes with the enum replaced with all possible words and add them to str_match_list
                for expansion in ParseNodifyExpansions(node_list[idx], word_types.word_strings[node_list_word](cur_word)):
                    str_match_lists.append(insertExpansion(expansion, idx, node_list))
                continue
            # otherwise, expand
            for expansion in ParseNodifyExpansions(node_list[idx], word_types.get_expansions(node_list[idx].word)):
                node_lists.append(insertExpansion(expansion, idx, node_list))
            # -- print_node_lists(node_lists)
        # prepare for next set of lists
        node_lists = str_match_lists
        # -- print_node_lists(node_lists)
        idx += 1

    # return size appropriate node_lists
    return filter(lambda x: len(x) == len(input_word_list), node_lists)