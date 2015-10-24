# parser.py
# summary: where imported string lists are parsed into trees

from wordtypes import WT
from wordtypes import get_expansions

def print_node_lists(node_lists):
	for node_list in node_lists:
		for node in node_list:
			print str(node) + " "
		print "\n"

def get_ancestry_str(node, left):
	if node.parent is None:
			return str(node)
	else:
		if left:
			return str(node) + " <- " + get_ancestry_str(node.parent, left)
		else:
			return get_ancestry_str(node.parent, left) + " -> " + str(node)


def print_tree(nodes, left = True):
	for node in nodes:
		print get_ancestry_str(node, left)

class ParseNode:
	def __init__(self, word, parent):
		self.word = word
		self.parent = parent
	def __str__(self):
		return str(self.word)

def ParseNodifyExpansions(parent):
	expansions = get_expansions(parent.word)
	parsed_expansions = []
	for expansion in expansions:
		parsed_expansion = []
		for word in expansion:
			parsed_expansion.append(ParseNode(word, parent))
		parsed_expansions.append(parsed_expansion)
	return parsed_expansions

def parse_string_lists(input_word_list = [], node_lists = [[ParseNode(WT.Sentence, None)]]):
	idx = 0
	while idx < len(input_word_list):
		# get next string in the input sentence
		cur_word = input_word_list[idx]
		# fill str_match_lists with node_lists with matching ParseNoded strings up to the idx.
		str_match_lists = []
		while len(node_lists) > 0:
			# print_node_lists(node_lists)
			node_list = node_lists.pop() 
			# check if node_list is too small and needs to be skipped
			if len(node_list) <= idx: 
				continue
			# if the current index is a str, check if it matches the current word
			if type(node_list[idx].word) is str:
				#print node_list[idx] + ", " + cur_word
				if node_list[idx].word == cur_word:	
					str_match_lists.append(node_list)
				else:
					continue
			# otherwise, expand
			else:
				for expansion in ParseNodifyExpansions(node_list[idx]):
					if idx + 1 < len(node_list):
						node_lists.append(node_list[:idx] + expansion + node_list[idx + 1:])
					else:
						node_lists.append(node_list[:idx] + expansion)
		# prepare next set of lists
		node_lists = str_match_lists
		idx += 1

	size_appropriate_node_lists = []
	for node_list in node_lists:
		if len(node_list) == len(input_word_list):
			size_appropriate_node_lists.append(node_list)
	return size_appropriate_node_lists



# print_node_lists(parse_string_lists(["the","smelly","Harry", "and", "Harry", "sat"]))
# result = parse_string_lists(["Harry", "and", "Harry", "sat"])
# print_node_lists(result)
# print print_tree(result[0], False)