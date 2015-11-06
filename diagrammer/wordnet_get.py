import re

wordnet_dict_dir = 'diagrammer/WordNet-3.0/dict/'

verb_file_str = open(wordnet_dict_dir + 'verb.exc', 'r').read()
noun_file_str = open(wordnet_dict_dir + 'noun.exc', 'r').read()


def search_exc(word_str, exc_file_str):
    search_regex = re.compile(word_str + r"\s")
    result = re.findall(search_regex, exc_file_str)
    return len(result) > 0


def verb(word_str):
    return search_exc(word_str, verb_file_str)


def noun(word_str):
    return search_exc(word_str, noun_file_str)