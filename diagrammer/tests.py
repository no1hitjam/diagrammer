import unittest
import sentence_parser
import console

def parse(sentence_str): 
    split_sentence = console.split_sentence(sentence_str)
    possible_trees = sentence_parser.parse_string_list(split_sentence)
    return len(possible_trees) > 0

class TestParser(unittest.TestCase):
    def test1(self): self.assert_(parse(
        "Harry sat"
    ))
    def test2(self): self.assert_(parse(
        "Harry and Fred sat"
    ))
    def test2(self): self.assert_(parse(
        "Harry and Fred sat"
    ))
    def test3(self): self.assert_(parse(
        "Fred painted the chair"
    ))
    def test4(self): self.assert_(parse(
        "Fred painted the chair green and Harry blue"
    ))
    def test5(self): self.assert_(parse(
        "Fred is on the chair"
    ))
    def test6(self): self.assert_(parse(
        "Fred, the blue chair, is the blue chair"
    ))
    def test7(self): self.assert_(parse(
        "Fred quickly painted the chair"
    ))
    def test8(self): self.assert_(parse(
        "Fred painted the chair quickly and quietly"
    ))
    def test9(self): self.assert_(parse(
        "Fred is taller than the chair"
    ))
    def test10(self): self.assert_(parse(
        "Fred is around the chair and on the chair"
    ))
    def test11(self): self.assert_(parse(
        "Fred painted green on the chair"
    ))
    def test12(self): self.assert_(parse(
        "Fred painted the chair crumbling under the chair and the chair crumbling under the chair"
    ))