import re

wordnet_dict_dir = 'diagrammer/WordNet-3.0/dict/'

verb_file_name = wordnet_dict_dir + 'verb.exc'
verb_file = open(verb_file_name, 'r')
verb_file_str = verb_file.read()


def verb(word_str):
    search_regex = re.compile(word_str + r"\s")
    # search_regex = re.compile(word_str)
    result = re.findall(search_regex, verb_file_str)
    return len(result) > 0
