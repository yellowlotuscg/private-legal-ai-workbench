import unittest
from legal_ai.retrieval import Passage,retrieve
class Tests(unittest.TestCase):
 def test_matter_boundary(self):
  ps=[Passage("a","a.md","notice deadline"),Passage("b","b.md","notice deadline")]
  self.assertEqual([p.source for p in retrieve("notice",ps,"a")],["a.md"])
 def test_no_answer(self): self.assertEqual(retrieve("unrelated",[Passage("a","a","notice")],"a"),[])
if __name__=="__main__": unittest.main()
