* Subtypes need some sort of structure. So you can specify a certain kind of verb or all types of verbs.

* Rather than populating the node_lists with EVERY noun or EVERY verb, when you get to those nodes have the
  parser 'reach into' the store of nouns and verbs. 

  This should significantly speed up parsing, especially as you add words.

* Optimize so that it doesn't do predicate expansion unless it actually sees a verb or adverb at the start, the only things predicate can expand to.

* When failing to find a string, output the failing string

* 