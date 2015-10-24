# parser.py
# summary: where imported string lists are parsed into trees

from wordtypes import WT
from wordtypes import get_expansions

def print_node_lists(node_lists):
	for node_list in node_lists:
		for node in node_list:
			print str(node) + " "
		print "\n"

class ParseNode:
	def __init__(self, word, parent):
		self.word = word
		self.parent = parent

def parse_string_lists(input_word_list = [], node_lists = [[]]):
	idx = 0
	while idx < len(input_word_list):
		#print "idx: " + str(idx)
		# get next string in the input sentence
		cur_word = input_word_list[idx]
		# fill str_match_lists with node_lists with matching ParseNoded strings up to the idx.
		str_match_lists = []
		print "idx: " + str(idx)
		while len(node_lists) > 0:
			#print_node_lists(node_lists)
			node_list = node_lists.pop()
			#print "node_list: " + str(node_list) 
			# check if node_list is too small and needs to be skipped
			if len(node_list) <= idx: 
				continue
			# if the current index is a str, check if it matches the current word
			if type(node_list[idx]) is str:
				print node_list[idx] + ", " + cur_word
				if node_list[idx] == cur_word:	
					str_match_lists.append(node_list)
				else:
					continue
			
			# otherwise, expand
			else:
				for expansion in get_expansions(node_list[idx]):
					if idx + 1 < len(node_list):
						node_lists.append(node_list[:idx] + expansion + node_list[idx + 1:])
					else:
						node_lists.append(node_list[:idx] + expansion)
		# prepare next set of lists
		node_lists = str_match_lists
		idx += 1
	return node_lists
	
#print parse_string_lists(["Harry", "and", "Harry", "sat"], [[WT.Sentence]])
