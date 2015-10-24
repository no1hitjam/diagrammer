# console.py
# summary: deals with console I/O

#from parser import parse_string_lists
from sentence_parser import parse_string_lists

def get_ancestry_list(node):
	if node.parent is None:
		return [node]
	else:
		return get_ancestry_list(node.parent) + [node]

def print_tree(nodes):
	ancestries = map(get_ancestry_list, nodes)
	for a_idx, ancestry in enumerate(ancestries):
		a_str = ""
		for n_idx, node in enumerate(ancestry):
			def arrow(idx): return " -> " if idx != 0 else ""
			if a_idx == 0:
				a_str += arrow(n_idx) + str(node)
			else:
				if len(ancestries[a_idx - 1]) > n_idx and node == ancestries[a_idx - 1][n_idx]:
					for i in range(len(str(node)) + (4 if n_idx != 0 else 0)):
						a_str += " "
				else:
					a_str += arrow(n_idx) + str(node)
		print a_str

input_str = ""
while(input_str != "q"):
	input_str = raw_input("Enter sentence:\n")
	input_str_split = input_str.split()
	results = parse_string_lists(input_str.split())
	for result in results:
		print_tree(result)
