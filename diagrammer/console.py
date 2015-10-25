# console.py
# summary: deals with console I/O

from sentence_parser import parse_string_list

def get_ancestry_list(node):
	if node.parent is None:
		return [node]
	else:
		return get_ancestry_list(node.parent) + [node]

def tree_str(nodes):
	return_str = ""
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
		return_str += a_str + "\n"
	return return_str + "_____________________________________________________________"

def split_sentence(sentence_str):
	comma_idx = sentence_str.find(", ")
	space_idx = sentence_str.find(" ")
	if comma_idx == -1 and space_idx == -1:
		return [sentence_str]
	elif space_idx == 0:
		return split_sentence(sentence_str[1:])
	elif space_idx < comma_idx or comma_idx == -1:
		return [sentence_str[:space_idx]] + split_sentence(sentence_str[space_idx + 1:] if len(sentence_str) > space_idx else [])
	else: return [sentence_str[:comma_idx], ","] + split_sentence(sentence_str[comma_idx + 2:])

def console_loop():
	print "Enter 'q' to quit"
	input_str = ""
	while(input_str != "q"):
		input_str = raw_input("Enter sentence:\n")
		input_str_split = split_sentence(input_str)
		results = parse_string_list(input_str_split)
		result_file = open("out/result.txt", "w+")
		result_file.truncate()
		result_file.write("possible trees:\n")
		for result in results:
			print tree_str(result)
			result_file.write(tree_str(result))
		result_file.close()